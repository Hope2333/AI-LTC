Compatibility entrypoint for the legacy task-router prompt.

Apply `shared-repo-contract.prompt.md` first.
Apply `prompts/phases/execution.prompt.md`.

Use this file only when an existing workflow still references the legacy filename.
For new integrations, route through the phase prompt and the active skill system directly.

Purpose:
- classify the current batch primary task type before execution begins
- route to the matching skill context
- keep the routing decision explicit so the next operator can verify or override

Task type classification:
- `coding`
- `docs`
- `data`
- `infra`
- `research`
- `review`

Structured output contract:
- `Status`
- `Decision`
- `Task Type`
- `Why This Type`
- `Active Skill`
- `Skill Loaded`
- `Next Action`
- `Stop Reason`
