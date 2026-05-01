# Role Quick Reference

Use this file when you want the shortest possible reminder of the v1 framework.

## Default Rule

- The generalist role is the default ongoing operator
- Architect and optimizer roles are invoked only for bootstrap architecture or targeted optimization/audit

## Which Role To Use

- new project, blank repo, or architecture not settled:
  - architect
  - prompt:
    - `prompts/shared-repo-contract.prompt.md`
    - `prompts/roles/architect.prompt.md`

- normal project execution:
  - generalist
  - prompt:
    - `prompts/shared-repo-contract.prompt.md`
    - `prompts/roles/generalist.prompt.md`

- normal checkpoint / sequencing / lane review:
  - supervisor
  - prompt:
    - `prompts/shared-repo-contract.prompt.md`
    - `prompts/roles/supervisor.prompt.md`

- architecture deadlock, repeated blocker, hard refactor, or audit:
  - optimizer / auditor
  - prompt:
    - `prompts/shared-repo-contract.prompt.md`
    - `prompts/roles/optimizer.prompt.md`
  - only after:
    - `@ARCHITECT_HELP`
    - `ESCALATION_REQUEST.md`

## Required Support Files

- The architect role hands off with `00_HANDOFF.md`
- The active operator escalates with `ESCALATION_REQUEST.md`

## Anti-Patterns

- do not keep architect or optimizer roles hovering over normal execution
- do not wake high-cost roles for ordinary bounded implementation work
- do not skip `00_HANDOFF.md` after architecture bootstrap
- do not escalate without a summarized blocker
