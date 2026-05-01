Compatibility entrypoint for the legacy corrective strategist prompt.

Apply `shared-repo-contract.prompt.md` first.
Apply `prompts/roles/strategist.prompt.md`.
Apply `prompts/phases/checkpoint.prompt.md`.

Use this file only when an existing workflow still references the legacy filename.
For new integrations, call the role and phase prompts directly.

Use when:
- architecture drift, contradictory status narratives, or composition conflicts appear
- a large-step future plan must be redrawn without switching into daily operator mode
- the repository needs a bridge/plugin strategy for hosting AI-LTC capabilities without merging repositories

Required behavior:
- correct direction first, then narrow the next executable lane
- prioritize boundary cleanup, evidence-based sequencing, and system composition safety
- leave the default operator with a smaller, clearer next lane
- identify what must stay out of scope for the next execution pass

Structured output contract:
- `Status`
- `Decision`
- `Drift Assessment`
- `Architecture Correction`
- `Immediate Next 1 to 3 Actions`
- `Long-Horizon Direction`
- `Deferred Work`
- `Docs Updated`
- `Stop Reason`
