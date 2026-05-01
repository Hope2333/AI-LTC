# Legacy To Role / Phase / Adapter Mapping

<!-- status: experimental -->
<!-- updated: 2026-04-28 -->

This file records coexistence mappings before any legacy prompt is split or deleted.

## Migration Rule

- Do not remove legacy prompt entrypoints during mapping.
- Keep role intent, phase flow, shared constraints, and provider/platform deltas separate.
- Treat provider-named legacy files as compatibility entrypoints until their behavior is covered by role / phase / constraint / adapter fragments.

## Legacy Prompt Mappings

### qwen-generalist-autopilot.prompt.md

Maps to:

- `prompts/roles/generalist.prompt.md`
- `prompts/phases/execution.prompt.md`
- `prompts/constraints/token-context.prompt.md`
- `prompts/constraints/safety-boundary.prompt.md`
- `prompts/adapters/qwen.adapter.md`

Migration status: in_progress
Risk: legacy filename is now a thin compatibility entrypoint; provider-specific execution behavior should stay in adapter layers, not generalist role logic.

### qwen-supervisory-generalist.prompt.md

Maps to:

- `prompts/roles/supervisor.prompt.md`
- `prompts/phases/checkpoint.prompt.md`
- `prompts/phases/review.prompt.md`
- `prompts/constraints/output-format.prompt.md`
- `prompts/adapters/qwen.adapter.md`

Migration status: in_progress
Risk: legacy filename is now a thin compatibility entrypoint; supervision, checkpointing, and provider-specific formatting may be coupled.

### gpt-bootstrap-architect.prompt.md

Maps to:

- `prompts/roles/architect.prompt.md`
- `prompts/phases/init.prompt.md`
- `prompts/constraints/safety-boundary.prompt.md`
- `prompts/adapters/openai.adapter.md`

Migration status: in_progress
Risk: legacy filename is now a thin compatibility entrypoint; architecture role behavior should stay role-first.

### gpt-corrective-strategist.prompt.md

Maps to:

- `prompts/roles/strategist.prompt.md`
- `prompts/phases/review.prompt.md`
- `prompts/constraints/token-context.prompt.md`
- `prompts/adapters/openai.adapter.md`

Migration status: in_progress
Risk: legacy filename is now a thin compatibility entrypoint; corrective strategy and provider assumptions may be mixed.

### gpt-optimizer-auditor.prompt.md

Maps to:

- `prompts/roles/optimizer.prompt.md`
- `prompts/phases/review.prompt.md`
- `prompts/constraints/output-format.prompt.md`
- `prompts/adapters/openai.adapter.md`

Migration status: in_progress
Risk: legacy filename is now a thin compatibility entrypoint; narrow audit behavior may be hidden behind legacy provider naming.

## Adapter Samples

### OpenCode build / plan

Maps to:

- `prompts/roles/generalist.prompt.md` for build-like execution
- `prompts/roles/architect.prompt.md` and `prompts/roles/strategist.prompt.md` for plan-like read-only analysis
- `prompts/adapters/opencode.adapter.md`

Migration status: reference
Risk: OpenCode's built-in agent names should not replace AI-LTC role abstractions.

### Claude Code

Maps to:

- `prompts/adapters/claude.adapter.md`

Migration status: reference
Risk: terminal, IDE, desktop, and browser surfaces need separate evaluation evidence before routing claims.
