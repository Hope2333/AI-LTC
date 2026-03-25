# AI-LTC 模板说明

AI-LTC = `AI-LongTimeCoding(plan)`。

AI-LTC 是一套面向长期 AI 辅助开发的可复用协作框架。
它把分阶段的 GPT / Qwen 协作方式沉淀成一套可以复制、改造、持续演化的工作骨架：
- GPT 负责高成本的架构设计，以及按需介入的优化 / 审计
- Qwen 负责默认的日常评估、监督、执行与持续推进
- 交接、升级、relay、文档自进化等规则都被显式写出来，减少跨会话和跨模型时的上下文重建成本

这个仓库的目标不是单纯堆提示词，而是提供一套可以移植到其他项目中的长期协作脚手架。

公开前说明：
- v1 主线文档和 prompt 现在尽量避免本地私有路径假设
- `archive/v0/` 继续作为历史归档保留
- GitHub 仓库 `Hope2333/AI-LTC` 当前作为规范远端备份，后续在进一步检查和整理后计划开放给公众

## 一键部署到 GitHub

仓库命名 / 说明建议：
- 仓库名：`AI-LTC`
- 描述：`AI-LongTimeCoding(plan)`

在当前目录使用 `gh` 一键部署：

```sh
cd AI-LTC
git init -b main
git add .
git commit -m "Initial AI-LTC v1 framework."
gh repo create AI-LTC --private --source=. --remote=origin --push --description "AI-LongTimeCoding(plan)"
```

可复用提示词：

```text
Initialize this directory as a git repository, create a GitHub repo with gh, use the repo name `AI-LTC`, set the description to `AI-LongTimeCoding(plan)`, add the files, create the first commit, set `origin`, and push the current branch.
```

当前框架版本：`v1`

这个目录现在采用 v1 协作模型：
- GPT 默认不常驻，只在你明确需要时出现
- GPT 主要扮演：
  - 初期总架构师
  - 后期优化师 / 审计员
- Qwen 作为默认主力，负责：
  - 主评估
  - 主监督
  - 主执行
- 旧框架已归档到 `archive/v0/`

来源：
- 来源基础：从一个长期真实项目中提炼并泛化
- 核心协议来源：`docs/ai-collaboration.md`
- 人类入口模式：`docs/ai-workbench.md`
- relay 入口模式：`docs/ai-relay.md`

## 现在的结构

为了减少重复和后续漂移，公共前置约束已经抽到：
- `shared-repo-contract.prompt.md`

v1 还新增了：
- `FRAMEWORK-V1.md`
- `ARCHITECTURE-LAYERS.md`
- `STATE-FLOWS.md`
- `INIT-RECIPES.md`
- `UPGRADE-MATRIX.md`
- `FORMAT-STRATEGY.md`
- `TOOLS.md`
- `TOKEN-CONTEXT-STRATEGY.md`
- `INIT-QWEN.md`
- `USE-CASES.md`
- `AI-LTC-INIT-QUESTIONNAIRE.template.md`
- `ai-ltc-config.template.json`
- `00_HANDOFF.template.md`
- `ESCALATION_REQUEST.template.md`
- `gpt-bootstrap-architect.prompt.md`
- `gpt-optimizer-auditor.prompt.md`
- `qwen-init-routing.prompt.md`
- `qwen-generalist-autopilot.prompt.md`
- `qwen-supervisory-generalist.prompt.md`

## 推荐使用方式

1. 先贴 `shared-repo-contract.prompt.md`
2. 如果目标项目是 `v0 -> v1` 升级，或还没有 init resolver config，先用 `qwen-init-routing.prompt.md`
3. 再按阶段选角色：
   - 如果 Qwen 需要先判断项目当前是“全新 / 半道加入 / 混沌状态”，并确认 AI-LTC 来源模式，先用 `qwen-init-routing.prompt.md`
   - 项目初期或大重构起步：`gpt-bootstrap-architect.prompt.md`
   - 正常推进期默认：`qwen-generalist-autopilot.prompt.md`
   - Qwen 主导的检查/监督/节点评估：`qwen-supervisory-generalist.prompt.md`
   - 只有明确需要时才用：`gpt-optimizer-auditor.prompt.md`
4. GPT 完成骨架后，用 `00_HANDOFF.template.md` 生成 `00_HANDOFF.md`
5. Qwen 遇到死锁或反复报错时，用 `ESCALATION_REQUEST.template.md` 生成 `ESCALATION_REQUEST.md` 并触发 `@ARCHITECT_HELP`
6. 如果只是想让执行中的 AI 稳定续跑，可改用 `continue-execution.prompt.md`
7. 需要时最后追加 `human-addendum.template.md`

## 架构阅读顺序

- `FRAMEWORK-V1.md`
- `ARCHITECTURE-LAYERS.md`
- `STATE-FLOWS.md`
- `INIT-RECIPES.md`
- `UPGRADE-MATRIX.md`
- `FORMAT-STRATEGY.md`
- `TOOLS.md`
- `TOKEN-CONTEXT-STRATEGY.md`
- `INIT-QWEN.md`

## v1 核心逻辑

- 贵脑做设计，快手做执行，按需请专家
- GPT 定上限，Qwen 扩规模
- GPT 不全程围观，只在明确场景短暂介入
- 如果框架已经部署好，但项目状态还不明确，可先让 Qwen 用 `qwen-init-routing.prompt.md` 做一次初始分流
- 如果项目是从 `v0` 升到 `v1`，则建议把 Qwen init 视为半强制迁移步骤

## 角色分工

- GPT 初期：
  - 总架构师
  - 深度思考、定规范、搭骨架
  - 完工即退场

- Qwen 中期：
  - 全能工程师
  - 主评估、主监督、主执行
  - 在实战中动态补文档、补结构

- GPT 后期：
  - 优化师 / 审计员
  - 只在瓶颈、重构、专项审计时短暂唤醒

## shared header 包含的内容

- 统一 read order：先读 `AGENTS.md`、`.ai/README.md`、`docs/ai-relay.md`、`docs/ai-collaboration.md`，再读 active lane docs
- `.ai/` 是本地私有 active lane state
- 如果 `.ai/` 缺失，要先重建最小本地工作区
- `docs/modernization/*` 同名文件只算 bridge notes，不覆盖 `.ai/` active state
- 默认不进入提交范围：`.omx/`、`.ai/`、`.sisyphus/`、`AGENTS.md`
- 有统一的 bounded-pass、反循环、结构化输出约束
- 有统一的构建偏好：能用 GitHub Actions 做干净验证时，优先用 GitHub Actions
- 有统一的固定退出语句模板，便于程序解析
- 有统一的状态字段模板，便于程序稳定取值
- 有 v1 交接清单协议：`00_HANDOFF.md`
- 有 v1 升级机制：`@ARCHITECT_HELP` + `ESCALATION_REQUEST.md`
- 有 v1 文档自进化规则：Qwen 可直接更新文档，但要留下更新标记
- 有 init 时的 resolver config：`.ai/system/ai-ltc-config.json`
- 有 init 问答模板：`AI-LTC-INIT-QUESTIONNAIRE.template.md`

## 固定退出语句

- `STOP_NO_NEW_EVIDENCE`
- `STOP_REPEATED_BLOCKER`
- `STOP_BOUNDED_PASS_EXHAUSTED`
- `STOP_WAIT_NO_PROGRESS`
- `STOP_REVIEW_GATE_REACHED`

这些短语用于无新证据、重复 blocker、bounded pass 用尽、等待无进展、到达 review gate 时的统一退出。

## 固定状态字段

- `Status`
- `Decision`
- `Stop Reason`
- `Next Action`

这些字段用于让 execution / checkpoint / planning 输出更接近稳定协议。

## 文件说明

- `examples/collaboration-system/`
  一个可复制到其他项目的协作系统模板示例。

- `examples/collaboration-system/bootstrap-checklist.md`
  复制到新项目后第一天应该修改什么的检查清单。

- `examples/collaboration-system/install-example.md`
  复制模板到新项目时的安装说明。

- `examples/collaboration-system/copy-into-new-repo.sh`
  一个最小复制脚本，用于把模板骨架复制到新仓库。

- `examples/collaboration-system/VERSION.md`
  这套模板自己的版本信息。

- `examples/collaboration-system/CHANGELOG.md`
  这套模板自己的变更记录。

- `shared-repo-contract.prompt.md`
  所有角色 prompt 的公共前置说明。

- `AI-LTC-INIT-QUESTIONNAIRE.template.md`
  init 阶段给 Qwen 的最小问答模板。
  用于确认 AI-LTC 来源模式、本地位址或云 repo、项目状态和默认模型。

- `ai-ltc-config.template.json`
  AI-LTC resolver 配置模板。
  复制到目标项目后，应落在 `.ai/system/ai-ltc-config.json`。

- `00_HANDOFF.template.md`
  GPT 向 Qwen 交接时必须生成的交接清单模板。

- `ESCALATION_REQUEST.template.md`
  Qwen 遇到死锁、重复 blocker、逻辑卡死时发给 GPT 的定点求助模板。

- `INIT-QWEN.md`
  给 Qwen 3.5 Plus 的 init 文档。
  用于在框架部署完毕后，判断项目属于全新、半道加入还是混沌状态，并推荐后续模型和 prompt。

- `gpt-bootstrap-architect.prompt.md`
  GPT 初期架构师 prompt。

- `gpt-optimizer-auditor.prompt.md`
  GPT 优化师 / 审计员 prompt。

- `qwen-generalist-autopilot.prompt.md`
  Qwen 全能工程师 prompt。
  是 v1 默认主力。

- `qwen-supervisory-generalist.prompt.md`
  Qwen 主监督 / 主评估 prompt。
  用于让 Qwen 也能承担 checkpoint、lane 判断和节点评审。

- `qwen-init-routing.prompt.md`
  Qwen 3.5 Plus 的 init 分流 prompt。
  用于在接管前先评估项目状态，确认 AI-LTC 来源模式，并推荐接下来应使用的模型和 prompt 组合。

- `lower-cost-execution.prompt.md`
  旧通用执行版，保留兼容性。
  现在明确要求：尽量优先窄的 GitHub Actions 构建/验证路径，本地构建主要用于快速 sanity 和 blocker 隔离。
  同时要求在提前停止时输出固定 `Stop Reason`，并尽量提供固定状态字段。

- `qwen-lower-cost-autopilot.prompt.md`
  旧版 Qwen 强化执行 prompt，保留兼容性。
  v1 默认更推荐 `qwen-generalist-autopilot.prompt.md`。
  现在也明确限制了单次 pass、等待次数、循环风险，并把 GitHub Actions 设为优先证明路径。
  同时要求在停止时输出固定 `Stop Reason`，并尽量提供固定状态字段。

- `checkpoint-review.prompt.md`
  轻量监督复盘。

- `supervisory-evaluation-planning.prompt.md`
  常规“评估 + 规划”。

- `strategic-checkpoint-long-horizon.prompt.md`
  既看当前状态，也看 lane / phase / roadmap 的战略复盘。

- `long-range-planning.prompt.md`
  长期 / 超长期规划。

- `continue-execution.prompt.md`
  用于代替只发 `continue.` 的续跑提示词。

- `human-addendum.template.md`
- `scripts/init_validator.py`
- `scripts/resolver_validator.py`
- `scripts/upgrade_validator.py`
- `scripts/state_pack_generator.py`
- `scripts/state_pack_validator.py`
  人类每轮附加要求模板。

另外，`examples/collaboration-system/` 提供了一套可复制到其他项目的最小协作系统骨架。
同时新增了 `USE-CASES.md`，用于公开说明常见使用场景，并作为更系统的场景路由入口。
同时新增了 `INIT-RECIPES.md`，用于标准化 fresh init / update / upgrade / resume 与骨架复制策略。
同时新增了 `UPGRADE-MATRIX.md`，用于标准化升级判定矩阵与 rc 发布纪律。
同时新增了 `FORMAT-STRATEGY.md`，用于正式说明 markdown / YAML / JSON / CSV / mixed 的分层策略，以及语言策略。
同时新增了 `TOOLS.md`，用于集中说明当前 validator / generator 工具层。
同时新增了 `TOKEN-CONTEXT-STRATEGY.md`，用于正式说明 token、context、配额与长会话节省策略。
它现在也已经升级到 v1 的 GPT/Qwen 分阶段框架。
并新增了 `ROLE-QUICK-REFERENCE.md`，便于快速选角色。

## 备注

这些文件是提取副本，便于在仓库外复用。
这些文件是可复用模板。复制到其他仓库后，应以目标仓库自己的 `docs/` 文件和本地 `.ai/` lane 文件作为源头。
不要在目标项目里把 AI-LTC 根目录绝对路径散写进多个 `.ai` 文件；应集中写到 `.ai/system/ai-ltc-config.json`。
默认 resolver 策略应是：本地 AI-LTC 仓库优先，远端 `https://github.com/Hope2333/AI-LTC` 作为后备，Qwen 仅在必要时才刷新本地副本。

轻量工具：
- 用 `python3 scripts/init_validator.py /path/to/target-repo` 校验 init 状态
- 用 `python3 scripts/resolver_validator.py /path/to/target-repo` 校验 resolver 配置
- 用 `python3 scripts/upgrade_validator.py /path/to/target-repo --target-version v1.8.1` 校验升级分类
- 用 `python3 scripts/state_pack_generator.py /path/to/target-repo` 生成紧凑 state pack
- 用 `python3 scripts/state_pack_validator.py /path/to/state-pack.md` 校验 state pack

轻量工具：
- 用 `python3 scripts/init_validator.py /path/to/target-repo` 校验 init 状态
- 用 `python3 scripts/resolver_validator.py /path/to/target-repo` 校验 resolver 配置
- 用 `python3 scripts/upgrade_validator.py /path/to/target-repo --target-version v1.7.0` 校验升级分类
- 用 `python3 scripts/state_pack_generator.py /path/to/target-repo` 生成紧凑 state pack
