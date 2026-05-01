# AI-LTC Todo Tasks — Historical Runtime And Experimental Alignment

**Created**: 2026-04-06
**Last Updated**: 2026-05-02
**AI-LTC Version**: v1.5.15
**Line**: Experimental framework, evaluation, bridge validation, and historical runtime alignment

---

## Task 1: Fix OpenCode Zen Upstream Throttle Blocking

**Priority**: High
**Status**: External Runtime Follow-Up
**Description**: The "Upstream error from Alibaba: Request rate increased too quickly" message blocks ULW-Loop and Agent tasks. This is NOT a real API error — it's an upstream routing text message that should trigger forced retry at 3s intervals, NOT model fallback.

### Subtasks

| # | Subtask | Status | File |
|---|---------|--------|------|
| 1.1 | Add upstream throttle patterns to RETRYABLE_ERROR_PATTERNS | ✅ Done | `constants.ts` |
| 1.2 | Add upstream throttle pattern to AUTO_RETRY_PATTERNS | ✅ Done | `error-classifier.ts` |
| 1.3 | Add `upstream_throttle` error type to `classifyErrorType()` | ✅ Done | `error-classifier.ts` |
| 1.4 | Implement `handleUpstreamThrottleRetry()` with 3s interval, 30 max retries | ✅ Done | `message-update-handler.ts` |
| 1.5 | Add upstream throttle detection before normal fallback flow | ✅ Done | `message-update-handler.ts` |
| 1.6 | Add test cases for upstream throttle retry | ⏭ External follow-up | upstream runtime repo |
| 1.7 | Build and verify TypeScript compilation | ⏭ External follow-up | upstream runtime repo |

### Verification Criteria

- [ ] Upstream runtime repo proves throttle error triggers retry on the same model at 3s intervals
- [ ] Upstream runtime repo proves max 30 retries before normal fallback resumes
- [ ] Upstream runtime repo proves no model fallback occurs during upstream throttle retry
- [ ] Upstream runtime TypeScript compilation passes with no errors
- [ ] Upstream runtime existing tests still pass

**AI-LTC boundary**: The implementation files listed above are not present in this repository. AI-LTC tracks the requirement and verification criteria, but the executable tests/build belong in the upstream runtime repository.

---

## Task 2: Rename AI-LTC Experimental Adapter Line

**Priority**: Medium
**Status**: Complete for Experimental
**Description**: Rename the provider-specific experimental adapter line to remove preview-era wording.

### Subtasks

| # | Subtask | Status | File |
|---|---------|--------|------|
| 2.1 | Update provider adapter name and version | ✅ Done | provider adapter config |
| 2.2 | Update BRANCH-GOVERNANCE.md line name | ✅ Done | `BRANCH-GOVERNANCE.md` |
| 2.3 | Bump VERSION to v1.5.15 | ✅ Done | `VERSION` |
| 2.4 | Bump ai-ltc-config.template.json version | ✅ Done | `ai-ltc-config.template.json` |
| 2.5 | Align consumer registry expected versions | ✅ Done | `cross-repo-registry.json` |
| 2.6 | Update README.md version history | ✅ Done | `README.md` |
| 2.7 | Commit and push Experimental branch | ✅ Done | git |
| 2.8 | Tag Experimental provider naming checkpoint | ✅ Done | `v1.5.15-exp-provider-naming-boundary` |

### Verification Criteria

- [x] Preview-era provider line wording updated in active docs
- [x] VERSION file shows v1.5.15
- [x] Config template shows v1.5.15
- [x] Registry expects v1.5.15 for consumer repos
- [x] Current Experimental branch changes committed
- [x] Experimental branch pushed to GitHub
- [x] Experimental checkpoint tag pushed to GitHub

---

## Task 3: Update AI-LTC Todo Tasks Document

**Priority**: Low
**Status**: Current
**Description**: This document itself — tracking historical task state without contradicting current repository facts.

### Subtasks

| # | Subtask | Status | File |
|---|---------|--------|------|
| 3.1 | Create Todo Tasks document | ✅ Done | This file |
| 3.2 | Commit Todo Tasks document | ✅ Done | git |
| 3.3 | Refresh tracker for v1.5.15, pushed CI, and external-runtime boundaries | ✅ Done | This file |

---

## Task 4: 2026-04-28 Experimental Evaluation v0.2 Alignment

**Priority**: High
**Status**: Complete
**Description**: Convert the 2026-04-28 Experimental direction into concrete schema, mapping, evidence, and local validation surfaces.

### Subtasks

| # | Subtask | Status | File |
|---|---------|--------|------|
| 4.1 | Add evaluation v0.2 schema files | ✅ Done | `evaluation/schemas/*.schema.yaml` |
| 4.2 | Add legacy prompt mapping | ✅ Done | `prompts/_mapping/legacy-to-role-phase-adapter.md` |
| 4.3 | Update README / README.zh with Experimental current state | ✅ Done | `README.md`, `README.zh.md` |
| 4.4 | Extend model/tool/task/result registries with v0.2 fields and seeds | ✅ Done | `evaluation/*/registry.yaml`, `evaluation/results/2026-04.yaml` |
| 4.5 | Add evaluation registry validator | ✅ Done | `scripts/evaluation_validator.py` |
| 4.6 | Add prompt mapping validator | ✅ Done | `scripts/prompt_mapping_validator.py` |
| 4.7 | Add freshness and field-shape validation | ✅ Done | `scripts/evaluation_validator.py` |
| 4.8 | Add CI workflow for `make check` | ✅ Done | `.github/workflows/check.yml` |
| 4.9 | Split CI checks into diagnosable validator steps | ✅ Done | `.github/workflows/check.yml` |
| 4.10 | Stabilize CI freshness validation timezone | ✅ Done | `.github/workflows/check.yml` |
| 4.11 | Move GitHub Actions JavaScript actions to Node 24-compatible v6 lines | ✅ Done | `.github/workflows/check.yml` |

### Verification Criteria

- [x] `make validate-evaluation` passes
- [x] `make validate-prompts` passes
- [x] `make validate-provider-naming` passes
- [x] `make validate-ts-imports` passes
- [x] `make validate-config-registry` passes
- [x] `make check` passes
- [x] `git diff --check` passes
- [x] CI runs all `make check` components
- [x] GitHub Actions check-run succeeds with zero annotations

---

## Task 5: 2026-05-02 Execution Environment Evaluation Alignment

**Priority**: High
**Status**: Complete
**Description**: Apply the 2026-05-02 update documents by treating coding tools as execution environments with surfaces, harness features, permission models, freshness, and evidence.

### Subtasks

| # | Subtask | Status | File |
|---|---------|--------|------|
| 5.1 | Add explicit `freshness_status` schema and validator support | ✅ Done | `evaluation/schemas/*.schema.yaml`, `scripts/evaluation_validator.py` |
| 5.2 | Refresh P0 tool execution-environment records | ✅ Done | `evaluation/tools/registry.yaml` |
| 5.3 | Refresh P0 model observation dates and freshness | ✅ Done | `evaluation/models/registry.yaml` |
| 5.4 | Add 2026-05 evidence result for the execution-environment direction | ✅ Done | `evaluation/results/2026-05.yaml` |
| 5.5 | Update public evaluation docs for explicit freshness status | ✅ Done | `README.md`, `README.zh.md`, `docs/EVALUATION-SCHEMA.md`, `evaluation/README.md` |

### Verification Criteria

- [x] `make validate-evaluation` passes with 19 results
- [x] `make validate-provider-naming` passes
- [x] `make check` passes
- [x] `git diff --check` passes

---

## Current Repository Blockers

| ID | Description | Impact | Workaround |
|----|-------------|--------|------------|
| None | — | — | — |

## External Follow-ups

1. Complete Task 1.6-1.7 in the upstream runtime repo that owns `constants.ts`, `error-classifier.ts`, `message-update-handler.ts`, and `index.test.ts`.
2. Decide separately whether a main-branch release tag is needed. Experimental is already committed, tagged for the provider-naming boundary checkpoint, pushed, and CI-verified.

## Current AI-LTC Verification Snapshot

- Local `make check`: passes, including all validators and 36 bridge smoke checks.
- Local `git diff --check`: passes.
- GitHub Actions `check` on `Experimental`: succeeds with zero annotations.
- Latest pushed commit at the time of this refresh: `ba89554 Refresh tracker against verified Experimental state`.

## Historical Commit Note

- This document is a historical tracker. Use `git log` and GitHub Actions for current commit and CI evidence.

---

## Notes

- Upstream throttle retry uses **same model** (no fallback), 3s cooldown, 30 max attempts
- After 30 retries, falls back to normal model fallback flow
- This is specific to OpenCode Zen's Alibaba routing layer, not OpenRouter
- The error message pattern: `"Upstream error from Alibaba: Request rate increased too quickly. To ensure system stability, please adjust your client logic to scale requests more smoothly over time."`
