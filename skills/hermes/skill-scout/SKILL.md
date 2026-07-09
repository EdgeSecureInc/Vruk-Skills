---
name: skill-scout
description: Use for RagStackProxy skill_discovery task packages — researching published instructional skills for a capability the user wants, and (after the user approves one specific candidate) fetching that approved skill's SKILL.md. Triggers on task_type skill_discovery or a skill_discovery_phase field.
---

# Skill Scout Skill

Use this skill whenever a RagStackProxy task package has `task_type: skill_discovery`
(or a `skill_discovery_phase` field). The package's `skill_discovery_topic` names the
capability the user wants a ready-made skill for (e.g. "meeting notes", "changelog
writing"). Your job depends on the phase.

## Boundaries

- Work ONLY on the topic named in the package. Never touch Assistant vaults or the
  package's forbidden_paths.
- You have NO shell in this workflow. This is read-only WEB work — use the web tools
  (web_search / web_extract). Do NOT run curl, terminal commands, file writes, or
  installs. The local assistant validates and installs; you only research and fetch.
- Return INSTRUCTIONAL skills only — SKILL.md-style skills that are guidance/procedure
  the assistant reads. Do NOT return skills whose value is running a CLI, an MCP
  server, or external code; the local assistant cannot execute those.
- In the FETCH phase, fetch ONLY the single package named in `approved_candidate`.
  Never fetch, substitute, or bundle anything the user did not explicitly approve.
- Answer strictly in the JSON envelope the package's prompt demands. No markdown
  fences. Your FINAL message must be ONLY that JSON object — nothing before or after.

## Phase: research  (skill_discovery_phase == "research" or absent)

1. Search for published, INSTRUCTIONAL skills that deliver `skill_discovery_topic`.
   Good sources: GitHub repositories of `SKILL.md` / Claude-skill / prompt-skill
   collections (`<topic> skill SKILL.md site:github.com`, `awesome claude skills`),
   the curated HiveMind catalog repo when reachable, and public skill directories.
   Cross-check more than one source; a single strong source is enough, never return
   empty just because one registry was unreachable.
2. For each candidate worth returning, capture: a clear `name`, the `source_url`
   (the exact page/repo where the skill lives — REQUIRED; a candidate with no URL is
   useless because the user must see where it came from), a one-line `description`,
   and `telemetry`: `{github_stars: int, claude_installs: int-or-null, maintained:
   bool}`. Use real figures you can see; set `claude_installs` null when unknown and
   `maintained` from recent commit activity.
3. Return up to 4 candidates in `skill_candidates`, ranked best-first — prefer
   maintained skills with higher adoption (stars/installs). Return `[]` if nothing
   trustworthy and instructional exists. Do NOT invent stars or sources.

The local assistant then shows the user these candidates with their source and
telemetry and asks them to approve ONE. Nothing is fetched until they do.

## Phase: fetch  (skill_discovery_phase == "fetch")

The package carries `approved_candidate` ({name, source_url}) — the ONE skill the
user approved. Fetch that skill's `SKILL.md` from its source and return:

- `skill_content`: `{"name": ..., "description": ..., "body": ...}` where `body` is
  the skill's markdown instructions **with NO frontmatter** (strip any `---` block;
  the local assistant rebuilds its own clean frontmatter). Keep the body faithful to
  the source — do not add instructions of your own.

If the approved skill cannot be fetched (page gone, not actually a SKILL.md, or it
turns out to be a capability/executable skill rather than instructional), return
`skill_content: {}` and say so briefly in `work_summary`. Never fetch a different
skill as a substitute.

## Record keeping

In every phase, also return `lesson_candidates` for durable tips learned about
finding skills for this kind of topic (good source registries, quality signals) so
future runs get faster.
