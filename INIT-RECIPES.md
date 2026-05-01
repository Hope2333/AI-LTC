# INIT-RECIPES

This document standardizes how AI-LTC init should behave in real repositories.
It defines when init is required, when the initial skeleton should be copied, and how to distinguish between fresh init, update, upgrade, and resume.

## Core Init Modes

### 1. Fresh Init

Use when:
- `.ai/system/init-status.md` does not exist
- `.ai/system/ai-ltc-config.json` does not exist
- the target repository has never used AI-LTC before

Required actions:
1. ask for the human-facing output language first
2. set init status to `INITING`
3. determine AI-LTC source mode and source location
4. copy the initial skeleton into the target repository
5. write `.ai/system/ai-ltc-config.json`
6. classify project state
7. choose the next operator and prompt stack
8. promote init status to `VERSION`

Skeleton rule:
- copy the full initial skeleton when the target repository does not already contain a usable AI-LTC relay surface

Expected result:
- target repository becomes AI-LTC-aware
- next work can move to normal execution or architect bootstrap

### 2. Resume Init

Use when:
- `.ai/system/init-status.md` exists
- status is `INITING`
- a previous init was interrupted or killed

Required actions:
1. read `.ai/system/init-status.md`
2. resume from the last unfinished init step
3. do not restart blindly unless the state is corrupted
4. confirm whether the skeleton copy already happened
5. finish unresolved questionnaire/config tasks
6. promote init status to `VERSION` when done

Skeleton rule:
- copy only the missing skeleton parts if the copy was partial
- do not overwrite already customized target-repository files without a good reason

Expected result:
- interrupted init becomes complete without destroying local progress

### 3. Update

Use when:
- AI-LTC is already installed
- init status is `VERSION`
- current framework version is compatible
- the repository needs refreshed templates, prompts, or docs but not a migration jump

Required actions:
1. compare current local AI-LTC framework version with target repository expectations
2. refresh only compatible files or recommended docs
3. preserve target-specific `.ai/active-lane/*` state
4. do not reset customized lane history

Skeleton rule:
- update only the shared skeleton surface that is safe to refresh
- never overwrite active target-repository working state as if it were a template

Expected result:
- target repository stays on the same major/minor framework track
- no unnecessary migration churn

### 4. Upgrade

Use when:
- AI-LTC is already installed
- init status is `VERSION`
- framework expectations changed materially, such as `v0 -> v1`
- new resolver/state model or routing model must be introduced

Required actions:
1. classify the current installed version
2. determine the migration target version
3. preserve target-specific working state
4. update the framework-facing files that define the new operating model
5. write new config fields such as resolver, language, or state-transition fields
6. leave a clear next action after the upgrade

Skeleton rule:
- upgrade the skeleton selectively, not by blind replacement
- preserve target-specific lane docs, local history, and live state unless they are invalid under the new version

Expected result:
- target repository lands on the new framework version without losing live context

## Status File Rule

Use `.ai/system/init-status.md` as the first init control file.

Standard values:
- `UNINITIALIZED`
  - AI-LTC not initialized yet
- `INITING`
  - init in progress
- `INSTALLED`
  - installed and versioned; next action is update, upgrade, or normal execution

Recommended fields:
- `Status`
- `Decision`
- `Stop Reason`
- `Next Action`
- optional `Current Version`
- optional `Target Version`
- optional `Last Completed Step`

## Skeleton Copy Strategy

### Copy Full Skeleton

Do this only when:
- the repository has no AI-LTC relay surface at all
- the current repository is clearly a fresh target
- the current repository is so chaotic that a new skeleton is safer than patching missing pieces

Typical copied items:
- `AGENTS.md` template or repository AI guide equivalent
- `docs/ai-relay.md`
- `docs/ai-collaboration.md`
- `docs/ai-workbench.md`
- `.ai/README.md`
- `.ai/system/ai-ltc-config.json`
- `.ai/system/init-status.md`
- active-lane placeholder docs
- `00_HANDOFF.md` and `ESCALATION_REQUEST.md` placeholders when appropriate

### Copy Partial Skeleton

Do this when:
- the repository already has a partial relay surface
- the repository needs only missing files or new framework features
- the repository already has customized lane state that should not be overwritten

Typical partial additions:
- new config fields
- new strategy docs
- new template files
- missing `.ai/system/*` files

### Do Not Recopy Blindly

Do not do this when:
- active lane docs already contain real state
- `00_HANDOFF.md` or `ESCALATION_REQUEST.md` contain real current context
- the repository is already on the target framework version and only needs normal execution

## Language Handling Rule

### Output Language
- ask for the human-facing output language first when it is not configured yet
- store it in `.ai/system/ai-ltc-config.json` as `human_summary_language`

### Input Language
- working language remains English
- human input language may be:
  - fixed to one language
  - multi-language
  - `auto-detect`
- store it in `.ai/system/ai-ltc-config.json` as `human_input_language_policy`

### Practical Default
- `working_language`: `English`
- `human_summary_language`: chosen during init
- `human_input_language_policy`: `auto-detect`

## Decision Table

- No config + no status file: `Fresh Init`
- `Status: INITING`: `Resume Init`
- `Status: INSTALLED` + same framework line: `Update`
- `Status: INSTALLED` + framework jump or migration needed: `Upgrade`
- `Status: INSTALLED` + no framework action needed: skip init and continue normal execution

## Guardrails

- do not overwrite live target-repository state as if it were still a template
- ask output language first before other human-facing language questions
- allow input language auto-detect when the operator does not want to lock it
- keep working language English even when summaries are not English
- when in doubt, preserve live lane state and upgrade only the framework surface
- if the target repository already has a typed local config model, add AI-LTC-required fields compatibly instead of force-replacing the whole schema
- if the target repository has cross-package imports, add or refresh a composition contract check for dependencies, exports, and imports before declaring the system green
- if the target repository has historical `summary`, `final`, `report`, or `100% complete` docs, explicitly mark the current source-of-truth docs so lower-cost AIs do not plan from stale closeout files
- a deployment is not complete if prompt/template files exist but `.ai/README.md`, `docs/ai-relay.md`, or `docs/ai-collaboration.md` are missing
- after init completes, run the framework-check phase to establish a version baseline
- after init completes, run the task-routing phase to establish the default task type and skill context for the project

## Short Summary

- `Fresh Init` = first-time install
- `Resume Init` = continue interrupted init
- `Update` = same framework line, lighter refresh
- `Upgrade` = framework migration with preservation
- output language should be asked first
- input language may be auto-detected
- copy the skeleton only as much as the repository actually needs
