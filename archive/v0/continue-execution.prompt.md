Apply `shared-repo-contract.prompt.md` first.

You are resuming an already-active lower-cost execution session.

Do not treat this as a fresh planning turn.
Resume from:
- the latest assistant message in the current conversation
- the active `.ai` lane docs resolved through `docs/ai-relay.md`
- the latest local branch / commit / workflow state you can verify quickly

Primary goal:
- continue the current batch from the latest confirmed state
- keep momentum without reopening already-settled analysis
- stay inside the active lane and current phase unless fresh evidence clearly disproves them

Execution rules:
- do not restart from broad repo analysis unless the handoff is clearly stale or contradicted
- do not restate the whole plan if the current batch is already known
- derive the current layered TODO state quickly:
  - lane goal
  - current batch
  - immediate next tasks
- pick the critical-path next step and execute it
- prefer a narrow GitHub Actions proof path over a broad local build loop when both can prove the same point
- keep local builds short and scoped; use them mainly for sanity checks, blocker isolation, and minimal repros
- update the active handoff docs after any meaningful state change

Bounded-pass rule:
- treat this continuation as one bounded pass
- do at most 5 to 8 meaningful steps before handing back, unless a review gate happens earlier
- if the same blocker appears twice without new evidence, stop
- if there is no meaningful new evidence, stop
- if a wait loop produces no new state after 2 safe checks, stop

Review gates:
- new first blocker
- first green build for the current batch
- PR readiness / merge judgment point
- phase exit criterion reached or disproved
- bounded pass exhausted

Structured handback contract:
- `Status`
- `Decision`
- `Current Branch`
- `Current Head Commit`
- `Layered TODO State`
- `Latest Workflow`
- `Blocker Or Green Status`
- `Local Verification`
- `Next Action`
- `Docs Updated`
- `Stop Reason`

Allowed `Stop Reason` values:
- `STOP_NO_NEW_EVIDENCE`
- `STOP_REPEATED_BLOCKER`
- `STOP_BOUNDED_PASS_EXHAUSTED`
- `STOP_WAIT_NO_PROGRESS`
- `STOP_REVIEW_GATE_REACHED`

Language contract:
- use English for relay-file updates, task instructions, commands, and technical evidence
- use Chinese for the final summary to the human
- keep file paths, commit IDs, workflow IDs, and code identifiers in original English form

Do not:
- start a new phase on your own
- broaden scope casually
- recursively restate the same plan
- default to long local builds when a narrow GitHub Actions proof path already exists
- leave the handoff docs stale
