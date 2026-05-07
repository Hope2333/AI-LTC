# AI-LTC

[中文版](README.zh.md)

**AI-LongTerm Coordination** — A reusable framework for long-horizon AI collaboration.

> Turn multi-session AI work from chaotic handoffs into a stable, verifiable operating system.

## Why It Exists

Most AI coding workflows burn expensive models continuously, lose context between sessions, and have no recovery path when things go wrong. AI-LTC solves this with:

- **Staged role separation**: architect roles handle structure, generalist roles execute day-to-day, optimizer roles return only for bounded audits
- **File-based state**: Context lives in `.ai/state.json`, not in conversation history
- **Kernel-verified transitions**: Every phase change validated against formal state machine rules
- **Error recovery**: 6 error types with defined detection and recovery strategies
- **Multi-session orchestration**: Parallel independent sessions via OpenCode `task()`

## Quick Start

### 1. Install into your project

```bash
# Clone AI-LTC into your project
git clone https://github.com/Hope2333/AI-LTC.git .ai/AI-LTC

# Copy the runtime template
cp -r .ai/AI-LTC/.ai-template/* .ai/

# Configure
edit .ai/system/ai-ltc-config.json
```

### 2. Run init

Apply `prompts/phases/init.prompt.md` with the appropriate role and adapter fragments to your AI operator. It will:
- Classify your project state (greenfield / midstream / chaotic)
- Write resolver config
- Recommend the next model and prompt

### 3. Start working

- **Normal execution**: `prompts/roles/generalist.prompt.md` + `prompts/phases/execution.prompt.md`
- **Architecture bootstrap**: `prompts/roles/architect.prompt.md` + `prompts/phases/init.prompt.md`
- **Review/checkpoint**: `prompts/roles/supervisor.prompt.md` + `prompts/phases/checkpoint.prompt.md`

Legacy prompt filenames remain supported. The Experimental lane now also seeds a role / phase / constraint / adapter prompt layout under `prompts/` for coexistence migration.

### Try the Demo

```bash
cd examples/demo-cli
python main.py greet --name Alice
python main.py wordcount hello world from AI-LTC
python -m pytest tests/test_main.py -v  # 8 tests, all passing
```

## Architecture

### Kernel (Rules)
| File | Purpose |
|---|---|
| `kernel/state_schema.json` | SSOT — the only valid state structure |
| `kernel/control.yaml` | Authority chain: who can write what |
| `kernel/state_machine.yaml` | Legal phase transitions |
| `kernel/error_model.yaml` | 6 error types + recovery strategies |
| `kernel/arbitration.yaml` | Conflict resolution when agents disagree |

### Runtime (State)
| File | Purpose |
|---|---|
| `.ai/state.json` | Current runtime state (SSOT) |
| `.ai/system/ai-ltc-config.json` | Resolver config, model routing, language policy |
| `.ai/logs/` | Decision, state, and error logs |
| `.ai/history/snapshots/` | State snapshots for rollback |

### Prompts (Roles)
| Role | Prompt | When to Use |
|---|---|---|
| Architect | `prompts/roles/architect.prompt.md` | Initial design, skeleton setup |
| Generalist | `prompts/roles/generalist.prompt.md` | Day-to-day execution (default) |
| Supervisor | `prompts/roles/supervisor.prompt.md` | Checkpoints, sequencing |
| Strategist | `prompts/roles/strategist.prompt.md` | Architecture drift, long-range replanning |
| Optimizer | `prompts/roles/optimizer.prompt.md` | Narrow audits, hard blockers |

Experimental migration references:
- `docs/PROMPT-MIGRATION.md`
- `docs/PROMPT-DECOUPLING-PLAN.md`
- `PROMPTS.md`

## Lifecycle

```
INIT → HANDOFF_READY → EXECUTION → REVIEW → OPTIMIZER → EXECUTION
  │                                              │
  └──────────────────────────────────────────────┘
                                  ↓
                           CHECKPOINT → (new batch or close)
```

Each transition is validated against `kernel/state_machine.yaml`. Illegal transitions are rejected.

## OML Integration (v1.5.10+)

AI-LTC integrates with oh-my-litecode (OML) via a thin adapter bridge:
- **AI-LTC = Brain**: State machine, memory, error recovery, cross-repo sync
- **OML = Body**: Plugin loading, MCP gateway, session management, worker pool, hooks engine

Architecture: `docs/OML-BRIDGE-ARCHITECTURE.md`
Integration plan: `docs/OML-INTEGRATION-PLAN.md`
Platform adapters: `docs/OML-PLUGIN-ADAPTER.md`
Design principles: `docs/BRAIN-BODY-SEPARATION.md`

## Experimental Direction

AI-LTC now distinguishes between:

- `main`: stable framework layer
- `Experimental`: the active experimental branch

AI-LTC uses `main` as the stable framework branch and `Experimental` as the branch for prompt refactoring, adapter experiments, and time-versioned model/tool evaluation.

The Experimental lane is where adapter work, prompt migration scaffolding, and time-scoped evaluation records land before they are abstracted into `main`.

### Current State: 2026-04-28

- `Experimental` is established and should be treated as the active experimental branch, not a future rename target.
- Prompt migration is in the mapping stage. Do not delete legacy prompt entrypoints yet.
- Evaluation is on schema v0.2, with separate model, tool, task, and result schema drafts.
- Tool evaluation records must distinguish surface, harness, access model, permission model, and known failure modes.
- Model evaluation records must include deployment fit before they influence routing decisions.

Canonical design references:
- `docs/BRANCH-REFACTOR-PLAN.md`
- `docs/PROMPT-DECOUPLING-PLAN.md`
- `docs/EVALUATION-SCHEMA.md`
- `docs/AI-LTC-vs-OML-BOUNDARY.md`
- `docs/HOME-AI-CONSUMER-FRAMEWORK.md`
- `prompts/_mapping/legacy-to-role-phase-adapter.md`

## Evaluation v0.2

Evaluation records live under `evaluation/` and stay experimental until summarized into stable framework conclusions.

```text
evaluation/
├── models/registry.yaml
├── tools/registry.yaml
├── tasks/registry.yaml
├── results/2026-04.yaml
└── schemas/
    ├── model.schema.yaml
    ├── tool.schema.yaml
    ├── task.schema.yaml
    └── result.schema.yaml
```

Evidence flow:

```text
OML run evidence
-> Experimental evaluation results
-> AI-LTC main summary / routing principles
```

Body produces evidence. Brain interprets evidence. `main` absorbs only stable principles.

Local validation:

```bash
make validate-evaluation
make validate-prompts
make validate-provider-naming
make validate-ts-imports
make validate-config-registry
make check
```

`make validate-evaluation` validates schema shape, selected field types, references, `tested_at` dates, freshness windows, and explicit `freshness_status` bucket consistency; it does not generate scores or automate evaluation. `make validate-prompts` validates legacy mapping references. `make validate-provider-naming` checks that provider-specific terms stay inside compatibility, adapter, mapping, or evidence surfaces. `make validate-ts-imports` validates local TypeScript imports in bridge and adapter files without requiring a TypeScript toolchain. `make validate-config-registry` checks `VERSION`, `cross-repo-registry.json`, and `ai-ltc-config.template.json` stay aligned. `make check` runs all validations plus the existing bridge integration smoke test.

CI runs `make check` through `.github/workflows/check.yml`.

## Version History

| Tag | What Changed |
|---|---|
| `v1.5.3` | Kernel v0.1 + Runtime v0.1 + Demo CLI + public README rewrite |
| `v1.5.4` | Branch governance + benchmark framework + multi-session config |
| `v1.5.5` | Context overflow, circuit breakers, transition hooks, memory system, cross-repo management |
| `v1.5.6` | Code quality gate: thresholds, regression rules, execution integration |
| `v1.5.7` | enve-derived templates: multi-distro CI, packaging workflows, version adaptation, execution prompts, dependency ledger, manual testing |
| `v1.5.11` | OML bridge integration: bridge layer, platform adapters (OpenCode, Claude Code, Aider), memory/context bridge, deployment scripts |
| `v1.5.12` | Enhanced task system (priority, tags, QA, evidence, timestamps), unified security model (hash chain, audit trail, secret detection, tamper detection, atomic writes) |
| `v1.5.13` | enve-derived templates: cross-CLI adapter architecture, OML Core spec, AI-LTC integration plan |
| `v1.5.14` | Upstream throttle retry (OpenCode Zen Alibaba routing), provider line rename, AI-LTC Todo Tasks document |
| `v1.5.15` | Reasoning efficiency kernel: Caveman Compression, Chain-of-Draft (Zoom), Think Deep Not Just Long (Google), Headroom. Prompts moved to `prompts/`. Intuition file system. |
| `unreleased` | 2026-04-28 Experimental alignment: evaluation schema v0.2, legacy prompt mapping, harness/tool fields, model deployment-fit fields, and AI-LTC/OML evidence-flow clarification. |

## Project Structure

```
AI-LTC/
├── kernel/                    # Formal kernel (rules, schemas, state machine)
├── adapters/                    # Model-specific adapters (Experimental lane)
│   ├── */                       # Provider- or platform-specific adapters
│   ├── registry.ts              # Platform adapter registry
│   └── types.ts                 # Shared adapter types
├── evaluation/                  # Experimental registries, schemas, tasks, and dated results
│   ├── models/                  # Time-versioned model candidates
│   ├── tools/                   # Tool/harness surface records
│   ├── tasks/                   # Reusable evaluation task definitions
│   ├── results/                 # Dated experiment results
│   └── schemas/                 # v0.2 record-family schema drafts
├── bridge/                      # OML integration bridge layer
│   ├── index.ts                 # Bridge entry point
│   ├── oml-bridge.ts            # Core bridge logic
│   ├── event-map.yaml           # Event mapping table
│   ├── capability-registry.ts   # Plugin capability registry
│   ├── memory-adapter.ts        # Memory bridge
│   ├── context-compact.ts       # Context compaction
│   ├── cross-session.ts         # Cross-session sharing
│   └── protocol.md              # Task/result protocol
├── .ai-template/              # Runtime template (copy to .ai/ in target projects)
├── examples/
│   ├── demo-cli/              # Minimum runnable demo (8 tests passing)
│   ├── collaboration-system/  # Copyable collaboration template
│   └── benchmark/             # Cross-model comparison tasks
├── scripts/                   # Validators and tools
├── prompts/                   # Legacy entrypoints + new migration scaffold
│   ├── roles/                 # Role abstractions
│   ├── phases/                # Phase fragments
│   ├── constraints/           # Shared boundaries
│   ├── adapters/              # Provider/platform deltas
│   ├── _mapping/              # Legacy-to-role/phase/adapter coexistence map
│   └── *.prompt.md            # Legacy compatibility entrypoints
├── kernel/reasoning-policy.yaml  # Reasoning efficiency rules (Caveman, CoD, DTR, Headroom)
├── PROMPTS.md                 # Root prompt guide (minimal)
├── BRANCH-GOVERNANCE.md       # Dual-branch responsibilities and merge rule
├── docs/BRANCH-SEMANTICS.md   # Stable vs Experimental semantics
├── docs/BRANCH-REFACTOR-PLAN.md # Iteration 1 branch refactor design
├── docs/PROMPT-MIGRATION.md   # Legacy prompt coexistence plan
├── docs/PROMPT-DECOUPLING-PLAN.md # Iteration 1 prompt decoupling design
├── docs/EVALUATION-SCHEMA.md  # Evaluation data requirements
├── docs/AI-LTC-vs-OML-BOUNDARY.md # Canonical Brain/Body ownership doc
```

## License

MIT. See [LICENSE](LICENSE).

## Contributing

Small, focused improvements preferred. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Community

- **Issues**: GitHub Issues
- **Discussions**: Recommended for questions and ideas
- **Discord / WeChat**: Not configured yet
