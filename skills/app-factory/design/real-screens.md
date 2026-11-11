# Design tool: real screens

The interface is built in the app's actual framework with sample data and shown running. Use when the technology in `plan.md` is decided and this machine can run it (iOS needs a Mac with Xcode and a simulator; web needs only a browser).

1. Create the minimal project skeleton for the approved framework: enough to build and launch, nothing else. No backend, no sign-in, no persistence.
2. Brief `developer` (with `ux-designer` reviewing) to build the design system first as real code (colour, type and spacing tokens; shared components), then every screen from those components, fed by a sample-data file with realistic content.
3. Wire navigation so every main journey runs. Each state (empty, loading, error) is reachable, for example through a debug switch or sample-data variants.
4. Launch it: the iOS Simulator tool for iOS, an emulator for Android, the browser for web. Capture a screenshot of every screen and state, light and dark if planned.
5. Record in `docs/design.md` how to launch it and which files hold the tokens, components and sample data.

Everything built here is kept: stage 4 replaces the sample data with real logic. Say so in the build plan so it is not built twice.
