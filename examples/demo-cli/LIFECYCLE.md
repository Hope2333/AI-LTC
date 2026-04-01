# Demo CLI — Full Lifecycle Walkthrough

This document demonstrates the complete AI-LTC lifecycle using the demo-cli project.

## Test Case 1: Happy Path (Single Task)

### INIT Phase
```
.ai/state.json: phase=INIT, status=idle
.ai/system/init-status.md: Status=INITING → INSTALLED
.ai/system/ai-ltc-config.json: Written with project config
```
**Exit condition**: Config written, project state classified as `greenfield`
**Transition**: INIT → HANDOFF_READY

### HANDOFF_READY Phase
```
00_HANDOFF.md: Written with 5 tasks defined
.ai/active-lane/lane.md: Lane goal set, boundaries defined
```
**Exit condition**: Handoff complete, next actions explicit
**Transition**: HANDOFF_READY → EXECUTION

### EXECUTION Phase
```
Task 1: Create main.py with argparse structure → done
Task 2: Implement greet command → done
Task 3: Implement wordcount command → done
Task 4: Write unit tests → done
.ai/state.json: iteration increments, tasks update to done
.ai/logs/decision.log: Each decision logged
```
**Exit condition**: All tasks done, tests pass locally
**Transition**: EXECUTION → REVIEW

### REVIEW Phase
```
Task 5: Review code quality → done
.ai/logs/state.log: Phase transition logged
Review findings: No critical issues
```
**Exit condition**: Review passed, no blockers
**Transition**: REVIEW → CHECKPOINT

### CHECKPOINT Phase
```
.ai/state.json: phase=CHECKPOINT, status=done
.ai/history/snapshots/: State snapshot saved
.ai/logs/metrics.json: task_success_rate=1.0, retry_count=0
```
**Exit condition**: Metrics recorded, lane closed
**Result**: ✅ SUCCESS

---

## Test Case 2: Error Recovery (Forced Retry)

### Scenario
Task 2 (greet command) has a bug: missing `--name` flag validation.

### EXECUTION Phase
```
Task 2: Implement greet → done (but buggy)
Task 4: Tests fail — greet("") should handle empty name
.ai/logs/error.log: type=tool_failure, message=test failure
```
**Recovery**: Retry with fix (add validation)
**Result**: Tests pass on retry 1

### REVIEW Phase
```
Task 5: Review finds missing edge case in wordcount
Finding: wordcount("  ") returns 0, should it?
Decision: Acceptable behavior, note in docs
```
**Exit condition**: Review passed with minor note
**Result**: ✅ SUCCESS (with 1 retry)

---

## Test Case 3: Long Task with Escalation

### Scenario
Project scope expands: add file I/O for saving greeting history.

### EXECUTION Phase
```
Tasks 1-4: Complete as before
New Task 6: Implement greeting history (file I/O)
New Task 7: Add --history flag to greet command
.ai/state.json: tasks expanded, iteration continues
```

### Blocker Detection
```
Blocker: File path handling differs between OS
Retry 1: Use pathlib → still fails on Windows paths
Retry 2: Add os.path fallback → still inconsistent
Retry 3: Same issue → dead_loop detected
.ai/logs/error.log: type=dead_loop, action=escalate
```

### Escalation
```
@ARCHITECT_HELP emitted
ESCALATION_REQUEST.md written:
  - Problem: Cross-platform file path handling
  - Attempted: pathlib, os.path, both fail
  - Ask: Recommend cross-platform strategy
```

### OPTIMIZER Phase
```
Optimizer intervention:
  - Recommend using pathlib exclusively
  - Add platform-specific test fixtures
  - Simplify file format to JSON lines
```

### EXECUTION (Optimizer Return)
```
Task 6: Re-implement with pathlib + JSON lines → done
Task 7: Add --history flag → done
Tests pass on all platforms
```

### CHECKPOINT Phase
```
.ai/logs/metrics.json:
  task_success_rate: 0.85
  retry_count: 3
  escalation_frequency: 1
```
**Result**: ✅ SUCCESS (with escalation)

---

## Verification Commands

```bash
cd examples/demo-cli
python main.py greet --name Alice
python main.py wordcount hello world from AI-LTC
python -m pytest tests/test_main.py -v
```
