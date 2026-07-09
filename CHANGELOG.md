# Changelog

## v1 — 2026-07-09

Initial catalog. Relocated the four content skills previously baked into the
installer (`templates/install-root/skills/`) — vendored from the live
RagStackProxy repo copies (source of truth; the deployed hermes-store copies of
mcp-scout/hivemind-backup had drifted older, see AIAgentTemplates#98):

- `skills/hermes/skill-scout` v1
- `skills/hermes/mcp-scout` v1
- `skills/hermes/hivemind-backup` v1
- `skills/hermes/hivemind-graphiti` v1 (vendored from the deployed store — it had no repo copy)
