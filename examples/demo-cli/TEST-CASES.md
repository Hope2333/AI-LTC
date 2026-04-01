# Demo CLI — Test Cases

## Overview

Three test cases validate the AI-LTC framework at different stress levels.

---

## Test Case 1: Happy Path

**Goal**: Prove the framework works under ideal conditions.

**Setup**:
- Fresh project, no prior state
- Simple scope: 2 CLI commands, 1 test file
- No external dependencies

**Expected Flow**:
INIT → HANDOFF_READY → EXECUTION → REVIEW → CHECKPOINT

**Success Criteria**:
- All 5 tasks completed without retry
- Tests pass on first run
- No escalation triggered
- state.json transitions are all legal per kernel/state_machine.yaml
- All log files populated

**Metrics Target**:
- task_success_rate: 1.0
- retry_count: 0
- escalation_frequency: 0

---

## Test Case 2: Error Recovery

**Goal**: Prove the error system works when things go wrong.

**Setup**:
- Same as Test Case 1, but with intentional bugs:
  - greet command missing input validation
  - wordcount edge case with extra spaces

**Expected Flow**:
INIT → HANDOFF_READY → EXECUTION → (tool_failure → retry) → REVIEW → CHECKPOINT

**Success Criteria**:
- Error detected and logged to .ai/logs/error.log
- Recovery strategy from kernel/error_model.yaml followed
- Retry succeeds within max_retries (3)
- Error state cleared after recovery

**Metrics Target**:
- task_success_rate: 1.0 (after recovery)
- retry_count: 1-2
- escalation_frequency: 0

---

## Test Case 3: Long Task with Escalation

**Goal**: Prove the escalation and optimizer system works under sustained pressure.

**Setup**:
- Expanded scope: add file I/O for greeting history
- Cross-platform complexity triggers dead_loop
- Requires optimizer intervention

**Expected Flow**:
INIT → HANDOFF_READY → EXECUTION → (dead_loop → escalate) → OPTIMIZER → EXECUTION → REVIEW → CHECKPOINT

**Success Criteria**:
- Dead loop detected after 3 retries (per kernel/error_model.yaml)
- ESCALATION_REQUEST.md written with proper format
- Optimizer provides actionable intervention
- Post-optimizer execution completes successfully
- All arbitration rules followed per kernel/arbitration.yaml

**Metrics Target**:
- task_success_rate: 0.85+ (some tasks may be deferred)
- retry_count: 3+
- escalation_frequency: 1

---

## Running the Tests

### Automated Verification
```bash
cd examples/demo-cli
python -m pytest tests/test_main.py -v
```

### Manual Verification
1. Copy .ai-template/ to .ai/ in the demo project
2. Run through each test case scenario
3. Verify state.json transitions match kernel/state_machine.yaml
4. Verify log files are populated correctly
5. Verify metrics match expected targets
