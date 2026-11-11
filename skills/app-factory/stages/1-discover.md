# Stage 1: Discover

**Objective:** decide with the user whether the idea is worth building and what exactly to build, then record it once in `plan.md`.

**Rule:** no project document is written until the user says to create `plan.md` (the research report in step 4 is the one exception, and only on request). Until then the only file you touch is `.factory/notes.md`.

## Steps

1. **Initialize.** Save the idea exactly as written to a temporary file, then `factory.py init --name "<short name>" --idea-file <file>` and `factory.py start 1`. If resuming, read `.factory/notes.md` and continue from the first undecided topic.

2. **Quick viability scan.** One `product-researcher` in quick-scan mode: at most eight searches, reply of 250 words or fewer with links. Does the problem exist and for whom, who already solves it and how well, is it buildable, any obvious blocker (legal, platform, cost). No file.

3. **Verdict in chat.** A short, honest read with evidence labels: does it make sense in the market, is it viable, how confident you are, and the two or three things that would change the answer.

4. **Clarify the idea** (one or two question rounds): the problem and who has it, the user's vision, how it might make money, any constraints, and the **platform**: mobile, web (application, installable web app, content site, or API only), or both. Record it in the notes; it decides which file in `platforms/` later stages read. Then one question: **continue with a full research report, continue without it, pivot, or stop.**
   - *With report:* launch three `product-researcher` agents in parallel on the clarified idea (market need, competitors and business potential, technical feasibility). Each writes its section to `docs/research/`. You write only `docs/market-research.md`: one-page summary, competitor table, scores of 1 to 5 with criteria and confidence for need, business potential and feasibility, a recommendation, and links to the sections. Spot-check a sample of cited links first.
   - *Pivot:* agree the new direction and return to step 2. *Stop:* `factory.py reject` is not needed; leave the stage in progress and say how to resume.

5. **Scope and scale.** Must-have features for the first version, what is deliberately left out, expected users at launch and plausible growth. Propose a scope yourself; cut features that are there only because they are easy.

6. **Design direction.** Visual style, color palette, typography, light and dark modes, reference apps the user likes. Suggest tools and say what each is for:
   - **Seeing the screens in stage 2:** real screens run in the simulator or browser, a high-fidelity coded prototype, Penpot (free, editable), or Figma with a paid seat. Figma's free plan allows too few AI tool calls for a full design; say so now.
   - **Palette:** Coolors (generate palettes), Realtime Colors (see a palette on a live layout), Material Theme Builder (full Material token sets).
   - **Typography:** Fontpair or Google Fonts.
   - **Reference screens:** Mobbin (screens from shipped apps).
   - **Fast AI mockups:** Google Stitch, Figma Make, v0 for a first look before real design.

   These change; if unsure a tool still exists or is free, check before recommending. On request, show two or three palette and type options as a quick visual preview.

7. **Technology.** First ask the user's technical background once and pitch explanations to it. Read the platform file for the options to compare. Then, one decision at a time (app framework, backend, database, sign-in, hosting, and any algorithm central to the product, such as matching, ranking, recommendation or sync): what it is and does in plain language; two or three realistic options with trade-offs in cost, speed of development, performance, lock-in and where each stops scaling against the agreed growth; your recommended option and why. Verify facts that carry a decision (pricing, limits, platform support) with a quick search. Ask `senior-supervisor` to review the resulting set of choices once.

8. **Summary and plan.md.** Recap every decision in chat and ask whether to create `plan.md`. On yes, write it from `templates/plan.md`, including the idea verbatim from `.factory/idea.md`; delete `.factory/notes.md`; `git init` and commit if the folder is not a repository; `factory.py complete 1`.

After every question round, update `.factory/notes.md` with the decisions so far (a short list, not prose).

## Gate 1

The user approves `plan.md`. Approval fixes the scope, design direction and technology; later changes go through `reopen 1`.
