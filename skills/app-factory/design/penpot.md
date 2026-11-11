# Design tool: Penpot

A free, open-source design tool with an official MCP server. Use when the user wants an editable design file without a paid Figma seat. This path has had little testing: say so, and fall back to another tool if it does not work rather than forcing it.

1. Check whether this session has Penpot tools (names containing `penpot`). If not, tell the user how to connect, following Penpot's current help page (https://help.penpot.app/mcp/): in Penpot, enable MCP under account Integrations, generate a key (shown once), copy the server URL, and add it to Claude as an MCP server. Never ask the user to paste the key into chat.
2. Confirm write access with one small change in a new file before designing. If it fails, report exactly what failed and ask which other tool to use.
3. Build the design system first (colours, typography, components), then compose screens from the components. Board names carry the screen ID (`SCR-n`).
4. Connect the main journeys with prototype interactions.
5. Export or capture each screen as an image for the self-check and for the user.
6. Record the Penpot file link in `docs/design.md`.
