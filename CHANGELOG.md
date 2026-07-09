# Changelog

## v2 — 2026-07-09

Removed `skill-scout` and `mcp-scout`: reclassified as META skills (machinery
hardwired to gateway code — `--skills` preloads in `outworlder_client.py`). They
now ship with the INSTALLER under `templates/meta-skills/hermes/` as
`hivemind-hermes-skill-scout` / `hivemind-hermes-mcp-scout` (#96 naming
convention) and update through installer releases, not this catalog. The catalog
keeps content skills only: `hivemind-backup`, `hivemind-graphiti`.

## v1 — 2026-07-09

Initial catalog. Relocated the four content skills previously baked into the
installer (`templates/install-root/skills/`) — vendored from the live
RagStackProxy repo copies (source of truth; the deployed hermes-store copies of
mcp-scout/hivemind-backup had drifted older, see AIAgentTemplates#98):

- `skills/hermes/skill-scout` v1
- `skills/hermes/mcp-scout` v1
- `skills/hermes/hivemind-backup` v1
- `skills/hermes/hivemind-graphiti` v1 (vendored from the deployed store — it had no repo copy)
