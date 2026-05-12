# 00_HANDOFF

Legacy compatibility template. Do not use this as a new AI-LTC handoff
requirement. New target repositories keep active handoff state under `.ai/`,
with `.ai/state.json` as the first-order task source.

// Created by architect on YYYY-MM-DD: initial architecture handoff to generalist

- Status: `ready_for_generalist`
- Decision: `handoff`
- Stop Reason: `STOP_REVIEW_GATE_REACHED`
- Next Action: Start from the top pending task, not from fresh architecture analysis.

## Handoff Bundle
- `.ai/state.json`
- `.ai/active-lane/ai-handoff.md`
- `.ai/active-lane/status.md`
- `.ai/active-lane/current-status.md`
- `.ai/active-lane/roadmap.md`

## Completed
- skeleton folders created
- core interfaces or boundaries defined
- active lane / relay entrypoints chosen

## Pending By Priority
1. highest-priority implementation module
2. next supporting module
3. first verification / CI milestone

## Risks And Watchpoints
- architecture assumptions that may break
- known technical debt accepted for speed
- boundaries that the generalist role must not cross without escalation

## Execution Guardrails
- keep scope inside the selected lane
- prefer narrow GitHub Actions proof paths
- if a task packet conflicts with `.ai/state.json`, stop and report the conflict
- do not duplicate the full task table in status docs; point to the canonical state
- if repeated failure exceeds the batch, trigger `@ARCHITECT_HELP`
