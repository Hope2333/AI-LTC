# STATE-FLOWS

This document defines the normal state flow for AI-LTC v1.
It explains how work should move from initialization into execution, when handoff is required, when escalation is justified, and how GPT should return control to Qwen after a narrow intervention.

## Core Flow

```text
init
  -> handoff-ready
  -> execution
  -> review-gate or escalation
  -> optimizer-intervention
  -> optimizer-return
  -> execution
  -> checkpoint / closeout
```

This is not a strict BPMN engine.
It is the default operating state machine for long-horizon AI collaboration.
See `INIT-RECIPES.md` for the concrete rules that distinguish fresh init, resume init, update, and upgrade.

## State 1: init

Purpose:
- classify project state
- resolve AI-LTC source mode
- decide whether GPT bootstrap is needed now
- establish `.ai/system/ai-ltc-config.json`

Typical entry conditions:
- fresh repository
- `v0 -> v1` migration
- missing resolver config
- mixed or unclear AI source setup

Primary operator:
- `Qwen 3.5 Plus`

Prompt stack:
1. `shared-repo-contract.prompt.md`
2. `qwen-init-routing.prompt.md`
3. `AI-LTC-INIT-QUESTIONNAIRE.template.md` when bounded user input is needed

Required artifacts:
- `.ai/system/ai-ltc-config.json`
- `.ai/system/init-status.md`

Exit conditions:
- project state classified
- source mode resolved
- next primary operator chosen

Next state:
- `handoff-ready` when GPT bootstrap is required
- `execution` when Qwen can begin directly

## State 2: handoff-ready

Purpose:
- complete the architect-to-builder transfer
- ensure Qwen receives a bounded, executable starting point

Typical entry conditions:
- GPT bootstrap work finished
- initial skeleton is usable
- a real lane can now be defined

Primary operator:
- `GPT-5.4`

Prompt stack:
1. `shared-repo-contract.prompt.md`
2. `gpt-bootstrap-architect.prompt.md`
3. `00_HANDOFF.template.md`

Required artifacts:
- `00_HANDOFF.md`
- lane handoff/status/roadmap docs
- relay entrypoints in `docs/`

Exit conditions:
- `00_HANDOFF.md` written
- initial lane docs exist
- next execution batch is explicit

Next state:
- `execution`

## State 3: execution

Purpose:
- normal delivery
- bounded implementation
- lane upkeep
- proof collection
- day-to-day corrections inside the current lane

Primary operator:
- `Qwen 3.5 Plus`

Prompt stack:
1. `shared-repo-contract.prompt.md`
2. `qwen-generalist-autopilot.prompt.md`
3. optional `continue-execution.prompt.md`

Required artifacts:
- active `.ai/active-lane/*`
- resolver config if external AI-LTC access matters
- current batch handoff facts

Allowed outcomes:
- green proof
- first blocker identified
- bounded-pass stop
- review gate reached
- true escalation request

Next state:
- `review-gate`
- `escalation`
- `checkpoint-closeout`

## State 4: review-gate

Purpose:
- pause after meaningful new evidence
- decide whether to continue, narrow, pause, or close the current batch

Primary operator:
- usually `Qwen 3.5 Plus`
- optionally human-only if no AI review is needed

Prompt stack:
1. `shared-repo-contract.prompt.md`
2. `qwen-supervisory-generalist.prompt.md`

Required artifacts:
- current handoff/status/roadmap docs
- latest proof evidence
- current blocker or green result

Exit conditions:
- next action is explicit
- lane or phase status is clear

Next state:
- `execution`
- `escalation`
- `checkpoint-closeout`

## State 5: escalation

Purpose:
- package a real architecture-grade blocker for high-cost intervention
- prevent GPT from being pulled into normal implementation churn

Entry conditions:
- repeated blocker
- architecture deadlock
- cross-module redesign need
- optimizer-level audit justified

Primary operator:
- `Qwen 3.5 Plus` prepares the escalation

Prompt stack:
1. `shared-repo-contract.prompt.md`
2. current execution or supervisory prompt
3. `ESCALATION_REQUEST.template.md`

Required artifacts:
- `ESCALATION_REQUEST.md`
- narrowed evidence summary
- active lane docs

Exit conditions:
- escalation package is complete
- scope is narrow enough for GPT intervention

Next state:
- `optimizer-intervention`

## State 6: optimizer-intervention

Purpose:
- allow GPT to solve a narrow high-value problem
- avoid turning GPT into the default ongoing operator again

Primary operator:
- `GPT-5.4`

Prompt stack:
1. `shared-repo-contract.prompt.md`
2. `gpt-optimizer-auditor.prompt.md`
3. `ESCALATION_REQUEST.md`

Required artifacts:
- `ESCALATION_REQUEST.md`
- latest lane docs
- recent proof evidence

Allowed outputs:
- narrow redesign
- targeted audit
- performance/security guidance
- concrete return instructions for Qwen

Exit conditions:
- intervention result is documented
- Qwen can resume with bounded next steps

Next state:
- `optimizer-return`

## State 7: optimizer-return

Purpose:
- hand control back to Qwen cleanly
- prevent optimizer work from becoming a second long-lived execution lane

Primary operator:
- `GPT-5.4` writes the return guidance
- `Qwen 3.5 Plus` resumes execution

Required artifacts:
- updated `ESCALATION_REQUEST.md` or a short return note
- updated lane docs when the plan changed
- explicit next action for Qwen

Return rule:
- GPT should exit after the narrow intervention
- Qwen becomes the default operator again
- if the plan materially changed, update handoff/roadmap docs before resuming

Next state:
- `execution`

## State 8: checkpoint-closeout

Purpose:
- end a batch, milestone, or lane cleanly
- preserve enough state that the next AI does not need to reconstruct context

Primary operator:
- `Qwen 3.5 Plus` by default
- `GPT-5.4` only if a final audit or strategic checkpoint was explicitly requested

Required artifacts:
- current status in lane docs
- clear `Next Action` or closure note
- any final proof links or references

Possible outcomes:
- next batch defined
- lane paused
- lane closed
- phase moved

## Global Guardrails

- do not skip `init` when resolver state is unclear
- do not skip `handoff-ready` when GPT bootstrap created the skeleton
- do not call GPT from normal `execution` just because GPT is stronger
- always create `ESCALATION_REQUEST.md` before optimizer intervention
- after optimizer intervention, always return to Qwen unless a human explicitly changes the model plan
- prefer updating existing lane docs over creating parallel status files

## Quick Routing Summary

- if no stable config exists: start at `init`
- if GPT just built the skeleton: go to `handoff-ready`
- if normal work is ongoing: stay in `execution`
- if meaningful evidence landed: pass through `review-gate`
- if the blocker is architecture-grade: move to `escalation`
- if GPT is solving a narrow high-value problem: use `optimizer-intervention`
- when GPT is done: force `optimizer-return`
- when a batch or lane is complete: use `checkpoint-closeout`
