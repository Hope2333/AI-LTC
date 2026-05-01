# AI-LTC Templates

Extracted prompt templates for collaboration, checkpoint review, and long-range planning.

Source basis: generalized from a long-running real repository before being cleaned for reuse
Source documents:
- `docs/ai-collaboration.md`
- `docs/ai-workbench.md`
- `docs/ai-relay.md`

Files:
- `examples/collaboration-system/`
- `examples/collaboration-system/bootstrap-checklist.md`
- `examples/collaboration-system/install-example.md`
- `examples/collaboration-system/copy-into-new-repo.sh`
- `examples/collaboration-system/VERSION.md`
- `examples/collaboration-system/CHANGELOG.md`
- `shared-repo-contract.prompt.md`
- `lower-cost-execution.prompt.md`
- `lower-cost-autopilot.prompt.md`
- `checkpoint-review.prompt.md`
- `supervisory-evaluation-planning.prompt.md`
- `strategic-checkpoint-long-horizon.prompt.md`
- `long-range-planning.prompt.md`
- `continue-execution.prompt.md`
- `human-addendum.template.md`

Recommended composition:
1. Apply `shared-repo-contract.prompt.md`
2. Apply one role-specific prompt
3. Use `continue-execution.prompt.md` when you want a stronger replacement for a bare `continue.` during an active execution session
4. Optionally append `human-addendum.template.md`

Shared contract covers:
- read order through `docs/ai-relay.md`
- local-only `.ai/` lane state
- missing `.ai/` recovery rule
- bridge-note rule for `docs/modernization/*`
- non-commit scope for `.omx/`, `.ai/`, `.sisyphus/`, and `AGENTS.md`
- bounded-pass / anti-loop safety rules
- fixed stop phrases for machine-readable early exits
- fixed status fields for machine-readable summaries
- structured-output defaults
- preference for GitHub Actions as the primary clean proof path when available

Standard stop phrases:
- `STOP_NO_NEW_EVIDENCE`
- `STOP_REPEATED_BLOCKER`
- `STOP_BOUNDED_PASS_EXHAUSTED`
- `STOP_WAIT_NO_PROGRESS`
- `STOP_REVIEW_GATE_REACHED`

Standard status fields:
- `Status`
- `Decision`
- `Stop Reason`
- `Next Action`

A copyable collaboration-system example lives under `examples/collaboration-system/`.

Project default:
- for this repository, prefer `lower-cost-autopilot.prompt.md` on the execution side
- use high-reasoning planning prompts for checkpoint, evaluation, and long-range planning roles
- prefer narrow GitHub Actions validation over long local full builds when both can prove the same point
- keep local builds short and scoped for sanity checks, blocker isolation, and minimal repros

Note:
These files are meant for reuse. Once copied into another repository, that repository's own `docs/` files and local-only `.ai/` lane files become the source of truth.
