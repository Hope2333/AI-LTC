# BRANCH-GOVERNANCE

This document defines the responsibilities, boundaries, and merge rules for AI-LTC's dual-branch model.
See `docs/BRANCH-SEMANTICS.md` for the short operational summary and `docs/BRANCH-REFACTOR-PLAN.md` for the branch refactor design.

## Branch Roles

### main (Framework Layer)
**Purpose**: Stable, model-agnostic AI collaboration kernel, runtime, and public framework surface.
**Audience**: Anyone who wants to use AI-LTC with any model.
**Versioning**: `v1.5.x` tags.

**What lives here**:
- `kernel/` — state schema, control model, error model, arbitration, state machine
- `.ai-template/` — runtime state templates, logs, snapshots
- `examples/` — demo projects, collaboration system templates
- `scripts/` — validators and tools
- Legacy prompt entrypoints that remain model-agnostic enough to preserve compatibility
- Stable prompt migration docs and role / phase / constraint abstractions once proven
- README, CONTRIBUTING, LICENSE
- `ai-ltc-config.template.json` (without experimental_mode or multi_session blocks)

**What does NOT live here**:
- Anything tied to a specific model's behavior quirks
- Experimental-only evaluation records that have not earned promotion
- Experimental session orchestration
- `adapters/` directory

### Experimental
**Purpose**: Active experimental branch for adapters, prompt refactoring, evaluation schema/data, migration scaffolding, and platform-specific runtime adjustments.
**Audience**: Contributors validating new structures, adapters, and evidence before promotion to `main`.
**Versioning**: `v1.5.x` experimental tags; historical preview suffixes may remain only for continuity.

**What lives here**:
- Everything from main (via merge)
- `adapters/` — provider-specific experimental modes, orchestrators, sessions, and adapter specs
- additional adapter directories as future experiments require
- `evaluation/` — dated registries, v0.2 schemas, task definitions, and experiment records
- new prompt migration scaffolding under `prompts/roles/`, `prompts/phases/`, `prompts/constraints/`, and `prompts/adapters/`
- prompt coexistence mapping under `prompts/_mapping/`
- `experimental_mode` and `multi_session` blocks in `ai-ltc-config.template.json`
- prompt modifications and adapters that leverage provider- or platform-specific capabilities

**What does NOT live here**:
- Modifications to `kernel/` files that change protocol rules (those go to main first)
- Modifications to `.ai-template/` that are not provider-specific
- unstable branch semantics that are undocumented

## Merge Rules

### Experimental → Main (Backport)
**Allowed**:
- Bug fixes in kernel files that apply to all models
- Improvements to error recovery strategies that are model-agnostic
- Better state machine constraints that don't assume specific model behavior
- README improvements, demo fixes, script updates
- New validators or tools

**Not Allowed**:
- Anything in `adapters/` directory
- Prompt changes that rely on provider-specific capabilities
- `experimental_mode` or `multi_session` config blocks
- Session orchestration logic
- experimental evaluation records without a stable summary or promotion rationale

### Main → Experimental (Forward)
**Always Allowed**: All main commits merge into the actual Experimental branch automatically.
The Experimental branch should regularly merge main to stay current with framework improvements.

## Decision Flowchart

When you have a change to make:

```
Is this change model-agnostic?
  ├── Yes → Does it modify kernel, .ai-template, examples, scripts, or README?
  │         ├── Yes → Commit to main
  │         └── No → Does it belong in shared prompts?
  │                   ├── Yes → Commit to main
  │                   └── No → Review: might belong in adapter
  └── No → Is it experimental, provider-specific, or evaluation-heavy?
            ├── Yes → Commit to Experimental
            └── No → Review: maybe it belongs in main after abstraction cleanup
```

## Directory Responsibility Matrix

| Directory | Owned By | Can Be Modified By |
|---|---|---|
| `kernel/` | main | main only (Experimental may suggest, but changes merge through main) |
| `.ai-template/` | main | main only |
| `examples/` | main | both (Experimental may add provider-specific demo variants) |
| `scripts/` | main | main only |
| `adapters/` | Experimental | Experimental only |
| `evaluation/` | Experimental | Experimental only until records are summarized |
| `shared-repo-contract.prompt.md` | main | main only |
| legacy root prompt entrypoints | main | main only unless they become provider-specific |
| `prompts/roles/`, `prompts/phases/`, `prompts/constraints/` | Experimental | Experimental first, then promote to main when stable |
| `prompts/adapters/` | Experimental | Experimental only |
| `adapters/{provider}/*.prompt.md` | Experimental | Experimental only |

## Adapter Interface Contract

Every adapter in `adapters/{model}/` must include:

1. `adapter.yaml` — Model capabilities, quirks, routing, validation references
2. At least one prompt file that adapts kernel behavior to the model
3. Clear documentation of what is model-specific vs what is universal

## Version Alignment

- Current repo `VERSION`: `v1.5.15`
- main tags remain `v1.5.x`
- Experimental is already the active experimental branch; do not describe it as a future rename target
- Experimental tags may continue using historical preview suffixes only when preserving old evidence trails
- Line name: active provider-specific lines remain tracked in adapter and evaluation records
- Experimental tags do not need to numerically mirror main tags if the experimental lane evolves independently
- When Experimental work is abstracted and promoted, main gets the stable tag; Experimental keeps its evidence trail

## Review Checklist

Before merging Experimental → main:
- [ ] No files in `adapters/` are included
- [ ] No `experimental_mode` or `multi_session` config changes
- [ ] No prompt changes that reference provider-specific behavior without abstraction cleanup
- [ ] Experimental evaluation records are either excluded or summarized into stable conclusions
- [ ] All kernel changes are model-agnostic
- [ ] Demo tests still pass
- [ ] README changes are accurate
