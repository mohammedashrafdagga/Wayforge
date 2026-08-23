#!/usr/bin/env python3
"""merge_master_doc.py — additive-only merge of a feature-local doc into a master doc.

RealSoft Workflow's master docs (workflow/data-model.md, workflow/api-registry.md,
workflow/user-stories.md) are additive-only: a feature may append new content, never
rewrite or delete an existing entry. This script performs the mechanical append.

It does NOT decide whether a same-named collision is a real semantic conflict (e.g.
same entity name with different fields) — that judgment belongs to validate_docs.py,
which must be run first and must pass before this script is invoked. This script's
own collision handling is intentionally conservative: in "entity" mode any heading
collision is treated as a hard stop, and in "group" mode a heading collision only
ever appends new content beneath the existing heading, never touching existing
lines.

Sections are delimited by level-2 (##) markdown headings. A ```mermaid fenced block
is always treated as one atomic unit: never split, never line-diffed internally.

Usage:
    merge_master_doc.py --mode entity --source features/<slug>/data-model.md \
        --master data-model.md

    merge_master_doc.py --mode group --source features/<slug>/api-registry.md \
        --master api-registry.md

Modes:
    entity  — headings must be globally unique (data-model.md). A heading that
              already exists in the master doc is a hard conflict: the script
              exits non-zero and changes nothing. Use this for entity-per-section
              docs.
    group   — headings represent a recurring group (a feature slug) that multiple
              runs may add to (api-registry.md, user-stories.md). An existing
              heading is fine; new content is appended beneath it, skipping any
              block (line, or whole mermaid fence) that is already present
              verbatim anywhere in that section, so re-running is idempotent.

Exit codes:
    0  merge applied (or nothing new to merge)
    1  usage error
    2  entity-mode heading collision — user must resolve manually
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^```")


@dataclass
class Section:
    heading: str
    body_lines: list[str] = field(default_factory=list)

    def body_text(self) -> str:
        return "\n".join(self.body_lines).strip("\n")


def parse_sections(text: str) -> tuple[str, list[Section]]:
    """Split a doc into (preamble_before_first_##, [Section...])."""
    lines = text.splitlines()
    preamble: list[str] = []
    sections: list[Section] = []
    current: Section | None = None
    in_fence = False

    for line in lines:
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence

        m = HEADING_RE.match(line) if not in_fence else None
        if m:
            if current is not None:
                sections.append(current)
            current = Section(heading=m.group(1))
            continue

        if current is None:
            preamble.append(line)
        else:
            current.body_lines.append(line)

    if current is not None:
        sections.append(current)

    return "\n".join(preamble).rstrip("\n"), sections


def atomic_blocks(body_lines: list[str]) -> list[str]:
    """Split a section body into atomic units: a mermaid fence is one unit,
    every other non-blank line is its own unit."""
    blocks: list[str] = []
    buf: list[str] = []
    in_fence = False

    for line in body_lines:
        if FENCE_RE.match(line.strip()):
            if in_fence:
                buf.append(line)
                blocks.append("\n".join(buf))
                buf = []
                in_fence = False
            else:
                in_fence = True
                buf = [line]
            continue

        if in_fence:
            buf.append(line)
            continue

        if line.strip() == "":
            continue
        blocks.append(line)

    if buf:
        blocks.append("\n".join(buf))

    return blocks


def merge_entity_mode(master_pre: str, master_sections: list[Section], source_sections: list[Section]) -> tuple[str, list[str], list[str]]:
    existing = {s.heading: s for s in master_sections}
    conflicts = []
    to_add = []

    for s in source_sections:
        if s.heading not in existing:
            to_add.append(s)
            continue
        if existing[s.heading].body_text() == s.body_text():
            continue  # identical re-merge (e.g. review ran twice) — not a conflict, nothing to do
        conflicts.append(s.heading)

    if conflicts:
        return "", [], conflicts

    added = [s.heading for s in to_add]
    out_sections = list(master_sections) + to_add
    return render(master_pre, out_sections), added, []


def merge_group_mode(master_pre: str, master_sections: list[Section], source_sections: list[Section]) -> tuple[str, list[str], list[str]]:
    by_heading = {s.heading: s for s in master_sections}
    out_sections = list(master_sections)
    added: list[str] = []

    for src in source_sections:
        if src.heading not in by_heading:
            out_sections.append(src)
            by_heading[src.heading] = src
            added.append(f"{src.heading} (new section)")
            continue

        target = by_heading[src.heading]
        existing_blocks = set(atomic_blocks(target.body_lines))
        new_blocks = [b for b in atomic_blocks(src.body_lines) if b not in existing_blocks]

        if not new_blocks:
            continue

        if target.body_lines and target.body_lines[-1].strip() != "":
            target.body_lines.append("")
        for b in new_blocks:
            target.body_lines.extend(b.split("\n"))
            target.body_lines.append("")
        added.append(f"{src.heading} (+{len(new_blocks)} entries)")

    return render(master_pre, out_sections), added, []


def render(preamble: str, sections: list[Section]) -> str:
    parts = [preamble.rstrip("\n")]
    for s in sections:
        parts.append(f"## {s.heading}")
        body = s.body_text()
        if body:
            parts.append(body)
        parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["entity", "group"], required=True)
    ap.add_argument("--source", required=True, type=Path, help="feature-local doc to merge from")
    ap.add_argument("--master", required=True, type=Path, help="master doc to merge into (edited in place)")
    ap.add_argument("--dry-run", action="store_true", help="report what would change without writing")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"source doc not found: {args.source}", file=sys.stderr)
        return 1
    if not args.master.exists():
        print(f"master doc not found: {args.master}", file=sys.stderr)
        return 1

    master_pre, master_sections = parse_sections(args.master.read_text())
    _, source_sections = parse_sections(args.source.read_text())

    if not source_sections:
        print(f"no ## sections found in {args.source} — nothing to merge")
        return 0

    if args.mode == "entity":
        new_text, added, conflicts = merge_entity_mode(master_pre, master_sections, source_sections)
    else:
        new_text, added, conflicts = merge_group_mode(master_pre, master_sections, source_sections)

    if conflicts:
        print(f"CONFLICT: the following headings already exist in {args.master} and --mode entity "
              f"forbids rewriting them: {', '.join(conflicts)}", file=sys.stderr)
        print("Resolve manually: either this is genuinely a new entity (rename it) or it's an "
              "intentional edit to an existing one, which requires the user to edit the master "
              "doc directly — this script will not guess.", file=sys.stderr)
        return 2

    if not added:
        print(f"{args.master} already contains everything in {args.source} — nothing to merge")
        return 0

    print(f"merging into {args.master}: {', '.join(added)}")
    if args.dry_run:
        print("--dry-run set, not writing")
        return 0

    args.master.write_text(new_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
