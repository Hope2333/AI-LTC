Compatibility entrypoint for the legacy framework-check prompt.

Apply `shared-repo-contract.prompt.md` first.
Apply `prompts/phases/checkpoint.prompt.md`.

Use this file only when an existing workflow still references the legacy filename.
For new integrations, call the phase prompt directly.

Purpose:
- detect whether the AI-LTC framework installed in the target repository is outdated compared to the configured source
- produce a structured advisory so the human or next operator can decide whether to update or upgrade
- do not apply upgrades automatically

Read first:
- `.ai/system/ai-ltc-config.json`
- `.ai/AI-LTC/` when present
- `VERSION.md` or `CHANGELOG.md` when the framework source is a folder copy

Advisory output:
- write or update `.ai/system/framework-update-advisory.md`
- include installed version, latest known version, delta classification, recommended action, checked date, and next check due
- update `last_framework_check` in `.ai/system/ai-ltc-config.json`

Structured output contract:
- `Status`
- `Decision`
- `Installed Version`
- `Latest Known Version`
- `Delta Classification`
- `Recommended Action`
- `New Features Summary`
- `Advisory Written`
- `Config Updated`
- `Stop Reason`
