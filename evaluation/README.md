# Evaluation

## Purpose

Store dated, minimal, reviewable evidence about models, tools, tasks, and experiment outcomes.

The goal of this first version is stable recording, not automatic scoring.
The canonical schema overview is `docs/EVALUATION-SCHEMA.md`.
Record-family schema drafts live under `evaluation/schemas/`.

## Layout

```text
evaluation/
├── models/registry.yaml
├── tools/registry.yaml
├── tasks/registry.yaml
├── results/
│   └── 2026-04.yaml
└── schemas/
    ├── model.schema.yaml
    ├── tool.schema.yaml
    ├── task.schema.yaml
    └── result.schema.yaml
```

## Freshness Windows

- `0-30` days: fresh
- `31-90` days: referenceable
- `90+` days: stale until re-tested

## Recording Rules

- every result needs `tested_at`
- every result needs a concrete task id
- every result needs structured `evidence`
- every result must state scope and confidence
- seed records may be qualitative, but they must say so explicitly

## Validation

Run:

```bash
make validate-evaluation
make validate-provider-naming
make validate-ts-imports
```

This checks YAML parsing, v0.2 required fields, duplicate ids, selected field types, `tested_at` date format, freshness windows, result task references, result subject references, evidence list shape, provider naming boundaries, and local TypeScript import resolution. It does not score records or automate evaluation.

## v0.2 Additions

- tool records distinguish surfaces, harness features, access model, permission model, and known failure modes
- model records include deployment fit for hosted, local, mobile, and always-on use
- result records keep evidence pointers separate from observations and recommendations
- validators report freshness from `tested_at`: fresh (`0-30` days), referenceable (`31-90` days), stale (`90+` days)

## Promotion Rule

Records in `evaluation/results/` do not become framework truth automatically.
They influence `main` only after a human or stable review summarizes them into abstraction-level conclusions.
