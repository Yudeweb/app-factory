# Stage 4: Technical architecture and technology selection

**Objective:** an architecture chosen for this product, with alternatives compared, costs estimated and every significant decision recorded.

**Inputs:** approved `docs/02-product/` and `docs/03-design/`, plus `docs/01-research/technical-feasibility.md`.

## Steps

1. `factory.py start 4`.
2. State the growth assumptions first, in `scalability.md`: expected initial users, plausible growth, concurrency, data volume, traffic shape. Label them as assumptions. Every later choice is sized against these.
3. Brief `software-architect` to compare real alternatives and recommend, never to pick by popularity. Where the choice is meaningful, present two or three options with advantages, disadvantages, complexity, estimated infrastructure cost, development implications, maintainability, scalability and lock-in risk. Cover:
   - **Client:** Flutter, React Native, native iOS and Android, or another fit; implications for performance, platform coverage, speed and maintenance.
   - **Backend:** language and framework, API style (REST, GraphQL, other), authentication, authorization, business logic placement, background jobs, integrations, real-time needs. Include a managed backend-as-a-service as a candidate when it fits.
   - **Data:** database technology, entities and relationships, schema, indexes, constraints, validation, migrations, backup and recovery. Include an ER diagram (Mermaid).
   - **Files:** images, documents, uploads, generated and temporary files, backups.
   - **Infrastructure:** provider, hosting model, environments, CDN, networking, domains, monitoring, logging.
   - **Security and privacy:** authentication and authorization model, secrets management, encryption, input validation, rate limiting, dependency scanning, access control, and the data-protection rules that may apply (for example GDPR). Flag regulatory questions as needing qualified validation; make no compliance claims.
   - **Scalability:** what handles the assumed load, the first bottleneck, and when each component would need upgrading or replacing.
4. In parallel where useful, have `security-reviewer` challenge the security design and `devops-engineer` check the infrastructure and cost estimate.
5. Verify claims that drive the decision: current pricing pages, version support, platform requirements. Label estimates.
6. Write one ADR per significant decision in `docs/10-decisions/` using `templates/adr.md` (context, options, decision, reasoning, consequences).
7. Ask `senior-supervisor` for an independent review of the whole proposal; resolve or record every objection.
8. Update `docs/traceability.md` (requirement → component `C-n`).
9. `factory.py complete 4`.

## Gate 4

The user approves the architecture, stack, infrastructure and cost implications. After approval, do not substitute technologies or change the architecture materially without `reopen 4` and a new approval.

## Deliverables (in `docs/04-architecture/` unless noted)

`architecture.md` (with diagrams), `tech-stack.md`, `database.md`, `api-spec.md`, `infrastructure.md`, `security.md`, `scalability.md`, `operating-costs.md`, and at least one `docs/10-decisions/ADR-*.md`
