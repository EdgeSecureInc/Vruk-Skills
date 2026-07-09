#!/usr/bin/env python3
"""Deterministic content hash for a skill directory.

The manifest's `content_hash` is `sha256:<hex>` over every regular file in the
skill directory, walked in sorted relative-path order, feeding for each file:

    <relative/posix/path>\0<raw file bytes>\0

Dotfiles, dot-directories, and the install sidecar `hivemind-version.json` are
skipped — so a deployed skill directory hashes identically to its catalog
directory. The same algorithm must be used by any consumer (installer, scanner,
mothership) that wants to answer "has this skill changed since it was installed?".

Usage: skillhash.py <skill-dir> [<skill-dir> ...]
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def skill_content_hash(skill_dir: Path) -> str:
    h = hashlib.sha256()
    files = sorted(
        p for p in skill_dir.rglob("*")
        if p.is_file() and p.name != "hivemind-version.json"
        and not any(part.startswith(".") for part in p.relative_to(skill_dir).parts)
    )
    for p in files:
        h.update(p.relative_to(skill_dir).as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        d = Path(arg)
        print(f"{skill_content_hash(d)}  {d}")
