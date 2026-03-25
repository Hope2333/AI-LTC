#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PREFIXES = [
    "- Target Root:",
    "- Init Status:",
    "- Init Decision:",
    "- Next Action:",
    "- Framework Version:",
    "- Source Mode:",
    "- Working Language:",
    "- Human Summary Language:",
    "- Human Input Policy:",
    "- Default Operator Model:",
    "- Skeleton Status:",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a generated AI-LTC state-pack markdown file."
    )
    parser.add_argument("state_pack", help="Path to the state-pack markdown file.")
    args = parser.parse_args()

    path = Path(args.state_pack).resolve()
    if not path.exists():
        print(f"ERROR: missing file: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if not text.startswith("# AI-LTC State Pack"):
        errors.append("missing state-pack heading")

    for prefix in REQUIRED_PREFIXES:
        if prefix not in text:
            errors.append(f"missing required line with prefix: {prefix}")

    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1

    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
