# Stage 2: Design

**Objective:** let the user see and approve what the app will look like before it is built, and leave one handoff document developers can build from.

**Inputs:** `plan.md` (scope, platform and design direction) and the platform file's design notes.

**API or backend only:** there are no screens. Follow the API-only path in `platforms/web.md`: `software-architect` writes the API contract to `docs/design.md`, then `factory.py complete 2`.

## Steps

1. `factory.py start 2`.

2. **Choose how to see the screens.** Ask one question, recommending by situation, then read only that tool's guide in `design/`:
   - **Real screens** (`design/real-screens.md`): built in the app's framework with sample data and run in the simulator or browser. Recommend when the machine can run the chosen technology; the work carries into the build.
   - **High-fidelity coded prototype** (`design/coded-prototype.md`): recommend when nothing can be run yet or for a fast first look.
   - **Penpot** (`design/penpot.md`): free editable design file.
   - **Figma** (`design/figma.md`): only with a paid seat.

3. **Structure.** Brief `ux-designer` for the navigation model, the screen list (`SCR-n`, each linked to requirement IDs) and the flow of each main journey. Check that every must-have requirement has a screen. If a choice changes the experience materially (navigation model, onboarding length), put two or three options to the user before detailed work.

4. **Design system, then screens,** in the chosen tool, to this bar whatever the tool:
   - colours, type and spacing from the direction in `plan.md`, defined once and used everywhere;
   - every screen in the list, with realistic content for this product, never placeholder text;
   - empty, loading and error states; real icons; a phone frame for mobile; light and dark if planned;
   - contrast and touch-target or click-target sizes meet WCAG 2.2 AA;
   - every main journey can be clicked through from start to finish.

5. **Check it yourself before the user sees anything.** Open the design (browser tool, simulator, or exported images), walk every main journey, and screenshot each screen and state. Compare against the screen list and the bar above. Fix what is broken, missing or plain, and check again. Never present a design in which a journey cannot be completed or a screen is unstyled; if the tool cannot get there, say so and ask whether to switch tools.

6. **Show it:** the screenshots in chat, plus the link or exact way to open it.

7. `docs/design.md`: the tool used and how to open the design; screen list with states and the requirements each serves; design tokens in a form developers can use; behaviour notes; assets; open accessibility issues.

8. `factory.py complete 2`.

## Gate 2

The user approves the design. State which tool was used and anything that could not be shown.
