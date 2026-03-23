# AI Collaboration Protocol

## Purpose

Use the lower-cost AI for iterative execution and bounded fixes.
Use the higher-cost AI for checkpoints, sequencing, and risk review.

## Role Split

### Supervisory AI

- Owns long-term sequencing and phase boundaries.
- Reviews at meaningful checkpoints.
- Updates roadmap-level documents when priorities change.

### Lower-Cost Execution AI

- Executes the current lane with the smallest correct change.
- Reads the active roadmap and derives:
  - lane goal
  - current batch
  - immediate next tasks
- Prefers a narrow GitHub Actions proof path over a broad local build loop when both can prove the same point.
- Keeps local builds short and scoped.
- Updates handoff docs after every meaningful state change.

## Bounded-Pass Rule

- Treat each execution or supervisory run as one bounded pass.
- If there is no meaningful new evidence after one pass, stop explicitly.
- If the same blocker, recommendation, or wait state appears twice without new evidence, stop and return with the matching stop phrase.

## Message Contract From Lower-Cost AI

When handing back, include:
- `Status`
- `Decision`
- current branch
- current head commit
- current layered TODO state
- latest relevant workflow run and conclusion
- first confirmed blocker or confirmation of green status
- local verification performed
- exact `Next Action`
- which handoff docs were updated
- `Stop Reason`
