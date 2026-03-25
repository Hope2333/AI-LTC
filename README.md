# AI-LTC Templates

AI-LTC = `AI-LongTimeCoding(plan)`.

AI-LTC is a reusable collaboration framework for long-horizon AI-assisted software work.
It packages a practical operating model for staged GPT/Qwen collaboration:
- GPT defines architecture and intervenes only when high-cost design or optimization is justified
- Qwen handles the default day-to-day supervision, execution, and bounded iteration
- handoff, escalation, relay, and self-evolving-doc rules are made explicit so multi-session work can continue without rebuilding context each time

This repository is meant to be copied, adapted, and used as a planning-and-execution scaffold for other projects, not just as a prompt dump.

Public-ready note:
- v1 now avoids local-only path assumptions in the mainline docs and prompts
- archived v0 remains preserved as historical reference
- GitHub repo `Hope2333/AI-LTC` is currently the canonical remote backup and is planned for later public release after further review

## One-Click GitHub Deployment

Repository naming / description suggestion:
- repo name: `AI-LTC`
- description: `AI-LongTimeCoding(plan)`

One-click deploy with `gh` from this directory:

```sh
cd AI-LTC
git init -b main
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

Source basis: generalized from a long-running real repository before being cleaned for reuse
Source documents:
- `docs/ai-collaboration.md`
- `docs/ai-workbench.md`
- `docs/ai-relay.md`

Files:
- `archive/v0/`
- `FRAMEWORK-V1.md`
- `INIT-QWEN.md`
- `USE-CASES.md`
- `examples/collaboration-system/`
- `examples/collaboration-system/ROLE-QUICK-REFERENCE.md`
- `examples/collaboration-system/bootstrap-checklist.md`
- `examples/collaboration-system/install-example.md`
- `examples/collaboration-system/copy-into-new-repo.sh`
- `examples/collaboration-system/VERSION.md`
- `examples/collaboration-system/CHANGELOG.md`
- `shared-repo-contract.prompt.md`
- `AI-LTC-INIT-QUESTIONNAIRE.template.md`
- `ai-ltc-config.template.json`
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
2. If the target repo is upgrading from v0 or has no init resolver config, run `qwen-init-routing.prompt.md`
3. Choose the v1 role prompt:
   - `qwen-init-routing.prompt.md` when Qwen must first classify the project, confirm AI-LTC source mode, and recommend the next model/prompt
   - `gpt-bootstrap-architect.prompt.md` for early architecture / framework setup
   - `qwen-generalist-autopilot.prompt.md` for normal day-to-day work
   - `qwen-supervisory-generalist.prompt.md` for Qwen-led checkpoints / sequencing
   - `gpt-optimizer-auditor.prompt.md` only when explicitly needed
4. Use `00_HANDOFF.template.md` when GPT hands work to Qwen
5. Use `ESCALATION_REQUEST.template.md` when Qwen triggers `@ARCHITECT_HELP`
6. Use `continue-execution.prompt.md` when you want a stronger replacement for a bare `continue.` during an active execution session
7. Optionally append `human-addendum.template.md`

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
- if the project is a v0-to-v1 migration, or if no resolver config exists, treat Qwen init as required

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
- init-time resolver config via `.ai/system/ai-ltc-config.json`
- question-window style init intake via `AI-LTC-INIT-QUESTIONNAIRE.template.md`

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
A public-facing use-case guide now lives in `USE-CASES.md`.
That example has now been upgraded to the v1 GPT/Qwen staged framework.
It now also includes `ROLE-QUICK-REFERENCE.md` for fast operator selection.

Project default:
- for ongoing repository work, prefer `qwen-generalist-autopilot.prompt.md`
- for Qwen-led review / sequencing, prefer `qwen-supervisory-generalist.prompt.md`
- use `gpt-bootstrap-architect.prompt.md` only for explicit architecture/bootstrap work
- use `gpt-optimizer-auditor.prompt.md` only for explicit optimization, audit, refactor, or escalation work
- prefer narrow GitHub Actions validation over long local full builds when both can prove the same point
- keep local builds short and scoped for sanity checks, blocker isolation, and minimal repros
- do not hardcode AI-LTC local filesystem paths into project prompts or `.ai` files; resolve them through init config instead
- default resolver policy: prefer the local AI-LTC checkout first, fall back to `https://github.com/Hope2333/AI-LTC`, and let Qwen refresh the local checkout only when needed

Note:
These files are meant for reuse. Once copied into another repository, that repository's own `docs/` files and local-only `.ai/` lane files become the source of truth.
