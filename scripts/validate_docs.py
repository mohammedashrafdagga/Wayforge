#!/usr/bin/env python3
"""validate_docs.py — pre-merge conflict guard for Wayforge master docs.

Runs before scripts/merge_master_doc.py in /wayforge-review. Flags things a mechanical
append can't safely judge on its own: the same entity name showing up with
different fields, two Mermaid blocks that define the same entity differently, or
two features registering the same HTTP method+path. Any hit here is a hard stop —
the user resolves it by hand (rename an entity, adjust a path, or confirm it's an
intentional edit to an existing master entry). This script never auto-resolves.

Usage:
    validate_docs.py --kind data-model --source features/<slug>/data-model.md --master data-model.md
    validate_docs.py --kind api-registry --source features/<slug>/api-registry.md --master api-registry.md
    validate_docs.py --kind user-stories --source features/<slug>/user-stories.md --master user-stories.md

Exit codes:
    0  no conflicts found, safe to merge
    1  usage error
    2  conflicts found — do not merge until the user resolves them
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
TABLE_ROW_RE = re.compile(r"^\|\s*(GET|POST|PUT|PATCH|DELETE)\s*\|\s*([^|]+?)\s*\|")
FENCE_RE = re.compile(r"^```")


def parse_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = None
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
        m = HEADING_RE.match(line) if not in_fence else None
        if m:
            current = m.group(1)
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def extract_table(body: str) -> dict[str, str]:
    """Very small markdown table -> {'<name>': 'raw field/type text'} extractor,
    for the entity-attribute table under a data-model.md ## heading."""
    fields = {}
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in ("field", "---", ""):
            continue
        if set(cells[0]) <= {"-"}:
            continue
        fields[cells[0]] = " | ".join(cells[1:])
    return fields


def extract_mermaid(body: str) -> list[str]:
    blocks = []
    buf: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line.strip()):
            if in_fence:
                buf.append(line)
                blocks.append("\n".join(buf))
                buf = []
                in_fence = False
            elif line.strip().startswith("```mermaid"):
                in_fence = True
                buf = [line]
            continue
        if in_fence:
            buf.append(line)
    return blocks


def validate_data_model(source_text: str, master_text: str) -> list[str]:
    problems = []
    source_sections = parse_sections(source_text)
    master_sections = parse_sections(master_text)

    for name, src_body_lines in source_sections.items():
        src_body = "\n".join(src_body_lines)
        if name not in master_sections:
            continue  # new entity, nothing to check against

        master_body = "\n".join(master_sections[name])
        src_fields = extract_table(src_body)
        master_fields = extract_table(master_body)

        if src_fields and master_fields and src_fields != master_fields:
            diff_keys = sorted(set(src_fields) ^ set(master_fields)) or sorted(
                k for k in src_fields if src_fields[k] != master_fields.get(k)
            )
            problems.append(
                f"data-model: entity '{name}' already exists in the master doc with different "
                f"fields ({', '.join(diff_keys) or 'field text differs'}). Confirm whether this "
                f"is a new entity that needs a distinct name, or an intentional edit to the "
                f"existing '{name}' that requires a manual master-doc change."
            )

        src_mermaid = extract_mermaid(src_body)
        master_mermaid = extract_mermaid(master_body)
        if src_mermaid and master_mermaid and src_mermaid != master_mermaid:
            problems.append(
                f"data-model: entity '{name}' has a Mermaid diagram that differs from the one "
                f"already in the master doc. Diagram blocks are atomic — resolve by hand, do not "
                f"let this merge silently pick one."
            )

    # near-duplicate heading names (case/plural drift) across source vs master
    for name in source_sections:
        for existing in master_sections:
            if existing == name:
                continue
            if existing.lower() == name.lower() or existing.lower().rstrip("s") == name.lower().rstrip("s"):
                problems.append(
                    f"data-model: '{name}' (new) looks like it may be the same concept as "
                    f"existing entity '{existing}' — confirm these are genuinely distinct before "
                    f"merging, otherwise the master doc will end up with two names for one thing."
                )

    return problems


def validate_api_registry(source_text: str, master_text: str) -> list[str]:
    problems = []
    source_sections = parse_sections(source_text)
    master_sections = parse_sections(master_text)

    master_routes: dict[tuple[str, str], str] = {}
    for feature, lines in master_sections.items():
        for line in lines:
            m = TABLE_ROW_RE.match(line.strip())
            if m:
                master_routes[(m.group(1), m.group(2))] = feature

    for feature, lines in source_sections.items():
        for line in lines:
            m = TABLE_ROW_RE.match(line.strip())
            if not m:
                continue
            key = (m.group(1), m.group(2))
            if key in master_routes and master_routes[key] != feature:
                problems.append(
                    f"api-registry: {key[0]} {key[1]} is already registered under feature "
                    f"'{master_routes[key]}' in the master doc; '{feature}' registers it again. "
                    f"Two features must not silently claim the same route."
                )

    return problems


def validate_user_stories(source_text: str, master_text: str) -> list[str]:
    # Lightweight: flag an exact-duplicate story line under a different feature heading,
    # which usually means the story was miscategorized rather than genuinely new.
    problems = []
    source_sections = parse_sections(source_text)
    master_sections = parse_sections(master_text)

    master_story_lines: dict[str, str] = {}
    for feature, lines in master_sections.items():
        for line in lines:
            s = line.strip()
            if s.startswith("- As a"):
                master_story_lines[s] = feature

    for feature, lines in source_sections.items():
        for line in lines:
            s = line.strip()
            if s.startswith("- As a") and s in master_story_lines and master_story_lines[s] != feature:
                problems.append(
                    f"user-stories: an identical story already exists under feature "
                    f"'{master_story_lines[s]}': \"{s}\". Confirm '{feature}' isn't duplicating it."
                )

    return problems


VALIDATORS = {
    "data-model": validate_data_model,
    "api-registry": validate_api_registry,
    "user-stories": validate_user_stories,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind", choices=list(VALIDATORS), required=True)
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--master", required=True, type=Path)
    args = ap.parse_args()

    if not args.source.exists():
        print(f"source doc not found: {args.source}", file=sys.stderr)
        return 1
    if not args.master.exists():
        print(f"master doc not found: {args.master}", file=sys.stderr)
        return 1

    problems = VALIDATORS[args.kind](args.source.read_text(), args.master.read_text())

    if not problems:
        print(f"OK: no conflicts between {args.source} and {args.master}")
        return 0

    print(f"CONFLICTS found between {args.source} and {args.master} — resolve before merging:", file=sys.stderr)
    for p in problems:
        print(f"  - {p}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
