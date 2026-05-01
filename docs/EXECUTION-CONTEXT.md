# AI-LTC Execution Context

## For the Execution Agent — Read This First

This document contains all operational context needed to work on the AI-LTC repository correctly: versioning, branching, commit conventions, file ownership, evaluation scaffolding, and the OML integration plan.
Canonical design references:
- `docs/BRANCH-REFACTOR-PLAN.md`
- `docs/PROMPT-DECOUPLING-PLAN.md`
- `docs/EVALUATION-SCHEMA.md`
- `docs/AI-LTC-vs-OML-BOUNDARY.md`
- `prompts/_mapping/legacy-to-role-phase-adapter.md`

---

## 1. Branch Governance

### Two-Branch Model

| Branch | Purpose | Version Tags | What Lives Here |
|--------|---------|-------------|-----------------|
| **main** | Stable framework layer | `v1.5.x` | `kernel/`, `.ai-template/`, `examples/`, `scripts/`, stable docs, promoted abstractions |
| **Experimental** | Active experimental branch | `v1.5.x` experimental tags; historical preview suffixes only for continuity | adapters, prompt migration scaffolding, evaluation schemas/results, provider-specific work |

Current git branch carrying `Experimental`: `Experimental`.

### Directory Ownership

| Directory | Branch | Who Can Modify |
|-----------|--------|---------------|
| `kernel/` | main | main only |
| `.ai-template/` | main | main only |
| `examples/` | main | both |
| `scripts/` | main | main only |
| `adapters/` | Experimental | Experimental only |
| `evaluation/` | Experimental | Experimental only until summarized |
| Legacy root prompt files (`*.prompt.md`) | main | main only unless provider-specific |
| `prompts/roles/`, `prompts/phases/`, `prompts/constraints/` | Experimental | Experimental first, then promote |
| `prompts/adapters/` | Experimental | Experimental only |
| provider-specific adapter prompts | Experimental | Experimental only |

### Merge Rules

- **main → Experimental**: Always allowed, merge regularly
- **Experimental → main**: Only model-agnostic changes (kernel fixes, scripts, README, promoted abstractions). NO `adapters/`, NO `experimental_mode`, NO provider-specific prompt deltas
- **Decision rule**: If the change is model-agnostic → main. If it's experimental, provider-specific, or evidence-heavy → Experimental.

---

## 2. Version Management

### Current Versions

| Item | Value |
|--------|-------------|
| Repo `VERSION` | `v1.5.15` |
| Stable branch family | `main` |
| Experimental branch family | `Experimental` |
| Historical Experimental suffixes | old provider-preview suffixes may appear in old tags only |

### Versioning Rules

1. **Single source of truth**: `VERSION` file in repo root
2. **main tags**: `v1.5.x` — increment by 1 for each kernel-level release
3. **Experimental tags**: use the active `Experimental` branch; preserve old provider-preview suffixes only when referencing historical evidence trails
4. **Experimental tags do NOT need to match main tags** — they evolve independently
5. **When backporting to main**: main gets the stable tag, Experimental keeps its evidence trail
6. **When merging main → Experimental**: Experimental merges and may get a new tag

### When to Bump Versions

- **main**: After kernel changes, scripts, or significant docs land
- **Experimental**: After adapter changes, evaluation scaffolding, experimental mode updates, or any meaningful migration step
- **Both**: After major feature additions (like the OML bridge)

### Files to Update When Bumping

1. `VERSION` — new version number
2. `ai-ltc-config.template.json` — `framework_version` field
3. provider adapter specs — `min_framework_version` where applicable
4. `BRANCH-GOVERNANCE.md` — version alignment table
5. `README.md` — version history table
6. Consumer repos' `.ai/system/ai-ltc-config.json` — `framework_version` and `installed_framework_tag`
7. `cross-repo-registry.json` — branch semantics and expected consumer versions

---

## 3. Commit Conventions

### Style

- Short, imperative subject line with sentence-style capitalization and trailing period
- Example: `Add code quality gate to control.yaml.`
- Keep commits narrowly scoped — one logical change per commit

### Examples from Recent History

```
Add OML integration docs: bridge architecture, platform adapters, brain/body separation principles. Update README.
Add cross-repo management: VERSION, registry, framework-check script.
Add Claude Code leak insights: context overflow, circuit breakers, transition hooks, and memory system. Bump to v1.5.10.
Refactor preview branch into adapter architecture: sessions → provider adapters.
Add BRANCH-GOVERNANCE.md: dual-branch responsibilities and merge rules.
```

### Commit Rules

- **Never commit `.omx/` or `.ai/` directories**
- **Never commit AI-LTC's own `.ai/` directory** (it's local-only workspace state)
- **Commit to the correct branch** per the directory ownership matrix above
- **Tag after significant commits** — use `git tag -a v1.5.x -m "description"` on main, and an explicitly named Experimental tag on the `Experimental` branch

---

## 4. OML Integration Plan (Phase 1-4)

### What's Done (Documentation Only)

| File | Content |
|------|---------|
| `docs/OML-INTEGRATION-PLAN.md` | 4-phase roadmap with deliverables and validation criteria |
| `docs/OML-BRIDGE-ARCHITECTURE.md` | Technical spec: event mapping, capability registry, task protocol, permissions |
| `docs/OML-PLUGIN-ADAPTER.md` | Platform adapter guide: OpenCode, Claude Code, Aider, custom |
| `docs/BRAIN-BODY-SEPARATION.md` | Design principles: mutual exclusion, two-tier state, deterministic hooks |

### Evaluation Validation

Run `make validate-evaluation` after editing `evaluation/`. This checks v0.2 shape, selected field types, references, `tested_at` dates, and freshness windows; it does not score records or automate routing. Run `make validate-prompts` after editing `prompts/_mapping/`. Run `make validate-provider-naming` after edits that may expose provider-specific terms outside compatibility, adapter, mapping, or evidence surfaces. Run `make validate-ts-imports` after editing bridge or adapter TypeScript imports. Run `make validate-config-registry` after editing `VERSION`, `cross-repo-registry.json`, or `ai-ltc-config.template.json`. Run `make check` before handoff to include all validators and the existing bridge integration smoke test. CI also runs `make check` through `.github/workflows/check.yml`.

### What Needs to Be Built

#### Phase 1: Bridge Foundation (Priority: High)

| File | Description | Expected Lines |
|------|-------------|---------------|
| `bridge/index.ts` | Bridge entry point, exports `OmlBridge` class | ~20 |
| `bridge/oml-bridge.ts` | Core logic: state→hook mapping, memory routing, error handling | ~200 |
| `bridge/event-map.yaml` | AI-LTC event → OML hook name → payload schema | ~50 |
| `bridge/capability-registry.ts` | Plugin discovery, registration, progressive loading | ~100 |
| `bridge/protocol.md` | Task/result JSON protocol (Brain↔Body) | ~30 |

**Validation**: AI-LTC state machine triggers OML hooks, OML session storage persists AI-LTC memory, at least one OML subagent invocable via bridge.

#### Phase 2: Platform Adapter Layer (Priority: Medium)

| File | Description | Expected Lines |
|------|-------------|---------------|
| `adapters/opencode/index.ts` | OpenCode plugin adapter (25+ event types) | ~80 |
| `adapters/claude-code/index.ts` | Claude Code adapter (Skills + Hooks + MCP) | ~80 |
| `adapters/aider/index.ts` | Aider adapter (custom commands) | ~50 |
| `adapters/registry.ts` | Platform detection + adapter selection | ~60 |

**Validation**: AI-LTC capabilities installable on OpenCode and Claude Code.

#### Phase 3: Memory & Context (Priority: Medium)

| File | Description | Expected Lines |
|------|-------------|---------------|
| `bridge/memory-adapter.ts` | AI-LTC memory ↔ OML session bridge | ~80 |
| `bridge/context-compact.ts` | 3-level context compression | ~60 |
| `bridge/cross-session.ts` | Cross-session knowledge sharing | ~60 |

#### Phase 4: Automation & CI (Priority: Low)

| File | Description | Expected Lines |
|------|-------------|---------------|
| `scripts/integration-test.sh` | Integration test suite | ~100 |
| `scripts/deploy-adapter.sh` | Adapter deployment script | ~80 |
| `Makefile` | Build automation | ~30 |

### Key Design Constraints

1. **Mutual Exclusion**: Brain (AI-LTC) has no direct filesystem/tool access. Body (OML) makes no orchestration decisions.
2. **Minimal Surface**: ~500 lines of TypeScript total for the bridge.
3. **Progressive Loading**: Capabilities loaded on-demand, not at startup (saves 36%+ context window).
4. **File-based Transport**: Primary transport is file-based JSON (`.ai/bridge/tasks/<taskId>.json`) for Termux compatibility.
5. **Deterministic Hooks**: Prompts are suggestions. Hooks are enforcement.

---

## 5. Consumer Repositories

### enve

| Field | Value |
|-------|-------|
| Path | `/home/miao/develop/enve` |
| Config | `.ai/system/ai-ltc-config.json` |
| Branch | `Experimental` |
| Expected Version | `v1.5.15` |
| Status | Active — Skia m100 migration in progress, code quality CI added |

### oh-my-litecode

| Field | Value |
|-------|-------|
| Path | `/home/miao/develop/oh-my-litecode` |
| Config | `.ai/system/ai-ltc-config.json` |
| Branch | `Experimental` |
| Expected Version | `v1.5.15` |
| Status | Active — OML is the "Body" in the Brain/Body architecture |

### Framework Check

Run `bash scripts/framework-check.sh` to verify all consumer repos are aligned with the correct AI-LTC version.

---

## 6. Quality Gate

### Thresholds

| Score Range | Action |
|-------------|--------|
| ≥ 90 | Acceptable, proceed normally |
| 80-89 | Warning — log top problematic files as advisory |
| < 80 | Block — require human review before phase transition |

### Regression Rule

If quality score drops by **>5 points** from the project baseline, log a blocker. The execution agent must identify the top 3 worst files and propose fixes.

### Baseline

- **enve**: 94.71 (measured 2026-04-03)
- **Regression threshold**: 90

---

## 7. Cross-Repo Registry

Located at `cross-repo-registry.json`. Contains:
- Framework version
- Branch version mapping
- Consumer repo registration (path, config location, branch, expected version)

When adding a new consumer repo:
1. Add entry to `consumer_repos` in `cross-repo-registry.json`
2. Update the consumer repo's `.ai/system/ai-ltc-config.json` with correct version and branch
3. Run `scripts/framework-check.sh` to verify

---

## 8. Operational Rules

### What NOT to Do

- **Do not** commit to `main` if the change is provider-specific or experimental — use the `Experimental` branch
- **Do not** include `adapters/` files in backports to `main`
- **Do not** commit `.ai/` or `.omx/` directories
- **Do not** treat `.ai/active-lane/*` as public repository truth
- **Do not** bump versions without updating all related files (VERSION, config template, adapter.yaml, BRANCH-GOVERNANCE.md, README.md)
- **Do not** merge preview → main without running the review checklist in BRANCH-GOVERNANCE.md
- **Do not** start Phase 2 before Phase 1 is validated
- **Do not** rewrite existing kernel files — extend them

### What to Do

- **Do** commit to the correct branch per directory ownership
- **Do** run `scripts/framework-check.sh` after any version change
- **Do** update `cross-repo-registry.json` when adding consumer repos
- **Do** update `evaluation/` with dated evidence when experimental conclusions matter
- **Do** tag after significant commits
- **Do** follow the commit style: imperative, sentence-case, trailing period
- **Do** keep commits narrowly scoped
- **Do** validate Phase 1 before starting Phase 2

---

## 9. File Structure Reference

```
AI-LTC/
├── VERSION                              # Single source of truth for version
├── cross-repo-registry.json             # Consumer repo registration
├── BRANCH-GOVERNANCE.md                 # Branch responsibilities and merge rules
├── ai-ltc-config.template.json          # Template for consumer repo configs
├── kernel/                              # Protocol layer (main only)
│   ├── state_schema.json
│   ├── control.yaml                     # Authority chain + quality gate
│   ├── state_machine.yaml               # Legal phase transitions
│   ├── error_model.yaml                 # Error types + recovery
│   └── arbitration.yaml                 # Conflict resolution
├── adapters/                            # Model-specific adapters (Experimental)
│   └── provider-specific adapters/
│       ├── adapter.yaml
│       ├── experimental-mode.prompt.md
│       └── orchestrator.prompt.md
├── evaluation/                         # Experimental registries, schemas, tasks, and dated results
├── prompts/
│   ├── roles/                          # Role scaffolds
│   ├── phases/                         # Phase scaffolds
│   ├── constraints/                    # Shared boundaries
│   └── adapters/                       # Provider/platform deltas
├── bridge/                              # OML integration (TODO - Phase 1)
│   ├── index.ts
│   ├── oml-bridge.ts
│   ├── event-map.yaml
│   ├── capability-registry.ts
│   └── protocol.md
├── docs/                                # Design documentation
│   ├── OML-INTEGRATION-PLAN.md
│   ├── OML-BRIDGE-ARCHITECTURE.md
│   ├── OML-PLUGIN-ADAPTER.md
│   └── BRAIN-BODY-SEPARATION.md
├── scripts/
│   ├── framework-check.sh               # Cross-repo version validation
│   ├── evaluation_validator.py          # Evaluation v0.2 shape/reference validation
│   ├── prompt_mapping_validator.py      # Prompt migration mapping validation
│   ├── integration-test.sh              # TODO - Phase 4
│   └── deploy-adapter.sh                # TODO - Phase 4
├── .ai-template/                        # Runtime templates
├── examples/
│   ├── demo-cli/
│   └── collaboration-system/
└── README.md
```
