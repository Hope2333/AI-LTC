#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


IMPORT_PATTERN = re.compile(r"\bfrom\s+['\"](?P<target>\.{1,2}/[^'\"]+)['\"]")
DEFAULT_SCAN_ROOTS = ("bridge", "adapters")


def resolve_import(source: Path, target: str) -> Path | None:
    base = (source.parent / target).resolve()
    candidates = [
        base,
        base.with_suffix(".ts"),
        base / "index.ts",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate local TypeScript relative imports in bridge and adapters."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    errors: list[str] = []
    files_checked = 0
    imports_checked = 0

    for scan_root in DEFAULT_SCAN_ROOTS:
        root_path = root / scan_root
        if not root_path.exists():
            errors.append(f"{scan_root}: scan root missing")
            continue

        for source in sorted(root_path.rglob("*.ts")):
            files_checked += 1
            text = source.read_text(encoding="utf-8")
            for match in IMPORT_PATTERN.finditer(text):
                imports_checked += 1
                target = match.group("target")
                resolved = resolve_import(source, target)
                if resolved is None:
                    relative_source = source.relative_to(root).as_posix()
                    errors.append(f"{relative_source}: unresolved import {target!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "OK: TypeScript local imports validated "
        f"({files_checked} files, {imports_checked} imports)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
