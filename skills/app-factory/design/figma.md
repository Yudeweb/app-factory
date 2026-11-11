# Design tool: Figma

Use only with a paid Figma seat. Figma's free Starter plan allows only a handful of AI tool calls a month (reported as 6, later 20), and a full design needs far more.

1. Check which Figma tools this session has (names containing `figma`; the write tool is `use_figma` at the time of writing) and check the account's plan and seat. On a Starter plan or a View seat, do not start: tell the user and ask which other tool to use.
2. Ask once which team or drafts location to use. Confirm write access with one small change. Never describe a Figma design that does not exist.
3. Build the design system as variables and components first, then compose screens from them. Frame names carry the screen ID (`SCR-n`). Batch work into as few tool calls as practical.
4. Connect the main journeys in a prototype.
5. Capture a screenshot of each frame for the self-check and for the user.
6. Record file and page links in `docs/design.md`.

If the plan's limit is reached part-way, stop, say what exists so far, and ask whether to continue in another tool.
