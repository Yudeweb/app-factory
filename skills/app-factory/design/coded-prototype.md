# Design tool: high-fidelity coded prototype

A clickable prototype that looks like the finished app, not a wireframe. Use when nothing can be run yet or for a fast first look.

- **One self-contained file,** `docs/prototype/index.html`: all styles and scripts inline, no build step, no network requests at runtime (inline SVG icons; system fonts or one embedded font). It must open by double-click.
- **Tokens once:** colours, type scale, spacing and radii from the direction in `plan.md` as CSS variables, light and dark if planned. Every screen uses them; no one-off values.
- **Device frame:** for mobile, render inside a phone-sized frame (about 390 by 844) with status bar and safe areas, centred on the page. For web, real responsive layouts.
- **All screens in one file,** each a section with an id; navigation shows one at a time and every button or tab that should lead somewhere does. Keep a small screen index outside the frame to jump to any screen and state.
- **States:** empty, loading and error variants reachable from the index.
- **Realistic content:** plausible names, numbers, dates and lists; no placeholder text.
- **Polish:** consistent spacing, clear hierarchy, pressed and disabled states, simple transitions.

Open it in the browser tool to check it (see the stage guide), then tell the user how to open the file. If an Artifact tool is available, also publish it as a private page and give the link.
