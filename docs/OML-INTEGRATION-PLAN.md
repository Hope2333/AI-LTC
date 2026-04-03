# OML Integration Plan

## Overview

Integrate AI-LTC (Brain — state machine, memory, error recovery, cross-repo sync) with oh-my-litecode / OML (Body — plugin loading, MCP gateway, session management, worker pool, hooks engine).

**Strategy**: Thin adapter bridge (~500 lines TypeScript). AI-LTC kernel events map to OML hook triggers. OML plugins become AI-LTC "capabilities".

---

## Phase 1: Bridge Foundation (Week 1-2)

### Goal
Establish the minimal communication layer between AI-LTC kernel and OML runtime.

### Deliverables

1. **`bridge/oml-bridge.ts`** — Core bridge module
   - Maps AI-LTC state transitions → OML hook triggers
   - Routes AI-LTC memory operations → OML session storage
   - Maps AI-LTC error handling → OML pool-recovery system
   - Exposes OML plugins as AI-LTC "capabilities"

2. **`bridge/event-map.yaml`** — Event mapping table
   - AI-LTC kernel event → OML hook name → payload schema
   - Example: `state.transition:EXECUTION→REVIEW` → `oml:review:start` → `{ sessionId, phase, artifacts }`

3. **`bridge/capability-registry.ts`** — Plugin capability registry
   - Discovers OML plugins via `plugin-loader.ts`
   - Registers each plugin as an AI-LTC capability with metadata
   - Provides `getCapability(name)`, `listCapabilities()`, `invokeCapability(name, args)`

4. **`bridge/protocol.md`** — Task/result protocol spec
   - Brain → Body: `{ taskId, type, payload, timeout }`
   - Body → Brain: `{ taskId, status, result, error }`
   - JSON-over-stdio or file-based (for Termux compatibility)

### Validation
- AI-LTC state machine can trigger OML hooks
- OML session storage persists AI-LTC memory operations
- At least one OML subagent (e.g., `scout`) is invocable via the bridge

---

## Phase 2: Platform Adapter Layer (Week 2-3)

### Goal
Enable AI-LTC to drive OML's plugin system across multiple coding platforms (OpenCode, Claude Code, Aider, Termux).

### Deliverables

1. **`adapters/opencode/`** — OpenCode plugin adapter
   - Maps AI-LTC capabilities to OpenCode plugin format
   - Uses OpenCode's `~/.config/opencode/plugins/` convention
   - Handles OpenCode's 25+ event types

2. **`adapters/claude-code/`** — Claude Code adapter
   - Maps AI-LTC capabilities to Claude Code Skills + Hooks + MCP
   - Uses `.claude/skills/` and `.claude/hooks/` conventions
   - Handles Termux-specific patches

3. **`adapters/aider/`** — Aider adapter (future)
   - Maps AI-LTC capabilities to Aider's config + custom commands
   - Uses `.aider.conf.yaml` convention

4. **`adapters/registry.ts`** — Platform adapter registry
   - `detectPlatform()` → selects correct adapter
   - `installCapabilities(adapter, capabilities)` → deploys AI-LTC to target platform
   - `uninstallCapabilities(adapter)` → cleans up

### Validation
- AI-LTC capabilities installable on OpenCode
- AI-LTC capabilities installable on Claude Code
- Cross-platform capability parity verified

---

## Phase 3: Memory & Context Integration (Week 3-4)

### Goal
Connect AI-LTC's memory system with OML's session management for persistent, cross-session knowledge.

### Deliverables

1. **`bridge/memory-adapter.ts`** — Memory bridge
   - AI-LTC `memory.write(key, value)` → OML `session-manager.setContext(sessionId, key, value)`
   - AI-LTC `memory.read(key)` → OML `session-manager.getContext(sessionId, key)`
   - AI-LTC `memory.compact()` → OML `session-manager.fork(sessionId, { shallow: true })`

2. **`bridge/context-compact.ts`** — Context compaction
   - Implements 3-level compression (Micro → Session → Full)
   - Triggers at AI-LTC phase transitions
   - Uses OML's checkpoint system for recovery

3. **`bridge/cross-session.ts`** — Cross-session knowledge sharing
   - Shared memory pool accessible by all sessions
   - Prevents duplicate work across parallel sessions
   - Uses OML's session search + merge capabilities

### Validation
- Memory persists across session restarts
- Context compaction reduces token usage by >30%
- Cross-session knowledge prevents duplicate plugin invocations

---

## Phase 4: Automation & CI (Week 4-5)

### Goal
Automate the integration lifecycle — build, test, deploy, and version sync.

### Deliverables

1. **`scripts/integration-test.sh`** — Integration test suite
   - Tests bridge event mapping
   - Tests plugin capability invocation
   - Tests cross-platform adapter installation
   - Tests memory persistence

2. **`scripts/deploy-adapter.sh`** — Adapter deployment script
   - `deploy-adapter opencode [target-repo]` — installs AI-LTC bridge as OpenCode plugin
   - `deploy-adapter claude-code [target-repo]` — installs AI-LTC bridge as Claude Code skills/hooks
   - `deploy-adapter all [target-repo]` — installs all adapters

3. **`Makefile`** — Build automation
   - `make bridge` — builds TypeScript bridge
   - `make test` — runs integration tests
   - `make deploy-opencode` — deploys to OpenCode
   - `make deploy-claude` — deploys to Claude Code

4. **`cross-repo-registry.json`** update — Register oh-my-litecode as a consumer repo
   - Add `oh-my-litecode` entry with path, config, expected version

### Validation
- `make test` passes on both Termux and GNU/Linux
- `make deploy-opencode` installs working plugin
- Framework check passes for all consumer repos

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    AI-LTC (Brain)                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ State Machine│  │ Memory System │  │ Error Recovery │  │
│  │ (Phases/    │  │ (Ephemeral +  │  │ (Retry budgets,│  │
│  │  Transitions)│  │  Persistent)  │  │  stuck detect) │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                │                   │           │
│  ┌──────┴────────────────┴───────────────────┴────────┐  │
│  │              Bridge Layer (~500 lines TS)           │  │
│  │  event-map.yaml | capability-registry | protocol   │  │
│  └──────────────────────┬─────────────────────────────┘  │
└─────────────────────────┼────────────────────────────────┘
                          │ Task/Result Protocol
┌─────────────────────────┼────────────────────────────────┐
│                    OML (Body)                             │
│  ┌─────────────┐  ┌───┴──────────┐  ┌────────────────┐  │
│  │ Platform    │  │ Plugin Loader │  │ MCP Gateway    │  │
│  │ Detection   │  │ (resolve,     │  │ (tool registry,│  │
│  │ (Termux,    │  │  install,     │  │  progressive   │  │
│  │  GNU/Linux) │  │  load)        │  │  loading)      │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Session     │  │ Pool Manager  │  │ Hook System    │  │
│  │ Management  │  │ (agent        │  │ (PreToolUse,   │  │
│  │ (lifecycle, │  │  lifecycle,   │  │  PostToolUse,  │  │
│  │  compaction)│  │  concurrency) │  │  Stop)         │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┼────────────────────────────────┐
│              Platform Adapters                            │
│  ┌─────────────┐  ┌───┴──────────┐  ┌────────────────┐  │
│  │ OpenCode    │  │ Claude Code  │  │ Aider (future) │  │
│  │ Plugin      │  │ Skills+Hooks │  │ Custom Commands│  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Dependencies

- OML 0.2.0-alpha or later (TypeScript core modules)
- AI-LTC v1.5.10 or later
- Node.js >= 20.0.0
- Python 3.8+ (for OML Bash fallbacks)

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| OML TypeScript migration incomplete | Medium | Use Bash fallbacks for missing TS modules |
| Termux hook compatibility issues | Medium | Platform adapter handles Termux-specific patches |
| Context window pressure from too many capabilities | High | Progressive tool loading (on-demand, not at startup) |
| Plugin ecosystem maturity | Low | Vet third-party plugins, use only core OML plugins initially |
