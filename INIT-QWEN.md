# INIT-QWEN

Purpose:
- this document is for `Qwen 3.5 Plus` at init time, after the framework is deployed but before normal execution begins
- Qwen should use it to classify the project state, confirm the AI-LTC source resolver, and recommend the next model + prompt combination
- for `v0 -> v1` upgrades, treat this init step as a semi-required migration pass

When init is required:
- the project is a fresh AI-LTC deployment
- the project is upgrading from `v0` to `v1`
- `.ai/system/ai-ltc-config.json` does not exist
- `.ai/system/ai-ltc-config.json` exists but is incomplete, stale, or points to a missing source

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
- `local_path`
  - AI-LTC is available as a local directory on the same machine
- `git_repo`
  - AI-LTC should be resolved from a Git repository URL + ref
- `cloud_reference`
  - AI-LTC is not mounted locally; prompts are referenced through a cloud repo or mirrored source of truth

Default source preference:
- prefer `local_path` when a healthy local AI-LTC checkout exists
- use `git_repo` as the fallback canonical remote source
- the default remote should be `https://github.com/Hope2333/AI-LTC` unless the user overrides it
- allow Qwen to refresh the local checkout from the remote only when the local copy is missing, stale, or required for the current task

Init questionnaire expectations:
- keep the intake small: 3 to 5 answers
- ask only for:
  - source mode
  - local root or repo URL/ref when applicable
  - project state
  - default operator model
  - whether GPT bootstrap is needed now
  - optionally whether Qwen may refresh the local AI-LTC checkout from the remote when required
- store answers in one place, not across many lane docs

Resolver rule:
- do not hardcode AI-LTC filesystem paths directly into multiple project prompts or `.ai` docs
- write a single resolver config at `.ai/system/ai-ltc-config.json`
- other docs should point to the resolver, not to the raw path
- store both the preferred local source and the fallback remote source in the resolver when available

Expected init artifacts:
- `.ai/system/ai-ltc-config.json`
- `.ai/system/init-status.md`
- optionally `.ai/system/model-routing.md`

Default recommendation logic:
- if `greenfield`:
  - recommend GPT first with `gpt-bootstrap-architect.prompt.md`
  - require `00_HANDOFF.md`
  - then hand off to Qwen
- if `midstream`:
  - recommend Qwen first with `qwen-generalist-autopilot.prompt.md`
  - if ongoing checkpoints are needed, add `qwen-supervisory-generalist.prompt.md`
- if `chaotic`:
  - recommend a short Qwen-led cleanup / classification pass first
  - if the cleanup reveals architecture-level uncertainty, trigger `@ARCHITECT_HELP`
  - then use `gpt-optimizer-auditor.prompt.md`

Expected Qwen init output:
- `Status`
- `Decision`
- `Project State`
- `AI-LTC Source Mode`
- `Resolver Config Status`
- `Why This State`
- `Recommended Model`
- `Recommended Prompt Stack`
- `Need GPT Now`
- `Next Action`
- `Stop Reason`

Prompt stack examples:
- greenfield:
  - `shared-repo-contract.prompt.md`
  - `gpt-bootstrap-architect.prompt.md`
  - `00_HANDOFF.template.md`
- midstream:
  - `shared-repo-contract.prompt.md`
  - `qwen-generalist-autopilot.prompt.md`
- midstream with active checkpoint need:
  - `shared-repo-contract.prompt.md`
  - `qwen-supervisory-generalist.prompt.md`
- chaotic with real architecture trouble:
  - `shared-repo-contract.prompt.md`
  - `qwen-supervisory-generalist.prompt.md`
  - `ESCALATION_REQUEST.template.md`
  - `gpt-optimizer-auditor.prompt.md`

Guardrails:
- Qwen should not recommend GPT just because GPT is stronger
- Qwen should recommend GPT only when:
  - the project is still pre-architecture
  - or the current problem is clearly architecture-heavy
  - or a true escalation exists
- Qwen should not spray absolute AI-LTC paths into multiple docs
- if the source mode is unresolved, finish resolver setup before normal execution starts
