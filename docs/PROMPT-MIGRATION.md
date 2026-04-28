# Prompt Migration

Design doc: `docs/PROMPT-DECOUPLING-PLAN.md`.

## Goal

Move from provider-bound prompt filenames toward a composable structure:

- roles
- phases
- constraints
- adapters

This migration is coexistence-first. Legacy prompt entrypoints stay available until the new structure proves itself.
This file is the short operational summary; the full design write-up lives in `docs/PROMPT-DECOUPLING-PLAN.md`.

## Current Problem

Existing filenames mix together:

- provider identity
- role identity
- phase expectations
- execution constraints

That makes prompt knowledge hard to reuse across providers and hard to audit independently.

## Target Structure

```text
prompts/
├── roles/
├── phases/
├── constraints/
├── adapters/
└── _mapping/
```

## Coexistence Rules

1. Do not delete legacy prompt files during scaffold introduction.
2. Put stable role intent into `prompts/roles/`.
3. Put lifecycle-specific instructions into `prompts/phases/`.
4. Put reusable boundaries into `prompts/constraints/`.
5. Put provider or platform deltas only into `prompts/adapters/`.
6. Record coexistence mappings in `prompts/_mapping/` before splitting or deleting legacy entrypoints.

## Validation

Run:

```bash
make validate-prompts
```

This checks that mapping references point to existing prompt files and that migration statuses use the expected vocabulary. It does not rewrite prompts or decide migration readiness.

## Mapping Seed

| Legacy File | Target Role | Target Phase | Adapter Delta |
|---|---|---|---|
| `prompts/gpt-bootstrap-architect.prompt.md` | `prompts/roles/architect.prompt.md` | `prompts/phases/init.prompt.md` | `prompts/adapters/openai.adapter.md` |
| `prompts/qwen-generalist-autopilot.prompt.md` | `prompts/roles/generalist.prompt.md` | `prompts/phases/execution.prompt.md` | `prompts/adapters/qwen.adapter.md` |
| `prompts/qwen-supervisory-generalist.prompt.md` | `prompts/roles/supervisor.prompt.md` | `prompts/phases/review.prompt.md` | `prompts/adapters/qwen.adapter.md` |
| `prompts/gpt-corrective-strategist.prompt.md` | `prompts/roles/strategist.prompt.md` | `prompts/phases/checkpoint.prompt.md` | `prompts/adapters/openai.adapter.md` |
| `prompts/gpt-optimizer-auditor.prompt.md` | `prompts/roles/optimizer.prompt.md` | `prompts/phases/review.prompt.md` | `prompts/adapters/openai.adapter.md` |

## What This Pass Adds

- minimal role files
- minimal phase files
- minimal shared constraint files
- minimal adapter delta files

These files are scaffolds, not final replacements.
