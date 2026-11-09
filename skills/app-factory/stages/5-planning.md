# Stage 5: Development planning, quality assurance and CI/CD

**Objective:** an execution plan detailed enough that implementation can run without the user.

**Inputs:** approved stages 2, 3 and 4.

## Steps

1. `factory.py start 5`.
2. **Task breakdown** (you): translate the PRD, design and architecture into tasks small enough to verify individually, and write them to `docs/05-planning/tasks.json`:

   ```json
   {"tasks": [{
     "id": "T-1", "title": "...", "description": "...", "expected_result": "...",
     "role": "developer", "specialization": "mobile|backend|frontend|database|devops|qa|docs",
     "milestone": "M1", "priority": 1, "depends_on": [],
     "files": ["paths this task owns"],
     "acceptance": ["..."], "tests": ["TC-1"], "docs": ["docs/..."],
     "status": "pending", "attempts": 0
   }]}
   ```

   Tasks that could run at the same time must not own the same files. Run `factory.py task validate` (checks IDs, dependencies and cycles).
3. `development-plan.md`: milestones, phases, the dependency graph (Mermaid) and which tasks can run concurrently. The first milestone ends in a running skeleton of the app so there is working software from then on.
4. `repository-spec.md`: directory layout, naming conventions, coding standards, branching strategy (a short-lived branch per task), pull-request rules, commit conventions, review process.
5. Brief `qa-engineer` for `test-strategy.md` and `test-cases.md`: unit, integration, API, database, UI, end-to-end, regression, performance, security, accessibility, and device and platform compatibility, as applicable. Every acceptance criterion maps to at least one test case (`TC-n`); tests check the requirement, not just that code runs.
6. Brief `devops-engineer` for `cicd.md` and the pipeline configuration (GitHub Actions unless the architecture chose otherwise): build, lint and format, tests, dependency and vulnerability scanning, artifacts, environment configuration, staging deployment, release management, rollback. Production deployment requires manual approval in the pipeline itself.
7. `definition-of-done.md`: for a task (code merged, acceptance checks verified, tests passing in CI, docs updated, evidence recorded) and for a milestone.
8. `release-and-rollback.md`.
9. Ask `senior-supervisor` to review the plan for missing work, wrong ordering and file conflicts between parallel tasks.
10. Update `docs/traceability.md` (story → task → test).
11. `factory.py complete 5`.

## Gate 5

Present the plan, milestone list, what will need the user during implementation (accounts, credentials, paid services, with estimated costs) and an [ESTIMATE] of the work involved. Approval of this gate authorizes autonomous implementation within this plan.

## Deliverables (all in `docs/05-planning/`)

`development-plan.md`, `tasks.json`, `repository-spec.md`, `test-strategy.md`, `test-cases.md`, `cicd.md`, `definition-of-done.md`, `release-and-rollback.md`
