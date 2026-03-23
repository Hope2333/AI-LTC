# AI-LTC Framework v1

Core logic:
- expensive brain does design
- fast hands do execution
- specialists are called only on demand

Role model:
- GPT = architect or optimizer/auditor
- Qwen = default generalist operator

Lifecycle:
1. Initial phase
   - GPT acts as architect
   - defines skeleton, interfaces, folders, lane docs
   - must leave `00_HANDOFF.md`
   - exits after the handoff
2. Middle phase
   - Qwen acts as generalist engineer
   - owns supervision, evaluation, and execution by default
   - may update docs as reality changes
   - should not wake GPT unless escalation conditions are met
3. Late / exception phase
   - GPT appears as optimizer or auditor
   - reads `ESCALATION_REQUEST.md`
   - performs targeted intervention
   - exits after the fix or audit

Mandatory micro-controls:
- Handoff protocol
  - architect must leave `00_HANDOFF.md`
- Escalation trigger
  - Qwen uses `@ARCHITECT_HELP`
  - Qwen writes `ESCALATION_REQUEST.md`
- Self-evolving docs
  - Qwen may update lane/framework docs
  - add a note:
    - `// Updated by Qwen on YYYY-MM-DD: <reason>`

Default policy:
- for ongoing repos, default to Qwen first
- use GPT only when:
  - you explicitly want it
  - the project is still at an early architecture/bootstrap stage
  - Qwen raises a real escalation
