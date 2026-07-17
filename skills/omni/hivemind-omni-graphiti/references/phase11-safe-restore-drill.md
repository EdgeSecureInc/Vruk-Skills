# Phase 11 Safe Restore Drill

Use this reference when resuming Hivemind RAGStack after Phase 10 backup readiness is green and the user asks to run Phase 11.

## Source/runtime boundary

- Source/template repo: `~/Vruk-Forge` (clone of `EdgeSecureInc/Vruk-Forge`)
- Runtime/install root: `~/<ragstack-install-root>`
- Copy Phase 11 files from:
  `~/Vruk-Forge/hivemind/RAGStack/templates/install-root`
- Copy into:
  `~/<ragstack-install-root>`

## Phase 11 read set

Read the canonical installer path first, then Phase 11 files:

- `ReadMe.md`
- `HIVEMINDMAP.md`
- `hivemind/RAGStack/START_HERE.md`
- `hivemind/RAGStack/prompts/install-master-prompt.md`
- `hivemind/RAGStack/docs/phase-11-restore-drill.md`
- `hivemind/RAGStack/checklists/phase-11.md`
- `hivemind/RAGStack/prompts/stages/26-phase11-restore-drill.md`

## Baseline before Phase 11

Run from the runtime root and require Phase 10 green before copying/running Phase 11:

```bash
./scripts/check_stack.sh
./scripts/run_phase10_all_tests.sh
```

Expected key marker:

- `PHASE10_BACKUP_ALL_TESTS_PASS`

## Phase 11 files to copy

```text
config/backup/restore_policy.yaml
scripts/restore_hivemind_backup_drill.py
scripts/phase11_restore_status.sh
scripts/run_phase11_restore_tests.py
scripts/run_phase11_restore_tests.sh
scripts/run_phase11_all_tests.sh
tests/restore_scenarios/phase11_restore_scenarios.yaml
tests/expected_results/phase11_expected_behaviors.yaml
```

Make scripts executable after copying.

## Validation sequence

```bash
./scripts/phase11_restore_status.sh
./scripts/run_phase11_restore_tests.sh
./scripts/run_phase11_all_tests.sh
./scripts/restore_hivemind_backup_drill.py --dry-run --json
./scripts/restore_hivemind_backup_drill.py --execute --i-understand --json
```

If no Phase 10 archive exists, create one first:

```bash
./scripts/create_hivemind_backup.py --execute --i-understand --json
```

Expected Phase 11 markers:

- `PHASE11_RESTORE_POLICY_PASS`
- `PHASE11_RESTORE_STATUS_PASS`
- `PHASE11_RESTORE_STATIC_TESTS_PASS`
- `PHASE11_RESTORE_ALL_TESTS_PASS`
- `PHASE11_RESTORE_DRY_RUN_PASS`
- `PHASE11_RESTORE_DRILL_PASS`
- `PHASE11_RESTORE_VERIFY_PASS`

## Safety checks

The drill must restore only into `runtime/restore_drills/phase11/` by default. Verify:

- `target_is_live_root` is false.
- Restore target path starts under `<ragstack-install-root>/runtime/restore_drills/phase11/`.
- The live install root was not overwritten.
- `PHASE11_RESTORE_REPORT.json` exists in the restore target.
- Forbidden restored path hits are empty, especially:
  - `.env.local`
  - `runtime/graphiti/secrets/neo4j_password`
  - `runtime/graphiti/graphiti.env`
  - `runtime/graphiti/venv`
  - `runtime/qdrant/storage`
  - `runtime/mem0`
  - `runtime/ollama`

## Reporting

Append the Phase 11 status to `INSTALL_REPORT.local.md` with:

- baseline Phase 10 status
- copied Phase 11 files
- status/test markers
- archive path used
- restore drill target path
- restored file count
- forbidden-path check result
- restore report path
- explicit non-claims

Non-claims to preserve: not production disaster recovery, not encrypted offsite backup retention, not live database consistency for every store, not OAuth/API-token portability, not full-machine image restore, not safe destructive restore onto the live install root.
