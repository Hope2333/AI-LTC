# AI-LTC

[English Version](README.md)

**AI-LongTerm Coordination** — 面向长期 AI 协作的可复用框架。

> 把 AI 协作从混乱交接变成稳定、可验证的操作系统。

## 为什么存在

大多数 AI 编码工作流持续燃烧昂贵模型、会话间丢失上下文、出错时没有恢复路径。AI-LTC 通过以下方式解决：

- **分阶段模型分工**：GPT 设计架构，Qwen 日常执行，GPT 只在审计时回归
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

对 AI 操作者应用 `qwen-init-routing.prompt.md`，它会：
- 分类项目状态（全新 / 半道 / 混沌）
- 写入 resolver 配置
- 推荐下一个模型和 prompt

### 3. 开始工作

- **日常执行**：`qwen-generalist-autopilot.prompt.md`
- **架构引导**：`gpt-bootstrap-architect.prompt.md`
- **审查/检查点**：`qwen-supervisory-generalist.prompt.md`

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
| 架构师 | `gpt-bootstrap-architect.prompt.md` | 初始设计、骨架搭建 |
| 全能工程师 | `qwen-generalist-autopilot.prompt.md` | 日常执行（默认） |
| 监督员 | `qwen-supervisory-generalist.prompt.md` | 检查点、排序 |
| 策略师 | `gpt-corrective-strategist.prompt.md` | 架构漂移、长期重规划 |
| 优化师 | `gpt-optimizer-auditor.prompt.md` | 窄审计、硬阻塞 |

## 生命周期

```
INIT → HANDOFF_READY → EXECUTION → REVIEW → OPTIMIZER → EXECUTION
  │                                              │
  └──────────────────────────────────────────────┘
                                  ↓
                           CHECKPOINT →（新批次或关闭）
```

每次转移都经过 `kernel/state_machine.yaml` 验证。非法转移会被拒绝。

## 版本历史

| Tag | 变更内容 |
|---|---|
| `v1.5.3` | Kernel v0.1 + Runtime v0.1 + Demo CLI + public README rewrite |

## 项目结构

```
AI-LTC/
├── kernel/                    # 形式化内核（规则、schema、状态机）
├── .ai-template/              # 运行时模板（复制到目标项目的 .ai/）
├── examples/
│   ├── demo-cli/              # 最小可运行 demo（8 个测试通过）
│   └── collaboration-system/  # 可复制的协作系统模板
├── scripts/                   # 验证器和工具
├── shared-repo-contract.prompt.md   # 所有角色的公共规则
├── qwen-*.prompt.md           # Qwen 角色 prompt
├── gpt-*.prompt.md            # GPT 角色 prompt
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
