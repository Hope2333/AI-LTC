# UPGRADE-MATRIX

This document standardizes how AI-LTC should classify and execute framework updates across repositories.
It is the companion to `INIT-RECIPES.md`.
`INIT-RECIPES.md` explains the operational steps.
`UPGRADE-MATRIX.md` explains the decision table, compatibility intent, and release discipline.

## Core Decision Matrix

| Current State | Installed Version | Target Version | Recommended Mode | Skeleton Action | Notes |
| --- | --- | --- | --- | --- | --- |
| `NULL` | none | any v1 | `Fresh Init` | full copy | repository has no usable AI-LTC surface |
| `INITING` | partial | same target | `Resume Init` | partial or none | continue interrupted init, do not restart blindly |
| `VERSION` | same major/minor line | newer patch/minor on same line | `Update` | partial refresh | preserve live lane state |
| `VERSION` | older line | newer incompatible line | `Upgrade` | selective replacement | preserve live lane state, migrate config fields |
| `VERSION` | same line and no framework delta needed | same line | `Normal Execution` | none | skip init/update logic entirely |

## Compatibility Intention

### Safe Update

Treat as `Update` when:
- the target repository is already on the same major framework line
- resolver fields are already compatible
- prompt routing model is unchanged
- only docs, templates, or lightweight tooling need refresh

Examples:
- `v1.4.1 -> v1.5.0`
- `v1.6.0 -> v1.7.0`

### Real Upgrade

Treat as `Upgrade` when:
- a resolver or init model changes materially
- state files gain new required semantics
- the framework crosses a major line
- a previous installed line would leave the target repo ambiguous or partially broken

Examples:
- `v0 -> v1.x`
- future `v1.x -> v2.0.0-rc1`

## Skeleton Upgrade Rules

### Full Skeleton Copy

Allowed only when:
- no AI-LTC relay surface exists
- the repository is effectively fresh
- the existing state is so incomplete that preservation provides no value

### Selective Skeleton Upgrade

Preferred when:
- the target repo already has live `.ai/active-lane/*`
- `00_HANDOFF.md` or `ESCALATION_REQUEST.md` contain real current state
- only framework scaffolding needs refresh

Typical selective updates:
- prompt templates
- new strategy docs
- new config fields
- new validator tools
- new example guidance

### Never Blindly Replace

Never blindly replace:
- live active-lane docs
- customized project relay files
- real handoff or escalation files
- project-specific local-only state

## Version Signals

Use these signals to decide what to do:
- `.ai/system/init-status.md`
- `.ai/system/ai-ltc-config.json`
- `framework_version` inside the resolver config
- optional current installed version markers
- actual presence of relay/docs skeleton files

## Upgrade Validator Expectations

A repository is upgrade-ready when:
- init status is parseable
- resolver config is valid
- working language is `English`
- summary/input language policy is explicit
- the framework version is present
- the repository can be classified into exactly one of:
  - `Fresh Init`
  - `Resume Init`
  - `Update`
  - `Upgrade`
  - `Normal Execution`

## Release Discipline

### Before v2

If AI-LTC needs a major-line cut:
- do not jump straight to `v2.0.0`
- cut `v2.0.0-rc1` first
- validate at least one real repository and the example template
- promote to `v2.0.0` only after the rc line is stable

### Why

- major changes should not first appear as irreversible stable tags
- the framework is long-horizon infrastructure, not a throwaway prompt bundle
- `-rcX` gives room to test state migration, upgrade tooling, and compatibility assumptions

## Practical Examples

### Example 1: Fresh Target Repo

- current status: no `.ai/system/` files
- target framework: `v1.7.0`
- result: `Fresh Init`

### Example 2: Interrupted Install

- current status: `INITING`
- resolver config exists but handoff not complete
- result: `Resume Init`

### Example 3: Existing v1 Repo, New Tooling

- current status: `VERSION`
- installed line: `v1.6.0`
- target line: `v1.7.0`
- result: `Update`

### Example 4: Future Major Line

- current status: `VERSION`
- installed line: `v1.9.x`
- target line: `v2.0.0-rc1`
- result: `Upgrade`

## Short Summary

- `Fresh Init` = no framework yet
- `Resume Init` = interrupted install
- `Update` = same line, lighter refresh
- `Upgrade` = framework migration
- `Normal Execution` = no framework action needed
- major cuts should go through `v2.0.0-rcX` before `v2.0.0`
