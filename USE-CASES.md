# Use Cases

AI-LTC is designed for long-horizon AI-assisted software work.
This document is the routing guide for choosing the right model, prompt stack, and control artifacts by project situation.

## How To Read This File

For each scenario, check:
- when the scenario applies
- the primary model choice
- the recommended prompt stack
- required control files or artifacts
- when GPT should stay out
- the normal stop condition

## Global Routing Rules

- default ongoing operator: `Qwen 3.5 Plus`
- default escalation target: `GPT-5.4` in optimizer/auditor mode
- local AI-LTC checkout should be preferred first
- remote fallback should normally be `https://github.com/Hope2333/AI-LTC`
- if the repository is a `v0 -> v1` migration or lacks `.ai/system/ai-ltc-config.json`, run init before normal execution
- if a narrow GitHub Actions proof path exists, prefer it over a broad local build loop

## Scenario 1: Brand-New Project

When to use:
- architecture is not settled
- folder structure is not settled
- lane docs do not exist yet
- you want the initial system ceiling defined carefully

Primary model:
- `GPT-5.4`

Fallback model:
- `Qwen 3.5 Plus` only after the architect handoff exists

Recommended prompt stack:
1. `shared-repo-contract.prompt.md`
2. `gpt-bootstrap-architect.prompt.md`
3. `00_HANDOFF.template.md`

Required artifacts:
- `00_HANDOFF.md`
- initial `docs/ai-relay.md`
- initial `.ai/README.md`
- initial lane handoff/status/roadmap files

GPT should stay out after:
- the skeleton is usable
- the handoff is written
- the first execution lane is defined

Normal stop condition:
- architect handoff completed and approved

## Scenario 2: v0 To v1 Migration

When to use:
- the repository already has an older AI-LTC style
- prompts or docs still assume hardcoded paths
- init resolver config does not exist
- model roles are still ambiguous

Primary model:
- `Qwen 3.5 Plus`

Fallback model:
- `GPT-5.4` only if migration reveals architecture-level ambiguity

Recommended prompt stack:
1. `shared-repo-contract.prompt.md`
2. `qwen-init-routing.prompt.md`
3. `AI-LTC-INIT-QUESTIONNAIRE.template.md`
4. `qwen-supervisory-generalist.prompt.md` when cleanup decisions are needed

Required artifacts:
- `.ai/system/ai-ltc-config.json`
- `.ai/system/init-status.md`
- updated relay docs in the target repository

Key routing rule:
- local AI-LTC first
- remote fallback second
- Qwen may refresh local AI-LTC only when needed and allowed

Normal stop condition:
- resolver config written and v1 route selected

## Scenario 3: Midstream Project With Existing Structure

When to use:
- the repository already has active code and docs
- a lane exists or can be inferred
- architecture is mostly settled
- execution should resume quickly

Primary model:
- `Qwen 3.5 Plus`

Fallback model:
- `GPT-5.4` only if Qwen emits `@ARCHITECT_HELP`

Recommended prompt stack:
1. `shared-repo-contract.prompt.md`
2. `qwen-init-routing.prompt.md` if classification is still needed
3. `qwen-generalist-autopilot.prompt.md`

Required artifacts:
- active lane docs under `.ai/`
- resolver config if AI-LTC source is not already clear

Qwen should own:
- execution
- day-to-day supervision
- relay upkeep
- bounded iteration

Normal stop condition:
- current batch reaches a green proof, review gate, or bounded-pass stop

## Scenario 4: Ongoing Delivery Or Long Session Work

When to use:
- the project already has a stable lane
- work is mainly implementation or focused verification
- you want a stronger replacement for a bare `continue.`

Primary model:
- `Qwen 3.5 Plus`

Recommended prompt stack:
1. `shared-repo-contract.prompt.md`
2. `qwen-generalist-autopilot.prompt.md`
3. optional `continue-execution.prompt.md`

Optional control artifacts:
- `00_HANDOFF.md` if execution resumed after a GPT bootstrap
- `.ai/active-lane/*`

Keep GPT out when:
- blockers are implementation-level
- the lane is still coherent
- the next action is already obvious from the handoff

Normal stop condition:
- `STOP_REVIEW_GATE_REACHED`, `STOP_BOUNDED_PASS_EXHAUSTED`, or a concrete green result

## Scenario 5: Checkpoint, Lane Review, Or Sequencing Decision

When to use:
- you need a status read
- you need lane or phase judgment
- you want to know whether to continue, narrow, pause, or escalate

Primary model:
- `Qwen 3.5 Plus`

Fallback model:
- `GPT-5.4` only if the review reveals real architecture-heavy uncertainty

Recommended prompt stack:
1. `shared-repo-contract.prompt.md`
2. `qwen-supervisory-generalist.prompt.md`

Required artifacts:
- active handoff/status/roadmap docs
- recent proof evidence if available

Normal stop condition:
- a clear decision is recorded with `Status`, `Decision`, `Next Action`, and `Stop Reason`

## Scenario 6: Chaotic Repository, Broken Handoff, Or Mixed Sources Of Truth

When to use:
- docs disagree with each other
- `.ai/` is missing or stale
- lane ownership is unclear
- the next AI would otherwise need to reconstruct too much state

Primary model:
- `Qwen 3.5 Plus`

Fallback model:
- `GPT-5.4` only after a short Qwen cleanup/classification pass fails

Recommended prompt stack:
1. `shared-repo-contract.prompt.md`
2. `qwen-init-routing.prompt.md`
3. `qwen-supervisory-generalist.prompt.md`

Required artifacts:
- `.ai/system/init-status.md`
- repaired relay docs
- updated `.ai/system/ai-ltc-config.json` when resolver confusion exists

Escalate only when:
- the chaos is truly architecture-level
- multiple sources of truth cannot be reconciled by bounded cleanup

Normal stop condition:
- source of truth repaired and next primary operator chosen

## Scenario 7: Hard Refactor, Repeated Blocker, Or Architecture Deadlock

When to use:
- Qwen has repeated the same blocker
- the problem crosses module or architecture boundaries
- a high-cost redesign or audit is justified

Primary model:
- `GPT-5.4`

Entry requirement:
- Qwen should first emit `@ARCHITECT_HELP`
- write `ESCALATION_REQUEST.md`

Recommended prompt stack:
1. `shared-repo-contract.prompt.md`
2. `ESCALATION_REQUEST.template.md`
3. `gpt-optimizer-auditor.prompt.md`

Required artifacts:
- `ESCALATION_REQUEST.md`
- current lane docs
- narrowed evidence summary from Qwen

Normal stop condition:
- targeted architect intervention completed and handed back to Qwen

## Scenario 8: Performance, Quality, Or Security Audit

When to use:
- you want a short, high-value review
- delivery is moving, but you want a strategic or safety check
- a sprint or milestone just ended

Primary model:
- `GPT-5.4`

Fallback model:
- `Qwen 3.5 Plus` for cheaper preliminary checkpointing before escalation

Recommended prompt stack:
1. `shared-repo-contract.prompt.md`
2. `gpt-optimizer-auditor.prompt.md`

Optional supporting artifacts:
- `ESCALATION_REQUEST.md`
- recent checkpoint summary
- recent CI evidence

Normal stop condition:
- audit recommendations written and a new handoff path defined

## Scenario 9: Public Template Bootstrap For Another Repository

When to use:
- you want to copy AI-LTC into a new repository
- you want a clean reusable starting point instead of project residue

Primary entry:
- `examples/collaboration-system/README.md`
- `examples/collaboration-system/install-example.md`
- `examples/collaboration-system/bootstrap-checklist.md`
- `examples/collaboration-system/ROLE-QUICK-REFERENCE.md`

Then route to:
- `qwen-init-routing.prompt.md` if the target repository should classify itself first
- `gpt-bootstrap-architect.prompt.md` if the target repository is truly greenfield and needs a stronger first skeleton

Required artifacts after copy:
- `.ai/system/ai-ltc-config.json`
- `.ai/system/init-status.md`
- target-specific lane docs

Normal stop condition:
- target repository has a working relay surface and a chosen primary operator

## Fast Decision Table

- If the project is new and undefined: use `GPT-5.4` first.
- If the project exists and mostly makes sense: use `Qwen 3.5 Plus` first.
- If the repository is messy but recoverable: use `Qwen 3.5 Plus` to clean and classify first.
- If the same architecture-grade blocker repeats: escalate to `GPT-5.4`.
- If the repository is copying AI-LTC for the first time: use the example + init routing.
- If AI-LTC source resolution is unclear: resolve `.ai/system/ai-ltc-config.json` before normal execution.

## Summary

- `GPT-5.4` defines the ceiling, audits, and intervenes narrowly.
- `Qwen 3.5 Plus` is the default ongoing operator.
- `qwen-init-routing.prompt.md` is the front door for classification and resolver setup.
- `00_HANDOFF.md` and `ESCALATION_REQUEST.md` are the formal phase-transition artifacts.
- `USE-CASES.md` should be treated as the routing layer, not just as an example list.
