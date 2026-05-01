# Branch Semantics

Canonical iter1 design doc: `docs/BRANCH-REFACTOR-PLAN.md`.

## Purpose

Define the conceptual branch model without forcing an immediate git branch rename.
This file is the short operational summary; the full iter1 write-up lives in `docs/BRANCH-REFACTOR-PLAN.md`.

## Stable Terms

| Term | Meaning | Current Implementation |
|---|---|---|
| `main` | Stable framework layer | actual branch `main` |
| `Experimental` | Experimental lane for adapters, evaluation, migration scaffolding, and platform-specific work | actual branch `Experimental` |

## Why This Exists

The repository has already outgrown a purely model-named branch story:

- `adapters/` is broader than one provider
- prompt migration work is about abstractions, not one model
- evaluation data needs a neutral home
- AI-LTC / OML boundary work spans more than one provider

Using `Experimental` as the semantic name clarifies that the lane is for controlled experiments, not a permanent provider-only silo.

## Rules

### `main`

- keep stable framework assets here
- accept only model-agnostic abstractions
- absorb stable conclusions from Experimental

### `Experimental`

- stage new adapter work
- stage prompt migration scaffolding
- stage time-scoped evaluation records
- keep compatibility entrypoints until replacement is proven

## Naming Policy

- In conceptual docs, prefer `Experimental`
- Keep the historical branch name only when explaining old tags or old references
- Do not silently rename the git branch in the middle of unrelated work

## Promotion Gate

Experimental work may move to `main` only when:

1. filenames and concepts are no longer provider-bound
2. the change has at least minimal evidence or example coverage
3. any evaluation records used to justify the change are dated and attributable
4. user-facing docs remain understandable for existing users
