# AI-LTC Todo Tasks — Upstream Throttle Fix & Qwen3.6-Plus-WITH-OMO Rename

**Created**: 2026-04-06
**AI-LTC Version**: v1.5.14
**Line**: Qwen3.6-Plus-WITH-OMO (formerly Qwen3.6-Plus-Preview-WITH-OMO)

---

## Task 1: Fix OpenCode Zen Upstream Throttle Blocking

**Priority**: High
**Status**: In Progress
**Description**: The "Upstream error from Alibaba: Request rate increased too quickly" message blocks ULW-Loop and Agent tasks. This is NOT a real API error — it's an upstream routing text message that should trigger forced retry at 3s intervals, NOT model fallback.

### Subtasks

| # | Subtask | Status | File |
|---|---------|--------|------|
| 1.1 | Add upstream throttle patterns to RETRYABLE_ERROR_PATTERNS | ✅ Done | `constants.ts` |
| 1.2 | Add upstream throttle pattern to AUTO_RETRY_PATTERNS | ✅ Done | `error-classifier.ts` |
| 1.3 | Add `upstream_throttle` error type to `classifyErrorType()` | ✅ Done | `error-classifier.ts` |
| 1.4 | Implement `handleUpstreamThrottleRetry()` with 3s interval, 30 max retries | ✅ Done | `message-update-handler.ts` |
| 1.5 | Add upstream throttle detection before normal fallback flow | ✅ Done | `message-update-handler.ts` |
| 1.6 | Add test cases for upstream throttle retry | ⏸ Pending | `index.test.ts` |
| 1.7 | Build and verify TypeScript compilation | ⏸ Pending | `npm run build` |

### Verification Criteria

- [ ] Upstream throttle error triggers retry same model at 3s intervals
- [ ] Max 30 retries before falling back to normal model fallback
- [ ] No model fallback occurs during upstream throttle retry
- [ ] TypeScript compilation passes with no errors
- [ ] Existing tests still pass

---

## Task 2: Rename AI-LTC Line to Qwen3.6-Plus-WITH-OMO

**Priority**: Medium
**Status**: In Progress
**Description**: Rename the "Qwen3.6-Plus-Preview-WITH-OMO" line to "Qwen3.6-Plus-WITH-OMO" to reflect that this is the production line, not a preview.

### Subtasks

| # | Subtask | Status | File |
|---|---------|--------|------|
| 2.1 | Update adapter.yaml name and version | ✅ Done | `adapters/qwen36/adapter.yaml` |
| 2.2 | Update BRANCH-GOVERNANCE.md line name | ✅ Done | `BRANCH-GOVERNANCE.md` |
| 2.3 | Bump VERSION to v1.5.14 | ✅ Done | `VERSION` |
| 2.4 | Bump ai-ltc-config.template.json version | ✅ Done | `ai-ltc-config.template.json` |
| 2.5 | Update enve's ai-ltc-config.json version | ✅ Done | `enve/.ai/system/ai-ltc-config.json` |
| 2.6 | Update README.md version history | ⏸ Pending | `README.md` |
| 2.7 | Commit and tag both branches | ⏸ Pending | git |

### Verification Criteria

- [ ] All references to "Qwen3.6-Plus-Preview-WITH-OMO" updated to "Qwen3.6-Plus-WITH-OMO"
- [ ] VERSION file shows v1.5.14
- [ ] Config template shows v1.5.14
- [ ] enve config shows v1.5.14
- [ ] Both branches committed and tagged
- [ ] Pushed to GitHub

---

## Task 3: Update AI-LTC Todo Tasks Document

**Priority**: Low
**Status**: In Progress
**Description**: This document itself — tracking all tasks and their status.

### Subtasks

| # | Subtask | Status | File |
|---|---------|--------|------|
| 3.1 | Create Todo Tasks document | ✅ Done | This file |
| 3.2 | Commit Todo Tasks document | ⏸ Pending | git |

---

## Task 4: 2026-04-28 Experimental Evaluation v0.2 Alignment

**Priority**: High
**Status**: In Progress
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

### Verification Criteria

- [x] `make validate-evaluation` passes
- [x] `make validate-prompts` passes
- [x] `make check` passes
- [x] `git diff --check` passes
- [x] CI runs `make check`

---

## Current Blockers

| ID | Description | Impact | Workaround |
|----|-------------|--------|------------|
| None | — | — | — |

## Next Action

1. Complete Task 1.6-1.7 (tests + build verification) in the upstream runtime repo when that code is available.
2. Complete Task 2.7 / Task 3.2 by committing the current documentation and validation changes.
3. Push all changes to GitHub after review.

---

## Notes

- Upstream throttle retry uses **same model** (no fallback), 3s cooldown, 30 max attempts
- After 30 retries, falls back to normal model fallback flow
- This is specific to OpenCode Zen's Alibaba routing layer, not OpenRouter
- The error message pattern: `"Upstream error from Alibaba: Request rate increased too quickly. To ensure system stability, please adjust your client logic to scale requests more smoothly over time."`
