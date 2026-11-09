# App Factory

A reusable Claude workflow that takes an app idea from a plain description to a researched, designed, built, tested and launch-ready product. It is a skill plus a team of specialist subagents, not a separate service: it runs inside your normal Claude sessions.

You give the idea and approve at gates. The workflow does the research, product definition, Figma design, architecture, planning, implementation, QA and go-to-market preparation, and writes everything down as it goes.

## Status

Early and largely unproven. Read this before relying on it.

- **Tested:** the state script (`factory.py`) passes a simulated run of the whole lifecycle, including the cases it must refuse: starting a stage before the previous gate is approved, completing a stage with deliverables missing, a fourth attempt at a task, and dependency cycles.
- **Not yet tested:** a complete run on a real app idea with live agents. The stage guides and agent definitions are instructions for Claude; how well they perform on a real project has not been measured.
- **Not yet tested:** creating designs in Figma. Stage 3 depends on the Figma connector's write-to-canvas tool, which is in beta.
- There is no automated test suite or CI in this repository yet.

It is written for Claude Code (terminal, desktop app or IDE extension), which is where skills and subagents run.

## Install

```bash
./install.sh
```

This copies the skill to `~/.claude/skills/app-factory` and eleven agents to `~/.claude/agents/`. Anything it would overwrite is moved to `~/.claude/backups/` first. Run it again after editing this folder to update. Start a new session afterwards so the skill and agents are picked up.

Requirements: Python 3.9 or later, git, and for stage 3 the Figma connector connected to Claude with write access.

## Use

1. Create an empty folder for the new app and open it in Claude.
2. Run `/app-factory` followed by your idea, in as much or as little detail as you have.
3. The first stop is the Idea Validation Report: scores for market need, business potential and technical feasibility, a recommendation, and a few questions.
4. Approve, ask for changes, or reject. Each later gate works the same way.

To come back later: open the project folder and run `/app-factory continue`. For a quick look: `/app-factory status`, or read `docs/STATUS.md`.

## Lifecycle

| Stage | What happens | Gate |
|---|---|---|
| 0 | Idea recorded verbatim, project skeleton created | none |
| 1 | Three parallel researchers, Idea Validation Report | Gate 1 |
| 2 | PRD, functional spec, user stories, MVP scope, roadmap | Gate 2 |
| 3 | UX structure, design system, screens and prototype in Figma | Gate 3 |
| 4 | Architecture options compared, stack, database, costs, ADRs | Gate 4 |
| 5 | Task breakdown, test strategy, CI/CD, definition of done | Gate 5 |
| 6 | Autonomous implementation by the developer team | none |
| 7 | Independent QA and release readiness report | Gate 6 |
| 8 | Business strategy and go-to-market plan | Final gate |

## What a project folder contains

```
README.md
.factory/state.json        stage and gate state
docs/STATUS.md             generated status page
docs/traceability.md       idea → requirement → story → screen → task → test
docs/00-idea … 12-project-history
```

`docs/10-decisions/` holds the Architecture Decision Records, `docs/11-agent-logs/log.jsonl` the record of agent runs, and `docs/12-project-history/` the changelog and changes to approved work.

## The team

| Agent | Model | Used for |
|---|---|---|
| orchestrator (the main session) | Fable 5.2, or Opus 5.5 | planning, delegation, verification, gates |
| senior-supervisor | Opus | selective independent review and stuck problems |
| product-researcher, product-manager, ux-designer, software-architect, developer, qa-engineer, devops-engineer, security-reviewer, technical-writer, business-strategist | Sonnet | the work |

The orchestrator model is whichever model your session runs on; pick it in the app's model selector.

## Changing it

- **Model for a role:** edit `model:` in `agents/<role>.md` (`sonnet`, `opus`, `haiku`, `fable`, or a full model ID).
- **A role's behavior:** edit the body of its agent file.
- **A stage:** edit `skills/app-factory/stages/<n>-*.md`. If you change which files a stage must produce, change the matching list in `STAGES` at the top of `skills/app-factory/scripts/factory.py`.
- **A new role:** add `agents/<name>.md` and mention it in the relevant stage guide and in the team list in `SKILL.md`.

Run `./install.sh` after any change. Projects already in progress keep their own state and documents; they pick up the new instructions the next time the skill runs.

## State script

`skills/app-factory/scripts/factory.py` is the only thing that changes stage state. Run it from a project folder:

| Command | Effect |
|---|---|
| `status` | print the lifecycle, refresh `docs/STATUS.md` |
| `start N` | begin stage N; refused unless every earlier stage is finished and approved |
| `complete N` | finish stage N; refused if required deliverables are missing |
| `approve N --quote "…"` | record your approval with your words |
| `request-changes N --note "…"` | send a stage back for revision |
| `reject N --note "…"` | record a rejection |
| `reopen N --note "…"` | change a finished stage; later stages are flagged for review |
| `task validate / list / ready / start / done / fail / defer / reset` | stage 6 work items with dependencies and a three-attempt limit |
| `log …` | record an agent run |

## Known limitations

- Gates are enforced by the script and the workflow's instructions inside a Claude session. That is a strong convention, not a security boundary.
- There is no web dashboard; `docs/STATUS.md` and `/app-factory status` take its place.
- Figma's write-to-canvas tool is in beta and depends on your Figma seat. If it is unavailable the workflow asks whether to wait or to use a clickable HTML prototype as a stand-in.
- Market research uses public web sources only. Scores are reasoned judgments with stated confidence.
- Mobile testing runs on simulators and emulators. Real devices, store submission, paid services and production deployment need you.
- Long implementation stages span several sessions; they resume from `state.json` and `tasks.json`, not from conversation memory.

## License

MIT. See [LICENSE](LICENSE).
