# AI-LTC

[中文版](README.zh.md)

**AI-LongTerm Coordination** — A reusable framework for long-horizon AI collaboration.

> Turn multi-session AI work from chaotic handoffs into a stable, verifiable operating system.

## Why It Exists

Most AI coding workflows burn expensive models continuously, lose context between sessions, and have no recovery path when things go wrong. AI-LTC solves this with:

- **Staged model分工**: GPT designs architecture, Qwen executes day-to-day, GPT returns only for audits
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

Apply `qwen-init-routing.prompt.md` to your AI operator. It will:
- Classify your project state (greenfield / midstream / chaotic)
- Write resolver config
- Recommend the next model and prompt

### 3. Start working

- **Normal execution**: `qwen-generalist-autopilot.prompt.md`
- **Architecture bootstrap**: `gpt-bootstrap-architect.prompt.md`
- **Review/checkpoint**: `qwen-supervisory-generalist.prompt.md`

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
| Architect | `gpt-bootstrap-architect.prompt.md` | Initial design, skeleton setup |
| Generalist | `qwen-generalist-autopilot.prompt.md` | Day-to-day execution (default) |
| Supervisor | `qwen-supervisory-generalist.prompt.md` | Checkpoints, sequencing |
| Strategist | `gpt-corrective-strategist.prompt.md` | Architecture drift, long-range replanning |
| Optimizer | `gpt-optimizer-auditor.prompt.md` | Narrow audits, hard blockers |

## Lifecycle

```
INIT → HANDOFF_READY → EXECUTION → REVIEW → OPTIMIZER → EXECUTION
  │                                              │
  └──────────────────────────────────────────────┘
                                  ↓
                           CHECKPOINT → (new batch or close)
```

Each transition is validated against `kernel/state_machine.yaml`. Illegal transitions are rejected.

## Version History

| Tag | What Changed |
|---|---|
| `v1.5.3` | Kernel v0.1 + Runtime v0.1 + Demo CLI + public README rewrite |
| `v1.5.4` | Branch governance + benchmark framework + multi-session config |

## Project Structure

```
AI-LTC/
├── kernel/                    # Formal kernel (rules, schemas, state machine)
├── adapters/                  # Model-specific adapters (see BRANCH-GOVERNANCE.md)
│   └── qwen36/                # Qwen 3.6 Plus Preview (on preview branch)
├── .ai-template/              # Runtime template (copy to .ai/ in target projects)
├── examples/
│   ├── demo-cli/              # Minimum runnable demo (8 tests passing)
│   ├── collaboration-system/  # Copyable collaboration template
│   └── benchmark/             # Cross-model comparison tasks
├── scripts/                   # Validators and tools
├── BRANCH-GOVERNANCE.md       # Dual-branch responsibilities and merge rules
├── shared-repo-contract.prompt.md   # Common rules for all roles
├── qwen-*.prompt.md           # Qwen role prompts
├── gpt-*.prompt.md            # GPT role prompts
├── *.template.md              # Handoff, escalation, questionnaire templates
└── README.md / README.zh.md   # This file
```

## License

MIT. See [LICENSE](LICENSE).

## Contributing

Small, focused improvements preferred. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Community

- **Issues**: GitHub Issues
- **Discussions**: Recommended for questions and ideas
- **Discord / WeChat**: Not configured yet
