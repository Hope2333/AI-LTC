# ARCHITECTURE-LAYERS

AI-LTC uses three change classes and four operating layers.
The three change classes explain what should stay stable, what should track live project state, and what should evolve through repeated real-world use.
The four layers explain where those things live.

## Three Change Classes

### 1. Static

Purpose:
- stable framework rules
- role boundaries
- reusable templates
- low-frequency governance updates

Typical files:
- `FRAMEWORK-V1.md`
- `README.md`
- `README.zh.md`
- `shared-repo-contract.prompt.md`
- `00_HANDOFF.template.md`
- `ESCALATION_REQUEST.template.md`
- `USE-CASES.md`
- `FORMAT-STRATEGY.md`
- `ROLE-QUICK-REFERENCE.md`
- `LICENSE`
- `CONTRIBUTING.md`

Properties:
- rarely changes
- should not drift with one project's temporary state
- should stay reusable across repositories

### 2. Dynamic

Purpose:
- active lane state
- live handoff information
- current blockers, next actions, ownership, and status
- target-repository-specific AI-LTC resolver values

Typical files in a target repository:
- `.ai/active-lane/ai-handoff.md`
- `.ai/active-lane/current-status.md`
- `.ai/active-lane/roadmap.md`
- `.ai/system/ai-ltc-config.json`
- `.ai/system/init-status.md`
- `00_HANDOFF.md`
- `ESCALATION_REQUEST.md`

Properties:
- high-frequency changes
- strongly project-specific
- should normally remain local-only
- should not be copied blindly between repositories

### 3. Self-Evolving

Purpose:
- framework parts that improve from field use
- init routing rules
- model selection policy
- example skeleton upgrades
- reusable prompts that need periodic refinement

Typical files:
- `INIT-QWEN.md`
- `qwen-init-routing.prompt.md`
- `qwen-generalist-autopilot.prompt.md`
- `qwen-supervisory-generalist.prompt.md`
- `gpt-bootstrap-architect.prompt.md`
- `gpt-optimizer-auditor.prompt.md`
- `AI-LTC-INIT-QUESTIONNAIRE.template.md`
- `ai-ltc-config.template.json`
- `FORMAT-STRATEGY.md`
- `examples/collaboration-system/`
- `VERSION.md`
- `CHANGELOG.md`

Properties:
- changes in batches, not continuously every session
- should be updated from repeated evidence, not impulse edits
- acts as the bridge between framework theory and execution reality

## State Flow Reference

- `STATE-FLOWS.md` explains how work moves through `init`, `handoff-ready`, `execution`, `review-gate`, `escalation`, `optimizer-intervention`, `optimizer-return`, and `checkpoint-closeout`.
- Layer definitions explain where information lives.
- `STATE-FLOWS.md` explains when control should move between those layers and between GPT and Qwen.

## Four Operating Layers

### Layer 0: Shared Contract

Purpose:
- common read order
- output structure
- stop phrases
- status fields
- language rules
- commit and scope guardrails

Main file:
- `shared-repo-contract.prompt.md`

Change class:
- mostly Static

### Layer 1: Role Prompts

Purpose:
- define what each model should do in a given stage
- keep GPT limited to architect/optimizer roles
- keep Qwen as the default generalist operator

Main files:
- `gpt-bootstrap-architect.prompt.md`
- `gpt-optimizer-auditor.prompt.md`
- `qwen-init-routing.prompt.md`
- `qwen-generalist-autopilot.prompt.md`
- `qwen-supervisory-generalist.prompt.md`

Change class:
- Static at the boundary level
- Self-Evolving at the workflow-detail level

### Layer 2: Repository Skeleton And Relay Surface

Purpose:
- define how a target repository is structured for long-horizon AI work
- provide docs entrypoints, `.ai/` layout, templates, and reusable conventions

Main files:
- `examples/collaboration-system/project-template/AGENTS.md`
- `examples/collaboration-system/project-template/docs/ai-relay.md`
- `examples/collaboration-system/project-template/docs/ai-collaboration.md`
- `examples/collaboration-system/project-template/docs/ai-workbench.md`
- `examples/collaboration-system/project-template/.ai/README.md`
- `examples/collaboration-system/project-template/.ai/system/ai-ltc-config.json`

Change class:
- Self-Evolving for the template
- Dynamic after being instantiated inside a real target repository

### Layer 3: Runtime Working State

Purpose:
- hold the current active lane state in the target repository
- capture handoff and escalation artifacts
- express current reality rather than ideal architecture

Main files in a target repository:
- `.ai/active-lane/*`
- `.ai/system/*`
- `00_HANDOFF.md`
- `ESCALATION_REQUEST.md`

Change class:
- Dynamic

## v1 Implemented vs v2 Candidate

### Already Implemented In v1

- staged GPT/Qwen operating model
- `A-B-O` lifecycle logic in practical form
- `00_HANDOFF` protocol
- `ESCALATION_REQUEST` protocol
- self-evolving-doc rule for Qwen
- bounded-pass and anti-loop guardrails
- fixed stop phrases and fixed status fields
- Qwen init routing
- centralized resolver config via `.ai/system/ai-ltc-config.json`
- local-first and remote-fallback AI-LTC source policy
- reusable example skeleton

### Candidate For v2 Or Later

- a more explicit named four-layer governance spec as a first-class public artifact
- richer separation between stable framework docs and target-repository governance packs
- more formal workflow transition artifacts between Architect, Builder, and Optimizer phases
- optional automation around init generation, handoff validation, and escalation packaging
- stronger incident-library and case-study structure
- broader public-facing compatibility and governance documents
- token and context optimization rules for long sessions, including quota-aware prompt routing and compression discipline
- a structured-format strategy that clarifies when to use markdown only and when to add YAML, JSON, CSV, or mixed artifacts for machine-readable state
- a language strategy that preserves human readability while minimizing token waste, with explicit rules for English technical payloads versus Chinese human-facing summaries

## Recommended Rule Of Thumb

When deciding where a change belongs:
- if it is about one repository's current state, put it in that repository's `.ai/`
- if it is a reusable framework rule, keep it in the Static layer
- if it is a reusable improvement learned from repeated practice, put it in the Self-Evolving layer and version it

## Short Summary

- Static = framework constitution
- Dynamic = live project state
- Self-Evolving = framework improvements learned from real use
- Layer 0 defines common contract
- Layer 1 defines role behavior
- Layer 2 defines reusable repository skeleton
- Layer 3 carries live runtime state
