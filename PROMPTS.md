# AI-LTC Root Prompt Guide

All agent prompts live in `prompts/`. Kernel rules in `kernel/`.

## Quick Reference

| Role | Prompt File |
|------|-------------|
| Sisyphus (orchestrator) | `prompts/qwen-generalist-autopilot.prompt.md` |
| Supervisor | `prompts/qwen-supervisory-generalist.prompt.md` |
| Architect | `prompts/gpt-bootstrap-architect.prompt.md` |
| Auditor | `prompts/gpt-optimizer-auditor.prompt.md` |
| Strategist | `prompts/gpt-corrective-strategist.prompt.md` |

## Reasoning Rules (ALL agents)

See `kernel/reasoning-policy.yaml` for full spec. Core rules:

1. **Use deep-thinking tokens**: Hmm, Wait, Therefore, But, So, If, Then
2. **No filler**: Remove "I'd be happy to", "Let me", "the", "and" chains
3. **Caveman format**: Strip grammar, keep facts. 2-5 words per sentence.
4. **Chain-of-Draft**: Each reasoning step ≤ 5 words. Focus on essential transformations.
5. **Intuition files**: Update `.ai/memories/intuition.md` with work history patterns.

## Kernel Files

| File | Purpose |
|------|---------|
| `kernel/state_schema.json` | State file structure |
| `kernel/control.yaml` | Authority chain, quality gates |
| `kernel/state_machine.yaml` | Legal phase transitions |
| `kernel/error_model.yaml` | Error types + recovery |
| `kernel/security.yaml` | Integrity, access control, tamper detection |
| `kernel/reasoning-policy.yaml` | Reasoning efficiency rules |
