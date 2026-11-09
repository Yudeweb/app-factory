# Stage 8: Business strategy and go-to-market

**Objective:** a practical launch plan the user can choose from, built on the accepted product and refreshed research.

**Inputs:** the accepted application, `docs/01-research/`, `docs/02-product/`.

## Steps

1. `factory.py start 8`.
2. Have `product-researcher` refresh competitor pricing and positioning; the stage 1 research may be months old. Add new sources to `docs/01-research/sources.md`.
3. Brief `business-strategist` (with `product-manager` for the roadmap) to produce:
   - `business-strategy.md`: positioning, target customers, competitor positioning, unique value proposition, monetization model, brand identity direction.
   - `pricing.md`: pricing hypotheses with the reasoning and the experiments that would validate them.
   - `go-to-market.md`: launch roadmap in milestones, acquisition channels, marketing strategy, content, SEO, social media, launch campaigns, retention, feedback collection. Each channel carries a cheap validation experiment to run before committing real budget.
   - `store-listing.md`: App Store and Google Play titles, subtitles, descriptions, keywords and screenshot plan, with store-optimization reasoning.
   - `landing-page-spec.md`.
   - `kpis.md`: the metrics, their definitions, targets labeled as hypotheses, and the analytics events needed to measure them.
   - `launch-checklist.md`, including store accounts, legal pages, privacy disclosures and review requirements.
   - `post-launch-roadmap.md`: what to build next under each plausible outcome of launch.
4. Budgets: separate verified costs (with source and date) from estimates and assumptions.
5. `factory.py complete 8`.

## Final gate

The user approves the strategy and chooses which activities to execute. Spending money, publishing campaigns, submitting to stores and releasing anything publicly each need explicit authorization for that specific action; approval of the strategy document is not authorization to execute it.

## Deliverables (all in `docs/09-business/`)

`business-strategy.md`, `go-to-market.md`, `pricing.md`, `store-listing.md`, `landing-page-spec.md`, `kpis.md`, `launch-checklist.md`, `post-launch-roadmap.md`
