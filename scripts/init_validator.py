#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


VALID_STATUSES = {"UNINITIALIZED", "INITING", "INSTALLED"}
REQUIRED_KEYS = ("Status", "Decision", "Stop Reason", "Next Action")


def parse_status_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key:
            data[key] = value
    return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI-LTC .ai/system/init-status.md."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root. Defaults to current directory.",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    status_path = root / ".ai/system/init-status.md"
    config_path = root / ".ai/system/ai-ltc-config.json"

    errors: list[str] = []
    warnings: list[str] = []

    if not status_path.exists():
        errors.append(f"missing file: {status_path}")
    else:
        data = parse_status_file(status_path)
        for key in REQUIRED_KEYS:
            if key not in data:
                errors.append(f"missing field in init-status.md: {key}")

        status = data.get("Status", "")
        if status and status not in VALID_STATUSES:
            errors.append(
                f"invalid Status value: {status!r}; expected one of {sorted(VALID_STATUSES)}"
            )

        if status == "INSTALLED" and not config_path.exists():
            errors.append(
                "Status is INSTALLED but .ai/system/ai-ltc-config.json is missing"
            )

        if status == "UNINITIALIZED" and config_path.exists():
            warnings.append(
                "Status is UNINITIALIZED but resolver config exists; verify whether init should already be INSTALLED"
            )

    if warnings:
        for item in warnings:
            print(f"WARNING: {item}", file=sys.stderr)

    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1

    print(f"OK: {status_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
