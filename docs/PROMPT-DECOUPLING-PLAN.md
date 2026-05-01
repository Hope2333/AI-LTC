# Prompt Decoupling Plan

## Status

- Iteration: `iter1`
- Purpose: abstract prompts away from provider-bound filenames
- Scope: design, mapping, and scaffold definition

## Original Problem

Several legacy prompt files encoded multiple concerns in one filename:

- provider identity
- role identity
- lifecycle phase
- execution style

Examples:

- `qwen-generalist-autopilot.prompt.md`
- `qwen-supervisory-generalist.prompt.md`
- `gpt-bootstrap-architect.prompt.md`
- `gpt-corrective-strategist.prompt.md`

This created a structural contradiction:

- the kernel is moving toward role and state abstractions
- the prompt layer could still look model-bound

## Refactor Goal

Prompts should be composable from four layers:

1. role
2. phase
3. constraint
4. adapter

## Target Layout

```text
prompts/
├── roles/
├── phases/
├── constraints/
└── adapters/
```

## Layer Rules

### `roles/`

Contains stable behavioral intent:

- architect
- generalist
- supervisor
- strategist
- optimizer

No provider names in filenames.

### `phases/`

Contains lifecycle positioning:

- init
- execution
- review
- checkpoint
- optimizer

### `constraints/`

Contains reusable boundaries:

- output format
- language policy
- token/context limits
- safety or scope constraints

### `adapters/`

Contains provider or platform deltas only:

- OpenAI
- Qwen
- Claude
- OpenCode
- Codex

## Migration Policy

1. keep legacy files as compatibility entrypoints
2. add provider-neutral files in parallel
3. move stable content out of legacy files over time
4. leave only thin adapter-specific deltas in provider-named files

Current state: the legacy entrypoint contents are thin compatibility surfaces that delegate to role and phase prompts. Their filenames remain for compatibility and mapping validation.

## Mapping Table

| Legacy File | Role | Phase | Adapter |
|---|---|---|---|
| `prompts/gpt-bootstrap-architect.prompt.md` | `roles/architect.prompt.md` | `phases/init.prompt.md` | `adapters/openai.adapter.md` |
| `prompts/qwen-generalist-autopilot.prompt.md` | `roles/generalist.prompt.md` | `phases/execution.prompt.md` | `adapters/qwen.adapter.md` |
| `prompts/qwen-supervisory-generalist.prompt.md` | `roles/supervisor.prompt.md` | `phases/review.prompt.md` | `adapters/qwen.adapter.md` |
| `prompts/gpt-corrective-strategist.prompt.md` | `roles/strategist.prompt.md` | `phases/checkpoint.prompt.md` | `adapters/openai.adapter.md` |
| `prompts/gpt-optimizer-auditor.prompt.md` | `roles/optimizer.prompt.md` | `phases/review.prompt.md` | `adapters/openai.adapter.md` |

## What Counts As Success In Iteration 1

- the provider-neutral structure exists
- the mapping is written down
- legacy files remain usable
- the new structure can guide iteration 2 without another naming debate
