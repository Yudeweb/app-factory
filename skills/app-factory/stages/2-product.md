# Stage 2: Product definition and requirements

**Objective:** a product definition complete enough that someone who never saw the conversation could build the right thing.

**Inputs:** `docs/00-idea/`, the approved `docs/01-research/`, the user's Gate 1 answers.

## Steps

1. `factory.py start 2`.
2. Brief `product-manager` to produce the documents below. Before it starts, settle with the user any product decision that would change the MVP scope and that the research does not answer; batch these into one round of questions.
3. Required content:
   - **PRD** (`prd.md`): vision, value proposition, target users and personas where useful, user journeys, core functionality, business rules, roles and permissions, accessibility requirements, success measures.
   - **Functional specification** (`functional-spec.md`): for every major feature its purpose, expected behavior, user interaction, dependencies, acceptance criteria and edge cases. Each requirement has an `R-n` ID.
   - **Non-functional requirements** (`non-functional-requirements.md`): performance, reliability, security, privacy, accessibility, localization, supported platforms and versions, each measurable.
   - **User stories** (`user-stories.md`): `US-n`, each linked to requirements and carrying testable acceptance criteria.
   - **MVP scope** (`mvp-scope.md`): features prioritized with MoSCoW (must, should, could, won't for now), with the reason for each placement. State explicitly what is excluded.
   - **Roadmap** (`roadmap.md`): MVP, then later versions, with what would trigger each.
4. Review the result yourself against the research: every must-have traces to a validated need or a stated assumption; nothing in the MVP is there only because it is easy. Cut scope creep.
5. Update `docs/traceability.md` (assumption → requirement → story).
6. `factory.py complete 2`.

## Gate 2

The user approves the PRD and the MVP scope. Call out the features you placed outside the MVP and why.

## Deliverables (all in `docs/02-product/`)

`prd.md`, `functional-spec.md`, `non-functional-requirements.md`, `user-stories.md`, `mvp-scope.md`, `roadmap.md`
