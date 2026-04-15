# AI-LTC vs OML Boundary

## Status

- Iteration: `iter1`
- Purpose: make Brain / Body ownership actionable
- Scope: ownership and placement rules

## Core Framing

- AI-LTC is the Brain
- oh-my-litecode is the Body

The point is not branding. The point is ownership clarity.

## AI-LTC Owns

- state machine and phase semantics
- role abstractions
- routing principles
- recovery rules
- evaluation interpretation
- long-horizon coordination rules
- framework-facing documentation and governance

## OML Owns

- CLI and agent integration
- plugin loading
- hooks
- MCP access
- sessions
- worker lifecycle
- execution evidence capture
- platform-specific runtime details

## Experimental-Only Zone

The following belong in the Experimental lane until stabilized:

- new adapter experiments
- new prompt migration structures
- raw evaluation results
- provider-specific runtime heuristics

## Placement Rules

Ask these questions:

1. Is this about how the system decides, sequences, or interprets?
   - put it in AI-LTC
2. Is this about how the system runs tools, sessions, hooks, or workers?
   - put it in OML
3. Is this still experimental, provider-specific, or under evaluation?
   - keep it in Experimental first

## Duplication To Prevent

- AI-LTC should not become a second plugin runtime
- OML should not become a second orchestration policy engine
- both repos should not keep independent competing memories of the same routing truth

## Handoff Model

```text
OML executes and captures runtime evidence
-> AI-LTC records and interprets evaluation outcomes
-> stable conclusions return to AI-LTC mainline governance
```

## Iteration 1 Success Condition

This boundary is good enough for iter1 if a contributor can decide where a new feature belongs without inventing new philosophy each time.
