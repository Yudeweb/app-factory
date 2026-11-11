# Stage 5: QA

**Objective:** an independent verdict on whether the application matches what was approved, before the user spends time reviewing it.

## Steps

1. `factory.py start 5`.
2. Brief `qa-engineer` to test from the documents, not from developers' reports: every requirement and acceptance criterion in `plan.md`, the screens against `docs/design.md`, and the test plan. It builds the app from the documented instructions, runs the full automated suite, and exercises every main journey including error paths.
3. Test environments and platform checks come from the platform file (simulators and emulators for mobile; browsers, screen widths and audits for web). State what was covered and what was not.
4. In parallel: `security-reviewer` runs dependency and secret scans and reviews sign-in, permissions and input handling; `devops-engineer` proves a clean build and deployment from the instructions alone; `technical-writer` checks README, setup, deployment and troubleshooting instructions against the code.
5. Critical and major defects go back through the stage 4 task loop (add tasks, fix, re-verify) before continuing.
6. Write `docs/qa-report.md`: what was run with counts and environments; status per requirement; defects found and fixed; known issues and limitations; security findings; what was not tested and why; a readiness judgment.
7. Ask `senior-supervisor` to check the report's claims against the evidence.
8. `factory.py complete 5`.

## Gate 4: acceptance

Give the user the report, build artifacts, screenshots or a recorded walkthrough, and how to try the staging build. The user reviews the application personally. Stage 6 does not start before approval.
