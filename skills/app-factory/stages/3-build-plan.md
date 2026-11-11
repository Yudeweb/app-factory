# Stage 3: Build plan

**Objective:** an execution plan detailed enough that implementation can run without the user.

**Inputs:** `plan.md`, `docs/design.md`.

## Steps

1. `factory.py start 3`.
2. Brief `software-architect` for the technical detail developers need, as sections of `docs/build-plan.md`: component diagram and data model (Mermaid), database schema with indexes and constraints, API endpoints, sign-in and permission model, environments, secrets handling, backup. It implements the technology already approved in `plan.md`; it does not reopen those choices. Have `security-reviewer` check the security parts.
3. Write `docs/tasks.json` yourself:

   ```json
   {"tasks": [{
     "id": "T-1", "title": "...", "description": "...",
     "role": "developer", "specialization": "mobile|backend|frontend|database|devops|qa|docs",
     "milestone": "M1", "priority": 1, "depends_on": [],
     "files": ["paths this task owns"], "requirements": ["R-1"],
     "acceptance": ["..."], "tests": ["TC-1"],
     "status": "pending", "attempts": 0
   }]}
   ```

   Tasks small enough to verify one by one. Tasks that could run together must not own the same files. The first milestone ends in a running skeleton of the app. Run `factory.py task validate`.
4. Brief `qa-engineer` for the test plan section: which test levels apply, and at least one test case (`TC-n`) per acceptance criterion in `plan.md`.
5. Brief `devops-engineer` for the CI/CD section and the pipeline files (GitHub Actions unless `plan.md` says otherwise): build, lint, tests, dependency scanning, staging deployment, rollback, and a manual approval step before production.
6. Add to `docs/build-plan.md`: milestones, repository layout and conventions, branching (a short-lived branch per task), definition of done, and what will need the user during the build (accounts, credentials, paid services with estimated costs).
7. Ask `senior-supervisor` to review for missing work, wrong ordering and file conflicts between parallel tasks.
8. `factory.py complete 3`.

## Gate 3

The user approves the build plan. Approval authorizes autonomous implementation within it.
