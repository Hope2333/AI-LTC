# INIT-QWEN

Purpose:
- this document is for `Qwen 3.5 Plus` at init time, after the framework is deployed but before normal execution begins
- Qwen should use it to classify the project state and recommend the next model + prompt combination

Project-state classification:
- `greenfield`
  - brand new project
  - architecture not settled
  - lane structure not established
- `midstream`
  - project already has structure
  - a lane exists or can be inferred
  - execution can begin with bounded clarification
- `chaotic`
  - docs, lane state, ownership, or architecture are inconsistent
  - relay quality is poor
  - a cleanup or architecture reset may be needed before fast execution

Default recommendation logic:
- if `greenfield`:
  - recommend GPT first with `gpt-bootstrap-architect.prompt.md`
  - require `00_HANDOFF.md`
  - then hand off to Qwen
- if `midstream`:
  - recommend Qwen first with `qwen-generalist-autopilot.prompt.md`
  - if ongoing checkpoints are needed, add `qwen-supervisory-generalist.prompt.md`
- if `chaotic`:
  - recommend a short Qwen-led cleanup / classification pass first
  - if the cleanup reveals architecture-level uncertainty, trigger `@ARCHITECT_HELP`
  - then use `gpt-optimizer-auditor.prompt.md`

Expected Qwen init output:
- `Status`
- `Decision`
- `Project State`
- `Why This State`
- `Recommended Model`
- `Recommended Prompt Stack`
- `Need GPT Now`
- `Next Action`
- `Stop Reason`

Prompt stack examples:
- greenfield:
  - `shared-repo-contract.prompt.md`
  - `gpt-bootstrap-architect.prompt.md`
  - `00_HANDOFF.template.md`
- midstream:
  - `shared-repo-contract.prompt.md`
  - `qwen-generalist-autopilot.prompt.md`
- midstream with active checkpoint need:
  - `shared-repo-contract.prompt.md`
  - `qwen-supervisory-generalist.prompt.md`
- chaotic with real architecture trouble:
  - `shared-repo-contract.prompt.md`
  - `qwen-supervisory-generalist.prompt.md`
  - `ESCALATION_REQUEST.template.md`
  - `gpt-optimizer-auditor.prompt.md`

Guardrails:
- Qwen should not recommend GPT just because GPT is stronger
- Qwen should recommend GPT only when:
  - the project is still pre-architecture
  - or the current problem is clearly architecture-heavy
  - or a true escalation exists
