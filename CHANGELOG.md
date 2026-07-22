# Changelog

## v4 — 2026-07-22

Catalog ids caught up with the ecosystem-wide `hivemind-*` → `vruk-*` rename
(Vruk-Forge#164 group 2, commit a5243ad, previously unchangelogged) and the
docs-unification pass (Vruk-Forge#181):

- Skill ids/dirs are now `vruk-omni-backup` and `vruk-omni-graphiti`
  (formerly `hivemind-omni-backup` / `hivemind-omni-graphiti`).
- Both skills bumped to v3: conspicuous ARCHIVED-ERA banners added — their
  content describes the retired RagStackProxy/OutWorlder two-brain phase
  installs (`vruk/RAGStack/…`, `HIVEMINDMAP.md`) and is not yet qualified
  against the current LiteRag_Pydantic / LiteRag_Hermes variants; internal
  reference paths fixed to the current dir names.
- `content_hash` regenerated for both skills. The v3-era manifest hashes had
  gone stale: content edits at 49f85d2/80d45fc/a5243ad never re-ran
  `tools/skillhash.py` or bumped versions.
- `tools/skillhash.py` now skips the current install sidecar name
  `vruk-version.json` (was still skipping the retired `hivemind-version.json`),
  matching the deployed `skill_catalog_install.py` algorithm. Catalog-side
  hashes are unaffected (catalog dirs carry no sidecar).
- README rewritten for the unified doc contract; AGENTS.md added.

## v3 — 2026-07-09

Renamed both content skills to the #96 convention with the `omni` segment
(usable by any agent; the concealment rule forbids the cloud agent's name in
user-visible skill names, so `omni` is the neutral segment for user-facing
skills):

- `hivemind-backup` → `hivemind-omni-backup` v2 (now `runtime: omni`, `skills/omni/`)
- `hivemind-graphiti` → `hivemind-omni-graphiti` v2 (same)

Installers older than the omni store mapping will skip these (reported, not
silent); pair with the matching RagStackProxy release.

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
