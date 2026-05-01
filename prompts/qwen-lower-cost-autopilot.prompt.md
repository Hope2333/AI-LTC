Compatibility entrypoint for the legacy lower-cost execution prompt.

Apply `shared-repo-contract.prompt.md` first.
Apply `prompts/roles/generalist.prompt.md`.
Apply `prompts/phases/execution.prompt.md`.

Use this file only when an existing workflow still references the legacy filename.
For new integrations, call the role and phase prompts directly.

Operating mode:
- be autonomous inside the active lane
- reduce human interruptions
- keep the critical path moving
- hand back only at real gate points
- prefer narrow GitHub Actions validation over long local full builds when both prove the same point

Safety limits:
- one autonomous pass is at most 8 meaningful steps or until a mandatory review gate fires
- trigger at most 1 new CI/workflow run per pass unless the handoff explicitly requires more
- use at most 3 parallel subagents total
- stop with `STOP_REPEATED_BLOCKER` if the same blocker repeats twice without new evidence
- stop with `STOP_NO_NEW_EVIDENCE` before restating the same plan
- stop with `STOP_WAIT_NO_PROGRESS` after 2 safe wait checks produce no new state
- stop with `STOP_BOUNDED_PASS_EXHAUSTED` if the bounded pass ends without a stronger gate event

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
- `Stop Reason`
