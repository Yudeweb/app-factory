# Stage 7: Final QA and user acceptance

**Objective:** an independent verdict on whether the application matches what was approved, before the user spends time reviewing it.

**Inputs:** the built application and every approved document.

## Steps

1. `factory.py start 7`.
2. Brief `qa-engineer` to test as an independent party, from the documents rather than from the developers' reports: the PRD, every user story and acceptance criterion, the approved design (compare screens with the Figma designs), the architecture, the security requirements and the test plan. It runs the full automated suite and exercises every major journey in the running app.
3. For mobile apps, test on iOS simulators and Android emulators covering the supported OS versions and screen sizes. Real-device testing happens only if the user provides devices or approves a device-farm service; say which was done.
4. In parallel: `security-reviewer` runs the security checks (dependency scan, secrets scan, authentication and authorization paths, input handling); `devops-engineer` proves a clean build and deployment from the documented instructions alone; `technical-writer` checks the documentation against the code and fills gaps.
5. Critical or major defects go back through the stage 6 task loop (add tasks, fix, re-verify) before continuing. Do not hide them in the report.
6. Write `docs/07-testing/test-results.md` (what was run, pass and fail counts, environments), `docs/07-testing/known-issues.md`, and `docs/07-testing/release-readiness-report.md`: requirement-by-requirement status, failed tests, unresolved issues, known limitations, outstanding risks, and what was not tested and why.
7. Ask `senior-supervisor` to check the readiness report against the evidence.
8. `factory.py complete 7`.

## Gate 6: final product acceptance

Give the user: test results, build artifacts, screenshots or a recorded walkthrough, how to access the staging build, the documentation index, known limitations and the readiness assessment. The user reviews the application personally. Do not start stage 8 before approval.

## Deliverables

`docs/07-testing/test-results.md`, `docs/07-testing/known-issues.md`, `docs/07-testing/release-readiness-report.md`, `docs/08-deployment/deployment.md`
