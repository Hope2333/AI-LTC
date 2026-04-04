# Active Lane: OML Integration

## Goal

Build the thin adapter bridge (~500 lines TypeScript) between AI-LTC (Brain) and oh-my-litecode/OML (Body), enabling AI-LTC's state machine, memory, and error recovery to drive OML's plugin loading, MCP gateway, session management, and worker pool. Deliverables span 4 phases: bridge foundation → platform adapters → memory/context → automation/CI.

## Current Starting Point

- Status: `active`
- Decision: `continue`
- Phase: **Phase 1 (Bridge Foundation)** — Priority: High
- All documentation is complete: architecture, integration plan, plugin adapter guide, brain/body separation principles
- No code exists yet in `bridge/` or platform adapter directories
- Current branch: `v1.5-superqwen36-preview`
- Framework version: `v1.5.10-sqwen36pre`
- Qwen is the default operator for this lane (per v1 role model)
- Execution context document: `docs/EXECUTION-CONTEXT.md` (SSOT for operational rules)

## Workstreams

### 1. Phase 1: Bridge Foundation (Week 1-2)

**Priority**: High — Must complete before any other phase

| File | Description | Expected Lines | Status |
|------|-------------|---------------|--------|
| `bridge/index.ts` | Bridge entry point, exports `OmlBridge` class | ~20 | TODO |
| `bridge/oml-bridge.ts` | Core logic: state→hook mapping, memory routing, error handling | ~200 | TODO |
| `bridge/event-map.yaml` | AI-LTC event → OML hook name → payload schema | ~50 | TODO |
| `bridge/capability-registry.ts` | Plugin discovery, registration, progressive loading | ~100 | TODO |
| `bridge/protocol.md` | Task/result JSON protocol (Brain↔Body) | ~30 | TODO |

**Validation Criteria**:
- [ ] AI-LTC state machine triggers OML hooks
- [ ] OML session storage persists AI-LTC memory operations
- [ ] At least one OML subagent (e.g., `scout`) invocable via bridge

### 2. Phase 2: Platform Adapter Layer (Week 2-3)

**Priority**: Medium — Depends on Phase 1 validation

| File | Description | Expected Lines | Status |
|------|-------------|---------------|--------|
| `adapters/opencode/index.ts` | OpenCode plugin adapter (25+ event types) | ~80 | TODO |
| `adapters/claude-code/index.ts` | Claude Code adapter (Skills + Hooks + MCP) | ~80 | TODO |
| `adapters/aider/index.ts` | Aider adapter (custom commands) | ~50 | TODO |
| `adapters/registry.ts` | Platform detection + adapter selection | ~60 | TODO |

**Validation Criteria**:
- [ ] AI-LTC capabilities installable on OpenCode
- [ ] AI-LTC capabilities installable on Claude Code
- [ ] Cross-platform capability parity verified

### 3. Phase 3: Memory & Context (Week 3-4)

**Priority**: Medium — Depends on Phase 1 validation

| File | Description | Expected Lines | Status |
|------|-------------|---------------|--------|
| `bridge/memory-adapter.ts` | AI-LTC memory ↔ OML session bridge | ~80 | TODO |
| `bridge/context-compact.ts` | 3-level context compression | ~60 | TODO |
| `bridge/cross-session.ts` | Cross-session knowledge sharing | ~60 | TODO |

**Validation Criteria**:
- [ ] Memory persists across session restarts
- [ ] Context compaction reduces token usage by >30%
- [ ] Cross-session knowledge prevents duplicate plugin invocations

### 4. Phase 4: Automation & CI (Week 4-5)

**Priority**: Low — Depends on Phase 1-3 completion

| File | Description | Expected Lines | Status |
|------|-------------|---------------|--------|
| `scripts/integration-test.sh` | Integration test suite | ~100 | TODO |
| `scripts/deploy-adapter.sh` | Adapter deployment script | ~80 | TODO |
| `Makefile` | Build automation | ~30 | TODO |

**Validation Criteria**:
- [ ] `make test` passes on both Termux and GNU/Linux
- [ ] `make deploy-opencode` installs working plugin
- [ ] Framework check passes for all consumer repos

## Immediate Next Actions

1. **Create `bridge/` directory structure** — Initialize Phase 1 files per `docs/OML-BRIDGE-ARCHITECTURE.md` spec
2. **Implement `bridge/index.ts`** — Entry point with `OmlBridge` class export
3. **Implement `bridge/oml-bridge.ts`** — Core bridge logic mapping AI-LTC events to OML hooks
4. **Create `bridge/event-map.yaml`** — Event mapping table per architecture spec
5. **Implement `bridge/capability-registry.ts`** — Plugin discovery and progressive loading
6. **Write `bridge/protocol.md`** — Task/result JSON protocol specification

## Non-Goals

- Do NOT start Phase 2 before Phase 1 is validated
- Do NOT rewrite existing kernel files — extend them only
- Do NOT commit `.ai/` or `.omx/` directories
- Do NOT include `adapters/` files in backports to `main`
- No casual GPT escalation without `@ARCHITECT_HELP`
- Do NOT exceed ~500 lines total for bridge TypeScript (design constraint)

## Design Constraints

1. **Mutual Exclusion**: Brain has no direct filesystem/tool access. Body makes no orchestration decisions.
2. **Minimal Surface**: ~500 lines of TypeScript total for the bridge.
3. **Progressive Loading**: Capabilities loaded on-demand, not at startup (saves 36%+ context window).
4. **File-based Transport**: Primary transport is file-based JSON (`.ai/bridge/tasks/<taskId>.json`) for Termux compatibility.
5. **Deterministic Hooks**: Prompts are suggestions. Hooks are enforcement.

## Branch & Version Rules

- **Current branch**: `v1.5-superqwen36-preview`
- **Bridge code**: Goes to preview branch (adapter-layer work)
- **Platform adapters**: Go to preview branch (model-specific)
- **Kernel changes**: If any, must go to `main` first, then merge to preview
- **Version bump**: After Phase 1 completion, bump to `v1.5.11-sqwen36pre`

## Consumer Repos

| Repo | Path | Expected Version | Status |
|------|------|------------------|--------|
| enve | `/home/miao/develop/enve` | `v1.5.10-sqwen36pre` | Active |
| oh-my-litecode | `/home/miao/develop/oh-my-litecode` | `v1.5.10-sqwen36pre` | Active — OML is the "Body" |

## Quality Gate

- **Baseline**: enve 94.71 (measured 2026-04-03)
- **Regression threshold**: 90 (drop >5 points triggers blocker)
- **Pre-phase transition**: Quick quality check on changed files required

## Dependencies

- OML 0.2.0-alpha or later (TypeScript core modules)
- AI-LTC v1.5.10 or later
- Node.js >= 20.0.0
- Python 3.8+ (for OML Bash fallbacks)

## Reference Documents

| Document | Purpose |
|----------|---------|
| `docs/OML-BRIDGE-ARCHITECTURE.md` | Technical spec SSOT (interfaces, events, permissions, errors) |
| `docs/OML-INTEGRATION-PLAN.md` | 4-phase roadmap with deliverables and validation |
| `docs/OML-PLUGIN-ADAPTER.md` | Platform adapter guide (OpenCode, Claude Code, Aider) |
| `docs/BRAIN-BODY-SEPARATION.md` | Design principles (mutual exclusion, two-tier state, hooks) |
| `docs/EXECUTION-CONTEXT.md` | Operational manual (branching, versioning, commits, rules) |
| `kernel/control.yaml` | Authority chain and quality gate rules |
| `BRANCH-GOVERNANCE.md` | Dual-branch responsibilities and merge rules |