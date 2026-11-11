# Stage 4: Implement

**Objective:** build the approved plan with as little user involvement as the permission boundaries allow, keeping working software throughout.

**Inputs:** `plan.md`, `docs/design.md`, `docs/build-plan.md`, `docs/tasks.json`. Gate 3 approval is your authorization.

## Setup

`factory.py start 4`. Set up the repository and environment as the build plan specifies. Creating a remote repository or connecting a paid service needs the user unless Gate 3 covered it.

## The loop

Repeat until `factory.py task ready` returns nothing and no task is in progress:

1. `factory.py task ready` lists tasks whose dependencies are done.
2. Take the ready tasks that own disjoint files. For each, `factory.py task start <id>`, then launch its agent in the same message so they run in parallel, each on its own branch or worktree. A few at a time.
3. The brief is the task entry, the sections of the plan and design it needs, the files it owns, and the instruction to report what it ran.
4. **Verify before accepting:** read the diff, run the build and the relevant tests yourself, check each acceptance criterion. Send security-sensitive, complex or cross-cutting changes to `senior-supervisor` first.
5. Accepted: merge, confirm the main branch still builds and passes, then `factory.py task done <id> --evidence "<what you ran and saw>"`.
   Not accepted: `factory.py task fail <id> --note "<cause>"` and retry with a brief that states the cause and a different approach.
6. `factory.py log ...` for each agent run. Keep the README and setup instructions true to the code as it changes.

## Failures

- The script refuses a fourth attempt at a task. Send it to `senior-supervisor` with the history; after its verdict, `task reset`. If it concludes the plan itself is wrong, that is the user's decision (`reopen 1` or `reopen 3`).
- After an interruption, `factory.py status` and `task list` show where to resume. Re-verify tasks left in progress; do not assume they finished.

## Stays with the user

Unplanned spending, paid services, changes to approved decisions, risky data migrations, production secrets and deployment, external release, irreversible actions. Ask one clear question each and keep working on tasks that do not depend on the answer.

## Finish

Every task done, or deferred with the user's agreement (`task defer`); main branch passing in CI. Then `factory.py complete 4` and continue directly to stage 5.
