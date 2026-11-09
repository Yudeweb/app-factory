#!/usr/bin/env python3
"""App Factory state keeper.

Run from the project folder. This script is the only thing that changes stage
state, so gates and deliverable checks are enforced in one place:

  factory.py init --name NAME --idea-file FILE
  factory.py status
  factory.py start N | complete N
  factory.py approve N --quote "user's words" | request-changes N --note ... |
             reject N --note ... | reopen N --note ...
  factory.py task validate | list | ready | start ID | done ID --evidence ... |
             fail ID --note ... | defer ID --note ... | reset ID --note ...
  factory.py log --agent A --model M --task T --outcome ok|failed|rejected [--note ...]

Standard library only.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import uuid

VERSION = "1.0"
MAX_ATTEMPTS = 3

ROOT = pathlib.Path.cwd()
STATE = ROOT / ".factory" / "state.json"
DOCS = ROOT / "docs"
TASKS = DOCS / "05-planning" / "tasks.json"
LOG = DOCS / "11-agent-logs" / "log.jsonl"
CHANGES = DOCS / "12-project-history" / "changes.md"

DIRS = [
    "00-idea", "01-research", "02-product", "03-design", "04-architecture",
    "05-planning", "06-development", "07-testing", "08-deployment",
    "09-business", "10-decisions", "11-agent-logs", "12-project-history",
]

# gate: label of the approval gate that follows the stage, or None.
STAGES = [
    {"name": "Idea and initialization", "gate": None, "deliverables": [
        "docs/00-idea/original-idea.md",
        "docs/00-idea/project-overview.md",
        "docs/00-idea/assumptions-and-questions.md"]},
    {"name": "Market research and validation", "gate": "Gate 1", "deliverables": [
        "docs/01-research/idea-validation-report.md",
        "docs/01-research/competitor-analysis.md",
        "docs/01-research/sources.md"]},
    {"name": "Product definition", "gate": "Gate 2", "deliverables": [
        "docs/02-product/prd.md",
        "docs/02-product/functional-spec.md",
        "docs/02-product/non-functional-requirements.md",
        "docs/02-product/user-stories.md",
        "docs/02-product/mvp-scope.md",
        "docs/02-product/roadmap.md"]},
    {"name": "UI/UX design", "gate": "Gate 3", "deliverables": [
        "docs/03-design/figma-links.md",
        "docs/03-design/screen-inventory.md",
        "docs/03-design/user-flows.md",
        "docs/03-design/design-system.md",
        "docs/03-design/design-spec.md",
        "docs/03-design/handoff.md"]},
    {"name": "Architecture and technology", "gate": "Gate 4", "deliverables": [
        "docs/04-architecture/architecture.md",
        "docs/04-architecture/tech-stack.md",
        "docs/04-architecture/database.md",
        "docs/04-architecture/api-spec.md",
        "docs/04-architecture/infrastructure.md",
        "docs/04-architecture/security.md",
        "docs/04-architecture/scalability.md",
        "docs/04-architecture/operating-costs.md"]},
    {"name": "Planning, QA strategy, CI/CD", "gate": "Gate 5", "deliverables": [
        "docs/05-planning/development-plan.md",
        "docs/05-planning/tasks.json",
        "docs/05-planning/repository-spec.md",
        "docs/05-planning/test-strategy.md",
        "docs/05-planning/test-cases.md",
        "docs/05-planning/cicd.md",
        "docs/05-planning/definition-of-done.md",
        "docs/05-planning/release-and-rollback.md"]},
    {"name": "Autonomous implementation", "gate": None, "deliverables": [
        "docs/06-development/implementation-log.md"]},
    {"name": "Final QA", "gate": "Gate 6 (product acceptance)", "deliverables": [
        "docs/07-testing/test-results.md",
        "docs/07-testing/known-issues.md",
        "docs/07-testing/release-readiness-report.md",
        "docs/08-deployment/deployment.md"]},
    {"name": "Business and go-to-market", "gate": "Final gate", "deliverables": [
        "docs/09-business/business-strategy.md",
        "docs/09-business/go-to-market.md",
        "docs/09-business/pricing.md",
        "docs/09-business/store-listing.md",
        "docs/09-business/landing-page-spec.md",
        "docs/09-business/kpis.md",
        "docs/09-business/launch-checklist.md",
        "docs/09-business/post-launch-roadmap.md"]},
]

TASK_STATUSES = {"pending", "in_progress", "done", "failed", "escalated", "deferred"}


# ---------------------------------------------------------------- helpers

def now() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def die(msg: str) -> "None":
    print(f"REFUSED: {msg}", file=sys.stderr)
    sys.exit(1)


def write_json(path: pathlib.Path, data) -> None:
    """Atomic write so an interruption never leaves a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load_state() -> dict:
    if not STATE.exists():
        die("no App Factory project in this folder (run init first).")
    return json.loads(STATE.read_text(encoding="utf-8"))


def stage_index(value: str) -> int:
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("stage must be a number 0-8")
    if not 0 <= n < len(STAGES):
        raise argparse.ArgumentTypeError("stage must be a number 0-8")
    return n


def is_done(n: int, st: dict) -> bool:
    return st["status"] == ("approved" if STAGES[n]["gate"] else "completed")


def record(st: dict, event: str, note: str = "") -> None:
    entry = {"at": now(), "event": event}
    if note:
        entry["note"] = note
    st.setdefault("history", []).append(entry)


def missing_files(paths) -> list:
    out = []
    for rel in paths:
        p = ROOT / rel
        if not p.is_file() or p.stat().st_size == 0:
            out.append(rel)
    return out


# ------------------------------------------------------------------ tasks

def load_tasks() -> dict:
    if not TASKS.exists():
        die(f"{TASKS.relative_to(ROOT)} does not exist yet (it is written in stage 5).")
    try:
        data = json.loads(TASKS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"tasks.json is not valid JSON: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("tasks"), list):
        die('tasks.json must be an object with a "tasks" list.')
    for t in data["tasks"]:
        t.setdefault("status", "pending")
        t.setdefault("attempts", 0)
        t.setdefault("depends_on", [])
    return data


def task_errors(data: dict) -> list:
    errors, ids = [], {}
    for i, t in enumerate(data["tasks"]):
        tid = t.get("id")
        if not tid:
            errors.append(f"task #{i + 1} has no id")
            continue
        if tid in ids:
            errors.append(f"duplicate id {tid}")
        ids[tid] = t
        if not t.get("title"):
            errors.append(f"{tid}: no title")
        if not t.get("acceptance"):
            errors.append(f"{tid}: no acceptance criteria")
        if t["status"] not in TASK_STATUSES:
            errors.append(f"{tid}: unknown status {t['status']!r}")
    for tid, t in ids.items():
        for dep in t["depends_on"]:
            if dep not in ids:
                errors.append(f"{tid}: depends on unknown task {dep}")
    # cycle detection (depth-first, three colours)
    colour = {}

    def visit(tid, path):
        colour[tid] = 1
        for dep in ids[tid]["depends_on"]:
            if dep not in ids:
                continue
            if colour.get(dep) == 1:
                errors.append("dependency cycle: " + " -> ".join(path + [tid, dep]))
            elif dep not in colour:
                visit(dep, path + [tid])
        colour[tid] = 2

    for tid in ids:
        if tid not in colour:
            visit(tid, [])
    return errors


def find_task(data: dict, tid: str) -> dict:
    for t in data["tasks"]:
        if t.get("id") == tid:
            return t
    die(f"no task {tid}")


def deps_done(data: dict, t: dict) -> bool:
    status = {x["id"]: x["status"] for x in data["tasks"] if x.get("id")}
    return all(status.get(d) == "done" for d in t["depends_on"])


def is_ready(data: dict, t: dict) -> bool:
    return (t["status"] in ("pending", "failed")
            and t["attempts"] < MAX_ATTEMPTS and deps_done(data, t))


def task_counts(data: dict) -> dict:
    counts = {}
    for t in data["tasks"]:
        counts[t["status"]] = counts.get(t["status"], 0) + 1
    return counts


# --------------------------------------------------------------- commands

def cmd_init(args) -> None:
    if STATE.exists():
        print(f"Already initialized: {load_state()['id']}. Nothing changed.")
        return
    idea = pathlib.Path(args.idea_file).read_text(encoding="utf-8")
    if not idea.strip():
        die("the idea file is empty.")
    slug = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-") or "project"
    today = datetime.date.today().isoformat()
    pid = f"{slug}-{today}-{uuid.uuid4().hex[:6]}"

    for d in DIRS:
        (DOCS / d).mkdir(parents=True, exist_ok=True)

    def seed(rel: str, text: str) -> None:
        p = ROOT / rel
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")

    seed("docs/00-idea/original-idea.md",
         f"# Original idea\n\n- Project: {args.name} (`{pid}`)\n- Submitted: {now()}\n"
         "- This file is the user's idea exactly as written. Never edit it.\n\n---\n\n"
         + idea.rstrip("\n") + "\n")
    seed("README.md",
         f"# {args.name}\n\nProject `{pid}`, started {today} with App Factory.\n\n"
         "- Current status: [docs/STATUS.md](docs/STATUS.md)\n"
         "- Original idea: [docs/00-idea/original-idea.md](docs/00-idea/original-idea.md)\n"
         "- Decisions: [docs/10-decisions/](docs/10-decisions/)\n"
         "- History: [docs/12-project-history/](docs/12-project-history/)\n"
         "- Traceability: [docs/traceability.md](docs/traceability.md)\n\n"
         "To continue this project, open this folder in Claude and run `/app-factory continue`.\n")
    seed("docs/traceability.md",
         "# Traceability\n\nIdea → assumption (A) → requirement (R) → user story (US) → "
         "screen (SCR) → component (C) → task (T) → test (TC).\n\n"
         "| Assumption | Requirement | User story | Screen | Component | Task | Test | Status |\n"
         "|---|---|---|---|---|---|---|---|\n")
    seed("docs/12-project-history/changelog.md",
         f"# Changelog\n\n- {today}: project created.\n")
    seed("docs/12-project-history/changes.md",
         "# Changes to approved work\n\nEach entry: what changed, why, what it affects, "
         "and the approval.\n")

    state = {
        "factory_version": VERSION, "id": pid, "name": args.name, "created": now(),
        "stages": [{"status": "pending", "history": []} for _ in STAGES],
    }
    write_json(STATE, state)
    print(f"Initialized project {pid}")


def cmd_start(args) -> None:
    state = load_state()
    n, st = args.stage, state["stages"][args.stage]
    for m in range(n):
        if not is_done(m, state["stages"][m]):
            gate = STAGES[m]["gate"]
            need = f"approved at {gate}" if gate else "completed"
            die(f"stage {m} ({STAGES[m]['name']}) is '{state['stages'][m]['status']}'; "
                f"it must be {need} before stage {n} can start.")
    if st["status"] == "in_progress":
        print(f"Stage {n} is already in progress.")
        return
    if st["status"] not in ("pending", "needs_review", "rejected"):
        die(f"stage {n} is '{st['status']}'. Use reopen to change finished work.")
    st["status"] = "in_progress"
    st.setdefault("started", now())
    record(st, "started")
    write_json(STATE, state)
    print(f"Stage {n} started: {STAGES[n]['name']}")


def cmd_complete(args) -> None:
    state = load_state()
    n, st = args.stage, state["stages"][args.stage]
    if st["status"] != "in_progress":
        die(f"stage {n} is '{st['status']}', not in progress.")
    problems = [f"missing or empty: {p}" for p in missing_files(STAGES[n]["deliverables"])]
    if n == 4 and not list((DOCS / "10-decisions").glob("ADR-*.md")):
        problems.append("no ADR-*.md in docs/10-decisions/")
    if n == 5 and TASKS.exists():
        problems += [f"tasks.json: {e}" for e in task_errors(load_tasks())]
    if n == 6:
        open_tasks = [t["id"] for t in load_tasks()["tasks"]
                      if t["status"] not in ("done", "deferred")]
        if open_tasks:
            problems.append("tasks not done or deferred: " + ", ".join(open_tasks))
    if problems:
        die(f"stage {n} cannot be completed:\n  - " + "\n  - ".join(problems))
    gate = STAGES[n]["gate"]
    st["status"] = "awaiting_approval" if gate else "completed"
    st["completed"] = now()
    record(st, "completed")
    write_json(STATE, state)
    if gate:
        print(f"Stage {n} complete. Awaiting the user's approval at {gate}.")
    else:
        print(f"Stage {n} complete. No gate; stage {n + 1} may start.")


def gated_stage(args, state) -> dict:
    n, st = args.stage, state["stages"][args.stage]
    if not STAGES[n]["gate"]:
        die(f"stage {n} has no approval gate.")
    if st["status"] != "awaiting_approval":
        die(f"stage {n} is '{st['status']}', not awaiting approval.")
    return st


def cmd_approve(args) -> None:
    state = load_state()
    st = gated_stage(args, state)
    if not args.quote.strip():
        die("--quote must contain the user's own words of approval.")
    st["status"] = "approved"
    st["approval"] = {"at": now(), "quote": args.quote.strip()}
    record(st, "approved", args.quote.strip())
    write_json(STATE, state)
    print(f"{STAGES[args.stage]['gate']} approved.")


def cmd_request_changes(args) -> None:
    state = load_state()
    st = gated_stage(args, state)
    st["status"] = "in_progress"
    record(st, "changes_requested", args.note)
    write_json(STATE, state)
    print(f"Stage {args.stage} back in progress with requested changes.")


def cmd_reject(args) -> None:
    state = load_state()
    st = gated_stage(args, state)
    st["status"] = "rejected"
    record(st, "rejected", args.note)
    write_json(STATE, state)
    print(f"Stage {args.stage} rejected. Agree a new direction, then start it again.")


def cmd_reopen(args) -> None:
    state = load_state()
    n, st = args.stage, state["stages"][args.stage]
    if not is_done(n, st):
        die(f"stage {n} is '{st['status']}'; only finished stages can be reopened.")
    st["status"] = "in_progress"
    st.pop("approval", None)
    record(st, "reopened", args.note)
    flagged = []
    for m in range(n + 1, len(STAGES)):
        later = state["stages"][m]
        if later["status"] != "pending":
            later["status"] = "needs_review"
            later.pop("approval", None)
            record(later, "needs_review", f"stage {n} reopened")
            flagged.append(str(m))
    write_json(STATE, state)
    if CHANGES.exists():
        with CHANGES.open("a", encoding="utf-8") as fh:
            fh.write(f"\n## {now()}: stage {n} reopened\n\n- Reason: {args.note}\n"
                     f"- Later stages flagged for review: {', '.join(flagged) or 'none'}\n"
                     "- Impact and approval: _to be filled in_\n")
    print(f"Stage {n} reopened. Flagged for review: {', '.join(flagged) or 'none'}.")


def next_step(state: dict) -> str:
    for n, st in enumerate(state["stages"]):
        if is_done(n, st):
            continue
        s, name = st["status"], STAGES[n]["name"]
        return {
            "pending": f"start stage {n} ({name}).",
            "in_progress": f"stage {n} ({name}) is in progress; complete it when its deliverables are ready.",
            "awaiting_approval": f"waiting for the user's decision at {STAGES[n]['gate']} (stage {n}, {name}).",
            "needs_review": f"stage {n} ({name}) needs review after an earlier stage was reopened; start it again.",
            "rejected": f"stage {n} ({name}) was rejected; agree a new direction, then start it again.",
        }.get(s, f"stage {n} is '{s}'.")
    return "lifecycle complete."


def cmd_status(args) -> None:
    if not STATE.exists():
        print("No App Factory project in this folder.")
        return
    state = load_state()
    rows = []
    for n, st in enumerate(state["stages"]):
        gate = STAGES[n]["gate"] or "none"
        when = st.get("approval", {}).get("at") or st.get("completed") or st.get("started") or ""
        rows.append((str(n), STAGES[n]["name"], st["status"].replace("_", " "), gate, when))
    lines = [f"Project: {state['name']} ({state['id']})", f"Next: {next_step(state)}", ""]
    for r in rows:
        lines.append(f"  {r[0]}  {r[1]:<32} {r[2]:<18} {r[3]:<28} {r[4]}")
    task_line = ""
    if TASKS.exists():
        data = load_tasks()
        counts = task_counts(data)
        task_line = "Tasks: " + ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in sorted(counts.items()))
        lines += ["", task_line]
    print("\n".join(lines))

    md = [f"# Status: {state['name']}", "", f"- Project: `{state['id']}`",
          f"- Updated: {now()}", f"- Next: {next_step(state)}", "",
          "| Stage | Name | Status | Gate | Last change |", "|---|---|---|---|---|"]
    md += [f"| {' | '.join(r)} |" for r in rows]
    if task_line:
        md += ["", "## Tasks", "", task_line, "",
               "| ID | Title | Status | Attempts |", "|---|---|---|---|"]
        md += [f"| {t.get('id')} | {t.get('title', '')} | {t['status'].replace('_', ' ')} | {t['attempts']} |"
               for t in data["tasks"]]
    if LOG.exists():
        recent = LOG.read_text(encoding="utf-8").strip().splitlines()[-10:]
        md += ["", "## Recent agent runs", "", "| When | Agent | Model | Task | Outcome |", "|---|---|---|---|---|"]
        for line in recent:
            e = json.loads(line)
            md.append(f"| {e['at']} | {e['agent']} | {e['model']} | {e['task']} | {e['outcome']} |")
    (DOCS / "STATUS.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def cmd_log(args) -> None:
    load_state()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {"at": now(), "agent": args.agent, "model": args.model,
             "task": args.task, "outcome": args.outcome}
    if args.note:
        entry["note"] = args.note
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("Logged.")


def cmd_task(args) -> None:
    data = load_tasks()
    action = args.action

    if action == "validate":
        errors = task_errors(data)
        if errors:
            die("tasks.json has problems:\n  - " + "\n  - ".join(errors))
        print(f"tasks.json is valid: {len(data['tasks'])} tasks.")
        return
    if action == "list":
        for t in data["tasks"]:
            deps = ",".join(t["depends_on"]) or "-"
            print(f"  {t.get('id', '?'):<7} {t['status']:<12} attempts {t['attempts']}  deps {deps:<14} {t.get('title', '')}")
        return
    if action == "ready":
        ready = [t for t in data["tasks"] if is_ready(data, t)]
        ready.sort(key=lambda t: t.get("priority", 99))
        if not ready:
            print("No tasks are ready.")
        for t in ready:
            files = ", ".join(t.get("files", [])) or "(no files declared)"
            print(f"  {t['id']}  [{t.get('role', '?')}/{t.get('specialization', '-')}] {t.get('title', '')}  files: {files}")
        return

    if not args.id:
        die(f"task {action} needs a task id.")
    t = find_task(data, args.id)

    if action == "start":
        if t["status"] not in ("pending", "failed"):
            die(f"{t['id']} is '{t['status']}'.")
        if t["attempts"] >= MAX_ATTEMPTS:
            die(f"{t['id']} has already had {MAX_ATTEMPTS} attempts. Escalate it instead of retrying.")
        if not deps_done(data, t):
            die(f"{t['id']} has unfinished dependencies: {', '.join(t['depends_on'])}.")
        t["status"] = "in_progress"
        t["attempts"] += 1
        t["started"] = now()
        msg = f"{t['id']} started (attempt {t['attempts']} of {MAX_ATTEMPTS})."
    elif action == "done":
        if t["status"] != "in_progress":
            die(f"{t['id']} is '{t['status']}', not in progress.")
        if not (args.evidence or "").strip():
            die("--evidence is required: say what was run and what was observed.")
        t["status"] = "done"
        t["evidence"] = args.evidence.strip()
        t["finished"] = now()
        msg = f"{t['id']} done."
    elif action == "fail":
        if t["status"] != "in_progress":
            die(f"{t['id']} is '{t['status']}', not in progress.")
        if not (args.note or "").strip():
            die("--note is required: state the cause of the failure.")
        t.setdefault("failures", []).append({"at": now(), "note": args.note.strip()})
        if t["attempts"] >= MAX_ATTEMPTS:
            t["status"] = "escalated"
            msg = f"{t['id']} failed {MAX_ATTEMPTS} times and is now escalated. Send it to senior-supervisor."
        else:
            t["status"] = "failed"
            msg = f"{t['id']} failed (attempt {t['attempts']} of {MAX_ATTEMPTS}). Retry with a different approach."
    elif action == "defer":
        if not (args.note or "").strip():
            die("--note is required: record the user's agreement and the reason.")
        t["status"] = "deferred"
        t["deferred"] = {"at": now(), "note": args.note.strip()}
        msg = f"{t['id']} deferred."
    elif action == "reset":
        if t["status"] != "escalated":
            die(f"{t['id']} is '{t['status']}'; only escalated tasks can be reset.")
        if not (args.note or "").strip():
            die("--note is required: record the outcome of the escalation.")
        t.setdefault("failures", []).append({"at": now(), "note": "reset: " + args.note.strip()})
        t["status"] = "pending"
        t["attempts"] = 0
        msg = f"{t['id']} reset after escalation."
    else:
        die(f"unknown task action {action}")

    write_json(TASKS, data)
    print(msg)


# ------------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(description="App Factory state keeper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create the project skeleton")
    p.add_argument("--name", required=True)
    p.add_argument("--idea-file", required=True, help="file holding the idea verbatim")
    p.set_defaults(func=cmd_init)

    sub.add_parser("status", help="show the lifecycle and refresh docs/STATUS.md").set_defaults(func=cmd_status)

    for name, func, helptext in (("start", cmd_start, "begin a stage"),
                                 ("complete", cmd_complete, "finish a stage (checks deliverables)")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("stage", type=stage_index)
        p.set_defaults(func=func)

    p = sub.add_parser("approve", help="record the user's approval of a gate")
    p.add_argument("stage", type=stage_index)
    p.add_argument("--quote", required=True, help="the user's own words")
    p.set_defaults(func=cmd_approve)

    for name, func, helptext in (("request-changes", cmd_request_changes, "user asked for changes at a gate"),
                                 ("reject", cmd_reject, "user rejected at a gate"),
                                 ("reopen", cmd_reopen, "change an already finished stage")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("stage", type=stage_index)
        p.add_argument("--note", required=True)
        p.set_defaults(func=func)

    p = sub.add_parser("log", help="record an agent run")
    p.add_argument("--agent", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--outcome", required=True, choices=["ok", "failed", "rejected"])
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("task", help="work items for stage 6")
    p.add_argument("action", choices=["validate", "list", "ready", "start", "done", "fail", "defer", "reset"])
    p.add_argument("id", nargs="?")
    p.add_argument("--evidence")
    p.add_argument("--note")
    p.set_defaults(func=cmd_task)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
