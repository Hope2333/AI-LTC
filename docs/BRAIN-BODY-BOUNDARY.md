# Brain / Body Boundary

Canonical iter1 design doc: `docs/AI-LTC-vs-OML-BOUNDARY.md`.

## Purpose

Clarify what belongs in AI-LTC versus oh-my-litecode as the two projects continue to evolve together.
This file is the short operational summary; the full iter1 write-up lives in `docs/AI-LTC-vs-OML-BOUNDARY.md`.

## Boundary Summary

| Layer | AI-LTC | oh-my-litecode |
|---|---|---|
| Core role | Brain | Body |
| Owns | state machine, phase semantics, recovery logic, evaluation interpretation, routing principles | tool execution, session runtime, plugin loading, hooks, MCP access, worker lifecycle |
| Stores | durable framework rules, dated evaluation records, abstraction docs | runtime evidence, execution artifacts, session state, platform-specific integration details |
| Must not do | absorb tool-execution plumbing | absorb orchestration policy or phase authority |

## AI-LTC Responsibilities

- define role and phase abstractions
- define protocol and recovery rules
- define evaluation schema and freshness windows
- explain how evidence changes routing or governance
- promote stable conclusions back into the framework layer

## OML Responsibilities

- run tools and external CLIs
- host hooks, workers, sessions, and plugin mechanics
- collect execution evidence
- adapt platform differences
- expose body capabilities to the Brain

## Hand-Off Flow

```text
OML runs the task and collects evidence
-> AI-LTC records the result in dated evaluation form
-> AI-LTC updates routing or governance when the result becomes stable
```

## Duplication To Avoid

- AI-LTC should not embed CLI-specific execution heuristics that belong in OML
- OML should not become the owner of phase semantics or branch governance
- both projects should not maintain separate competing routing truths

## Placement Rule

If a change answers "how should the system think or decide?", prefer AI-LTC.
If a change answers "how does the system run, hook, or call a tool?", prefer OML.
