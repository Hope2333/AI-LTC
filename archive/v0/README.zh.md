# AI-LTC 模板说明

这个目录用于存放 AI 协作、阶段复盘、战略复盘、长期规划相关的提示词模板。

来源：
- 来源基础：较早的提取状态，仅用于历史归档
- 核心协议来源：`docs/ai-collaboration.md`
- 人类入口模式：`docs/ai-workbench.md`
- relay 入口模式：`docs/ai-relay.md`

## 现在的结构

为了减少重复和后续漂移，公共前置约束已经抽到：
- `shared-repo-contract.prompt.md`

各角色 prompt 现在只保留角色差异部分。

## 推荐使用方式

1. 先贴 `shared-repo-contract.prompt.md`
2. 再贴一个角色 prompt
3. 如果只是想让执行中的 AI 稳定续跑，可改用 `continue-execution.prompt.md`，代替只发 `continue.`
4. 需要时最后追加 `human-addendum.template.md`

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

- `lower-cost-execution.prompt.md`
  通用低成本执行版。
  现在明确要求：尽量优先窄的 GitHub Actions 构建/验证路径，本地构建主要用于快速 sanity 和 blocker 隔离。
  同时要求在提前停止时输出固定 `Stop Reason`，并尽量提供固定状态字段。

- `lower-cost-autopilot.prompt.md`
  lower-cost 执行角色的强化执行版。
  这个仓库的执行侧默认优先用它。
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
  人类每轮附加要求模板。

另外，`examples/collaboration-system/` 提供了一套可复制到其他项目的最小协作系统骨架。

## 备注

这些文件是提取副本，便于在仓库外复用。
这些文件是可复用模板。复制到其他仓库后，应以目标仓库自己的 `docs/` 文件和本地 `.ai/` lane 文件作为源头。
