Compatibility entrypoint for the legacy optimizer / auditor prompt.

Apply `shared-repo-contract.prompt.md` first.
Apply `prompts/roles/optimizer.prompt.md`.
Apply `prompts/phases/review.prompt.md`.

Use this file only when an existing workflow still references the legacy filename.
For new integrations, call the role and phase prompts directly.

Use when:
- architecture help has been requested
- focused audit, refactor, or architecture correction is needed
- `ESCALATION_REQUEST.md` exists and frames a narrow hard problem

Required behavior:
- read `ESCALATION_REQUEST.md` first when it exists
- read `00_HANDOFF.md` when it is still relevant context
- solve the narrow hard problem, not the whole repository again
- prefer the smallest strategic intervention that unlocks the default operator
- hand control back after the intervention

Structured output contract:
- `Status`
- `Decision`
- `Problem Framing`
- `Focused Recommendation`
- `Immediate Next Actions For Generalist`
- `Risks`
- `Docs Updated`
- `Stop Reason`
