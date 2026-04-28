#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_MAPPING = Path("prompts/_mapping/legacy-to-role-phase-adapter.md")
PATH_PATTERN = re.compile(r"`(prompts/[^`]+)`")
LEGACY_HEADING_PATTERN = re.compile(
    r"^###\s+([a-z0-9][a-z0-9_.-]+\.prompt\.md)\s*$",
    re.MULTILINE,
)
STATUS_PATTERN = re.compile(r"^Migration status:\s+([a-z_ -]+)\s*$", re.MULTILINE)
VALID_STATUSES = {"pending", "reference", "in_progress", "complete", "deprecated"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate prompt migration mapping references."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    parser.add_argument(
        "--mapping",
        default=str(DEFAULT_MAPPING),
        help=f"Mapping markdown path. Defaults to {DEFAULT_MAPPING}.",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    mapping = root / args.mapping
    errors: list[str] = []

    if not mapping.exists():
        print(f"ERROR: missing mapping file: {mapping}", file=sys.stderr)
        return 1

    text = mapping.read_text(encoding="utf-8")
    referenced_paths = sorted(set(PATH_PATTERN.findall(text)))
    if not referenced_paths:
        errors.append(f"{mapping.relative_to(root)}: no prompts/ paths found")

    for relative in referenced_paths:
        if not (root / relative).exists():
            errors.append(f"{mapping.relative_to(root)}: missing referenced path {relative}")

    legacy_headings = LEGACY_HEADING_PATTERN.findall(text)
    if not legacy_headings:
        errors.append(f"{mapping.relative_to(root)}: no legacy prompt headings found")

    for legacy_name in legacy_headings:
        legacy_path = root / "prompts" / legacy_name
        if not legacy_path.exists():
            errors.append(
                f"{mapping.relative_to(root)}:{legacy_name}: missing legacy prompt {legacy_path.relative_to(root)}"
            )

    statuses = STATUS_PATTERN.findall(text)
    if len(statuses) < len(legacy_headings):
        errors.append(
            f"{mapping.relative_to(root)}: expected at least one migration status per legacy heading"
        )
    for status in statuses:
        normalized = status.strip().replace(" ", "_")
        if normalized not in VALID_STATUSES:
            errors.append(
                f"{mapping.relative_to(root)}: invalid migration status {status!r}; expected one of {sorted(VALID_STATUSES)}"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "OK: prompt mapping validated "
        f"({len(legacy_headings)} legacy prompts, {len(referenced_paths)} referenced prompt paths)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
