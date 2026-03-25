#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


VALID_STATUSES = {"NULL", "INITING", "VERSION"}


def parse_kv_markdown(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key:
            data[key] = value
    return data


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def classify_mode(status: str, config_exists: bool, current_version: str, target_version: str) -> str:
    if status in {"", "NULL"}:
        return "Fresh Init"
    if status == "INITING":
        return "Resume Init"
    if status == "VERSION":
        if not current_version or not target_version:
            return "Normal Execution"
        current_major = current_version.split(".", 1)[0]
        target_major = target_version.split(".", 1)[0]
        if current_major != target_major:
            return "Upgrade"
        if current_version == target_version:
            return "Normal Execution"
        return "Update"
    return "Unknown"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI-LTC upgrade classification for a target repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root. Defaults to current directory.",
    )
    parser.add_argument(
        "--target-version",
        default="",
        help="Optional target AI-LTC version to compare against.",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    init_path = root / ".ai/system/init-status.md"
    config_path = root / ".ai/system/ai-ltc-config.json"

    init_data = parse_kv_markdown(init_path)
    cfg = load_json(config_path)

    errors: list[str] = []
    warnings: list[str] = []

    status = init_data.get("Status", "")
    if status and status not in VALID_STATUSES:
        errors.append(
            f"invalid Status value: {status!r}; expected one of {sorted(VALID_STATUSES)}"
        )

    current_version = str(cfg.get("framework_version", "")).strip()
    target_version = args.target_version.strip()
    config_exists = config_path.exists()

    if status == "VERSION" and not config_exists:
        errors.append("Status is VERSION but resolver config is missing")

    if config_exists:
        if cfg.get("working_language") != "English":
            errors.append("working_language must be 'English'")
        if "human_summary_language" not in cfg:
            errors.append("resolver config missing human_summary_language")
        if "human_input_language_policy" not in cfg:
            errors.append("resolver config missing human_input_language_policy")

    mode = classify_mode(status, config_exists, current_version, target_version)
    if mode == "Unknown":
        errors.append("could not classify repository into a valid init/update/upgrade mode")

    if status == "NULL" and config_exists:
        warnings.append(
            "Status is NULL but resolver config exists; verify whether the repository should actually be INITING or VERSION"
        )

    if status == "VERSION" and not current_version:
        warnings.append(
            "Status is VERSION but framework_version is empty; upgrade classification will be weaker"
        )

    if warnings:
        for item in warnings:
            print(f"WARNING: {item}", file=sys.stderr)

    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1

    print(f"OK: {root}")
    print(f"Mode: {mode}")
    if current_version:
        print(f"Current Version: {current_version}")
    if target_version:
        print(f"Target Version: {target_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
