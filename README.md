# AI-LTC Templates

AI-LTC = `AI-LongTimeCoding(plan)`.

## One-Click GitHub Deployment

Repository naming / description suggestion:
- repo name: `AI-LTC`
- description: `AI-LongTimeCoding(plan)`

One-click deploy with `gh` from this directory:

```sh
cd /home/miao/develop/AI-LTC
git init
git add .
git commit -m "Initial AI-LTC v1 framework."
gh repo create AI-LTC --private --source=. --remote=origin --push --description "AI-LongTimeCoding(plan)"
```

Reusable AI prompt for deployment:

```text
Initialize this directory as a git repository, create a GitHub repo with gh, use the repo name `AI-LTC`, set the description to `AI-LongTimeCoding(plan)`, add the files, create the first commit, set `origin`, and push the current branch.
```

Current framework version: `v1`

This directory now follows the v1 operating model:
- GPT appears only when explicitly needed:
  - early project bootstrap / architecture
  - later optimization / audit / hard-architecture intervention
- Qwen is the default day-to-day operator for:
  - supervision
  - evaluation
  - execution
- older flat prompts and conventions are archived under `archive/v0/`

Source repository: `/home/miao/develop/enve`
Source documents:
- `docs/ai-collaboration.md`
- `docs/ai-workbench.md`
- `docs/ai-relay.md`

Files:
- `archive/v0/`
- `FRAMEWORK-V1.md`
- `INIT-QWEN.md`
- `examples/collaboration-system/`
- `examples/collaboration-system/ROLE-QUICK-REFERENCE.md`
- `examples/collaboration-system/bootstrap-checklist.md`
- `examples/collaboration-system/install-example.md`
- `examples/collaboration-system/copy-into-new-repo.sh`
- `examples/collaboration-system/VERSION.md`
- `examples/collaboration-system/CHANGELOG.md`
- `shared-repo-contract.prompt.md`
- `00_HANDOFF.template.md`
- `ESCALATION_REQUEST.template.md`
- `gpt-bootstrap-architect.prompt.md`
- `gpt-optimizer-auditor.prompt.md`
- `qwen-init-routing.prompt.md`
- `qwen-generalist-autopilot.prompt.md`
- `qwen-supervisory-generalist.prompt.md`
- `lower-cost-execution.prompt.md`
- `qwen-lower-cost-autopilot.prompt.md`
- `checkpoint-review.prompt.md`
- `supervisory-evaluation-planning.prompt.md`
- `strategic-checkpoint-long-horizon.prompt.md`
- `long-range-planning.prompt.md`
- `continue-execution.prompt.md`
- `human-addendum.template.md`

Recommended composition:
1. Apply `shared-repo-contract.prompt.md`
2. Choose the v1 role prompt:
   - `qwen-init-routing.prompt.md` when Qwen must first classify the project and recommend the next model/prompt
   - `gpt-bootstrap-architect.prompt.md` for early architecture / framework setup
   - `qwen-generalist-autopilot.prompt.md` for normal day-to-day work
   - `qwen-supervisory-generalist.prompt.md` for Qwen-led checkpoints / sequencing
   - `gpt-optimizer-auditor.prompt.md` only when explicitly needed
3. Use `00_HANDOFF.template.md` when GPT hands work to Qwen
4. Use `ESCALATION_REQUEST.template.md` when Qwen triggers `@ARCHITECT_HELP`
5. Use `continue-execution.prompt.md` when you want a stronger replacement for a bare `continue.` during an active execution session
6. Optionally append `human-addendum.template.md`

v1 core logic:
- expensive brain does design
- fast hands do execution
- specialists are called only on demand

Role split:
- GPT = architect or optimizer/auditor
- Qwen = primary generalist operator

Default policy:
- ongoing supervision, evaluation, and execution should default to Qwen
- GPT should not hover continuously over active delivery
- exception: for a new or ambiguous project at the very beginning, prefer GPT first for the initial long-range system design
- if Qwen is taking over after framework deployment, let it run `qwen-init-routing.prompt.md` first to classify the project as `greenfield`, `midstream`, or `chaotic`

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
- v1 handoff protocol via `00_HANDOFF.md`
- v1 escalation trigger via `@ARCHITECT_HELP` and `ESCALATION_REQUEST.md`
- self-evolving docs rule for Qwen-updated lane / framework docs

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
That example has now been upgraded to the v1 GPT/Qwen staged framework.
It now also includes `ROLE-QUICK-REFERENCE.md` for fast operator selection.

Project default:
- for ongoing repository work, prefer `qwen-generalist-autopilot.prompt.md`
- for Qwen-led review / sequencing, prefer `qwen-supervisory-generalist.prompt.md`
- use `gpt-bootstrap-architect.prompt.md` only for explicit architecture/bootstrap work
- use `gpt-optimizer-auditor.prompt.md` only for explicit optimization, audit, refactor, or escalation work
- prefer narrow GitHub Actions validation over long local full builds when both can prove the same point
- keep local builds short and scoped for sanity checks, blocker isolation, and minimal repros

Note:
These are extracted copies for reuse. The repository-side source of truth remains the `docs/` files inside `enve` plus the local-only `.ai/` lane files resolved through `docs/ai-relay.md`.
