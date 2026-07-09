# Backup and Restore Operations Reference

Phase 13 owns the backup, restore, and rebuild procedure.

## Default local paths

- `runtime/backups/` holds local backup archives.
- `runtime/restore_drills/` holds safe restore-drill output.
- `resources/` holds large/non-Git assets that should be manifestable and later syncable.
- `resources/manifests/RESOURCE_MANIFEST.json` stores the resource manifest.

## Default sequence

```bash
./scripts/create_hivemind_backup.py
./scripts/run_hivemind_backup_cycle.py
./scripts/run_rebuild_drill.sh
./scripts/run_outworlder_boundary_tests.sh
```

## Default retention plan

- Keep latest 3 local backups.
- Keep every 10th backup as a long-term point.
- Never delete in dry-run mode.
- Execute deletion requires `--execute --i-understand`.

## Safe restore drill

Restore drills verify the archive manifest, required control-plane files, vaults, policy/config files, SQLite audit/queue data, handoff records, resources, Qdrant rebuildability, and forbidden-path exclusions. They must not target the live install root by default.

## Agent note

Phase 13 agents should run this procedure only after phases 1-12 are verified. Phase 10, Phase 11, and Phase 12 are prerequisites, not backup phases.
