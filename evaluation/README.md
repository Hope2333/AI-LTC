# Evaluation

## Purpose

Store dated, minimal, reviewable evidence about models, tools, tasks, and experiment outcomes.

The goal of this first version is stable recording, not automatic scoring.
The canonical iter1 schema doc is `docs/EVALUATION-SCHEMA.md`.

## Layout

```text
evaluation/
├── models/registry.yaml
├── tools/registry.yaml
├── tasks/registry.yaml
└── results/
    └── 2026-04.yaml
```

## Freshness Windows

- `0-30` days: fresh
- `31-90` days: referenceable
- `90+` days: stale until re-tested

## Recording Rules

- every result needs `tested_at`
- every result needs a concrete task id
- every result needs a source or evidence pointer
- every result must state scope and confidence
- seed records may be qualitative, but they must say so explicitly

## Promotion Rule

Records in `evaluation/results/` do not become framework truth automatically.
They influence `main` only after a human or stable review summarizes them into abstraction-level conclusions.
