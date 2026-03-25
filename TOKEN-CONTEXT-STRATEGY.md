# TOKEN-CONTEXT-STRATEGY

AI-LTC should treat token budget, context length, and model quota as operating constraints rather than as afterthoughts.
This document defines the v1.5 strategy for long-session efficiency.

## Goals

- reduce unnecessary token spend
- reduce repeated context restatement
- keep long sessions stable under bounded context limits
- respect model quotas such as Codex allocations or expensive-model budget windows
- preserve enough state that work can resume without re-deriving everything

## Core Principles

- keep the working language in English for technical payloads
- keep human-facing summaries separate from machine-oriented state
- prefer small structured anchors over repeated long prose
- prefer updating a live state file over re-explaining the entire project every turn
- use the cheapest model that can move the current state forward safely
- call the expensive model only for true architecture, audit, or optimizer work

## Main Sources Of Waste

### 1. Repeated Restatement
- re-sending the same repository history
- re-explaining the same blocker
- repeating full plans when only one step changed

### 2. Overusing Expensive Models
- asking GPT to watch normal execution
- escalating before a blocker is clearly architecture-grade

### 3. Wrong Format Choice
- forcing JSON for narrative docs
- using long markdown prose for small machine state
- pasting large logs when a narrowed summary would do

### 4. Missing State Compression
- no handoff file
- no active lane doc
- no init status file
- no resolver config

## Compression Strategy

### Handoff Compression
- keep `00_HANDOFF.md` short and operational
- preserve only:
  - done
  - next
  - risks
  - known boundaries

### Lane Compression
- active lane docs should carry current truth
- each bounded pass should update the minimal delta, not rewrite the full story

### Escalation Compression
- `ESCALATION_REQUEST.md` should narrow the problem
- include:
  - one-sentence problem
  - attempted fixes
  - current blocker
  - exact ask

### Review Compression
- checkpoint outputs should prefer:
  - `Status`
  - `Decision`
  - `Next Action`
  - `Stop Reason`

## Quota-Aware Model Routing

### Default
- use `Qwen 3.5 Plus` for ongoing execution, bounded review, and init routing

### Upgrade To GPT Only When
- architecture is still undefined
- repeated blocker is truly architecture-grade
- a high-value audit or optimization pass is justified

### Codex / Expensive-Model Discipline
- do not burn high-cost turns on routine progress narration
- do not ask for long-form system redesign when a small local repair is enough
- use one bounded pass, then stop or hand off

## Recommended Format By Token Efficiency

### Cheapest Stable Formats
- small JSON for strict machine state
- compact markdown with fixed fields for live docs
- CSV only for flat registries

### Most Expensive Patterns
- deeply nested YAML for conversational state
- long markdown essays for operational status
- repeated log dumps

### Mixed Strategy
- markdown explanation
- plus one small JSON or YAML block only when deterministic parsing matters

## Long-Session Tactics

### 1. Resolve Once, Reuse Often
- store AI-LTC source, language policy, and model defaults in `.ai/system/ai-ltc-config.json`

### 2. Update State Files, Not Whole Narratives
- use `.ai/active-lane/*`
- use `.ai/system/init-status.md`
- use `00_HANDOFF.md`
- use `ESCALATION_REQUEST.md`

### 3. Prefer Narrow Proof Paths
- use GitHub Actions for clean proof when available
- avoid long local loops that consume time and create noisy state

### 4. Carry Only The Delta
- each new message should prefer the newest evidence and the newest blocker
- avoid replaying solved history unless it changes the decision

## Working Guidance For Natural Language

### Best Default
- English for working state and technical payload

Why:
- code identifiers, paths, commands, and schema fields are usually already English
- prompt reuse is easier
- token cost is often lower than mixed bilingual technical payloads

### Human Language Layer
- let init configure:
  - `human_summary_language`
  - `human_input_language_policy`

Why:
- this preserves operator comfort without contaminating machine-oriented state

## v1.5 Operational Rule

- working language: fixed English
- human-facing summary language: configured during init
- human input language policy: configured during init
- token savings should come first from state discipline and routing discipline, not from premature micro-compression tricks

## Candidate v2 Work

- model-budget profiles by project type
- explicit token budget hints in resolver config
- optional compressed lane snapshot formats
- automated summarization checkpoints
- evidence-driven comparison of markdown+JSON vs markdown+YAML in real long-running projects
