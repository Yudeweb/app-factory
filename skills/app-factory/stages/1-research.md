# Stage 1: Market research and idea validation

**Objective:** give the user an honest, sourced evaluation of the idea as fast as possible.

**Inputs:** everything in `docs/00-idea/`.

## Steps

1. `factory.py start 1`.
2. Launch three `product-researcher` agents in one message so they run in parallel, each with web search and one perspective:
   - **Market need** → `docs/01-research/market-need.md`: what the problem is, who has it and how often, how they cope today, where current solutions fall short, evidence of demand (reviews, forums, search interest, public discussions), segments and trends.
   - **Business potential** → `docs/01-research/competitor-analysis.md` and `docs/01-research/business-potential.md`: direct and indirect competitors with features and pricing, monetization models in the category, differentiation openings, distribution channels, entry barriers, first-customer acquisition hypotheses.
   - **Technical feasibility** → `docs/01-research/technical-feasibility.md`: complexity, required technologies and their maturity, third-party dependencies and their terms, integration risks, rough development and infrastructure cost drivers, security, privacy and regulatory constraints, scalability concerns.

   Each brief must require evidence labels, a link and date for every external claim, and a list of what could not be verified.
3. Check the three reports: open a sample of cited links, remove or relabel anything unsupported, and note contradictions between reports.
4. Collect all sources into `docs/01-research/sources.md` (title, link, date published or accessed, what it supports).
5. Write `docs/01-research/idea-validation-report.md` yourself with these sections: executive summary; problem analysis; target audience; market research; competitor comparison (table); evidence of demand; potential differentiation; monetization opportunities; technical feasibility; risks and uncertainties; opportunities; recommended next steps.
6. End the report with the **structured evaluation**: market need, business potential and technical feasibility, each scored 1 to 5 with the criteria stated, the evidence behind the score, and a confidence level (low, medium, high) reflecting how much of it rests on facts versus assumptions. Do not invent market sizes or revenue figures; give ranges with their basis or say the data is unavailable.
7. Conclude with exactly one recommendation: **Proceed**, **Proceed after validation** (say what to validate and how cheaply), **Reconsider or pivot**, or **Do not proceed**.
8. Update `docs/00-idea/assumptions-and-questions.md`: which assumptions research confirmed, contradicted or left open.
9. `factory.py complete 1`.

## Gate 1

Present the report summary, the scores and recommendation, and only the questions that research could not answer and that change the outcome (typically three to six). If the user's answers change the direction, audience or requirements, record them, rerun only the affected research, revise the report and complete again. Proceed to stage 2 only after approval.

## Deliverables

- `docs/01-research/idea-validation-report.md`
- `docs/01-research/competitor-analysis.md`
- `docs/01-research/sources.md`
