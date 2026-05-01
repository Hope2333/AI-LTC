# AI-LTC Benchmark Framework

Cross-model comparison for AI-LTC runtime behavior.

## Purpose

Run the **same task** through the **same state machine** with **different models**, then compare:
- State transition compliance
- Error trigger frequency
- Iteration convergence
- Escalation necessity
- Token efficiency

## Test Tasks

### Task 1: Simple Implementation
**Scope**: Create a Python function that validates email format
**Expected**: 1-3 iterations, no escalation, clean state transitions
**Tests**: Basic execution loop, state machine compliance

### Task 2: Error Recovery
**Scope**: Fix a broken import chain in a multi-file project
**Expected**: 3-5 iterations, 1-2 retries, possible escalation
**Tests**: Error detection, recovery strategy, dead_loop prevention

### Task 3: Architecture Design
**Scope**: Design a plugin system for an existing CLI tool
**Expected**: 5-8 iterations, architect-level reasoning, handoff required
**Tests**: Multi-phase transitions, handoff quality, optimizer intervention

## Metrics

| Metric | Description | Target |
|---|---|---|
| `state_compliance` | % of transitions that follow kernel/state_machine.yaml | 100% |
| `error_rate` | Errors triggered per task | < 2 per task |
| `recovery_success` | % of errors successfully recovered | > 80% |
| `iteration_count` | Total iterations to complete task | < max_iterations |
| `escalation_count` | Times @ARCHITECT_HELP was triggered | 0 for Task 1, ≤1 for Task 2 |
| `token_efficiency` | Estimated tokens used vs optimal baseline | < 2x baseline |
| `convergence_time` | Wall-clock time from start to CHECKPOINT | < 30 min per task |

## Model Profiles

### Provider Adapter Under Test
- **Adapter**: provider-specific adapter under `adapters/`
- **Branch**: `Experimental`
- **Config**: `experimental_mode.enabled = true`

### Model-Agnostic Baseline
- **Adapter**: none (model-agnostic)
- **Branch**: `main`
- **Config**: `experimental_mode.enabled = false`

### High-Reasoning Reference
- **Adapter**: optional provider-specific adapter
- **Branch**: `main`
- **Config**: role prompts only

## Running a Benchmark

1. Set up the test project (copy `examples/benchmark/task-{N}/` to a temp directory)
2. Configure `ai-ltc-config.json` with the target model
3. Run the task through the AI-LTC lifecycle
4. Collect logs from `.ai/logs/`
5. Run `python3 scripts/benchmark_analyzer.py /path/to/logs/`
6. Compare results across models

## Results Storage

Results are stored in `examples/benchmark/results/`:
- `results/provider-adapter-task1.json`
- `results/model-agnostic-task1.json`
- `results/high-reasoning-reference-task1.json`
- `results/comparison.md` (auto-generated)
