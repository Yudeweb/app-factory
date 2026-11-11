# Analyze mode: assess an existing app repository

**Objective:** an honest assessment of the repository in the working directory, judged against what its owner intends it to become: the app idea, the monetization and business plan, and the technical stack.

**Separate from the lifecycle.** Do not call `factory.py`, create `.factory/`, or start a stage. Do not offer to start the six-stage workflow. The only files you may write are the vision record (step 7) and, on request, the report. Never edit code.

**Read and safe checks only.** You and your agents may read files and git history, list dependencies, and run outdated-package and known-vulnerability checks that do not execute project code. No installing, building or running the app. The one exception is the test run in step 4, and only if the user agrees in that run.

## Steps

1. **Orient.** Read the README, manifests, top-level structure, docs and `git log` in summary. Look for an existing vision: `vision.md`, or a "Vision" section in `plan.md`. Tell the user in two or three lines what the app is and how far along it looks.

2. **Intent, round one.** The repository shows what exists, not what is intended, so ask before judging. Every question offers "Not decided yet". Cover:
   - who it is for, and whether it is personal or meant for release;
   - the monetization plan;
   - which tasks must work at shipment (multi-select, options drawn from the features you found);
   - features planned but not built yet.

   If a vision exists, summarize it and ask only what is new or has changed.

3. **Two agents, launched together,** both briefed with the intended product:
   - `product-researcher`, quick scan: competitors and their pricing, signs of demand, obvious blockers. Ask it to open the most relevant pages, not rely on search snippets.
   - `software-architect`, read-only repository review: stack, architecture and data model, dependency health, tests and CI, secrets or security red flags, what breaks first under growth, gaps between documentation and code, and each must-work task rated implemented, partial, missing, or cannot tell without running. Reply of 400 words or fewer with file references.

   For a large repository, say which areas to sample and report what was covered.

4. **Offer the test run.** Ask once: run the repository's existing test suite, or not. If yes, run only its standard test command and report the result. If no, must-work tasks are "looks implemented, not verified".

5. **Intent, round two.** Put the gaps you found to the user in groups: planned, must work at shipment, not wanted, or not decided yet.

6. **Verdict in chat.** Three sections (idea; monetization and business; technical stack), each with findings and file references, strengths, risks, a score of 1 to 5 with its criterion and a confidence level, and evidence labels. Judge against the vision: a planned feature that is not built yet does not lower a score. Then:
   - **Gap table:** gap, class (planned, must work at shipment, unplanned suggestion, not wanted), current state.
   - **Path to shipment:** the ordered steps between the repository today and the shipment the user described.
   - Open decisions, and what you could not determine and why.

7. **Record the vision** from `templates/vision.md`. First run in a repository: ask whether to use `vision.md` (recommend it, especially where `plan.md` is an approved App Factory plan) or a "Vision" section in `plan.md`. In `plan.md`, insert the section before any change log; never append after it. Later runs update the same place and add a dated line to its update log.

8. **Ask what next:** save the analysis report (default `docs/app-analysis.md`, with the date and commit it describes), go deeper on one area, or stop.
