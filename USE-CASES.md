# Use Cases

AI-LTC is designed for long-horizon AI-assisted software work.

## 1. Brand-New Project

Recommended stack:
- `shared-repo-contract.prompt.md`
- `gpt-bootstrap-architect.prompt.md`
- `00_HANDOFF.template.md`

Why:
- architecture and lane structure do not exist yet
- GPT should define the initial ceiling, then hand off to Qwen

## 2. Midstream Project With Existing Structure

Recommended stack:
- `shared-repo-contract.prompt.md`
- `qwen-init-routing.prompt.md`
- `qwen-generalist-autopilot.prompt.md`

Why:
- the repo already has structure
- Qwen should classify the state and then take over ongoing execution

## 3. Ongoing Delivery / Long Session Work

Recommended stack:
- `shared-repo-contract.prompt.md`
- `qwen-generalist-autopilot.prompt.md`
- optional: `continue-execution.prompt.md`

Why:
- Qwen is the default operator in v1
- bounded passes + relay upkeep are enough for normal progress

## 4. Checkpoint / Lane Review

Recommended stack:
- `shared-repo-contract.prompt.md`
- `qwen-supervisory-generalist.prompt.md`

Why:
- this keeps supervision close to execution cost
- GPT stays out unless the issue is truly architectural

## 5. Chaotic Repository / Poor Docs / Broken Handoff

Recommended stack:
- `shared-repo-contract.prompt.md`
- `qwen-init-routing.prompt.md`
- `qwen-supervisory-generalist.prompt.md`

Fallback:
- if Qwen emits `@ARCHITECT_HELP`, add `ESCALATION_REQUEST.md` and use `gpt-optimizer-auditor.prompt.md`

## 6. Hard Refactor / Repeated Blocker / Architecture Deadlock

Recommended stack:
- `shared-repo-contract.prompt.md`
- `ESCALATION_REQUEST.template.md`
- `gpt-optimizer-auditor.prompt.md`

Why:
- GPT should appear only for narrow high-value intervention

## 7. Public Template Bootstrap For Another Repo

Recommended entry:
- `examples/collaboration-system/README.md`
- `examples/collaboration-system/install-example.md`
- `examples/collaboration-system/bootstrap-checklist.md`
- `examples/collaboration-system/ROLE-QUICK-REFERENCE.md`
