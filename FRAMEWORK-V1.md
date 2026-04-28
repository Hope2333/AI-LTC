# AI-LTC Framework v1

Core logic:
- expensive brain does design
- fast hands do execution
- specialists are called only on demand

Role model:
- architect role = initial structure, boundaries, and irreversible sequencing
- generalist role = default ongoing execution and supervision
- optimizer role = targeted audit or unblock intervention

State-flow reference:
- see `STATE-FLOWS.md` for the explicit `init -> handoff -> execution -> escalation -> optimizer return` route

Lifecycle:
1. Initial phase
   - architect role defines the initial structure
   - defines skeleton, interfaces, folders, lane docs
   - must leave `00_HANDOFF.md`
   - exits after the handoff
2. Middle phase
   - generalist role owns day-to-day execution
   - owns supervision, evaluation, and execution by default
   - may update docs as reality changes
   - should not invoke optimizer/architect intervention unless escalation conditions are met
3. Late / exception phase
   - optimizer role appears as bounded auditor or unblocker
   - reads `ESCALATION_REQUEST.md`
   - performs targeted intervention
   - exits after the fix or audit

Mandatory micro-controls:
- Handoff protocol
  - architect must leave `00_HANDOFF.md`
- Escalation trigger
  - generalist role uses `@ARCHITECT_HELP`
  - generalist role writes `ESCALATION_REQUEST.md`
- Self-evolving docs
  - active operator may update lane/framework docs
  - add a note:
    - `// Updated by operator on YYYY-MM-DD: <reason>`

Architecture layering:
- Static = reusable framework constitution
- Dynamic = live target-repository state
- Self-Evolving = framework pieces improved from real use
- see `ARCHITECTURE-LAYERS.md` for the full mapping

Default policy:
- for ongoing repos, default to the generalist role first
- use architect/optimizer roles only when:
  - you explicitly want it
  - the project is still at an early architecture/bootstrap stage
  - the active generalist raises a real escalation
