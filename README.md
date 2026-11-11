# App Factory

A reusable Claude workflow that takes an app idea from a plain description to a designed, built, tested and launch-ready product. It is a skill plus a team of specialist subagents, not a separate service: it runs inside your normal Claude Code sessions.

It starts as a conversation. After a quick market check, it asks multiple-choice questions to decide the idea, scope, scale, design direction and technology together with you, and only then writes one `plan.md`. From there specialist agents design, plan, build and test, stopping at five approval gates.

## Status

Early and largely unproven. Read this before relying on it.

- **Tested:** the state script (`factory.py`) passes a simulated run of the whole lifecycle, including the cases it must refuse: starting a stage before the previous gate is approved, completing a stage whose required output is missing, a fourth attempt at a task, and dependency cycles.
- **Not yet tested:** a complete run on a real app idea with live agents. The stage guides and agent definitions are instructions for Claude; how well they perform on a real project has not been measured.
- **Tested once:** the analyze mode, in its current form, on one real iOS repository. It completed end to end: two rounds of intent questions, market scan and code review in parallel, the repository's 654 package tests run with the owner's agreement, a verdict with gap table and path to shipment, and a `vision.md` written. The market scan still left several questions unresolved even when told to open pages, so treat its competitor and pricing findings as weak evidence. One run is not a measure of quality.
- **Not yet measured:** token use. Version 2 is designed to use fewer tokens than version 1 (one quick research pass before the conversation, seven required documents instead of about 45, shorter instructions), but no real run has been measured.
- **Not yet tested:** creating designs in Figma. Stage 2 depends on the Figma connector's write-to-canvas tool, which is in beta.
- There is no automated test suite or CI in this repository yet.

It is written for Claude Code (terminal, desktop app or IDE extension), which is where skills and subagents run.

## Install

```bash
./install.sh
```

This copies the skill to `~/.claude/skills/app-factory` and eleven agents to `~/.claude/agents/`. Anything it would overwrite is moved to `~/.claude/backups/` first. Run it again after editing this folder to update. Start a new session afterwards so the skill and agents are picked up.

Requirements: Python 3.9 or later, git, and for stage 2 the Figma connector connected to Claude with write access.

## Use

1. Create an empty folder for the new app and open it in Claude.
2. Run `/app-factory` followed by your idea, in as much or as little detail as you have.
3. You get a short verdict on whether the idea makes sense, then multiple-choice questions (always with a free-text "Other"). Nothing is written to the project yet.
4. When every important decision is made, it asks whether to create `plan.md`. Approving that plan is the first gate.

To come back later: open the project folder and run `/app-factory continue`. For a quick look: `/app-factory status`.

## Analyze an existing repo

Open any app repository in Claude and run `/app-factory analyze`. This is separate from the lifecycle below: it never touches stage state or gates and never edits code.

A repository shows what exists, not what is intended, so the analysis asks first and judges the code against your answers:

1. It reads the code, documentation and git history, and any vision recorded on an earlier run.
2. It asks multiple-choice questions (each with "Not decided yet"): who the app is for, the monetization plan, which tasks must work at shipment, and which features are planned but not built.
3. A quick market scan and a read-only code review run in parallel. Safe checks only (dependency listing, outdated and vulnerable packages); nothing is built or run.
4. It offers to run the repository's existing test suite. Without that, must-work tasks are reported as "looks implemented, not verified".
5. It asks you to classify the gaps it found: planned, must work at shipment, not wanted, or not decided yet.
6. You get a verdict in chat on the idea, the monetization and business plan, and the technical stack, each scored 1 to 5 with a confidence level. A planned feature that is not built yet does not lower a score. It includes a gap table and an ordered path to shipment.
7. It records your intent in `vision.md`, or in a "Vision" section of `plan.md` if you prefer; it asks which on the first run. Later runs read that record and ask only what changed.

Finally it asks whether to save the report as `docs/app-analysis.md`.

## Lifecycle

| Stage | What happens | Required output | Gate |
|---|---|---|---|
| 1 Discover | Quick viability scan, then the decision conversation | `plan.md` | 1 Plan |
| 2 Design | Design system, screens and prototype in Figma | `docs/design.md` | 2 Design |
| 3 Build plan | Technical design, tasks, test plan, CI/CD | `docs/build-plan.md`, `docs/tasks.json` | 3 Build plan |
| 4 Implement | Developer agents work through the tasks | tasks done | none |
| 5 QA | Independent verification and readiness report | `docs/qa-report.md` | 4 Acceptance |
| 6 Launch | Positioning, pricing, go-to-market | `docs/launch-plan.md` | 5 Launch |

### The decision conversation (stage 1)

1. Quick viability scan: one researcher, a handful of searches, no file.
2. A verdict in chat with sources and a confidence level.
3. Questions to clarify the idea, then a choice: continue with a full research report, continue without it, pivot, or stop. The full report (`docs/market-research.md`) is written once, on the clarified idea, only if you want it.
4. Scope and expected scale.
5. Design direction, with suggested tools: Figma for the real design, and palette, typography, reference and AI-mockup tools for an early feel.
6. Technology, explained at your level: what each choice is, the realistic alternatives with trade-offs, and a recommended option.
7. A summary, then `plan.md`.

Answers are kept in a small hidden file (`.factory/notes.md`) so an interrupted conversation can resume; it is removed once `plan.md` is written.

Other documents (a detailed requirements document, API reference, runbook and so on) are written only when a later stage needs one or you ask.

## What a project folder contains

```
plan.md                    every decision, with reasons and a change log
.factory/                  state, the original idea verbatim, agent run log
docs/STATUS.md             generated status page
docs/design.md, build-plan.md, tasks.json, qa-report.md, launch-plan.md
```

## The team

| Agent | Model | Used for |
|---|---|---|
| orchestrator (the main session) | whichever model the session runs; the most capable available is recommended | the conversation, delegation, verification, gates |
| senior-supervisor | Opus | selective independent review and stuck problems |
| product-researcher, product-manager, ux-designer, software-architect, developer, qa-engineer, devops-engineer, security-reviewer, technical-writer, business-strategist | Sonnet | the work |

## Changing it

- **Model for a role:** edit `model:` in `agents/<role>.md` (`sonnet`, `opus`, `haiku`, or a full model ID).
- **A role's behavior:** edit the body of its agent file.
- **A stage:** edit `skills/app-factory/stages/<n>-*.md`. If you change which files a stage must produce, change the matching list in `STAGES` at the top of `skills/app-factory/scripts/factory.py`.
- **A new role:** add `agents/<name>.md` and mention it in the relevant stage guide and in the team list in `SKILL.md`.

Agent and skill descriptions are loaded into every Claude session, so keep them to one short line.

Run `./install.sh` after any change.

## State script

`skills/app-factory/scripts/factory.py` is the only thing that changes stage state. Run it from a project folder:

| Command | Effect |
|---|---|
| `status` | print the lifecycle; refresh `docs/STATUS.md` once `plan.md` exists |
| `start N` | begin stage N (1 to 6); refused unless every earlier stage is finished and approved |
| `complete N` | finish stage N; refused if its required output is missing |
| `approve N --quote "…"` | record your approval with your words |
| `request-changes N --note "…"` | send a stage back for revision |
| `reject N --note "…"` | record a rejection |
| `reopen N --note "…"` | change a finished stage; later stages are flagged for review |
| `task validate / list / ready / start / done / fail / defer / reset` | stage 4 work items with dependencies and a three-attempt limit |
| `log …` | record an agent run |

## Known limitations

- Gates are enforced by the script and the workflow's instructions inside a Claude session. That is a strong convention, not a security boundary.
- There is no web dashboard; `docs/STATUS.md` and `/app-factory status` take its place.
- Projects started with version 1 (nine stages) cannot be continued with version 2.
- Figma's write-to-canvas tool is in beta and depends on your Figma seat. If it is unavailable the workflow asks whether to wait or to use a clickable HTML prototype as a stand-in.
- The design tools the workflow suggests are third-party products that change; it is told to check before recommending one.
- Market research uses public web sources only. Scores are reasoned judgments with stated confidence.
- Mobile testing runs on simulators and emulators. Real devices, store submission, paid services and production deployment need you.
- Long implementation stages span several sessions; they resume from the state and task files, not from conversation memory.

## License

MIT. See [LICENSE](LICENSE).
