# Vruk Skill Catalog

Curated, git-versioned catalog of **content skills** for Vruk installs, owned by
[EdgeSecureInc](https://github.com/EdgeSecureInc). A fresh install clones this
repo (no keys — it is public by design) to `runtime/skilltree/catalog-repo/` and
installs every `ships_by_default` skill into its runtime store; a timer
`git fetch`es for updates; rollback is `git checkout <tag/ref>` +
re-scan/re-install. Git history is the version log.

## What this repo is (and is not)

This repo owns exactly three things:

- `manifest.yaml` — the catalog (schema v1): one entry per curated skill, with
  version, `content_hash`, and provenance.
- `skills/` — the skill content itself (instructional `SKILL.md` + references).
- `tools/skillhash.py` — the canonical `content_hash` algorithm.

It holds **content only**: no policy, no whitelists/blacklists, no secrets, no
code the runtime executes. It does NOT own:

- the install/update machinery (`scripts/skill_catalog_install.py`, the fetch
  timer, the SkillTree scanner, the ST-9 allowlist in `config/skilltree.yaml`)
  — that ships with the installers in Vruk-Forge;
- META/machinery skills (skilltree, skillforge, the hermes scouts) — those
  version with the gateway code under `templates/meta-skills/` in Vruk-Forge;
- installers, the web UI, or fleet monitoring (see Related repos).

## Read order

1. This README — the contract.
2. `manifest.yaml` — what the catalog currently ships.
3. `CHANGELOG.md` — release notes (git tags mark releases; history lives ONLY
   here, never inline in other docs).
4. `skills/<runtime>/<slug>/SKILL.md` — the content, each labelled with its own
   qualification/archival status.

## How installed boxes consume this repo (ST-7 / ST-9)

Authoritative detail lives with the machinery, in the installers' install-root
doc `docs/vruk-skills.md` (Vruk-Forge, per variant). Summary:

- **ST-7 (catalog):** the installer clones this repo to
  `runtime/skilltree/catalog-repo/` and runs
  `scripts/skill_catalog_install.py --install`, which installs every
  `ships_by_default` skill into its runtime store after a fail-closed
  `skillforge.validate` gate, and writes a `vruk-version.json` sidecar beside
  each installed SKILL.md (catalog repo/ref/commit, id, version,
  `content_hash`). Idempotent: sidecar hash == manifest hash ⇒ untouched.
- **ST-9 (allowlisted auto-update):** a systemd timer runs `--fetch`
  (ff-only) every 6h; when this repo is allowlisted in the box's
  `config/skilltree.yaml`, a changed clone auto-updates `ships_by_default` +
  sidecar-tracked skills with no prompt (validate gate still runs); otherwise
  installed skills are untouched and the catalog just shows "update available".
- Rollback: `--rollback <tag/ref>` then `--install`. Repo URL override:
  `VRUK_SKILL_CATALOG_URL`.

## Layout

```
manifest.yaml            # the catalog: one entry per skill (see schema below)
CHANGELOG.md             # release notes; git tags mark releases
tools/skillhash.py       # canonical content_hash algorithm
skills/
  pydantic/<slug>/SKILL.md   # Assistant skills          -> vaults/Assistant/skills/<slug>/
  hermes/<slug>/SKILL.md     # two-brain agent skills    -> ~/.hermes/skills/vruk/<slug>/
  omni/<slug>/SKILL.md       # agent-neutral; installer/runtime maps the target store
```

A skill needed by more than one runtime is one **family** with a per-runtime
variant under each runtime dir, sharing a `family` id in the manifest. A new AI
runtime = a new subdir + a new target-store mapping.

## Qualification status

The supported install variants are **LiteRag_Pydantic** and **LiteRag_Hermes**
(one-shot installers in Vruk-Forge). Current catalog entries:

| Skill | Status |
| --- | --- |
| `vruk-omni-backup` | ARCHIVED-ERA content (retired RagStackProxy/OutWorlder two-brain era). **Not yet qualified against current LiteRag variants.** |
| `vruk-omni-graphiti` | ARCHIVED-ERA content (retired RAGStack phase installs; Graphiti/Neo4j are not part of current variants). **Not yet qualified against current LiteRag variants.** |

Archived-era skills stay in the catalog for reference and carry a conspicuous
banner in their SKILL.md; treat every path/script in them as unverified until a
skill is explicitly qualified against a supported variant.

## Manifest entry

```yaml
- id: skill-scout            # stable slug — NEVER put a version in it
  family: skill-scout        # groups per-runtime variants
  runtime: hermes            # pydantic | hermes | omni | <future-agent>
  path: skills/hermes/skill-scout
  kind: instructional
  trust: curated
  install_policy: confirm_once
  ships_by_default: true     # fresh install seeds this from the clone
  version: 1                 # our monotonic version
  updated: 2026-07-09
  content_hash: sha256:...    # tools/skillhash.py over the skill dir
  upstream_url: null         # set when the skill is vendored from a third party
  upstream_ref: null         # the exact upstream commit/tag vendored
  description: One line shown in catalogs.
```

## Versioning

- Bump `version` + `updated` + `content_hash` whenever a skill's content changes.
- Per-skill release tags: `skill/<runtime>/<id>/v<version>`; normal repo tags mark
  catalog releases. Skill names never carry versions or dates.
- Installed copies carry a `vruk-version.json` sidecar recording the
  version/hash/catalog ref they came from; a newer manifest version/hash means
  "update available".
- Third-party vendored skills pin `upstream_url` + `upstream_ref`; re-vendoring
  bumps `version`.

## Clean-clone verification

From a fresh clone, verify the manifest hashes match the content:

```bash
python3 tools/skillhash.py skills/omni/vruk-omni-backup skills/omni/vruk-omni-graphiti
grep content_hash manifest.yaml
```

Every printed hash must equal the corresponding manifest `content_hash`. The
algorithm (sha256 over sorted relative paths + bytes, skipping dotfiles and the
`vruk-version.json` sidecar) MUST stay byte-identical to the consumer copy in
the installers' `scripts/skill_catalog_install.py`.

## Related repos (EdgeSecureInc)

- [Vruk-Forge](https://github.com/EdgeSecureInc/Vruk-Forge) — ecosystem source
  of truth; the only supported installers (LiteRag_Pydantic, LiteRag_Hermes)
  and the catalog-consuming machinery.
- [Vruk-Console](https://github.com/EdgeSecureInc/Vruk-Console) — the web UI.
- [Vruk-MotherShip](https://github.com/EdgeSecureInc/Vruk-MotherShip) —
  internal fleet monitor.
