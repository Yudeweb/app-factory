# Analyze mode: assess an existing app repository

**Objective:** an honest assessment of the repository in the working directory on three things: the app idea, the monetization and business plan, and the technical stack.

**Separate from the lifecycle.** Do not call `factory.py`, create `.factory/` or `plan.md`, or start a stage. Change nothing in the repository unless the user asks for the report file. Do not offer to start the six-stage workflow.

**Read and safe checks only.** You and your agents may read files and git history, list dependencies, and run outdated-package and known-vulnerability checks that do not execute project code. Do not install dependencies, build, run the app or its tests, or run the repository's own scripts.

## Steps

1. **Orient yourself.** Read the README, manifests and dependency files, top-level structure, docs, and `git log` in summary. Tell the user in two or three lines what the app is and how far along it looks. If the repository does not say who the users are or how it should make money, ask one multiple-choice round; whatever stays unknown is reported as "not stated in the repo", never guessed.

2. **Two agents, launched together:**
   - `product-researcher`, quick scan, given your summary of the idea: competitors and their pricing, signs of demand, obvious blockers.
   - `software-architect`, read-only repository review: languages and frameworks, architecture and data model, dependency health, tests and CI, secrets or security red flags, what breaks first under growth, and gaps between what the README claims and what the code does. Reply of 400 words or fewer with file references.

   For a large repository, tell the architect which areas to sample and report what was covered.

3. **Verdict in chat,** three sections:
   - **Idea:** the problem, the users, and how it differs from what the scan found.
   - **Monetization and business:** the model the repository states or implies, how it compares with competitor pricing, what it costs to run, what is missing.
   - **Technical stack:** what it is, whether it fits the idea and the likely scale, risks, quality signals.

   For each: what you found with file references, strengths, risks, a score of 1 to 5 with the criterion and a confidence level, and evidence labels. Then the top recommendations in priority order, and a list of what you could not determine and why.

4. **Ask what next:** save the report to a file (default `docs/app-analysis.md`), go deeper on one area, or stop. Write the file only on request, with the date and the commit it describes.
