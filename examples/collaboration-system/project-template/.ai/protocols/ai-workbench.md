# AI Workbench

This is the human-facing control panel for AI collaboration in this repository.

## Use This First

If you only want one document to look at before talking to an AI, use this one.

## Current System

- Global relay rules: `.ai/protocols/ai-relay.md`
- AI role split and detailed contracts: `.ai/protocols/ai-collaboration.md`
- Canonical task state: local-only `.ai/state.json`
- Active lane handoff: local-only `.ai/active-lane/ai-handoff.md`
- Active status summary: local-only `.ai/active-lane/status.md`
- Compatibility status summary: local-only `.ai/active-lane/current-status.md`
- Active roadmap: local-only `.ai/active-lane/roadmap.md`
- Legacy architect-to-generalist handoff: `legacy/00_HANDOFF.md`
- Optional generalist-to-architect escalation summary: `ESCALATION_REQUEST.md`

## Stable Protocol Defaults

- In v1, the generalist role is the default ongoing operator.
- Architect and optimizer roles should normally appear only for bootstrap architecture or explicit escalation/optimization work.
- Treat one AI invocation as one bounded pass.
- Prefer narrow GitHub Actions validation over long local full builds when both can prove the same point.
- Keep local builds short and scoped for sanity checks, blocker isolation, and minimal repros.
- Use fixed stop phrases:
  - `STOP_NO_NEW_EVIDENCE`
  - `STOP_REPEATED_BLOCKER`
  - `STOP_BOUNDED_PASS_EXHAUSTED`
  - `STOP_WAIT_NO_PROGRESS`
  - `STOP_REVIEW_GATE_REACHED`
- Prefer fixed fields when the prompt supports them:
  - `Status`
  - `Decision`
  - `Stop Reason`
  - `Next Action`

## Human Control Pattern

- If the project is still at the very beginning, start with the architect role.
- Once the skeleton exists, switch to the generalist role as the default operator.
- Only wake architect or optimizer roles again when:
  - you explicitly want a high-cost audit or redesign
  - the generalist role has emitted `@ARCHITECT_HELP`
