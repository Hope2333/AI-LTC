#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROVIDER_PATTERN = re.compile(
    r"INIT-QWEN|qwen-|gpt-|\bQwen\b|\bGPT\b|qwen36|Qwen3\.6"
)

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".json",
    ".md",
    ".prompt",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

EXCLUDED_DIRS = {
    ".git",
    ".omx",
    ".ai",
    "__pycache__",
    "node_modules",
}

ALLOWED_PREFIXES = (
    "adapters/",
    "evaluation/",
    "prompts/_mapping/",
    "prompts/adapters/",
)

ALLOWED_FILES = {
    "cross-repo-registry.json",
    "docs/PROMPT-MIGRATION.md",
    "docs/PROMPT-DECOUPLING-PLAN.md",
    "scripts/provider_naming_validator.py",
}


def is_allowed(relative: str) -> bool:
    if relative in ALLOWED_FILES:
        return True
    return any(relative.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def should_scan(path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False
    if path.name.startswith("."):
        return False
    if path.suffix in TEXT_SUFFIXES:
        return True
    return path.name in {"Makefile", "VERSION", "LICENSE"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate provider-named prompt/model terms do not leak into stable "
            "or copyable repository surfaces."
        )
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
    scanned = 0

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if is_allowed(relative) or not should_scan(path.relative_to(root)):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        scanned += 1
        for line_number, line in enumerate(text.splitlines(), start=1):
            if PROVIDER_PATTERN.search(line):
                errors.append(f"{relative}:{line_number}: {line.strip()}")

    if errors:
        print(
            "ERROR: provider-specific naming leaked outside allowed compatibility/evidence surfaces:",
            file=sys.stderr,
        )
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: provider naming boundaries validated ({scanned} files scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
