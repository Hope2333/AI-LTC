# Evaluation Schema

## Status

- Iteration: `iter1`
- Schema version: `v0.2`
- Purpose: define the minimum durable evaluation data model
- Scope: schema and freshness rules, not automation

## Why This Exists

Evaluation conclusions go stale quickly if they are not tied to:

- when something was tested
- what version was tested
- where the conclusion came from

Without these fields, routing and governance decay into folklore.

## Data Families

The evaluation layer has four primary record families:

1. models
2. tools
3. tasks
4. results

Record-family schema drafts:

- `evaluation/schemas/model.schema.yaml`
- `evaluation/schemas/tool.schema.yaml`
- `evaluation/schemas/task.schema.yaml`
- `evaluation/schemas/result.schema.yaml`

## Required Fields

### Models

Minimum required fields:

- `id`
- `name`
- `provider`
- `model_type`
- `version`
- `release_date`
- `tested_at`
- `status`
- `source`
- `notes`

Recommended fields:

- `architecture`
- `context_length`
- `size`
- `capabilities`
- `deployment_fit`
- `strengths`
- `weaknesses`
- `scores`
- `boundary_notes`

### Tools

Minimum required fields:

- `id`
- `name`
- `category`
- `provider`
- `version`
- `tested_at`
- `status`
- `source`
- `notes`

Recommended fields:

- `installation_mode`
- `surfaces`
- `workspace_capabilities`
- `access_model`
- `harness_features`
- `permission_model`
- `capabilities`
- `strengths`
- `weaknesses`
- `known_failure_modes`
- `scores`
- `boundary_notes`

### Tasks

Minimum required fields:

- `id`
- `name`
- `description`

Recommended fields:

- `success_criteria`
- `preferred_roles`
- `preferred_signals`

### Results

Minimum required fields:

- `id`
- `task_id`
- `subject_type`
- `subject_id`
- `tested_at`
- `environment`
- `source`
- `evidence`
- `notes`

Recommended fields:

- `prompt_profile`
- `subject_version`
- `observations`
- `failure_modes_observed`
- `scores`
- `status`
- `confidence`
- `recommendation`

## Freshness Rules

- `0-30` days: fresh
- `31-90` days: referenceable
- `90+` days: stale until re-tested

Freshness is determined from `tested_at`, not from commit date alone.

## Version Rules

- `version` is required for models and tools even if the value is temporarily `unknown`
- `release_date` is required for models and strongly preferred for tools
- if the exact value is unknown, use a clear placeholder rather than omitting the field

## Source Rules

- every record needs a traceable `source`
- acceptable sources include repo files, release notes, test logs, or clearly named local evidence
- `source` should make later re-checking possible

## Validation

Run the local schema-shape validator before committing evaluation changes:

```bash
make validate-evaluation
make validate-provider-naming
make validate-ts-imports
make validate-config-registry
make check
```

`make validate-evaluation` validates YAML parsing, v0.2 required fields, duplicate ids, selected field types, `tested_at` date format, freshness windows, result task references, result subject references, and evidence list shape. It does not generate scores, weights, recommendations, or routing decisions. `make validate-provider-naming` verifies provider-specific terms stay inside compatibility, adapter, mapping, or evidence surfaces. `make validate-ts-imports` verifies local TypeScript imports in bridge and adapter files without requiring a TypeScript compiler. `make validate-config-registry` verifies version alignment across `VERSION`, `cross-repo-registry.json`, and `ai-ltc-config.template.json`. `make check` runs all validators plus the existing bridge integration smoke test.

## Status Vocabulary

Preferred values:

- `active`
- `reference`
- `experimental`
- `stale`
- `deprecated`

## Scoring Guidance

Scores are optional in iter1. If present, keep them lightweight and comparable.

Suggested result scores:

- `success`
- `stability`
- `cost`

Suggested model or tool scores:

- `reasoning`
- `coding`
- `latency`
- `cost_efficiency`
- `integration`
- `reproducibility`

## Non-Goals

- no automatic score generation
- no automatic routing
- no hidden weighting system
- no requirement to cover the full model or tool market
