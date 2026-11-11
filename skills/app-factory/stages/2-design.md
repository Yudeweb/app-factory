# Stage 2: Design

**Objective:** an editable Figma design and prototype covering the approved first version, and one handoff document developers can build from.

**Inputs:** `plan.md` (scope, platform and design direction) and the platform file's design notes.

**API or backend only:** there are no screens and no Figma. Follow the API-only path in `platforms/web.md`: `software-architect` writes the API contract to `docs/design.md`, then `factory.py complete 2`.

## Figma access first

Check which Figma tools this session has (names containing `figma`; the write-to-canvas tool is `use_figma` at the time of writing).

- **Can write:** design directly in Figma. Ask once which team or drafts location to use.
- **Read-only or absent:** tell the user what is missing and how to connect the Figma connector, and ask whether to wait or use the fallback. Never describe a Figma design that does not exist.
- **Fallback, only if the user agrees:** a clickable HTML prototype in `docs/prototype/` built from the design tokens, recorded in `docs/design.md` as a stand-in.

## Steps

1. `factory.py start 2`.
2. Brief `ux-designer` for structure first: navigation model, screen list (`SCR-n`, each linked to requirement IDs), and the flow for each main journey. Check that every must-have requirement has a screen. If a choice changes the experience materially (navigation model, onboarding length), put two or three options to the user before high-fidelity work.
3. Design system as Figma variables and components (colors, type, spacing, buttons, forms, navigation, dialogs), following the direction in `plan.md`.
4. Screens composed from those components, including empty, loading and error states, then a prototype connecting the main journeys.
5. Check contrast and touch-target sizes against WCAG 2.2 AA and fix what fails.
6. `docs/design.md`: Figma links; screen list with states and the requirements each serves; design tokens in a form developers can use; behavior notes; assets to export; open accessibility issues.
7. `factory.py complete 2`.

## Gate 2

The user approves the design and prototype. Give the Figma links and say plainly if any part used the fallback.
