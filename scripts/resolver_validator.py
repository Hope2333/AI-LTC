#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


VALID_SOURCE_MODES = {"local_path", "git_repo", "cloud_reference"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI-LTC .ai/system/ai-ltc-config.json."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root. Defaults to current directory.",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    config_path = root / ".ai/system/ai-ltc-config.json"

    if not config_path.exists():
        print(f"ERROR: missing file: {config_path}", file=sys.stderr)
        return 1

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {config_path}: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    required_keys = [
        "schema_version",
        "framework_version",
        "source_mode",
        "source_priority",
        "project_state",
        "working_language",
        "human_summary_language",
        "human_input_language_policy",
        "default_operator_model",
    ]

    for key in required_keys:
        if key not in config:
            errors.append(f"missing key: {key}")

    source_mode = config.get("source_mode")
    if source_mode and source_mode not in VALID_SOURCE_MODES:
        errors.append(
            f"invalid source_mode: {source_mode!r}; expected one of {sorted(VALID_SOURCE_MODES)}"
        )

    source_priority = config.get("source_priority")
    if source_priority is not None:
        if not isinstance(source_priority, list) or not source_priority:
            errors.append("source_priority must be a non-empty list")
        else:
            for item in source_priority:
                if item not in VALID_SOURCE_MODES:
                    errors.append(f"invalid source_priority entry: {item!r}")

    if config.get("working_language") != "English":
        errors.append("working_language must be 'English'")

    if source_mode == "local_path":
        local_root = config.get("local_root", "")
        if not local_root:
            warnings.append(
                "source_mode is local_path but local_root is empty; acceptable only before init is fully configured"
            )

    if source_mode == "git_repo":
        if not config.get("repo_url"):
            errors.append("source_mode is git_repo but repo_url is empty")

    if source_mode == "cloud_reference":
        if not config.get("cloud_reference"):
            errors.append("source_mode is cloud_reference but cloud_reference is empty")

    if warnings:
        for item in warnings:
            print(f"WARNING: {item}", file=sys.stderr)

    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1

    print(f"OK: {config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
