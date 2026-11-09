# Stage 0: Idea and initialization

**Objective:** turn whatever the user wrote into a recorded project, without changing their words and without interrogating them.

## Steps

1. Save the user's idea exactly as written to a temporary file. Do not fix, shorten or translate it.
2. Pick a short project name from the idea and run:
   `factory.py init --name "<name>" --idea-file <temp file>`
   This creates the `docs/` tree, `.factory/state.json`, the verbatim `docs/00-idea/original-idea.md` and the project README. If the folder is not a git repository, run `git init` and make the first commit after this stage.
3. `factory.py start 0`.
4. Write `docs/00-idea/project-overview.md`: the problem, intended users, target platforms, monetization ideas, technical preferences and constraints. Fill in only what the user stated; mark each gap as open rather than inventing an answer.
5. Write `docs/00-idea/assumptions-and-questions.md`: numbered assumptions (`A-1`, ...) you are making to proceed, and open questions. For each question note whether research can answer it or only the user can.
6. Start `docs/traceability.md` with the assumptions.
7. `factory.py complete 0`, then go straight into stage 1. Do not stop to ask questions here; questions come after research, when you know which ones matter.

## Deliverables

- `docs/00-idea/original-idea.md` (verbatim, never edited afterwards)
- `docs/00-idea/project-overview.md`
- `docs/00-idea/assumptions-and-questions.md`
