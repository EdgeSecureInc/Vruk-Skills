# AGENTS.md — Vruk-Skills

Entry contract for agents (and humans) working in this repo.

## What this repo is

The curated, public, git-versioned **skill catalog** consumed by installed Vruk
boxes (manifest schema v1 + content skills). Content only — no policy, no
secrets, no executable runtime code. The install/update machinery, META skills,
and the ST-9 allowlist live in the installers inside Vruk-Forge, not here.

## Read order

1. `README.md` — the full contract (layout, manifest schema, ST-7/ST-9
   consumption, qualification status, verification).
2. `manifest.yaml` — what ships.
3. `CHANGELOG.md` — history. History lives ONLY here; other docs stay timeless.
4. `skills/<runtime>/<slug>/SKILL.md` — the content itself.

## Hard rules

- **Hashes are load-bearing.** Any change to files under a skill directory
  (`skills/<runtime>/<slug>/`) invalidates that skill's manifest
  `content_hash`. After every content edit: bump `version`, set `updated`,
  regenerate the hash with `python3 tools/skillhash.py <skill-dir>`, and update
  `manifest.yaml`. Never edit skill content without doing all three.
- `tools/skillhash.py` must stay byte-identical in behavior to
  `skill_content_hash()` in the installers' `scripts/skill_catalog_install.py`
  (Vruk-Forge). Changing the algorithm on one side breaks update detection on
  every installed box.
- Skill ids/dirs are stable slugs — never put versions or dates in names.
- No inline changelogs in docs or skills; append to `CHANGELOG.md` only.
- Never claim a skill is qualified against a variant (LiteRag_Pydantic /
  LiteRag_Hermes) without an actual qualification run; unknown status is stated
  as "not yet qualified against current variants".
- Archived-era content (retired HiveMind/Citadel/RagStackProxy/RAGStack/
  OutWorlder terminology) must carry a conspicuous ARCHIVED-ERA banner and must
  never read as current instructions.
- This repo is public by design: nothing secret, nothing box-specific
  (no private hostnames, ports, keys, or user paths beyond generic `~/…`
  examples).

## Verify before handing off

```bash
python3 tools/validate_catalog.py
```

## Related repos (EdgeSecureInc)

Vruk-Forge (source of truth + installers) · Vruk-Console (web UI) ·
Vruk-MotherShip (fleet monitor).
