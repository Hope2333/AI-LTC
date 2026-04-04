# Task/Result Protocol: Brain ↔ Body Communication

## Brain → Body (Task Dispatch)

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

## Body → Brain (Result Collection)

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

## Transport

- **Primary**: File-based JSON (`.ai/bridge/tasks/<taskId>.json`)
- **Fallback**: stdio JSON
- **Locking**: File-based locking via `flock` or atomic rename
