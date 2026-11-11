#!/usr/bin/env python3
"""App Factory state keeper (v2).

Run from the project folder. This script is the only thing that changes stage
state, so gates and deliverable checks are enforced in one place:

  factory.py init --name NAME --idea-file FILE
  factory.py status
  factory.py start N | complete N                      (N = 1..6)
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

VERSION = "2.0"
MAX_ATTEMPTS = 3

ROOT = pathlib.Path.cwd()
FACTORY = ROOT / ".factory"
STATE = FACTORY / "state.json"
IDEA = FACTORY / "idea.md"
LOG = FACTORY / "agent-log.jsonl"
PLAN = ROOT / "plan.md"
TASKS = ROOT / "docs" / "tasks.json"
STATUS_MD = ROOT / "docs" / "STATUS.md"

# Stage numbers are 1-based for the user; index = number - 1.
# gate: label of the approval gate that follows the stage, or None.
STAGES = [
    {"name": "Discover", "gate": "Gate 1 (plan)", "deliverables": ["plan.md"]},
    {"name": "Design", "gate": "Gate 2 (design)", "deliverables": ["docs/design.md"]},
    {"name": "Build plan", "gate": "Gate 3 (build plan)",
     "deliverables": ["docs/build-plan.md", "docs/tasks.json"]},
    {"name": "Implement", "gate": None, "deliverables": []},
    {"name": "QA", "gate": "Gate 4 (acceptance)", "deliverables": ["docs/qa-report.md"]},
    {"name": "Launch", "gate": "Gate 5 (launch)", "deliverables": ["docs/launch-plan.md"]},
]
BUILD_PLAN, IMPLEMENT = 3, 4  # stage numbers with task checks

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
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if not str(state.get("factory_version", "")).startswith("2"):
        die("this project was created with App Factory v1 (nine stages), which this "
            "version cannot continue. Use the v1 skill, or start a new project.")
    return state


def stage_number(value: str) -> int:
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"stage must be a number 1-{len(STAGES)}")
    if not 1 <= n <= len(STAGES):
        raise argparse.ArgumentTypeError(f"stage must be a number 1-{len(STAGES)}")
    return n


def spec(n: int) -> dict:
    return STAGES[n - 1]


def get(state: dict, n: int) -> dict:
    return state["stages"][n - 1]


def is_done(n: int, st: dict) -> bool:
    return st["status"] == ("approved" if spec(n)["gate"] else "completed")


def record(st: dict, event: str, note: str = "") -> None:
    entry = {"at": now(), "event": event}
    if note:
        entry["note"] = note
    st.setdefault("history", []).append(entry)


def missing_files(paths) -> list:
    return [rel for rel in paths
            if not (ROOT / rel).is_file() or (ROOT / rel).stat().st_size == 0]


# ------------------------------------------------------------------ tasks

def load_tasks() -> dict:
    if not TASKS.exists():
        die(f"{TASKS.relative_to(ROOT)} does not exist yet (it is written in stage {BUILD_PLAN}).")
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


# --------------------------------------------------------------- commands

def cmd_init(args) -> None:
    """Creates only hidden state; no project documents exist until plan.md."""
    if STATE.exists():
        print(f"Already initialized: {load_state()['id']}. Nothing changed.")
        return
    idea = pathlib.Path(args.idea_file).read_text(encoding="utf-8")
    if not idea.strip():
        die("the idea file is empty.")
    slug = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-") or "project"
    pid = f"{slug}-{datetime.date.today().isoformat()}-{uuid.uuid4().hex[:6]}"
    FACTORY.mkdir(parents=True, exist_ok=True)
    IDEA.write_text(idea, encoding="utf-8")  # verbatim, never edited afterwards
    write_json(STATE, {
        "factory_version": VERSION, "id": pid, "name": args.name, "created": now(),
        "stages": [{"status": "pending", "history": []} for _ in STAGES],
    })
    print(f"Initialized project {pid}")


def cmd_start(args) -> None:
    state = load_state()
    n, st = args.stage, get(state, args.stage)
    for m in range(1, n):
        if not is_done(m, get(state, m)):
            gate = spec(m)["gate"]
            need = f"approved at {gate}" if gate else "completed"
            die(f"stage {m} ({spec(m)['name']}) is '{get(state, m)['status']}'; "
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
    print(f"Stage {n} started: {spec(n)['name']}")


def cmd_complete(args) -> None:
    state = load_state()
    n, st = args.stage, get(state, args.stage)
    if st["status"] != "in_progress":
        die(f"stage {n} is '{st['status']}', not in progress.")
    problems = [f"missing or empty: {p}" for p in missing_files(spec(n)["deliverables"])]
    if n == BUILD_PLAN and TASKS.exists():
        problems += [f"tasks.json: {e}" for e in task_errors(load_tasks())]
    if n == IMPLEMENT:
        open_tasks = [t["id"] for t in load_tasks()["tasks"]
                      if t["status"] not in ("done", "deferred")]
        if open_tasks:
            problems.append("tasks not done or deferred: " + ", ".join(open_tasks))
    if problems:
        die(f"stage {n} cannot be completed:\n  - " + "\n  - ".join(problems))
    gate = spec(n)["gate"]
    st["status"] = "awaiting_approval" if gate else "completed"
    st["completed"] = now()
    record(st, "completed")
    write_json(STATE, state)
    if gate:
        print(f"Stage {n} complete. Awaiting the user's approval at {gate}.")
    else:
        print(f"Stage {n} complete. No gate; stage {n + 1} may start.")


def gated_stage(args, state) -> dict:
    n, st = args.stage, get(state, args.stage)
    if not spec(n)["gate"]:
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
    print(f"{spec(args.stage)['gate']} approved.")


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
    n, st = args.stage, get(state, args.stage)
    if not is_done(n, st):
        die(f"stage {n} is '{st['status']}'; only finished stages can be reopened.")
    st["status"] = "in_progress"
    st.pop("approval", None)
    record(st, "reopened", args.note)
    flagged = []
    for m in range(n + 1, len(STAGES) + 1):
        later = get(state, m)
        if later["status"] != "pending":
            later["status"] = "needs_review"
            later.pop("approval", None)
            record(later, "needs_review", f"stage {n} reopened")
            flagged.append(str(m))
    write_json(STATE, state)
    if PLAN.exists():  # plan.md ends with its change log
        with PLAN.open("a", encoding="utf-8") as fh:
            fh.write(f"\n- {now()}: stage {n} ({spec(n)['name']}) reopened. Reason: {args.note} "
                     f"Later stages to review: {', '.join(flagged) or 'none'}.\n")
    print(f"Stage {n} reopened. Flagged for review: {', '.join(flagged) or 'none'}.")


def next_step(state: dict) -> str:
    for n in range(1, len(STAGES) + 1):
        st = get(state, n)
        if is_done(n, st):
            continue
        name = spec(n)["name"]
        return {
            "pending": f"start stage {n} ({name}).",
            "in_progress": f"stage {n} ({name}) is in progress; complete it when its deliverables are ready.",
            "awaiting_approval": f"waiting for the user's decision at {spec(n)['gate']} (stage {n}, {name}).",
            "needs_review": f"stage {n} ({name}) needs review after an earlier stage was reopened; start it again.",
            "rejected": f"stage {n} ({name}) was rejected; agree a new direction, then start it again.",
        }.get(st["status"], f"stage {n} is '{st['status']}'.")
    return "lifecycle complete."


def cmd_status(args) -> None:
    if not STATE.exists():
        print("No App Factory project in this folder.")
        return
    state = load_state()
    rows = []
    for n in range(1, len(STAGES) + 1):
        st = get(state, n)
        when = st.get("approval", {}).get("at") or st.get("completed") or st.get("started") or ""
        rows.append((str(n), spec(n)["name"], st["status"].replace("_", " "),
                     spec(n)["gate"] or "none", when))
    lines = [f"Project: {state['name']} ({state['id']})", f"Next: {next_step(state)}", ""]
    lines += [f"  {r[0]}  {r[1]:<12} {r[2]:<18} {r[3]:<22} {r[4]}" for r in rows]
    if (FACTORY / "notes.md").exists():
        lines += ["", "Discovery notes in progress: .factory/notes.md"]
    task_line, data = "", None
    if TASKS.exists():
        data = load_tasks()
        counts = {}
        for t in data["tasks"]:
            counts[t["status"]] = counts.get(t["status"], 0) + 1
        task_line = "Tasks: " + ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in sorted(counts.items()))
        lines += ["", task_line]
    print("\n".join(lines))

    if not PLAN.exists():
        return  # no project documents before plan.md
    md = [f"# Status: {state['name']}", "", f"- Project: `{state['id']}`",
          f"- Updated: {now()}", f"- Next: {next_step(state)}", "",
          "| Stage | Name | Status | Gate | Last change |", "|---|---|---|---|---|"]
    md += [f"| {' | '.join(r)} |" for r in rows]
    if data:
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
    STATUS_MD.parent.mkdir(parents=True, exist_ok=True)
    STATUS_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def cmd_log(args) -> None:
    load_state()
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
        ready = sorted((t for t in data["tasks"] if is_ready(data, t)),
                       key=lambda t: t.get("priority", 99))
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

    p = sub.add_parser("init", help="create the hidden project state")
    p.add_argument("--name", required=True)
    p.add_argument("--idea-file", required=True, help="file holding the idea verbatim")
    p.set_defaults(func=cmd_init)

    sub.add_parser("status", help="show the lifecycle; refresh docs/STATUS.md once plan.md exists").set_defaults(func=cmd_status)

    for name, func, helptext in (("start", cmd_start, "begin a stage"),
                                 ("complete", cmd_complete, "finish a stage (checks deliverables)")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("stage", type=stage_number)
        p.set_defaults(func=func)

    p = sub.add_parser("approve", help="record the user's approval of a gate")
    p.add_argument("stage", type=stage_number)
    p.add_argument("--quote", required=True, help="the user's own words")
    p.set_defaults(func=cmd_approve)

    for name, func, helptext in (("request-changes", cmd_request_changes, "user asked for changes at a gate"),
                                 ("reject", cmd_reject, "user rejected at a gate"),
                                 ("reopen", cmd_reopen, "change an already finished stage")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("stage", type=stage_number)
        p.add_argument("--note", required=True)
        p.set_defaults(func=func)

    p = sub.add_parser("log", help="record an agent run")
    p.add_argument("--agent", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--outcome", required=True, choices=["ok", "failed", "rejected"])
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("task", help="work items for the implementation stage")
    p.add_argument("action", choices=["validate", "list", "ready", "start", "done", "fail", "defer", "reset"])
    p.add_argument("id", nargs="?")
    p.add_argument("--evidence")
    p.add_argument("--note")
    p.set_defaults(func=cmd_task)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
