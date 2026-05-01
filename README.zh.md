# AI-LTC

[English Version](README.md)

**AI-LongTerm Coordination** — 面向长期 AI 协作的可复用框架。

> 把 AI 协作从混乱交接变成稳定、可验证的操作系统。

## 为什么存在

大多数 AI 编码工作流持续燃烧昂贵模型、会话间丢失上下文、出错时没有恢复路径。AI-LTC 通过以下方式解决：

- **分阶段角色分工**：architect 角色负责结构，generalist 角色负责日常执行，optimizer 角色只在有边界的审计中回归
- **文件化状态**：上下文存在 `.ai/state.json`，不在对话历史里
- **内核验证转移**：每次阶段变更都经过形式化状态机规则验证
- **错误恢复**：6 种错误类型，每种有定义好的检测和恢复策略

## 快速开始

### 1. 安装到你的项目

```bash
# 克隆 AI-LTC 到项目
git clone https://github.com/Hope2333/AI-LTC.git .ai/AI-LTC

# 复制运行时模板
cp -r .ai/AI-LTC/.ai-template/* .ai/

# 配置
编辑 .ai/system/ai-ltc-config.json
```

### 2. 运行初始化

对 AI 操作者组合应用 `prompts/phases/init.prompt.md` 以及对应 role / adapter 片段，它会：
- 分类项目状态（全新 / 半道 / 混沌）
- 写入 resolver 配置
- 推荐下一个模型和 prompt

### 3. 开始工作

- **日常执行**：`prompts/roles/generalist.prompt.md` + `prompts/phases/execution.prompt.md`
- **架构引导**：`prompts/roles/architect.prompt.md` + `prompts/phases/init.prompt.md`
- **审查/检查点**：`prompts/roles/supervisor.prompt.md` + `prompts/phases/checkpoint.prompt.md`

旧 prompt 文件名仍然保留作为兼容入口。Experimental 语义线已经开始在 `prompts/` 下并行引入 role / phase / constraint / adapter 结构。

### 试用 Demo

```bash
cd examples/demo-cli
python main.py greet --name Alice
python main.py wordcount hello world from AI-LTC
python -m pytest tests/test_main.py -v  # 8 个测试，全部通过
```

## 架构

### 内核（规则）
| 文件 | 用途 |
|---|---|
| `kernel/state_schema.json` | 唯一真相源 — 唯一合法的状态结构 |
| `kernel/control.yaml` | 权限链：谁能写什么 |
| `kernel/state_machine.yaml` | 合法的阶段转移 |
| `kernel/error_model.yaml` | 6 种错误类型 + 恢复策略 |
| `kernel/arbitration.yaml` | 智能体分歧时的冲突解决 |

### 运行时（状态）
| 文件 | 用途 |
|---|---|
| `.ai/state.json` | 当前运行时状态（SSOT） |
| `.ai/system/ai-ltc-config.json` | Resolver 配置、模型路由、语言策略 |
| `.ai/logs/` | 决策、状态、错误日志 |
| `.ai/history/snapshots/` | 用于回滚的状态快照 |

### Prompts（角色）
| 角色 | Prompt | 何时使用 |
|---|---|---|
| 架构师 | `prompts/roles/architect.prompt.md` | 初始设计、骨架搭建 |
| 全能工程师 | `prompts/roles/generalist.prompt.md` | 日常执行（默认） |
| 监督员 | `prompts/roles/supervisor.prompt.md` | 检查点、排序 |
| 策略师 | `prompts/roles/strategist.prompt.md` | 架构漂移、长期重规划 |
| 优化师 | `prompts/roles/optimizer.prompt.md` | 窄审计、硬阻塞 |

Experimental 迁移参考：
- `docs/PROMPT-MIGRATION.md`
- `docs/PROMPT-DECOUPLING-PLAN.md`
- `prompts/_mapping/legacy-to-role-phase-adapter.md`
- `PROMPTS.md`

## 生命周期

```
INIT → HANDOFF_READY → EXECUTION → REVIEW → OPTIMIZER → EXECUTION
  │                                              │
  └──────────────────────────────────────────────┘
                                  ↓
                           CHECKPOINT →（新批次或关闭）
```

每次转移都经过 `kernel/state_machine.yaml` 验证。非法转移会被拒绝。

## OML 集成（v1.5.10+）

AI-LTC 通过轻量 bridge 与 oh-my-litecode（OML）集成：

- **AI-LTC = Brain**：状态机、记忆、错误恢复、跨仓库同步
- **OML = Body**：插件加载、MCP 网关、会话管理、worker pool、hooks engine

架构：`docs/OML-BRIDGE-ARCHITECTURE.md`
集成计划：`docs/OML-INTEGRATION-PLAN.md`
平台适配器：`docs/OML-PLUGIN-ADAPTER.md`
设计原则：`docs/BRAIN-BODY-SEPARATION.md`

## Experimental 方向

AI-LTC 现在区分两层语义：

- `main`：稳定框架层
- `Experimental`：当前实际使用的实验分支

AI-LTC 使用 `main` 承载稳定框架，使用 `Experimental` 承载 prompt 重构、adapter 实验和带时间版本的模型/工具评估。

Experimental 负责承载适配器工作、prompt 迁移骨架和带时间戳的评估记录，稳定后再抽象回流 `main`。

### 当前状态：2026-04-28

- `Experimental` 已成立，应视为当前实验分支，不再作为未来重命名目标。
- Prompt 迁移处于 mapping 阶段；暂不删除旧 prompt 入口。
- Evaluation 已进入 schema v0.2，模型、工具、任务、结果分别有 schema 草案。
- 工具评估必须区分 surface、harness、access model、permission model 和 known failure modes。
- 模型评估必须记录 deployment fit，再影响 routing 判断。

规范文档：
- `docs/BRANCH-REFACTOR-PLAN.md`
- `docs/PROMPT-DECOUPLING-PLAN.md`
- `docs/EVALUATION-SCHEMA.md`
- `docs/AI-LTC-vs-OML-BOUNDARY.md`
- `prompts/_mapping/legacy-to-role-phase-adapter.md`

## Evaluation v0.2

评估记录位于 `evaluation/`。原始记录保持实验性质，只有被总结成稳定结论后才进入框架治理。

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

证据流：

```text
OML run evidence
-> Experimental evaluation results
-> AI-LTC main summary / routing principles
```

Body 产生证据。Brain 解释证据。`main` 只吸收稳定原则。

本地校验：

```bash
make validate-evaluation
make validate-prompts
make validate-provider-naming
make validate-ts-imports
make validate-config-registry
make check
```

`make validate-evaluation` 检查 schema 形状、部分字段类型、引用关系、`tested_at` 日期和 freshness 窗口，不生成评分，也不自动化 evaluation。`make validate-prompts` 校验旧 prompt mapping 的引用关系。`make validate-provider-naming` 校验 provider-specific 术语只出现在兼容、adapter、mapping 或证据表面。`make validate-ts-imports` 在不依赖 TypeScript toolchain 的情况下校验 bridge 和 adapter 文件里的本地 TypeScript import。`make validate-config-registry` 校验 `VERSION`、`cross-repo-registry.json` 和 `ai-ltc-config.template.json` 版本一致。`make check` 会运行全部校验和现有 bridge 集成冒烟测试。

CI 通过 `.github/workflows/check.yml` 运行 `make check`。

## 版本历史

| Tag | 变更内容 |
|---|---|
| `v1.5.3` | Kernel v0.1 + Runtime v0.1 + Demo CLI + public README rewrite |
| `v1.5.4` | 分支治理 + 对照验证框架 + 多会话配置 |
| `unreleased` | 2026-04-28 Experimental 对齐：evaluation schema v0.2、旧 prompt mapping、工具 harness 字段、模型 deployment-fit 字段、AI-LTC/OML 证据流澄清 |

## 项目结构

```
AI-LTC/
├── kernel/                    # 形式化内核（规则、schema、状态机）
├── adapters/                  # 模型特定适配器（Experimental lane）
│   └── */                     # provider / platform-specific adapters
├── evaluation/                # Experimental 评估注册表、schema、任务与结果
│   ├── models/                # 带时间版本的模型候选
│   ├── tools/                 # 工具 / harness surface 记录
│   ├── tasks/                 # 可复用评估任务
│   ├── results/               # 带日期的实验结果
│   └── schemas/               # v0.2 schema 草案
├── bridge/                    # OML 集成 bridge 层
│   ├── index.ts               # Bridge 入口
│   ├── oml-bridge.ts          # 核心 bridge 逻辑
│   ├── event-map.yaml         # 事件映射表
│   ├── capability-registry.ts # 插件能力注册表
│   ├── memory-adapter.ts      # 记忆 bridge
│   ├── context-compact.ts     # 上下文压缩
│   ├── cross-session.ts       # 跨会话共享
│   └── protocol.md            # Task/result 协议
├── .ai-template/              # 运行时模板（复制到目标项目的 .ai/）
├── examples/
│   ├── demo-cli/              # 最小可运行 demo（8 个测试通过）
│   ├── collaboration-system/  # 可复制的协作系统模板
│   └── benchmark/             # 跨模型对照任务
├── scripts/                   # 验证器和工具
├── BRANCH-GOVERNANCE.md       # 双分支职责和合并规则
├── docs/BRANCH-REFACTOR-PLAN.md # 分支重构设计
├── prompts/                   # 旧入口 + 新迁移骨架
│   ├── roles/                 # 角色抽象
│   ├── phases/                # 阶段片段
│   ├── constraints/           # 共享约束
│   ├── adapters/              # 提供方/平台差异
│   ├── _mapping/              # 旧入口到 role/phase/adapter 的映射
│   └── *.prompt.md            # 旧兼容入口
├── docs/PROMPT-DECOUPLING-PLAN.md # prompt 解耦设计
├── docs/EVALUATION-SCHEMA.md  # 评估数据结构要求
├── docs/AI-LTC-vs-OML-BOUNDARY.md # 规范版边界文档
├── *.template.md              # 交接、升级、问卷模板
└── README.md / README.zh.md   # 本文件
```

## 许可证

MIT。详见 [LICENSE](LICENSE)。

## 贡献

优先欢迎小而清晰的改进。见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 社区

- **Issues**：GitHub Issues
- **Discussions**：推荐作为提问和讨论的第一入口
- **Discord / 微信群**：暂未配置
