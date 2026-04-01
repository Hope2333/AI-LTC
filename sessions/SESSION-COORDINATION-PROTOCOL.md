# SESSION-COORDINATION-PROTOCOL

This document defines how multi-session parallel execution works in AI-LTC SuperQwen mode.

## Architecture

```
Orchestrator Session (main)
  ├── Session A: expert-arch     → .ai/sessions/expert-arch/
  ├── Session B: worker-impl     → .ai/sessions/worker-{name}/
  ├── Session C: worker-test     → .ai/sessions/worker-test/
  └── Session D: expert-review   → .ai/sessions/expert-review/
```

Each session is an independent OpenCode session spawned via `task()`.
Sessions do NOT share context with each other — they communicate only through `.ai/sessions/` files.

## Directory Structure

```
.ai/sessions/
  ├── active-sessions.json        ← orchestrator-managed session registry
  ├── merge-result.md             ← orchestrator's merged synthesis
  ├── expert-arch/
  │   ├── task-brief.md           ← input: what to analyze
  │   └── output.md               ← output: architecture decision
  ├── expert-review/
  │   ├── task-brief.md
  │   └── output.md
  ├── worker-{name}/
  │   ├── task-brief.md
  │   └── output.md
  ├── worker-test/
  │   ├── task-brief.md
  │   └── output.md
  └── researcher/
      ├── task-brief.md
      └── output.md
```

## Session Lifecycle

### 1. Spawn
- orchestrator writes `task-brief.md` for each session
- orchestrator calls `task()` with the appropriate session prompt
- orchestrator records session ID in `active-sessions.json`

### 2. Execute
- each session reads its `task-brief.md` and executes independently
- sessions write results to their `output.md`
- sessions do NOT read other sessions' outputs unless explicitly referenced in their brief

### 3. Collect
- orchestrator calls `background_output(task_id="...")` for each session
- orchestrator validates that `output.md` exists and is non-empty

### 4. Merge
- orchestrator synthesizes all session outputs into `merge-result.md`
- merge-result.md includes:
  - which sessions succeeded/failed
  - key findings from each session
  - unified next actions
  - conflicts between session outputs (if any)

### 5. Cleanup
- orchestrator cancels disposable sessions via `background_cancel(taskId="...")`
- session records older than the last 3 per role are archived or deleted
- `active-sessions.json` is updated to reflect completed state

## active-sessions.json Schema

```json
{
  "sessions": [
    {
      "id": "ses_abc123",
      "role": "expert-arch",
      "spawned_at": "2026-04-01T10:00:00Z",
      "status": "running",
      "task": "Design API contract for auth module",
      "output_file": ".ai/sessions/expert-arch/output.md"
    }
  ],
  "max_concurrent": 3,
  "last_updated": "2026-04-01T10:00:00Z"
}
```

## Conflict Resolution

When multiple sessions produce conflicting outputs:
1. expert-arch takes precedence over worker sessions for architectural decisions
2. expert-review findings block worker-impl until resolved
3. orchestrator surfaces conflicts in `merge-result.md` and escalates if unresolvable

## OpenCode Integration

Sessions are spawned using OpenCode's `task()` mechanism:

```typescript
task(
  subagent_type="explore",
  run_in_background=true,
  load_skills=[],
  description="expert-arch: Design auth API",
  prompt="Apply shared-repo-contract.prompt.md first.\n\nYou are an expert architect session...\n\nTask brief: Read .ai/sessions/expert-arch/task-brief.md"
)
```

Key rules:
- `run_in_background=true` for ALL sessions — never block on a single session
- `session_id` from task output is stored in `active-sessions.json`
- Use `session_id` for continuation if a session needs retry
- Cancel with `background_cancel(taskId="...")` after collecting results

## Safety

- max concurrent sessions: `multi_session.max_concurrent` (default: 3)
- session timeout: 10 minutes without output → cancel and retry
- retry limit: 1 retry per session before escalation
- if all sessions fail → emit `@ARCHITECT_HELP` with failure context