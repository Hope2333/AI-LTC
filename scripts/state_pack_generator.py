#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a compact AI-LTC state pack for a target repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target repository root. Defaults to current directory.",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. Defaults to stdout.",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    init_status = parse_kv_markdown(root / ".ai/system/init-status.md")
    resolver = load_json(root / ".ai/system/ai-ltc-config.json")
    handoff_exists = (root / "00_HANDOFF.md").exists()
    escalation_exists = (root / "ESCALATION_REQUEST.md").exists()
    active_lane = root / ".ai/active-lane"

    lines = [
        "# AI-LTC State Pack",
        "",
        f"- Target Root: `{root}`",
        f"- Init Status: `{init_status.get('Status', 'missing')}`",
        f"- Init Decision: `{init_status.get('Decision', 'missing')}`",
        f"- Next Action: `{init_status.get('Next Action', 'missing')}`",
        f"- Framework Version: `{resolver.get('framework_version', 'missing')}`",
        f"- Source Mode: `{resolver.get('source_mode', 'missing')}`",
        f"- Working Language: `{resolver.get('working_language', 'missing')}`",
        f"- Human Summary Language: `{resolver.get('human_summary_language', 'missing')}`",
        f"- Human Input Policy: `{resolver.get('human_input_language_policy', 'missing')}`",
        f"- Default Operator Model: `{resolver.get('default_operator_model', 'missing')}`",
        f"- Skeleton Status: `{resolver.get('skeleton_status', 'missing')}`",
        f"- Active Lane Exists: `{'yes' if active_lane.exists() else 'no'}`",
        f"- 00_HANDOFF.md Exists: `{'yes' if handoff_exists else 'no'}`",
        f"- ESCALATION_REQUEST.md Exists: `{'yes' if escalation_exists else 'no'}`",
    ]

    output = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
