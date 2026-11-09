# Stage 3: UI/UX design in Figma

**Objective:** an editable Figma design and prototype that covers the approved MVP, plus a handoff developers can build from.

**Inputs:** approved `docs/02-product/`.

## Figma access comes first

Check which Figma tools this session has (tool names containing `figma`; Figma's remote server exposes a write-to-canvas tool, `use_figma` at the time of writing).

- **Write tools available:** design directly in Figma.
- **Read-only tools, or no Figma tools:** tell the user plainly what is missing and how to connect the Figma connector (or add the remote server at `https://mcp.figma.com/mcp`), and ask whether to wait or to continue with the fallback below. Do not pretend a design exists in Figma when it does not.
- **Fallback, only with the user's agreement:** build the screens as a clickable HTML prototype in `docs/03-design/prototype/` using the design tokens, and record in `figma-links.md` that the Figma file is still to be produced. Figma's code-to-canvas feature can import it later.

Ask the user once which Figma team or drafts location to use, and record file links in `docs/03-design/figma-links.md`.

## Steps

1. `factory.py start 3`.
2. Brief `ux-designer` for **UX structure** first: information architecture, navigation model, screen inventory (`SCR-n`, each linked to user stories), user flows for every major journey, interaction patterns, and the empty, loading and error state of every screen, plus onboarding and authentication if the product has them.
3. Review the structure against the PRD: every must-have story has a screen and a flow. If a choice materially changes the experience (navigation model, onboarding length, visual direction), present two or three alternatives with trade-offs and let the user choose before high-fidelity work.
4. **Design system:** colors, typography, spacing scale, components (buttons, forms, navigation, cards, dialogs), icons, light and dark modes where appropriate, responsive behavior. Built as Figma variables and components so screens reuse them.
5. **Screens:** wireframes, then high-fidelity designs for every screen in the inventory, built from the design-system components.
6. **Prototype:** connect the main journeys so they can be clicked through.
7. **Evaluation:** check contrast and touch-target sizes against WCAG 2.2 AA, consistency of components, and that every flow can be completed. Record findings and fixes in `design-spec.md`.
8. **Handoff** (`handoff.md`): per screen, the Figma link, components used, states, behavior notes, assets to export, and design tokens in a form developers can consume.
9. Update `docs/traceability.md` (story → screen).
10. `factory.py complete 3`.

## Gate 3

The user approves the UX, the visual design and the prototype. Give the Figma links and say clearly if any part was produced through the fallback.

## Deliverables (all in `docs/03-design/`)

`figma-links.md`, `screen-inventory.md`, `user-flows.md`, `design-system.md`, `design-spec.md`, `handoff.md`
