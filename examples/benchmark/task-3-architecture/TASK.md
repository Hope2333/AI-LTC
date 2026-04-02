# Benchmark Task 3: Architecture Design

## Objective
Design a plugin system for an existing CLI tool.

## Starting State
A working CLI tool (`main.py`) with two commands: `greet` and `wordcount`.

## Constraints
- Design a plugin interface that allows third-party commands
- Define the plugin contract (what a plugin must implement)
- Implement one example plugin
- Update the CLI to discover and load plugins dynamically
- Write handoff document for implementation

## Success Criteria
- Plugin interface is well-defined and documented
- Example plugin works end-to-end
- Handoff document is clear and actionable
- Multi-phase transitions: INIT → HANDOFF_READY → EXECUTION → REVIEW → OPTIMIZER → EXECUTION → REVIEW → CHECKPOINT
- ≤ 8 iterations

## Setup
```bash
cp -r examples/benchmark/task-3-architecture /tmp/benchmark-task-3
cp .ai-template/* /tmp/benchmark-task-3/.ai/
cp examples/demo-cli/main.py /tmp/benchmark-task-3/
```
