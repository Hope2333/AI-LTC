# BRANCH-GOVERNANCE

This document defines the responsibilities, boundaries, and merge rules for AI-LTC's dual-branch model.

## Branch Roles

### main (Protocol Layer)
**Purpose**: Stable, model-agnostic AI collaboration kernel and runtime.
**Audience**: Anyone who wants to use AI-LTC with any model.
**Versioning**: `v1.5.x` tags.

**What lives here**:
- `kernel/` — state schema, control model, error model, arbitration, state machine
- `.ai-template/` — runtime state templates, logs, snapshots
- `examples/` — demo projects, collaboration system templates
- `scripts/` — validators and tools
- Role prompts that are model-agnostic (`shared-repo-contract.prompt.md`, `gpt-*.prompt.md`, `qwen-*.prompt.md` that don't reference experimental features)
- README, CONTRIBUTING, LICENSE
- `ai-ltc-config.template.json` (without experimental_mode or multi_session blocks)

**What does NOT live here**:
- Anything tied to a specific model's behavior quirks
- Experimental session orchestration
- Model-specific prompt constraints
- `adapters/` directory

### v1.5-superqwen36-preview (Adapter Layer)
**Purpose**: Qwen 3.6 Plus Preview adapter — model-specific runtime adjustments.
**Audience**: Users running Qwen 3.6 Plus (Preview) who want optimized behavior.
**Versioning**: `v1.5.x-sqwen36pre` tags.

**What lives here**:
- Everything from main (via merge)
- `adapters/qwen36/` — Qwen-specific experimental mode, orchestrator, sessions, adapter spec
- `experimental_mode` and `multi_session` blocks in `ai-ltc-config.template.json`
- Any prompt modifications that leverage Qwen 3.6 specific capabilities

**What does NOT live here**:
- Modifications to `kernel/` files that change protocol rules (those go to main first)
- Modifications to `.ai-template/` that are not Qwen-specific

## Merge Rules

### Preview → Main (Backport)
**Allowed**:
- Bug fixes in kernel files that apply to all models
- Improvements to error recovery strategies that are model-agnostic
- Better state machine constraints that don't assume specific model behavior
- README improvements, demo fixes, script updates
- New validators or tools

**Not Allowed**:
- Anything in `adapters/` directory
- Prompt changes that rely on Qwen 3.6 specific capabilities
- `experimental_mode` or `multi_session` config blocks
- Session orchestration logic

### Main → Preview (Forward)
**Always Allowed**: All main commits merge into preview automatically.
Preview branch should regularly merge main to stay current with kernel improvements.

## Decision Flowchart

When you have a change to make:

```
Is this change model-agnostic?
  ├── Yes → Does it modify kernel, .ai-template, examples, scripts, or README?
  │         ├── Yes → Commit to main
  │         └── No → Does it belong in shared prompts?
  │                   ├── Yes → Commit to main
  │                   └── No → Review: might belong in adapter
  └── No → Is it Qwen 3.6 specific?
            ├── Yes → Commit to preview (adapters/qwen36/)
            └── No → Create new adapter directory (adapters/{model}/)
```

## Directory Responsibility Matrix

| Directory | Owned By | Can Be Modified By |
|---|---|---|
| `kernel/` | main | main only (preview may suggest, but changes merge through main) |
| `.ai-template/` | main | main only |
| `examples/` | main | both (preview may add Qwen-specific demo variants) |
| `scripts/` | main | main only |
| `adapters/` | preview | preview only |
| `shared-repo-contract.prompt.md` | main | main only |
| `qwen-*.prompt.md` (root) | main | main only (model-agnostic Qwen prompts) |
| `gpt-*.prompt.md` | main | main only |
| `adapters/qwen36/*.prompt.md` | preview | preview only |

## Adapter Interface Contract

Every adapter in `adapters/{model}/` must include:

1. `adapter.yaml` — Model capabilities, quirks, routing, validation references
2. At least one prompt file that adapts kernel behavior to the model
3. Clear documentation of what is model-specific vs what is universal

## Version Alignment

- main tags: `v1.5.3`, `v1.5.4`, `v1.5.5`, etc.
- preview tags: `v1.5.10-sqwen36pre`, `v1.5.11-sqwen36pre`, etc.
- Preview tags do NOT need to match main tags — they track adapter evolution independently
- When preview's kernel changes are backported to main, main gets a new tag
- When main gets a new tag, preview should merge and get a new tag

## Review Checklist

Before merging preview → main:
- [ ] No files in `adapters/` are included
- [ ] No `experimental_mode` or `multi_session` config changes
- [ ] No prompt changes that reference Qwen 3.6 specific behavior
- [ ] All kernel changes are model-agnostic
- [ ] Demo tests still pass
- [ ] README changes are accurate
