# Role Quick Reference

Use this file when you want the shortest possible reminder of the v1 framework.

## Default Rule

- Qwen is the default ongoing operator
- GPT is invoked only for bootstrap architecture or targeted optimization/audit

## Which Role To Use

- new project, blank repo, or architecture not settled:
  - GPT architect
  - prompt:
    - `prompts/shared-repo-contract.prompt.md`
    - `gpt-bootstrap-architect.prompt.md`

- normal project execution:
  - Qwen generalist
  - prompt:
    - `prompts/shared-repo-contract.prompt.md`
    - `qwen-generalist-autopilot.prompt.md`

- normal checkpoint / sequencing / lane review:
  - Qwen supervisory generalist
  - prompt:
    - `prompts/shared-repo-contract.prompt.md`
    - `qwen-supervisory-generalist.prompt.md`

- architecture deadlock, repeated blocker, hard refactor, or audit:
  - GPT optimizer / auditor
  - prompt:
    - `prompts/shared-repo-contract.prompt.md`
    - `gpt-optimizer-auditor.prompt.md`
  - only after:
    - `@ARCHITECT_HELP`
    - `ESCALATION_REQUEST.md`

## Required Support Files

- GPT hands off with `00_HANDOFF.md`
- Qwen escalates with `ESCALATION_REQUEST.md`

## Anti-Patterns

- do not keep GPT hovering over normal execution
- do not wake GPT for ordinary bounded implementation work
- do not skip `00_HANDOFF.md` after GPT bootstrap
- do not escalate without a summarized blocker
