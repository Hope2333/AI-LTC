#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency is environment-provided
    print(f"ERROR: PyYAML is required to validate evaluation YAML: {exc}", file=sys.stderr)
    raise SystemExit(1)


RECORD_FAMILIES = {
    "models": {
        "registry": Path("evaluation/models/registry.yaml"),
        "schema": Path("evaluation/schemas/model.schema.yaml"),
    },
    "tools": {
        "registry": Path("evaluation/tools/registry.yaml"),
        "schema": Path("evaluation/schemas/tool.schema.yaml"),
    },
    "tasks": {
        "registry": Path("evaluation/tasks/registry.yaml"),
        "schema": Path("evaluation/schemas/task.schema.yaml"),
    },
}

RESULTS_GLOB = "evaluation/results/*.yaml"
RESULT_SCHEMA = Path("evaluation/schemas/result.schema.yaml")
VALID_RESULT_SUBJECTS = {"model", "tool", "task", "adapter", "prompt_profile"}
VALID_MODEL_TYPES = {
    "hosted",
    "open_weights",
    "local_runtime",
    "operator_surface",
    "role_family",
    "unknown",
}
VALID_TOOL_SURFACES = {
    "cli",
    "terminal",
    "web",
    "browser",
    "ide",
    "desktop",
    "api",
    "local_runtime",
    "repository",
}
MODEL_DEPLOYMENT_FIT_KEYS = {
    "local_cpu",
    "local_gpu",
    "hosted_api",
    "mobile_npu",
    "always_on_agent",
}
MODEL_SCORE_KEYS = {
    "reasoning",
    "coding",
    "latency",
    "cost_efficiency",
    "context_reliability",
}
TOOL_ACCESS_MODEL_KEYS = {"subscription", "rate_limit", "credits", "offline_capable"}
TOOL_PERMISSION_MODEL_KEYS = {
    "sandbox",
    "approval_required",
    "filesystem_scope",
    "network_scope",
}
TOOL_SCORE_KEYS = {
    "code_editing",
    "planning",
    "reproducibility",
    "integration",
    "cost_stability",
}
RESULT_SCORE_KEYS = {"success", "stability", "cost", "reproducibility"}
VALID_FRESHNESS_STATUS = {"fresh", "referenceable", "stale"}
FRESH_DAYS = 30
REFERENCEABLE_DAYS = 90


def parse_iso_date(value: Any, label: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{label}: expected YYYY-MM-DD string, got {type(value).__name__}")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{label}: invalid date {value!r}; expected YYYY-MM-DD") from exc


def freshness_bucket(tested_at: date, as_of: date) -> str:
    age_days = (as_of - tested_at).days
    if age_days < 0:
        return "future"
    if age_days <= FRESH_DAYS:
        return "fresh"
    if age_days <= REFERENCEABLE_DAYS:
        return "referenceable"
    return "stale"


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc


def required_fields(root: Path, schema_path: Path) -> list[str]:
    data = load_yaml(root / schema_path)
    fields = data.get("required_fields")
    if not isinstance(fields, list) or not all(isinstance(item, str) for item in fields):
        raise ValueError(f"{schema_path}: required_fields must be a list of strings")
    return fields


def registry_records(root: Path, registry_path: Path, family: str) -> list[dict[str, Any]]:
    data = load_yaml(root / registry_path)
    records = data.get(family)
    if not isinstance(records, list):
        raise ValueError(f"{registry_path}: expected top-level list key {family!r}")
    for index, item in enumerate(records):
        if not isinstance(item, dict):
            raise ValueError(f"{registry_path}: record {index} is not an object")
    return records


def validate_required(
    errors: list[str],
    registry_path: Path,
    records: list[dict[str, Any]],
    fields: list[str],
) -> None:
    seen: set[str] = set()
    for item in records:
        record_id = item.get("id", "<missing id>")
        if "id" in item:
            if item["id"] in seen:
                errors.append(f"{registry_path}:{record_id}: duplicate id")
            seen.add(item["id"])
        for field in fields:
            if field not in item:
                errors.append(f"{registry_path}:{record_id}: missing required field {field}")


def validate_tested_at(
    errors: list[str],
    registry_path: Path,
    records: list[dict[str, Any]],
    as_of: date,
    freshness_counts: dict[str, int],
) -> None:
    for item in records:
        record_id = item.get("id", "<missing id>")
        if "tested_at" not in item:
            continue
        try:
            tested_at = parse_iso_date(item["tested_at"], f"{registry_path}:{record_id}:tested_at")
        except ValueError as exc:
            errors.append(str(exc))
            continue

        bucket = freshness_bucket(tested_at, as_of)
        if bucket == "future":
            errors.append(
                f"{registry_path}:{record_id}: tested_at {item['tested_at']!r} is after validation date {as_of.isoformat()}"
            )
        else:
            if item.get("freshness_status") is not None and item["freshness_status"] != bucket:
                errors.append(
                    f"{registry_path}:{record_id}: freshness_status {item['freshness_status']!r} "
                    f"does not match tested_at-derived bucket {bucket!r}"
                )
            freshness_counts[bucket] = freshness_counts.get(bucket, 0) + 1


def is_number_or_null(value: Any) -> bool:
    return value is None or (isinstance(value, (int, float)) and not isinstance(value, bool))


def is_bool_or_null(value: Any) -> bool:
    return value is None or isinstance(value, bool)


def is_string_or_null(value: Any) -> bool:
    return value is None or isinstance(value, str)


def validate_list_of_strings(
    errors: list[str],
    registry_path: Path,
    record_id: Any,
    item: dict[str, Any],
    field: str,
) -> None:
    if field not in item:
        return
    value = item[field]
    if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
        errors.append(f"{registry_path}:{record_id}: {field} must be a list of strings")


def validate_number_map(
    errors: list[str],
    registry_path: Path,
    record_id: Any,
    item: dict[str, Any],
    field: str,
    allowed_keys: set[str],
) -> None:
    if field not in item:
        return
    value = item[field]
    if not isinstance(value, dict):
        errors.append(f"{registry_path}:{record_id}: {field} must be an object")
        return
    for key, nested_value in value.items():
        if key not in allowed_keys:
            errors.append(f"{registry_path}:{record_id}: {field}.{key} is not in schema")
        elif not is_number_or_null(nested_value):
            errors.append(f"{registry_path}:{record_id}: {field}.{key} must be a number or null")


def validate_freshness_status(
    errors: list[str],
    registry_path: Path,
    record_id: Any,
    item: dict[str, Any],
) -> None:
    if "freshness_status" not in item:
        return
    value = item["freshness_status"]
    if value not in VALID_FRESHNESS_STATUS:
        errors.append(
            f"{registry_path}:{record_id}: invalid freshness_status {value!r}"
        )


def validate_model_shapes(
    errors: list[str],
    registry_path: Path,
    records: list[dict[str, Any]],
) -> None:
    list_fields = [
        "architecture",
        "capabilities",
        "strengths",
        "weaknesses",
    ]
    for item in records:
        record_id = item.get("id", "<missing id>")
        if item.get("model_type") not in VALID_MODEL_TYPES:
            errors.append(
                f"{registry_path}:{record_id}: invalid model_type {item.get('model_type')!r}"
            )
        for field in list_fields:
            validate_list_of_strings(errors, registry_path, record_id, item, field)
        validate_freshness_status(errors, registry_path, record_id, item)

        deployment_fit = item.get("deployment_fit")
        if deployment_fit is not None:
            if not isinstance(deployment_fit, dict):
                errors.append(f"{registry_path}:{record_id}: deployment_fit must be an object")
            else:
                for key, value in deployment_fit.items():
                    if key not in MODEL_DEPLOYMENT_FIT_KEYS:
                        errors.append(f"{registry_path}:{record_id}: deployment_fit.{key} is not in schema")
                    elif not is_bool_or_null(value):
                        errors.append(f"{registry_path}:{record_id}: deployment_fit.{key} must be boolean or null")

        validate_number_map(errors, registry_path, record_id, item, "scores", MODEL_SCORE_KEYS)


def validate_tool_shapes(
    errors: list[str],
    registry_path: Path,
    records: list[dict[str, Any]],
) -> None:
    list_fields = [
        "surfaces",
        "workspace_capabilities",
        "harness_features",
        "capabilities",
        "strengths",
        "weaknesses",
        "known_failure_modes",
    ]
    for item in records:
        record_id = item.get("id", "<missing id>")
        for field in list_fields:
            validate_list_of_strings(errors, registry_path, record_id, item, field)
        validate_freshness_status(errors, registry_path, record_id, item)

        for surface in item.get("surfaces", []):
            if surface not in VALID_TOOL_SURFACES:
                errors.append(f"{registry_path}:{record_id}: invalid surface {surface!r}")

        access_model = item.get("access_model")
        if access_model is not None:
            if not isinstance(access_model, dict):
                errors.append(f"{registry_path}:{record_id}: access_model must be an object")
            else:
                for key, value in access_model.items():
                    if key not in TOOL_ACCESS_MODEL_KEYS:
                        errors.append(f"{registry_path}:{record_id}: access_model.{key} is not in schema")
                    elif key in {"subscription", "offline_capable"} and not is_bool_or_null(value):
                        errors.append(f"{registry_path}:{record_id}: access_model.{key} must be boolean or null")
                    elif key in {"rate_limit", "credits"} and not is_string_or_null(value):
                        errors.append(f"{registry_path}:{record_id}: access_model.{key} must be string or null")

        permission_model = item.get("permission_model")
        if permission_model is not None:
            if not isinstance(permission_model, dict):
                errors.append(f"{registry_path}:{record_id}: permission_model must be an object")
            else:
                for key, value in permission_model.items():
                    if key not in TOOL_PERMISSION_MODEL_KEYS:
                        errors.append(f"{registry_path}:{record_id}: permission_model.{key} is not in schema")
                    elif not is_string_or_null(value):
                        errors.append(f"{registry_path}:{record_id}: permission_model.{key} must be string or null")

        validate_number_map(errors, registry_path, record_id, item, "scores", TOOL_SCORE_KEYS)


def validate_task_shapes(
    errors: list[str],
    registry_path: Path,
    records: list[dict[str, Any]],
) -> None:
    for item in records:
        record_id = item.get("id", "<missing id>")
        for field in (
            "success_criteria",
            "preferred_roles",
            "preferred_signals",
            "evidence_expectations",
        ):
            validate_list_of_strings(errors, registry_path, record_id, item, field)


def validate_result_shapes(
    errors: list[str],
    result_path: Path,
    results: list[dict[str, Any]],
) -> None:
    for item in results:
        result_id = item.get("id", "<missing id>")
        for field in ("observations", "failure_modes_observed"):
            validate_list_of_strings(errors, result_path, result_id, item, field)
        validate_freshness_status(errors, result_path, result_id, item)

        evidence = item.get("evidence")
        if evidence is not None and not isinstance(evidence, dict):
            errors.append(f"{result_path}:{result_id}: evidence must be an object")

        validate_number_map(errors, result_path, result_id, item, "scores", RESULT_SCORE_KEYS)


def validate_result_links(
    errors: list[str],
    result_path: Path,
    results: list[dict[str, Any]],
    task_ids: set[str],
    model_ids: set[str],
    tool_ids: set[str],
) -> None:
    for item in results:
        result_id = item.get("id", "<missing id>")
        task_id = item.get("task_id")
        if task_id not in task_ids:
            errors.append(f"{result_path}:{result_id}: unknown task_id {task_id!r}")

        subject_type = item.get("subject_type")
        subject_id = item.get("subject_id")
        if subject_type not in VALID_RESULT_SUBJECTS:
            errors.append(f"{result_path}:{result_id}: invalid subject_type {subject_type!r}")
        elif subject_type == "model" and subject_id not in model_ids:
            errors.append(f"{result_path}:{result_id}: unknown model subject_id {subject_id!r}")
        elif subject_type == "tool" and subject_id not in tool_ids:
            errors.append(f"{result_path}:{result_id}: unknown tool subject_id {subject_id!r}")
        elif subject_type == "task" and subject_id not in task_ids:
            errors.append(f"{result_path}:{result_id}: unknown task subject_id {subject_id!r}")

        evidence = item.get("evidence")
        if isinstance(evidence, dict):
            for key in ("source_docs", "run_logs", "human_notes"):
                if key not in evidence:
                    errors.append(f"{result_path}:{result_id}: evidence missing {key}")
                elif not isinstance(evidence[key], list):
                    errors.append(f"{result_path}:{result_id}: evidence.{key} must be a list")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI-LTC evaluation registries against v0.2 schema drafts."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    parser.add_argument(
        "--as-of",
        default=date.today().isoformat(),
        help="Validation date for freshness checks, in YYYY-MM-DD format. Defaults to today.",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    errors: list[str] = []
    freshness_counts = {"fresh": 0, "referenceable": 0, "stale": 0}

    try:
        as_of = parse_iso_date(args.as_of, "--as-of")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        records_by_family: dict[str, list[dict[str, Any]]] = {}
        for family, paths in RECORD_FAMILIES.items():
            fields = required_fields(root, paths["schema"])
            records = registry_records(root, paths["registry"], family)
            validate_required(errors, paths["registry"], records, fields)
            validate_tested_at(errors, paths["registry"], records, as_of, freshness_counts)
            if family == "models":
                validate_model_shapes(errors, paths["registry"], records)
            elif family == "tools":
                validate_tool_shapes(errors, paths["registry"], records)
            elif family == "tasks":
                validate_task_shapes(errors, paths["registry"], records)
            records_by_family[family] = records

        result_fields = required_fields(root, RESULT_SCHEMA)
        result_files = sorted(root.glob(RESULTS_GLOB))
        if not result_files:
            errors.append(f"{RESULTS_GLOB}: no result files found")

        task_ids = {item["id"] for item in records_by_family["tasks"] if "id" in item}
        model_ids = {item["id"] for item in records_by_family["models"] if "id" in item}
        tool_ids = {item["id"] for item in records_by_family["tools"] if "id" in item}

        seen_results: set[str] = set()
        result_count = 0
        for result_file in result_files:
            results = registry_records(root, result_file.relative_to(root), "results")
            validate_required(errors, result_file.relative_to(root), results, result_fields)
            validate_tested_at(
                errors,
                result_file.relative_to(root),
                results,
                as_of,
                freshness_counts,
            )
            validate_result_shapes(errors, result_file.relative_to(root), results)
            for item in results:
                result_id = item.get("id")
                if result_id in seen_results:
                    errors.append(f"{result_file.relative_to(root)}:{result_id}: duplicate result id")
                if result_id:
                    seen_results.add(result_id)
            validate_result_links(
                errors,
                result_file.relative_to(root),
                results,
                task_ids,
                model_ids,
                tool_ids,
            )
            result_count += len(results)
    except ValueError as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "OK: evaluation v0.2 registries validated "
        f"({len(records_by_family['models'])} models, "
        f"{len(records_by_family['tools'])} tools, "
        f"{len(records_by_family['tasks'])} tasks, "
        f"{result_count} results; "
        f"freshness as of {as_of.isoformat()}: "
        f"{freshness_counts['fresh']} fresh, "
        f"{freshness_counts['referenceable']} referenceable, "
        f"{freshness_counts['stale']} stale)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
