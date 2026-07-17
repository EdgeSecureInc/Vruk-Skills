---
name: hivemind-omni-graphiti
description: Use for Hivemind Graphiti temporal brain work, graph search/export, namespace checks, Graphiti-aware backup readiness, and safe restore drill handoffs.
---

# Hivemind Graphiti Skill

Use this skill when a task involves the Hivemind temporal graph brain, profile brain maps, Graphiti namespaces, graph search, graph export, Graphiti-aware backup readiness, or safe restore drill handoffs.

## Core rule

Use the Hivemind Graphiti wrapper scripts. Do not use raw Graphiti MCP, raw Graphiti REST, raw Neo4j writes, or destructive graph operations unless your role explicitly allows it.

## Wrapper scripts

From the RAGStack install root:

```bash
./scripts/graphiti_search.py --query "..." --group-id company:BaseCompany:global --json
./scripts/graphiti_add_episode.py --name "..." --body "..." --group-id company:BaseCompany:profile:warden --source text --json
./scripts/graphiti_namespace_status.py --json
./scripts/graphiti_export_view.py --json
```

## Phase 9/10 install-resume pattern

When resuming installer work after Phase 9 or Phase 10:

- Treat the local source clone (e.g. `~/AIAgentTemplates`, from `EdgeSecureInc/Vruk-Forge`) as the source/template repo.
- Treat the RAGStack install root (e.g. `~/<ragstack-install-root>`) as the runtime/install root.
- Follow the canonical entry path before changing files:
  - `ReadMe.md`
  - `HIVEMINDMAP.md`
  - `hivemind/RAGStack/START_HERE.md`
  - `hivemind/RAGStack/prompts/install-master-prompt.md`
  - the active phase doc, checklist, and stage prompt.
- Re-run the prior phase baseline before installing the next phase.
- For Phase 10, require Phase 9 to be green before creating backup artifacts.
- Copy only the packaged template files for the active phase unless a source-truth doc says otherwise.
- For Phase 10, run the backup status, all-tests, dry-run, create, and verify sequence.
- Append concise results and explicit non-claims to `INSTALL_REPORT.local.md`.
- Do not run real ingestion, private/customer document processing, destructive restore, restart, or production disaster-recovery claims unless explicitly authorized.

Detailed Phase 10 command/reference notes live in:

```text
skills/hivemind-graphiti/references/phase10-backup-readiness.md
```

## Phase 10/11/12 resume notes

- Before rerunning Phase 10, compare the source-template Phase 10 files against the runtime install root and reinstall the Graphiti skill/reference files so useful Hermes self-improvements do not remain runtime-only.
- During a Phase 12.1/source-seal review, check Graphiti reference drift across all three copies: source template, runtime install root, and active Hermes skill. If the active Hermes Graphiti reference contains useful self-improvements, port it back into both source and runtime before declaring the source sealed.
- After resolving Graphiti reference drift, verify checksums for `skills/hivemind-graphiti/SKILL.md`, `references/phase10-backup-readiness.md`, and `references/phase11-safe-restore-drill.md` across source/runtime/active, then rerun the relevant prior-phase all-tests before reporting readiness for the next phase.
- Phase 10 must preserve Graphiti-safe exports and viewer artifacts, not raw Neo4j internals or Graphiti secrets.
- Phase 11 restore work must stay inside `runtime/restore_drills/phase11/` and must never overwrite the live install root by default.
- Phase 12 and later backup operations should primarily use the `hivemind-backup` skill. Use this Graphiti skill only for Graphiti baseline, namespace, smoke, export, or Graphiti-specific backup context.

Detailed Phase 11 command/reference notes live in:

```text
skills/hivemind-graphiti/references/phase11-safe-restore-drill.md
```

## Agent behavior

- Record meaningful agent events as episodes when your role permits it.
- Prefer short, useful episodes over dumping entire prompts or private documents.
- Preserve provenance with source descriptions such as `profile_summary`, `kanban_summary`, `approval_event`, `runtime_event`, or `document_schema`.
- Use profile namespaces for profile-specific context.
- Use company/global namespaces for shared context.
- Never write secrets, OAuth tokens, API keys, raw private documents, or hidden chain-of-thought content into Graphiti.

## Default write policy

- Warden may write/administer Graphiti through wrappers.
- Librarian may write curated knowledge episodes.
- Ledgerkeeper may write audit/approval episodes.
- Other profiles may search and propose writes unless later policy grants more access.

## Views

Graphiti-backed views are generated under:

```text
runtime/graphiti/exports/
runtime/graphiti/viewer/
```

Neo4j Browser can be used locally for live graph exploration when Neo4j is enabled.
