#!/usr/bin/env python3
"""Fail-closed validation for the Vruk skill catalog."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from skillhash import skill_content_hash


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.yaml"
REQUIRED = {
    "id",
    "family",
    "runtime",
    "path",
    "kind",
    "trust",
    "install_policy",
    "ships_by_default",
    "version",
    "updated",
    "content_hash",
    "upstream_url",
    "upstream_ref",
    "description",
}


def scalar(value: str) -> object:
    value = value.strip()
    if value == "null":
        return None
    if value in {"true", "false"}:
        return value == "true"
    if value.isdigit():
        return int(value)
    return value.strip('"\'')


def load_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_skills = False

    for number, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].rstrip()
        if not line:
            continue
        if line == "skills:":
            in_skills = True
            continue
        if not in_skills:
            continue
        match = re.fullmatch(r"  - ([a-z_]+):\s*(.+)", line)
        if match:
            current = {match.group(1): scalar(match.group(2))}
            entries.append(current)
            continue
        match = re.fullmatch(r"    ([a-z_]+):\s*(.*)", line)
        if match and current is not None:
            key = match.group(1)
            if key in current:
                raise ValueError(f"line {number}: duplicate key {key}")
            current[key] = scalar(match.group(2))
            continue
        raise ValueError(f"line {number}: unsupported manifest syntax")

    if not entries:
        raise ValueError("manifest has no skill entries")
    return entries


def validate() -> list[str]:
    errors: list[str] = []
    entries = load_entries()
    seen_ids: set[str] = set()
    declared_paths: set[Path] = set()

    for entry in entries:
        skill_id = str(entry.get("id", "<missing-id>"))
        missing = sorted(REQUIRED - entry.keys())
        if missing:
            errors.append(f"{skill_id}: missing {', '.join(missing)}")
            continue
        if skill_id in seen_ids:
            errors.append(f"{skill_id}: duplicate id")
        seen_ids.add(skill_id)

        relative = Path(str(entry["path"]))
        skill_dir = (ROOT / relative).resolve()
        if ROOT not in skill_dir.parents or not skill_dir.is_dir():
            errors.append(f"{skill_id}: path is not a catalog directory: {relative}")
            continue
        declared_paths.add(skill_dir)
        if skill_dir.name != skill_id:
            errors.append(f"{skill_id}: id must match directory name {skill_dir.name}")
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_id}: missing SKILL.md")
            continue

        expected = str(entry["content_hash"])
        actual = skill_content_hash(skill_dir)
        if expected != actual:
            errors.append(f"{skill_id}: content_hash is {expected}; expected {actual}")

        if not isinstance(entry["ships_by_default"], bool):
            errors.append(f"{skill_id}: ships_by_default must be true or false")
        if not isinstance(entry["version"], int) or entry["version"] < 1:
            errors.append(f"{skill_id}: version must be a positive integer")

        qualification_text = (
            str(entry["description"]) + "\n" + skill_file.read_text(encoding="utf-8")
        ).lower()
        if entry["ships_by_default"] and (
            "archived-era" in qualification_text or "not yet qualified" in qualification_text
        ):
            errors.append(f"{skill_id}: archived or unqualified content cannot ship by default")

    actual_paths = {
        path.parent.resolve()
        for path in (ROOT / "skills").glob("*/*/SKILL.md")
    }
    for path in sorted(actual_paths - declared_paths):
        errors.append(f"unlisted skill directory: {path.relative_to(ROOT)}")

    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, ValueError) as exc:
        print(f"catalog validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("catalog validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
