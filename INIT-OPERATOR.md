# INIT-OPERATOR

Purpose:
- this document is for the active init operator after the framework is deployed but before normal execution begins
- the operator should classify the project state, confirm the AI-LTC source resolver, and recommend the next role / phase / adapter stack
- for `v0 -> v1` upgrades, treat this init step as a semi-required migration pass

Init state model:
- `UNINITIALIZED`
  - init has not been completed
  - the repository needs a full init
- `INITING`
  - init is in progress
  - if the previous init was interrupted, resume instead of restarting blindly
- `INSTALLED`
  - AI-LTC is already installed
  - determine whether the next action is update, upgrade, or normal execution

Init order:
1. ask for the human-facing output language first
2. determine whether the target repository needs the initial skeleton copied or refreshed
3. write or update `.ai/system/init-status.md`
4. write or update `.ai/system/ai-ltc-config.json`
5. continue the rest of init routing and role / adapter selection

When init is required:
- the project is a fresh AI-LTC deployment
- the project is upgrading from `v0` to `v1`
- `.ai/system/ai-ltc-config.json` does not exist
- `.ai/system/ai-ltc-config.json` exists but is incomplete, stale, or points to a missing source
- `.ai/system/init-status.md` is `UNINITIALIZED` or `INITING`

Project-state classification:
- `greenfield`
  - brand new project
  - architecture not settled
  - lane structure not established
- `midstream`
  - project already has structure
  - a lane exists or can be inferred
  - execution can begin with bounded clarification
- `chaotic`
  - docs, lane state, ownership, or architecture are inconsistent
  - relay quality is poor
  - a cleanup or architecture reset may be needed before fast execution

AI-LTC source-mode classification:
- `folder`
  - AI-LTC is available as a local folder copy (default: `.ai/AI-LTC/`)
- `git_repo`
  - AI-LTC should be resolved from a Git repository URL + ref
- `cloud_reference`
  - AI-LTC is not mounted locally; prompts are referenced through a cloud repo or mirrored source of truth

Default source preference:
- prefer `folder` when a healthy local AI-LTC copy exists at `.ai/AI-LTC/`
- use `git_repo` as the fallback canonical remote source
- the default remote should be `https://github.com/Hope2333/AI-LTC` unless the user overrides it
- allow the active operator to refresh the local checkout from the remote only when the local copy is missing, stale, or required for the current task

Init questionnaire expectations:
- keep the intake small: 4 to 6 answers
- ask only for:
  - human-facing summary language first
  - source mode
  - local root or repo URL/ref when applicable
  - project state
  - default operator role/provider
  - whether architect bootstrap is needed now
  - optionally whether the active operator may refresh the local AI-LTC checkout from the remote when required
  - human-input language policy
- store answers in one place, not across many lane docs

Resolver rule:
- do not hardcode AI-LTC filesystem paths directly into multiple project prompts or `.ai` docs
- write a single resolver config at `.ai/system/ai-ltc-config.json`
- other docs should point to the resolver, not to the raw path
- store both the preferred local source and the fallback remote source in the resolver when available
- store the language policy in the resolver config rather than in scattered prompts

Expected init artifacts:
- `.ai/system/ai-ltc-config.json`
- `.ai/system/init-status.md`
- optionally `.ai/system/model-routing.md`
- optionally a copied or refreshed initial skeleton if the target repository did not already contain one

Default recommendation logic:
- if `greenfield`:
  - recommend architect role first with `prompts/roles/architect.prompt.md`
  - require `00_HANDOFF.md`
  - then hand off to the generalist role
- if `midstream`:
  - recommend generalist role first with `prompts/roles/generalist.prompt.md`
  - if ongoing checkpoints are needed, add `prompts/roles/supervisor.prompt.md`
- if `chaotic`:
  - recommend a short generalist/supervisor cleanup and classification pass first
  - if the cleanup reveals architecture-level uncertainty, trigger `@ARCHITECT_HELP`
  - then use `prompts/roles/optimizer.prompt.md`

Expected init output:
- `Status`
- `Decision`
- `Init State`
- `Project State`
- `AI-LTC Source Mode`
- `Resolver Config Status`
- `Skeleton Status`
- `Why This State`
- `Recommended Role`
- `Recommended Prompt Stack`
- `Need Architect Now`
- `Next Action`
- `Stop Reason`

Prompt stack examples:
- greenfield:
  - `shared-repo-contract.prompt.md`
  - `prompts/roles/architect.prompt.md`
  - `prompts/phases/init.prompt.md`
  - `00_HANDOFF.template.md`
- midstream:
  - `shared-repo-contract.prompt.md`
  - `prompts/roles/generalist.prompt.md`
  - `prompts/phases/execution.prompt.md`
- midstream with active checkpoint need:
  - `shared-repo-contract.prompt.md`
  - `prompts/roles/supervisor.prompt.md`
  - `prompts/phases/checkpoint.prompt.md`
- chaotic with real architecture trouble:
  - `shared-repo-contract.prompt.md`
  - `prompts/roles/supervisor.prompt.md`
  - `ESCALATION_REQUEST.template.md`
  - `prompts/roles/optimizer.prompt.md`

Framework awareness:
- run the framework-check prompt at the end of init to establish a baseline
- write the result to `.ai/system/framework-update-advisory.md`
- set `last_framework_check` in `.ai/system/ai-ltc-config.json` to today's date

Guardrails:
- do not recommend architect/optimizer roles just because they are stronger
- recommend architect/optimizer roles only when:
  - the project is still pre-architecture
  - or the current problem is clearly architecture-heavy
  - or a true escalation exists
- do not spray absolute AI-LTC paths into multiple docs
- if the source mode is unresolved, finish resolver setup before normal execution starts
- if init status is `INITING`, resume from the recorded step instead of restarting blindly
- if the target repository lacks the AI-LTC skeleton, copy the initial skeleton before normal init routing continues
