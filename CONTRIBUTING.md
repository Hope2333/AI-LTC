# Contributing

Thanks for contributing to AI-LTC.

## Scope

AI-LTC is a reusable framework for staged GPT/Qwen collaboration, relay upkeep, bounded-pass execution, and long-horizon AI-assisted software work.

## Contribution Guidelines

- keep changes small and well-scoped
- preserve the v1 role model unless a versioned framework change is intentional
- prefer additive improvement over prompt sprawl
- keep examples copyable and generic
- avoid leaking local-only paths, hostnames, tokens, or personal environment details

## Framework Rules

- Qwen is the default ongoing operator in v1
- GPT should usually appear only for bootstrap architecture or targeted optimizer/auditor work
- use `00_HANDOFF.md` for GPT→Qwen transfer
- use `@ARCHITECT_HELP` + `ESCALATION_REQUEST.md` for escalations

## Public-Readiness Rule

Before opening a PR or pushing a release-oriented change, check for:
- absolute local filesystem paths
- leaked local usernames / hostnames
- hardcoded private repository assumptions
- source-project-specific facts that were not generalized

## Suggested PR Content

Include:
- what changed
- why it improves the framework
- whether it affects v1 semantics or only documentation/examples
- any migration note if users of older prompts must adjust
