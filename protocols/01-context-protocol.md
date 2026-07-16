# 上下文协议 v0.1

## 目标

让 KB-Agent 每轮 loop 都知道“该看什么、不该看什么、看到长文后如何压缩、什么时候必须停止继续读”，从而避免上下文污染、凭印象改文件和不可复现。

## 固定必读

每轮运行必须读取以下内容，不得跳过：

1. `README.md`：项目状态、目录结构、当前阶段。
2. `DECISIONS.md`：用户已确认的关键决策。
3. `evals/03-rubric-v2.0.md`：当前评分标准。
4. `evals/failure-patterns.md`：历史失败模式。
5. 与任务相关的 SOP / protocol：
   - 上下文任务：`protocols/01-context-protocol.md`
   - 工具/执行任务：`protocols/02-tool-protocol.md`
   - 高风险/人审任务：`protocols/03-human-review-protocol.md`
6. 知识库目录或目标文件索引：优先读总览、目录、frontmatter、候选目标文件，而不是整库全文。

## 动态上下文

每轮按任务动态选择，必须记录在 run report：

| 动态项 | 说明 |
|---|---|
| 本次输入文章/链接/早报条目 | 原始素材，不直接入库 |
| 候选目标文件 | 可能被修改的 md 文件 |
| 相关历史条目 | 通过标签、关键词、反链、目录检索得到 |
| 最近一次失败教训 | 来自 `failure-patterns.md` 或上一轮 run report |
| 用户最新指令 | 若与历史决策冲突，以最新明确指令为准，并写入 DECISIONS |
| 当前评测 split | smoke / regression / holdout / full / live |

## 禁止行为

- 禁止一次性读取完整知识库全文。
- 禁止凭印象改文件；修改前必须读目标文件相关片段。
- 禁止跳过总览直接写入新文档。
- 禁止在未检索历史条目的情况下新建重复主题。
- 禁止把 gold 答案包放入被测 agent 上下文。
- 禁止把 API key、密码、cookie、私密求职信息放入上下文摘要。

## 读取顺序

### Curator 更新任务

1. README / DECISIONS / rubric / failure patterns
2. 本次输入素材
3. 知识库总览与候选目标文件目录
4. 相关历史条目，不超过 5 个
5. 源验证结果
6. 输出候选决策，再决定是否改库

### Doctor 诊断任务

1. README / DECISIONS / rubric / failure patterns
2. 上一次 Doctor 报告
3. 目录、git diff、changelog、frontmatter 统计
4. 抽样目标文件
5. 高风险文件或 stale 文件
6. 输出问题清单、自动修复建议、人审项

### Eval/Judge 任务

1. rubric v2
2. calibration set（若用户已确认）
3. actor input / actor output
4. gold 包（Judge only）
5. 评分证据

## 上下文压缩协议

读完任何长文、长 issue、PDF、报告或多文件上下文后，必须先压缩，再进入写作/修改。

固定压缩格式：

```markdown
## 事实摘要
- 只写可核查事实、数字、来源、日期。

## 判断依据
- 为什么收/拒/候选/归档？
- 引用 rubric、SL 判据或 SOP 条款。

## 待确认点
- 事实未核实、版权不清、目标文件不确定、需要用户判断的点。

## 最大泛化的最短程序
- 把本次经验压缩成以后可复用的规则、检查项或 failure pattern。
```

“最大泛化的最短程序”不是写感想，而是写成可以复用的规则。例如：

```text
如果来源是 GitHub issue 且 maintainer 未确认，则只能进入 candidate/verification，不得进入主知识库事实正文。
```

## Context Budget 阈值

Claude Code 官方公开文档没有给出固定自动 compact 百分比，只说明接近上下文上限会自动 compact，并提供 `/context` 查看占用、`/compact` 主动压缩。因此 KB-Agent 使用保守工程阈值：

| 上下文占用 | 协议动作 |
|---:|---|
| < 60% | 正常运行，但仍禁止整库读取 |
| 60-70% | 停止扩大检索范围，只允许读目标文件与证据 |
| 70-80% | 必须写 context snapshot：当前目标、已读证据、待办、风险 |
| 80-90% | 主动 compact；长文必须先摘要后继续 |
| > 90% | 禁止继续读取长文或修改文件；先 compact 或开新 run |

若运行环境无法显示百分比，则用代理指标：

- 本轮已读文件 > 12 个
- 单次素材 > 15,000 tokens
- 输出前已有多轮长推理
- 已出现“我记得/大概/应该”式不确定表达

触发任一代理指标时，按 80% 档处理。

## Run Context Packet 模板

```yaml
run_id: ""
task_type: curator_update | doctor_diagnosis | behavior_eval | state_eval | protocol_update
fixed_context_read:
  - README.md
  - DECISIONS.md
  - evals/03-rubric-v2.0.md
  - evals/failure-patterns.md
dynamic_context:
  user_input: ""
  candidate_files: []
  related_history: []
  recent_failure_pattern: ""
context_budget:
  estimate: "<60 | 60-70 | 70-80 | 80-90 | >90 | unknown"
  compaction_done: false
forbidden_context_checked:
  full_kb_read: false
  gold_leakage: false
  secrets_in_context: false
```
