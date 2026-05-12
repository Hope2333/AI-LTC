#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_FILES = [
    ".ai/state.json",
    ".ai/active-lane/ai-handoff.md",
    ".ai/active-lane/status.md",
    ".ai/active-lane/current-status.md",
    ".ai/active-lane/roadmap.md",
]

REQUIRED_HANDOFF_TERMS = [
    "Status:",
    "Decision:",
    "Stop Reason:",
    "Next Action:",
]

FORBIDDEN_ACTIVE_HANDOFF_FILES = [
    "00_HANDOFF.md",
    "docs/AI-LTC-HANDOFF-PROTOCOL.md",
    "docs/TASK-35-MANIFEST-EXECUTOR-PACKET.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI-LTC handoff bundle files in a target repository."
    )
    parser.add_argument("target_repo", help="Target repository root.")
    args = parser.parse_args()

    root = Path(args.target_repo).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            errors.append(f"missing required handoff file: {rel}")

    state_path = root / ".ai/state.json"
    lane_handoff = root / ".ai/active-lane/ai-handoff.md"
    status = root / ".ai/active-lane/status.md"

    for rel in FORBIDDEN_ACTIVE_HANDOFF_FILES:
        if (root / rel).exists():
            errors.append(
                f"{rel} is a legacy or docs-polluting handoff surface; "
                "active handoff must stay under .ai/"
            )

    docs_dir = root / "docs"
    if docs_dir.exists():
        for path in sorted(docs_dir.glob("*HANDOFF*.md")):
            warnings.append(
                f"{path.relative_to(root)} looks like an AI handoff document; "
                "prefer .ai/ unless it is durable project documentation"
            )
        for path in sorted(docs_dir.glob("TASK-*-EXECUTOR-PACKET.md")):
            errors.append(
                f"{path.relative_to(root)} is an executor packet in docs/; "
                "executor handoff packets must stay under .ai/"
            )

    if state_path.exists():
        try:
            state = json.loads(read(state_path))
        except json.JSONDecodeError as exc:
            errors.append(f".ai/state.json is not valid JSON: {exc}")
        else:
            for key in ("next_action", "context_summary"):
                if not state.get(key):
                    warnings.append(f".ai/state.json missing recommended key: {key}")

    if lane_handoff.exists():
        text = read(lane_handoff)
        for term in REQUIRED_HANDOFF_TERMS:
            if term not in text:
                errors.append(f".ai/active-lane/ai-handoff.md missing required term: {term}")
        if ".ai/state.json" not in text:
            errors.append(
                ".ai/active-lane/ai-handoff.md must point to canonical .ai/state.json"
            )

    if status.exists():
        text = read(status)
        if "| Task | Status |" in text or "|---:|---|" in text:
            errors.append(
                ".ai/active-lane/status.md appears to duplicate a task table; "
                "use a summary that points to .ai/state.json"
            )
        if ".ai/state.json" not in text:
            errors.append(
                ".ai/active-lane/status.md should point to canonical .ai/state.json"
            )

    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        for item in warnings:
            print(f"WARNING: {item}", file=sys.stderr)
        return 1

    for item in warnings:
        print(f"WARNING: {item}")
    print(f"OK: .ai-only AI-LTC handoff bundle present in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
