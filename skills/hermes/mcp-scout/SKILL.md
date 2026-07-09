---
name: mcp-scout
description: Use for RagStackProxy tool_learning task packages — researching MCP servers for a desktop application, installing/registering the chosen server, verifying it, and creating the per-app skill. Triggers on task_type tool_learning or tool_learning_phase fields.
---

# MCP Scout Skill

Use this skill whenever a RagStackProxy task package has `task_type: tool_learning`
(or a `tool_learning_phase` field). The package's `tool_learning_app` names one
desktop application (e.g. "Blender", "GIMP"). Your job depends on the phase.

## Boundaries

- Work ONLY with the application named in the package. Never touch Assistant
  vaults or the package's forbidden_paths.
- You have NO shell in this workflow. You RESEARCH and PLAN; the local
  assistant runs the two validated connector commands (register + test)
  itself and handles anything needing the user. Do not attempt terminal
  commands, file writes, or installs.
- Prefer OFFICIAL servers (published by the app vendor) or the single clearly
  dominant community server. Never pick abandoned or obscure servers when a
  maintained popular one exists.
- Answer strictly in the JSON envelope the package's prompt demands. No
  markdown fences. Your FINAL message must be ONLY that JSON object —
  nothing before or after it.

## Phase: research  (tool_learning_phase == "research" or absent)

Research is read-only WEB work — use the web tools (web_search / web_extract),
NOT a shell. Do not run curl or any terminal command in this phase.

1. Try the PulseMCP registry via web_extract on
   `https://api.pulsemcp.com/v0beta/servers?query=<app>&count_per_page=10`
   (results carry github_stars). This is BEST-EFFORT: the endpoint may return
   403/410 to some fetchers. If it fails, do NOT abort — fall back to a
   web_search for "<app> MCP server github" and read the top GitHub repos
   directly. Also cross-check `<app> site:github.com MCP` and the official
   registry page. A single good source is enough; never return empty just
   because one registry was unreachable.
2. For each candidate worth returning, capture: how the client runs it (the
   stdio command, e.g. `uvx blender-mcp`), whether the app needs an app-side
   plugin/addon, and any app version requirements.
3. Return up to 4 options in `tool_options` (shape per the task prompt).
   `official=true` only for vendor-published servers or a single dominant
   community server (an order of magnitude more adoption than alternatives).
   Rank by stars/maintenance; put the best first.

## Phase: setup  (tool_learning_phase == "setup")

The package carries `chosen_option` (name/install/source_url). Produce a PLAN
(you run nothing). Work out, from the chosen option:

1. **Connector command**: how the local assistant should launch the server —
   the runner `command` (one of uvx | uv | npx | python | python3 | pipx |
   node | docker) and its `args` list. Example for BlenderMCP: command `uvx`,
   args `["blender-mcp"]`. Pick a short lowercase `slug` (e.g. `blender-mcp`).
2. **System prerequisites** the user must do themselves → `human_steps`, each
   `{title, command, why}`. Includes the app install if it is not obviously
   already present and any `uv`/runtime install the connector needs. sudo
   ALWAYS goes here, never run by anyone but the user.
   - Always target the **latest STABLE** release of the app, not whatever a
     distro repo happens to ship (operator rule). Check the current stable
     version during research; if the distro package is materially behind,
     prefer an install method that delivers latest stable — the vendor's
     official Flatpak/Snap/PPA/repo or download — over a bare
     `apt install`. Note the version the chosen method installs in `notes`.
3. **In-app add-on**: set `connector.plugin_needed` true when the server needs
   an add-on/plugin enabled inside the app (BlenderMCP's addon.py + start the
   server from its panel; GIMP script-fu; etc.). Put the exact enable/start
   instructions in a `human_step` with an empty command (it is a GUI action),
   describing precisely where to click and what to start.
4. **Per-app skill**: write `skill_name` (`<app-slug>-driver`) and `skill_body`
   — the markdown body (NO frontmatter) the local assistant will save. Cover:
   the connector slug, how to confirm the app is running, core workflows for
   common asks in this app, and honesty rules (report failures plainly, never
   invent tool output).
5. Return JSON keys: `phase_status` ("plan_ready" | "failed"), `connector`
   ({slug, command, args, plugin_needed}), `human_steps` (array; [] when
   none), `skill_name`, `skill_body`, `notes` (short; app/version notes).

The local assistant then registers the connector (`hermes mcp add`), saves the
skill, and either tests immediately or relays your human_steps to the user.

## Phase: verify

Verification is done LOCALLY by the assistant (it runs `hermes mcp test`); you
are not called for it. If the connector still is not responding, the assistant
asks the user to make sure the app + its add-on are running, then re-tests.

## Record keeping

In every phase, also return `lesson_candidates` for durable tips learned
about this app/server (installation quirks, version constraints) so future
runs get faster.
