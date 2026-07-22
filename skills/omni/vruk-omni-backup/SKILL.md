---
name: vruk-omni-backup
description: Use for Vruk backup, restore, Git backup stub, and rebuild drills (archived RagStackProxy-era procedure).
---

# Vruk Backup Skill

> **ARCHIVED-ERA CONTENT.** This skill describes the retired
> RagStackProxy/OutWorlder two-brain era (phase-numbered installs,
> `vaults/OutWorlder/`, OutWorlder boundary tests). It is not yet qualified
> against the current supported variants (LiteRag_Pydantic / LiteRag_Hermes).
> Verify every script and path against your installed box before acting on it.

Use this skill for Vruk backup and restore work (retired-era "Phase 13" procedure).

## Runtime Boundaries

- Use the wrapper scripts.
- Include `vaults/Assistant/`, `vaults/OutWorlder/`, `policies/`, `config/`, SQLite audit/queue data, approval queues, handoff records, audit records, and resources.
- Exclude provider keys, OAuth state, private keys, raw credentials, `runtime/qdrant/`, generated index notes, prior backups, and temporary files.
- Destructive live restore is forbidden by default.
- Remote Git backup push is disabled until explicitly configured and human-approved.

## Standard Checks

```bash
./scripts/create_vruk_backup.py
./scripts/run_rebuild_drill.sh
./scripts/run_outworlder_boundary_tests.sh
```

## Expected Locations

```text
runtime/backups/
runtime/restore_drills/
resources/
resources/manifests/
config/backup/
```

## Non-Claims

This skill does not claim production disaster recovery, encrypted offsite retention, cloud sync, immutable backups, destructive live restore, OAuth/token portability, or full-machine restore.
