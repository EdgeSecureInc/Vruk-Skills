# Phase 10 Backup Readiness Reference

This reference captures the proven Phase 10 command sequence and the update/rerun lessons for Graphiti-aware backup readiness.

## Source and runtime roots

```text
Source/template repo:
/home/edgesecure/AIAgentTemplates

Runtime/install root:
/home/edgesecure/DenchoHivemindRAGStack

Active Hermes skill install:
/home/edgesecure/.hermes/skills/hivemind/hivemind-graphiti
```

## Required baseline before Phase 10

Run from the runtime/install root and require Phase 9 to be green before Phase 10 backup work:

```bash
./scripts/check_stack.sh
./scripts/run_phase9_all_tests.sh
./scripts/graphiti_smoke_test.py --json
./scripts/graphiti_namespace_status.py --json
./scripts/graphiti_export_view.py --json
```

Expected Phase 9 markers:

```text
PHASE9_GRAPHITI_ALL_TESTS_PASS
PHASE9_GRAPHITI_NAMESPACE_PASS
PHASE9_GRAPHITI_EXPORT_PASS
```

Do not continue Phase 10 if Phase 9 is not green.

## Source/runtime drift check before rerun

When the user says Phase 10 was updated, first compare the packaged source files with the runtime copies. At minimum check these paths under `templates/install-root` vs the runtime root:

```text
config/backup/backup_policy.yaml
scripts/create_hivemind_backup.py
scripts/verify_hivemind_backup.py
scripts/phase10_backup_status.sh
scripts/run_phase10_backup_tests.py
scripts/run_phase10_backup_tests.sh
scripts/run_phase10_all_tests.sh
tests/backup_scenarios/phase10_backup_scenarios.yaml
tests/expected_results/phase10_expected_behaviors.yaml
skills/hivemind-graphiti/SKILL.md
skills/hivemind-graphiti/references/phase10-backup-readiness.md
```

Useful quick comparison pattern:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, json
SRC=Path('/home/edgesecure/AIAgentTemplates/hivemind/RAGStack/templates/install-root')
DST=Path('/home/edgesecure/DenchoHivemindRAGStack')
files=[
 'config/backup/backup_policy.yaml',
 'scripts/create_hivemind_backup.py',
 'scripts/verify_hivemind_backup.py',
 'scripts/phase10_backup_status.sh',
 'scripts/run_phase10_backup_tests.py',
 'scripts/run_phase10_backup_tests.sh',
 'scripts/run_phase10_all_tests.sh',
 'tests/backup_scenarios/phase10_backup_scenarios.yaml',
 'tests/expected_results/phase10_expected_behaviors.yaml',
 'skills/hivemind-graphiti/SKILL.md',
 'skills/hivemind-graphiti/references/phase10-backup-readiness.md',
]
out=[]
for f in files:
    sp, dp = SRC/f, DST/f
    row={'file': f, 'source_exists': sp.exists(), 'runtime_exists': dp.exists()}
    for label, p in [('source', sp), ('runtime', dp)]:
        if p.exists():
            b=p.read_bytes(); row[label+'_sha256']=hashlib.sha256(b).hexdigest()
    row['differs']=row.get('source_sha256') != row.get('runtime_sha256')
    out.append(row)
print(json.dumps(out, indent=2, sort_keys=True))
PY
```

## Sync updated Phase 10 files

Copy the packaged Phase 10 files from source into runtime. Include the skill and its reference when source now carries the self-improvement:

```bash
SRC=/home/edgesecure/AIAgentTemplates/hivemind/RAGStack/templates/install-root
DST=/home/edgesecure/DenchoHivemindRAGStack
files=(
  config/backup/backup_policy.yaml
  scripts/create_hivemind_backup.py
  scripts/verify_hivemind_backup.py
  scripts/phase10_backup_status.sh
  scripts/run_phase10_backup_tests.py
  scripts/run_phase10_backup_tests.sh
  scripts/run_phase10_all_tests.sh
  tests/backup_scenarios/phase10_backup_scenarios.yaml
  tests/expected_results/phase10_expected_behaviors.yaml
  skills/hivemind-graphiti/SKILL.md
  skills/hivemind-graphiti/references/phase10-backup-readiness.md
)
for f in "${files[@]}"; do
  install -D -m 0644 "$SRC/$f" "$DST/$f"
done
chmod +x "$DST/scripts/create_hivemind_backup.py" \
  "$DST/scripts/verify_hivemind_backup.py" \
  "$DST/scripts/phase10_backup_status.sh" \
  "$DST/scripts/run_phase10_backup_tests.py" \
  "$DST/scripts/run_phase10_backup_tests.sh" \
  "$DST/scripts/run_phase10_all_tests.sh"
```

If the user asks to keep the active Hermes skill in sync, reinstall it from the source template too:

```bash
install -D -m 0644 "$SRC/skills/hivemind-graphiti/SKILL.md" \
  /home/edgesecure/.hermes/skills/hivemind/hivemind-graphiti/SKILL.md
install -D -m 0644 "$SRC/skills/hivemind-graphiti/references/phase10-backup-readiness.md" \
  /home/edgesecure/.hermes/skills/hivemind/hivemind-graphiti/references/phase10-backup-readiness.md
```

## Phase 10 command sequence

Run from the runtime/install root:

```bash
./scripts/phase10_backup_status.sh
./scripts/run_phase10_backup_tests.sh
./scripts/run_phase10_all_tests.sh
./scripts/create_hivemind_backup.py --dry-run --json
./scripts/create_hivemind_backup.py --execute --i-understand --json
./scripts/verify_hivemind_backup.py <ARCHIVE_PATH_FROM_CREATE_STEP> --json
```

Expected Phase 10 markers:

```text
PHASE10_BACKUP_POLICY_PASS
PHASE10_BACKUP_STATUS_PASS
PHASE10_BACKUP_STATIC_TESTS_PASS
PHASE10_BACKUP_ALL_TESTS_PASS
PHASE10_BACKUP_DRY_RUN_PASS
PHASE10_BACKUP_CREATE_PASS
PHASE10_BACKUP_VERIFY_PASS
```

The updated test suite should include skill-source sync checks such as:

```text
graphiti_skill_source_synced
phase10_reference_exists
phase10_reference_markers_present
phase10_reference_forbidden_paths_present
```

In the updated rerun observed during this session, Phase 10 reported 27/27 passing tests after the skill/reference sync.

## Backup archive expectations

The backup archive should contain:

```text
BACKUP_MANIFEST.json
config/backup/backup_policy.yaml
config/graphiti/graphiti_runtime.yaml
config/graphiti/namespaces.yaml
gateway/hivemind_graphiti.py
profiles/hivemind/profile_manifest.yaml
runtime/graphiti/exports/latest_graph_summary.json
runtime/graphiti/viewer/index.html
```

The manifest should report Phase 9 artifacts present.

## Forbidden archive paths

The archive must not contain:

```text
.env.local
runtime/graphiti/secrets/neo4j_password
runtime/graphiti/graphiti.env
runtime/graphiti/venv
runtime/qdrant/storage
runtime/mem0
runtime/ollama
runtime/backups
runtime/test_runs
companies/*/docs
```

## Reporting requirements

Append a concise Phase 10 entry to:

```text
INSTALL_REPORT.local.md
```

Include:

- baseline Phase 9 status
- copied/synced files
- status/test markers
- dry-run selected/skipped counts
- archive path and size
- verify result
- forbidden archive hit count
- whether skill/source/runtime checksums match when relevant
- explicit non-claims

## Phase 10 non-claims

Phase 10 does not claim:

- production disaster recovery
- encrypted offsite backup retention
- live database consistency for every store
- OAuth/API-token portability
- full-machine image restore
- destructive restore safety

Do not perform destructive restore work unless a later phase explicitly authorizes it.
