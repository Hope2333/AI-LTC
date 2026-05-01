Compatibility entrypoint for the legacy skill-injector prompt.

Apply `shared-repo-contract.prompt.md` first.
Apply the active role prompt.
Apply the active phase prompt.

Use this file only when an existing workflow still references the legacy filename.
For new integrations, load skills through the current skill system directly.

Purpose:
- load one domain-specific skill context for the current batch
- shape verification strategy, common traps, tool preferences, and output format
- record the active skill in `.ai/system/ai-ltc-config.json` as `active_skill` when that config exists

Available skill contexts:
- `coding`
- `docs`
- `data`
- `infra`
- `research`
- `review`

Structured output contract:
- `Status`
- `Decision`
- `Active Skill`
- `Skill Source`
- `Verification Strategy`
- `Common Traps Noted`
- `Tool Preferences`
- `Output Format`
- `Config Updated`
- `Stop Reason`
