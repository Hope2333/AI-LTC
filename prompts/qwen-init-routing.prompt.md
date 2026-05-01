Compatibility entrypoint for the legacy init-routing prompt.

Apply `shared-repo-contract.prompt.md` first.
Read `INIT-OPERATOR.md`.
Read `AI-LTC-INIT-QUESTIONNAIRE.template.md`.
Apply `prompts/phases/init.prompt.md`.

Use this file only when an existing workflow still references the legacy filename.
For new integrations, call the init phase prompt directly.

Required behavior:
- ask for the human-facing output language first when it is not configured
- assess project state as `greenfield`, `midstream`, or `chaotic`
- assess source mode as `folder`, `git_repo`, or `cloud_reference`
- recommend the next role and prompt stack
- decide whether architecture help is needed now
- recommend writing `.ai/system/ai-ltc-config.json` when config is missing
- prefer local framework source first and record remote fallback when both are possible
- update `.ai/system/init-status.md` through `UNINITIALIZED`, `INITING`, or `INSTALLED`

Structured output contract:
- `Status`
- `Decision`
- `Init State`
- `Project State`
- `AI-LTC Source Mode`
- `Resolver Config Status`
- `Language Policy`
- `Skeleton Status`
- `Why This State`
- `Recommended Role`
- `Recommended Prompt Stack`
- `Need Architecture Help Now`
- `Next Action`
- `Stop Reason`
