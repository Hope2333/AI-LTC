# AI Relay Protocol

Before substantial work, read:

1. `AGENTS.md`
2. `.ai/protocols/ai-relay.md`
3. `.ai/protocols/ai-collaboration.md` when multiple AIs are collaborating
4. `.ai/system/ai-ltc-config.json` when it exists
5. The area-specific handoff file for the lane you are touching

## Active Lane Registry

- Active lane
  - canonical state: `.ai/state.json`
  - handoff: `.ai/active-lane/ai-handoff.md`
  - status: `.ai/active-lane/status.md`
  - compatibility status: `.ai/active-lane/current-status.md`
  - roadmap: `.ai/active-lane/roadmap.md`

Optional v1 control files:
- legacy root handoff bootstrap: `legacy/00_HANDOFF.md`
- targeted escalation summary: `ESCALATION_REQUEST.md`
- init resolver config: `.ai/system/ai-ltc-config.json`
- init state note: `.ai/system/init-status.md`
- default resolver policy: local AI-LTC first, remote fallback second

The `.ai/` paths listed here are the authoritative active-lane state, and
`.ai/state.json` is first-order when supplemental handoff docs disagree.
Do not put transient AI-LTC handoff, packet, round, or temporary state files
under project `docs/`.

## Standard Stop Phrases

- `STOP_NO_NEW_EVIDENCE`
- `STOP_REPEATED_BLOCKER`
- `STOP_BOUNDED_PASS_EXHAUSTED`
- `STOP_WAIT_NO_PROGRESS`
- `STOP_REVIEW_GATE_REACHED`

## Standard Status Fields

- `Status`
- `Decision`
- `Stop Reason`
- `Next Action`

## Guardrails

- Prefer updating the existing handoff file over creating ad hoc status files.
- `docs/` is for durable project documentation, not private AI working state.
- `.ai/` is the local-only workspace for active AI handoff, status, roadmap, and resolver files.
- Prefer a narrow GitHub Actions proof path over a broad local build loop when both can prove the same point.
- Use local builds mainly for fast sanity checks, blocker isolation, and minimal repros.
- In v1, the generalist role is the default ongoing operator.
- Architect and optimizer roles should normally appear only for bootstrap architecture, explicit optimization, or escalation response.
