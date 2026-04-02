# Benchmark Task 1: Simple Implementation

## Objective
Create a Python module with an email validation function.

## Constraints
- Single file: `validator.py`
- Function: `validate_email(email: str) -> bool`
- Must handle: empty strings, missing @, missing domain, valid emails
- No external dependencies
- Include 3 unit tests

## Success Criteria
- All tests pass
- State transitions: INIT → HANDOFF_READY → EXECUTION → REVIEW → CHECKPOINT
- No escalation triggered
- ≤ 3 iterations

## Setup
```bash
cp -r examples/benchmark/task-1-simple /tmp/benchmark-task-1
cp .ai-template/* /tmp/benchmark-task-1/.ai/
```
