# Vruk Skill Catalog

Curated, git-versioned catalog of **content skills** for Vruk installs. A fresh
install clones this repo (no keys — it is public by design) to
`runtime/skilltree/catalog-repo/` and installs every `ships_by_default` skill into
its runtime store; a timer `git fetch`es for updates; rollback is `git checkout
<tag/ref>` + re-scan/re-install. Git history is the version log.

This repo holds **content only**: no policy, no whitelists/blacklists, no secrets,
no code the runtime executes. Framing/machinery skills (skilltree, skillforge)
version with the gateway code and are NOT here.

## Layout

```
manifest.yaml            # the catalog: one entry per skill (see schema below)
CHANGELOG.md             # release notes; git tags mark releases
tools/skillhash.py       # canonical content_hash algorithm
skills/
  pydantic/<slug>/SKILL.md   # Assistant skills   -> vaults/Assistant/skills/<slug>/
  hermes/<slug>/SKILL.md     # OutWorlder skills  -> ~/.hermes/skills/vruk/<slug>/
  omni/<slug>/SKILL.md       # agent-neutral; installer/runtime maps the target store
```

A skill needed by more than one runtime is one **family** with a per-runtime
variant under each runtime dir, sharing a `family` id in the manifest. A new AI
runtime = a new subdir + a new target-store mapping.

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
