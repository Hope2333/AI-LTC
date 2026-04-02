# Benchmark Task 2: Error Recovery

## Objective
Fix a broken import chain in a multi-file Python project.

## Starting State
The project has 3 files with circular import issues:
- `app.py` imports from `utils.py` and `models.py`
- `utils.py` imports from `models.py`
- `models.py` imports from `utils.py` (circular!)

## Constraints
- Fix the circular import without changing the public API
- Add tests to verify the fix
- Document what was wrong and how it was fixed

## Success Criteria
- All imports resolve correctly
- Tests pass
- Error recovery triggered at least once
- ≤ 5 iterations
- Dead_loop detection does NOT fire

## Setup
```bash
cp -r examples/benchmark/task-2-error-recovery /tmp/benchmark-task-2
cp .ai-template/* /tmp/benchmark-task-2/.ai/
```
