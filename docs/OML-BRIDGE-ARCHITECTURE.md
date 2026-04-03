# OML Bridge Architecture

## Purpose

Defines the technical specification for the thin adapter bridge between AI-LTC (Brain) and oh-my-litecode / OML (Body).

---

## 1. Design Principles

1. **Mutual Exclusion**: Brain has no direct filesystem/tool access. Body makes no orchestration decisions. Enforced structurally via permissions.
2. **Minimal Surface**: ~500 lines of TypeScript. The bridge is a translator, not a runtime.
3. **Deterministic Hooks**: Prompts are suggestions. Hooks are enforcement. The bridge triggers OML hooks that block invalid operations at the infrastructure level.
4. **Progressive Loading**: Capabilities are loaded on-demand, not at startup. Saves 36%+ of context window.
5. **Platform Agnostic**: The bridge knows nothing about Termux vs GNU/Linux. OML's platform layer handles that.

---

## 2. Event Mapping

### 2.1 State Transition → Hook Mapping

| AI-LTC State Transition | OML Hook Trigger | Payload |
|------------------------|------------------|---------|
| `SETUP → EXECUTION` | `oml:execution:start` | `{ sessionId, goal, tasks }` |
| `EXECUTION → REVIEW` | `oml:review:start` | `{ sessionId, phase, artifacts }` |
| `REVIEW → OPTIMIZER` | `oml:optimize:start` | `{ sessionId, reviewFindings }` |
| `OPTIMIZER → CHECKPOINT` | `oml:checkpoint:create` | `{ sessionId, summary, metrics }` |
| `Any → BLOCKED` | `oml:blocked:notify` | `{ sessionId, blocker, context }` |
| `BLOCKED → EXECUTION` | `oml:blocked:resolve` | `{ sessionId, resolution }` |
| `Any → DONE` | `oml:done:notify` | `{ sessionId, finalSummary }` |

### 2.2 Memory → Session Mapping

| AI-LTC Memory Operation | OML Session Operation |
|------------------------|----------------------|
| `memory.write(key, value)` | `session.setContext(sessionId, key, value)` |
| `memory.read(key)` | `session.getContext(sessionId, key)` |
| `memory.compact()` | `session.fork(sessionId, { shallow: true })` |
| `memory.list()` | `session.listContexts(sessionId)` |
| `memory.clear()` | `session.clearContext(sessionId)` |

### 2.3 Error → Recovery Mapping

| AI-LTC Error Type | OML Recovery Action |
|-------------------|---------------------|
| `tool_failure` | `pool-recovery.retry(taskId, strategy="exponential-backoff")` |
| `context_overflow` | `pool-recovery.checkpoint-restore(sessionId)` |
| `authority_violation` | `hooks-engine.trigger("permission:deny", { agent, field })` |
| `agent_stuck` | `pool-monitor.health-check(workerId) → pool-recovery.failover(taskId)` |

---

## 3. Capability Registry

### 3.1 Interface

```typescript
interface Capability {
  name: string;
  type: 'agent' | 'subagent' | 'mcp' | 'skill';
  description: string;
  platforms: string[];
  invoke(args: Record<string, unknown>): Promise<CapabilityResult>;
}

interface CapabilityResult {
  status: 'success' | 'error' | 'timeout';
  data?: unknown;
  error?: string;
  duration: number;
}
```

### 3.2 Discovery Protocol

```
1. Bridge calls OML plugin-loader.listPlugins()
2. For each plugin, reads plugin.json manifest
3. Registers as AI-LTC capability with metadata:
   - name: plugin.name
   - type: plugin.type
   - description: plugin.description
   - platforms: plugin.platforms
   - invoke: () => oml_plugin_run(plugin.name, args)
4. Returns capability list to AI-LTC kernel
```

### 3.3 Progressive Loading

```typescript
// At startup: register capability METADATA only (no tool definitions)
const capabilities = await bridge.discoverCapabilities();
// capabilities = [{ name: 'scout', type: 'subagent', description: '...' }, ...]

// When AI-LTC needs a capability: load its full definition on-demand
const fullDef = await bridge.loadCapability('scout');
// fullDef = { name: 'scout', tools: [...], prompts: [...], hooks: [...] }
```

---

## 4. Task/Result Protocol

### 4.1 Brain → Body (Task Dispatch)

```json
{
  "taskId": "task-<timestamp>-<random>",
  "type": "subagent|skill|mcp",
  "capability": "scout",
  "payload": {
    "description": "Find all auth middleware implementations",
    "scope": "src/**",
    "timeout": 300
  },
  "metadata": {
    "sessionId": "ses_abc123",
    "phase": "EXECUTION",
    "priority": 1
  }
}
```

### 4.2 Body → Brain (Result Collection)

```json
{
  "taskId": "task-<timestamp>-<random>",
  "status": "success|error|timeout",
  "result": {
    "findings": ["src/auth/middleware.ts", "src/api/auth.ts"],
    "context": "Found 2 implementations with different patterns"
  },
  "error": null,
  "duration": 12.5,
  "workerId": "worker-xyz"
}
```

### 4.3 Transport

- **Primary**: File-based JSON (`.ai/bridge/tasks/<taskId>.json`) — works on Termux, no network dependency
- **Fallback**: stdio JSON — for environments with fast I/O
- **Locking**: File-based locking via `flock` or atomic rename

---

## 5. Permission Model

### 5.1 Brain Permissions

| Action | Allowed | Denied |
|--------|---------|--------|
| Read state | ✅ | — |
| Write state | ✅ (kernel fields only) | — |
| Dispatch tasks | ✅ | — |
| Read files | ❌ | Must go through Body |
| Write files | ❌ | Must go through Body |
| Execute commands | ❌ | Must go through Body |
| Access MCP tools | ❌ | Must go through Body |

### 5.2 Body Permissions

| Action | Allowed | Denied |
|--------|---------|--------|
| Read files | ✅ | — |
| Write files | ✅ (within scope) | — |
| Execute commands | ✅ (within allowlist) | — |
| Access MCP tools | ✅ | — |
| Dispatch tasks | ❌ | Must go through Brain |
| Modify state machine | ❌ | Must go through Brain |
| Change phase | ❌ | Must go through Brain |

---

## 6. Error Handling

### 6.1 Bridge Errors

```typescript
class BridgeError extends Error {
  constructor(
    public code: 'OML_UNAVAILABLE' | 'CAPABILITY_NOT_FOUND' | 'TASK_TIMEOUT' | 'PROTOCOL_ERROR',
    public details: string,
    public recoverable: boolean
  ) {
    super(`[Bridge] ${code}: ${details}`);
  }
}
```

### 6.2 Recovery Strategy

| Error | Recovery | Escalate If |
|-------|----------|-------------|
| `OML_UNAVAILABLE` | Retry 3x with 1s backoff | OML still unavailable after retries |
| `CAPABILITY_NOT_FOUND` | Re-discover capabilities | Capability still missing after rediscovery |
| `TASK_TIMEOUT` | Retry with increased timeout | Task fails 3x with increased timeout |
| `PROTOCOL_ERROR` | Reset task file, retry | Protocol error persists after reset |

---

## 7. File Structure

```
AI-LTC/
├── bridge/
│   ├── index.ts              # Bridge entry point
│   ├── oml-bridge.ts         # Core bridge logic
│   ├── event-map.yaml        # Event mapping table
│   ├── capability-registry.ts # Plugin capability registry
│   ├── memory-adapter.ts     # Memory → Session bridge
│   ├── context-compact.ts    # Context compaction logic
│   └── protocol.md           # Task/result protocol spec
├── adapters/
│   ├── opencode/             # OpenCode plugin adapter
│   ├── claude-code/          # Claude Code adapter
│   ├── aider/                # Aider adapter (future)
│   └── registry.ts           # Platform adapter registry
├── docs/
│   ├── OML-INTEGRATION-PLAN.md
│   ├── OML-BRIDGE-ARCHITECTURE.md
│   ├── OML-PLUGIN-ADAPTER.md
│   └── BRAIN-BODY-SEPARATION.md
└── scripts/
    ├── integration-test.sh   # Integration test suite
    └── deploy-adapter.sh     # Adapter deployment script
```
