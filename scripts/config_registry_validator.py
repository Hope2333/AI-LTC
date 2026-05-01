#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VALID_SOURCE_MODES = {"folder", "git_repo", "cloud_reference", "local_path"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected top-level object")
    return data


def require_string(data: dict[str, Any], key: str, label: str, errors: list[str]) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: missing or empty string key {key!r}")
        return ""
    return value.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI-LTC registry and config template version alignment."
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

    version_path = root / "VERSION"
    registry_path = root / "cross-repo-registry.json"
    template_path = root / "ai-ltc-config.template.json"

    if not version_path.exists():
        errors.append("VERSION: missing")
        version = ""
    else:
        version = version_path.read_text(encoding="utf-8").strip()
        if not version:
            errors.append("VERSION: empty")

    try:
        registry = load_json(registry_path)
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        registry = {}

    try:
        template = load_json(template_path)
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        template = {}

    if version:
        registry_version = registry.get("framework_version")
        if registry_version != version:
            errors.append(
                f"cross-repo-registry.json: framework_version={registry_version!r}, expected {version!r}"
            )

        template_version = template.get("framework_version")
        if template_version != version:
            errors.append(
                f"ai-ltc-config.template.json: framework_version={template_version!r}, expected {version!r}"
            )

    branches = registry.get("branches")
    if not isinstance(branches, dict) or not branches:
        errors.append("cross-repo-registry.json: branches must be a non-empty object")
    else:
        for name, info in branches.items():
            if not isinstance(info, dict):
                errors.append(f"cross-repo-registry.json: branch {name!r} must be an object")
                continue
            branch_version = info.get("version")
            if version and branch_version != version:
                errors.append(
                    f"cross-repo-registry.json: branch {name!r} version={branch_version!r}, expected {version!r}"
                )
            require_string(info, "description", f"cross-repo-registry.json branch {name!r}", errors)

    consumers = registry.get("consumer_repos")
    if not isinstance(consumers, dict):
        errors.append("cross-repo-registry.json: consumer_repos must be an object")
    else:
        for name, info in consumers.items():
            if not isinstance(info, dict):
                errors.append(f"cross-repo-registry.json: consumer {name!r} must be an object")
                continue
            for key in ("path", "config", "branch", "expected_version"):
                require_string(info, key, f"cross-repo-registry.json consumer {name!r}", errors)
            if version and info.get("expected_version") != version:
                errors.append(
                    f"cross-repo-registry.json: consumer {name!r} expected_version={info.get('expected_version')!r}, expected {version!r}"
                )

    source_mode = template.get("source_mode")
    if source_mode not in VALID_SOURCE_MODES:
        errors.append(
            f"ai-ltc-config.template.json: source_mode={source_mode!r}, expected one of {sorted(VALID_SOURCE_MODES)}"
        )

    source_priority = template.get("source_priority")
    if not isinstance(source_priority, list) or not source_priority:
        errors.append("ai-ltc-config.template.json: source_priority must be a non-empty list")
    else:
        for item in source_priority:
            if item not in VALID_SOURCE_MODES:
                errors.append(
                    f"ai-ltc-config.template.json: invalid source_priority entry {item!r}"
                )

    for key in (
        "schema_version",
        "repo_url",
        "repo_ref",
        "working_language",
        "human_summary_language",
        "human_input_language_policy",
        "default_operator_model",
        "default_operator_prompt",
        "supervisory_prompt",
        "architect_prompt",
        "auditor_prompt",
    ):
        require_string(template, key, "ai-ltc-config.template.json", errors)

    if template.get("working_language") != "English":
        errors.append("ai-ltc-config.template.json: working_language must be 'English'")

    for section in ("experimental_mode", "multi_session", "observability", "security"):
        if not isinstance(template.get(section), dict):
            errors.append(f"ai-ltc-config.template.json: {section} must be an object")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "OK: config and registry alignment validated "
        f"(version {version}, {len(consumers or {})} consumer repos)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
