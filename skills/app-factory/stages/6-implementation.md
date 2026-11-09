# Stage 6: Autonomous implementation

**Objective:** build the approved plan with as little user involvement as the permission boundaries allow, keeping working software and current documentation throughout.

**Inputs:** approved stages 2 to 5. Gate 5 approval is your authorization.

## Setup

1. `factory.py start 6`.
2. Initialize the repository and development environment as specified in `repository-spec.md` and `cicd.md`. Creating a remote repository or connecting paid services needs the user if Gate 5 did not already cover it.

## The loop

Repeat until `factory.py task ready` returns nothing and no task is in progress:

1. `factory.py task ready` lists tasks whose dependencies are done.
2. Pick the ready tasks that own disjoint files. For each: `factory.py task start <id>`, then launch its agent (`developer` with the task's specialization, or `qa-engineer`, `devops-engineer`, `technical-writer`). Launch them in one message so they run in parallel, each in its own git worktree or branch. Keep to a few at a time.
3. The brief gives the task entry from `tasks.json`, the documents it references, the files it owns, the acceptance checks, and the instruction to open a pull request (or leave a branch) and report what was run.
4. When an agent returns, **verify before accepting**: read the diff, run the build and the relevant tests yourself, check each acceptance criterion. Send complex, security-sensitive or cross-cutting changes to `senior-supervisor` for review first.
5. Accepted: merge, confirm the main branch still builds and passes, then `factory.py task done <id> --evidence "<what you ran and saw>"`.
   Not accepted: `factory.py task fail <id> --note "<cause>"`, then retry with a brief that states the cause and a different approach. Never resend the same brief.
6. `factory.py log ...` for every agent run (agent, model, task, outcome).
7. Append notable problems and their resolution to `docs/06-development/implementation-log.md`, and keep `docs/traceability.md`, API docs and `docs/08-deployment/deployment.md` in step with the code.

## Failures

- An agent investigating a failure reads the logs and the code, states the cause, applies a justified fix and reruns the tests.
- The script refuses a fourth attempt at a task. At that point send it to `senior-supervisor` with the full history; if it concludes the plan or architecture is wrong, that is a decision for the user (`reopen 4` or `reopen 5`).
- If the session is interrupted, `factory.py status` and `task list` show exactly where to resume. Tasks left in progress are re-verified, not assumed done.

## Stays with the user

Unplanned spending, paid services, material architecture changes, risky or destructive migrations, production secrets, production deployment, external release, irreversible actions, changes of product direction. Raise these as one clear question each and keep working on tasks that do not depend on the answer.

## Finish

All tasks done (or explicitly deferred with the user's agreement via `task defer`), main branch green in CI, documentation current. Then `factory.py complete 6` and continue directly to stage 7.

## Deliverables

- `docs/06-development/implementation-log.md`
- every task in `tasks.json` done or deferred
