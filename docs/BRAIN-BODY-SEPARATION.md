# Brain/Body Separation Principles

## Core Thesis

AI agent systems achieve reliability by separating **coordination logic** (Brain) from **runtime execution** (Body). This is the dominant architectural pattern in 2026, validated by Praetorian, OpenCode, and Claude Code independently.

---

## 1. Mutual Exclusion

**The Brain cannot write. The Body cannot decide.**

| Layer | Can | Cannot |
|-------|-----|--------|
| **Brain** (AI-LTC) | Read state, write state, dispatch tasks, make phase decisions | Read files, write files, execute commands, access MCP tools |
| **Body** (OML) | Read files, write files, execute commands, access MCP tools | Dispatch tasks, modify state machine, change phase, make orchestration decisions |

This is **enforced structurally via permissions**, not by prompt instructions. Prompts are suggestions; permissions are enforcement.

### Evidence from Industry

- **OpenCode**: `plan` agent has `edit: { "*": "deny" }` — structurally cannot write code
- **Praetorian**: Coordinator has `Task`, `Read` — denied `Edit`, `Write`. Executor has `Edit`, `Write`, `Bash` — denied `Task`
- **Claude Code**: Hooks block operations at the infrastructure level, regardless of what the LLM "wants" to do

---

## 2. Two-Tier State

| Tier | Storage | Lifetime | Analogy |
|------|---------|----------|---------|
| **Ephemeral** | JSON files in `.ai/bridge/` | Lost on crash | RAM |
| **Persistent** | `.ai/state.json`, `.ai/logs/` | Survives restart | Disk |

The Brain's state machine lives in persistent storage. The Body's runtime state (worker PIDs, active tasks) lives in ephemeral storage. On restart, the Brain reads persistent state and reconstructs the Body's runtime state.

---

## 3. Deterministic Hooks

**Prompts are suggestions. Hooks are enforcement.**

The Body's hook system must block invalid operations at the infrastructure level:

```
Brain says: "Write to src/core/auth.ts"
  → Hook checks: Is this a valid transition? Is the file in scope?
  → If valid: allow
  → If invalid: block (regardless of what the Brain said)
```

This prevents:
- Hallucinated file paths
- Out-of-scope modifications
- Permission violations
- State machine bypasses

### Hook Types

| Type | When | Purpose |
|------|------|---------|
| `pre` | Before operation | Validate, check permissions, prepare context |
| `post` | After operation | Log results, update state, trigger next phase |
| `around` | Wraps operation | Measure duration, handle errors, retry logic |

---

## 4. Progressive Tool Loading

**Don't load all tools at startup. Load on-demand.**

| Approach | Context Cost | Startup Time |
|----------|-------------|--------------|
| Load all 51 OML plugins | ~71,800 tokens | Slow |
| Load metadata only | ~2,000 tokens | Fast |
| Load on-demand | ~0 tokens at startup | Fastest |

The bridge registers capability **metadata** (name, type, description) at startup. Full definitions (tools, prompts, hooks) are loaded only when the Brain decides to use a capability.

Measured savings: **36%+ of context window** (Praetorian: 71,800 → 0 tokens at startup).

---

## 5. Platform Abstraction

**The Brain knows nothing about Termux vs GNU/Linux.**

OML's platform detection layer normalizes:
- File paths (`/data/data/com.termux/files/usr` → `/usr` abstraction)
- Process spawning (`nohup` vs `systemd` vs `launchd`)
- Environment variables (Termux `$PREFIX` vs GNU `/usr/local`)
- Package managers (`pkg` vs `apt` vs `pacman`)

The Brain receives platform-agnostic interfaces. This is critical because:
1. The Brain's state machine is platform-independent by design
2. Platform-specific quirks should never leak into orchestration logic
3. Termux hook issues prove that platform adaptation is a real, unsolved problem

---

## 6. Three-Level Nested Loops

| Level | Scope | Mechanism | Limit |
|-------|-------|-----------|-------|
| **Level 1: Intra-Task** | Single agent execution | Iteration counter | Max 10 iterations |
| **Level 2: Inter-Phase** | Implementation → Review → Test cycle | Feedback loop gate | Blocks exit until all domains pass |
| **Level 3: Orchestrator** | Full workflow | State machine transitions | Re-invokes phases on failure |

**Stuck detection**: Three consecutive iterations with >90% output similarity → invoke external LLM for hint injection.

---

## 7. Context Compaction Gates

At each phase transition, the system checks context utilization:

| Utilization | Action |
|-------------|--------|
| < 75% | Proceed normally |
| 75-85% | Warning — should compact before next phase |
| > 85% | **Hard Block** — refuses to proceed without compaction |

Compaction levels:
1. **Micro**: Clear stale tool results and intermediate reasoning
2. **Session**: Extract key decisions to `.ai/state.json` `context_summary`
3. **Full**: Summarize entire history, preserve user messages only

---

## 8. Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|-----------------|
| Brain writes files directly | Breaks mutual exclusion, bypasses permission system | Brain dispatches task → Body writes file |
| Body makes phase decisions | Body has no global state view, leads to inconsistent state | Body reports results → Brain decides phase |
| Load all tools at startup | Context window pressure, 36%+ waste | Progressive loading on-demand |
| Rely on prompts for enforcement | LLMs hallucinate, forget, misinterpret | Use deterministic hooks for enforcement |
| Platform-specific logic in Brain | Brain becomes unmaintainable, breaks portability | Platform abstraction in Body layer |
| No compaction gates | Context overflow → hallucinated state | Hard block at >85% utilization |
