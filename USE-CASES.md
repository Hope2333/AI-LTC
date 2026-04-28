# USE CASES

AI-LTC is role-first. Pick the role and phase needed for the work, then bind that role to a provider/model through an adapter or local runtime policy.

## Role Defaults

| Situation | Default Role | Prompt Surface |
|---|---|---|
| New or unclear repository | Architect | `prompts/roles/architect.prompt.md` + `prompts/phases/init.prompt.md` |
| Existing repository with clear next work | Generalist | `prompts/roles/generalist.prompt.md` + `prompts/phases/execution.prompt.md` |
| Checkpoint, sequencing, or blocker review | Supervisor | `prompts/roles/supervisor.prompt.md` + `prompts/phases/checkpoint.prompt.md` |
| Architecture drift or long-range replanning | Strategist | `prompts/roles/strategist.prompt.md` + `prompts/phases/review.prompt.md` |
| Narrow high-value audit or unblock | Optimizer | `prompts/roles/optimizer.prompt.md` + `prompts/phases/review.prompt.md` |

Legacy provider-named prompt files remain compatibility entrypoints only. Their mappings live in `prompts/_mapping/legacy-to-role-phase-adapter.md`.

## Use Case 1: Greenfield Bootstrap

Use when the repository does not yet have a stable skeleton, boundaries, or first lane.

Flow:

1. Run the architect role with the init phase.
2. Produce `00_HANDOFF.md`.
3. Define the first lane and executable next action.
4. Hand off to the generalist role for execution.

Success condition:

- skeleton exists
- boundaries are explicit
- first execution batch is small and testable

## Use Case 2: Existing Repository Init

Use when the repository already works but lacks AI-LTC state, resolver config, or clear lane documents.

Flow:

1. Run init phase with a generalist or supervisor role.
2. Classify project state.
3. Write resolver/config facts.
4. Start execution only after the current lane is explicit.

Success condition:

- source mode is known
- next action is concrete
- no architecture role is invoked without a real architecture need

## Use Case 3: Normal Daily Execution

Use when the next task is bounded implementation, cleanup, docs upkeep, or local verification.

Flow:

1. Run the generalist role with the execution phase.
2. Keep changes narrow.
3. Verify with the smallest proof that supports the claim.
4. Update lane docs only when the real sequence changes.

Success condition:

- diff is scoped
- verification evidence exists
- no unnecessary role escalation occurred

## Use Case 4: Review Gate

Use after meaningful new evidence, a completed batch, or a possible blocker.

Flow:

1. Run the supervisor role with checkpoint/review phase.
2. Decide continue, narrow, pause, escalate, or close.
3. Preserve evidence and the next action.

Success condition:

- blocker status is clear
- next action is explicit
- stale assumptions are removed

## Use Case 5: Escalation

Use only when the active lane hits an architecture-grade blocker, repeated failure, or high-value audit need.

Flow:

1. Generalist or supervisor writes `ESCALATION_REQUEST.md`.
2. Optimizer or strategist reads only the narrowed evidence.
3. Intervention returns a bounded plan or fix.
4. Control returns to the generalist role.

Success condition:

- escalation is narrow
- intervention does not become an always-on execution lane
- return instructions are actionable

## Use Case 6: Evaluation Update

Use when a model, tool, prompt surface, or adapter claim needs dated evidence.

Flow:

1. Record the candidate in `evaluation/models/` or `evaluation/tools/`.
2. Define or reuse a task from `evaluation/tasks/`.
3. Record dated results in `evaluation/results/`.
4. Run `make validate-evaluation`.

Success condition:

- `tested_at` is present
- source/evidence is traceable
- raw results are not promoted into mainline policy without summary

## Routing Rule

Do not choose a provider first. Choose:

1. the role
2. the phase
3. the constraints
4. the adapter/provider delta

Then run the smallest verification path that proves the result.
