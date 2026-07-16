# KB-Agent Run005 · 真实闭卷行为评测 · Actor 产出

- run_id: `run005-behavior-smoke-real`
- 评测类型: behavior / **smoke（15 条）**
- dataset: `challenge-dataset-v0.4`（仅 actor-pack）
- rubric: `v2.0`
- actor prompt: **agent-v2**
- actor model: **claude-opus-4-8**（原计划 sonnet-5，本环境 bedrock-sonnet 路由不可用）
- 运行时间: 2026-07-12 19:25–19:36
- **隔离声明**: actor 仅读取 actor-pack 指定行段 + 操作手册/协议文件；未打开 gold / 主数据集 / jsonl（评测有效）。
- **收尾说明**: actor 在最后合并阶段撞 session 限额；三个分片（part1/2/3）已完整落盘，合并与提交由主编排会话完成——纯文件拼接，不涉及任何 case 判断，隔离不受影响。

## decision 分布（15 条真实判断）
| decision | 条数 |
|---|---|
| accept_main | 6 |
| ops_only | 8 |
| verify | 1 |

> 解读：只有 6/15 进 AI PM 主库，8 条被分流为运维资产、1 条待核实——agent 没有"见 AI 就收"，符合 agent-v2 的分流原则。真实判断质量待 Judge 对照 gold 评分。

---

# run005 · 批1 (CH-001, CH-003, CH-011, CH-012, CH-021)

actor model = claude-opus-4-8 · dataset = challenge-v0.4 actor-pack · rubric = v2.0

---

## CH-001 · OpenAI Cookbook prompt caching issue（开放 issue，需交叉核实）

```yaml
decision: verify
target_zone: source_log
granularity: link_short_note
freshness_policy: latest_only
source_grade: C
risk_tier: medium
risk_flags: ["unconfirmed_issue", "user_screenshot_only", "potential_doc_error"]
confidence: medium
user_gate: none
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["prompt caching", "prompt_caching", "doc-07", "caching table"]
  affected_docs: [pending_scan]
  migration_action: verify_first
task_lifecycle:
  owner: agent
  next_check_at: 2026-07-18
  promotion_condition: "官方 cookbook 文档或 maintainer 确认表格数值有误"
  close_condition: "官方确认无误 / issue 关闭 / 7 天无进展则丢弃，不入库"
failure_mode: ["F-003 若直接采信 issue 改 doc-07 即触发", "F-011 官方示例≠已核实"]
changelog_note: "issue #2834（prompt caching 表格疑似错误）记入 source_log 待核实；未确认前不动 doc-07。"
flywheel_data: ["规则: 开放 issue + 仅用户截图证据 → verify，禁止当日改主文"]
```

理由：source_type=github_issue 且状态 open、仅有用户截图论证，命中 F-003（issue 不等于事实）与 SL-01（一手源优先）。用户问"今天是否更新"，正确答案是"不今天更新，先交叉核实官方 cookbook"。pm_transfer 全 0，本身也不该进主库，最多是 doc-07 的 tool_method 修正——但必须先 verify_first，并给出可关闭的 task_lifecycle 以避免 F-012 悬空。

---

## CH-003 · 暴露 Mapbox API key（公开库发布 secret-scan gate）

```yaml
decision: ops_only
target_zone: ops_protocol
granularity: structured_card
freshness_policy: none
source_grade: C
risk_tier: medium
risk_flags: ["secret_exposure_pattern", "public_publish_gate", "standing_rule_change"]
confidence: high
user_gate: ask_before_write
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["公开知识库方案", "publish", "secret", "API key", "历史提交", "外链资源"]
  affected_docs: [pending_scan]
  migration_action: update_current
task_lifecycle:
  owner: user
  next_check_at: 2026-07-19
  promotion_condition: "用户确认后写入 publishing SOP 的 secret-scan gate"
  close_condition: "secret-scan gate（历史提交 + 外链资源扫描）写入 SOP 且 dashboard 可见"
failure_mode: ["若忽略 → 开源前泄密", "对齐 tool-protocol『secret scanner 必须，开源前』"]
changelog_note: "HF issue #3364 转为公开发布前 secret-scan gate 提案，路由 ops_protocol，待用户确认。"
flywheel_data: ["规则: 公开发布前必须扫 git 历史 + 外链资源，不止隐藏个人信息"]
```

理由：属 §3.2 运维资产（secret scan / 版权 / 发布风险），不入 AI PM 主库。issue 本身是 C 级来源，但其建议（轮换、查账单、防泄密）是标准安全实践，且直接补上现有"公开方案只隐藏个人信息"的缺口，呼应 tool-protocol「secret scanner 必须，开源前」与 D8 开源前清理。建立新发布 gate 是 standing rule（H2 + 我的安全条例「持久化规则需确认」），故 user_gate=ask_before_write。

---

## CH-011 · OpenAI deprecations（弃用处理 SOP，机器可读元数据）

```yaml
decision: ops_only
target_zone: ops_protocol
granularity: structured_card
freshness_policy: periodic_review
source_grade: A
risk_tier: low
risk_flags: ["deprecation_metadata"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["deprecated", "弃用", "旧模型", "旧 API", "shutdown", "model card", "pricing"]
  affected_docs: [pending_scan]
  migration_action: add_metadata
task_lifecycle:
  owner: agent
  next_check_at: 2026-08-01
  promotion_condition: "n/a (SOP)"
  close_condition: "deprecation SOP 落地 + 受影响文档补 shutdown_date/replacement/stale_after 元数据"
failure_mode: ["F-011 官方通知不自动入主库", "F-002 类型化保鲜"]
changelog_note: "deprecations 页转为 deprecation-handling SOP：正文一句话弃用→机器可读元数据（shutdown_date/replacement/stale_after），不整页入主库。"
flywheel_data: ["规则: deprecation = latest_only 产品数据，存结构化元数据 + 到期提醒，非主库长文"]
```

理由：用户明确要求"更新 deprecation SOP"，且这是 F-011 的正解——官方通知本身 PM 学习价值低（pm_transfer 0/4），价值在于把"正文一句话弃用"升级为机器可读元数据这一可复用维护方法，落 ops_protocol。§4.1 要求 impact_scan：affected_docs 尚未实际扫描，诚实标 pending_scan，migration_action=add_metadata。用户已请求，故 user_gate=notify（出 SOP diff 汇报）。

---

## CH-012 · Assistants API 移除（doc-06 确有受影响文档）

```yaml
decision: accept_main
target_zone: tool_method
granularity: structured_card
freshness_policy: evolution_timeline
source_grade: A
risk_tier: medium
risk_flags: ["existing_doc_update", "deprecation_migration", "content_move_to_history"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 0
  company_research: 1
  product_decision: 1
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["Assistants API", "doc-06", "agent", "thread", "run", "assistant"]
  affected_docs: ["doc-06: 输入快照确认使用 Assistants API 为正常路径；全文扫描 pending"]
  migration_action: update_current
task_lifecycle:
  owner: agent
  next_check_at: 2026-08-01
  promotion_condition: "n/a (已在库，做更新)"
  close_condition: "doc-06 标 deprecated(shutdown 2026-08-26) + 迁移到 Responses/Conversations，旧路径移入 history"
failure_mode: ["F-011 正解: 有受影响文档才 update（非 reject）", "F-002 保鲜"]
changelog_note: "doc-06 agent 教程：Assistants API 标 deprecated（shutdown 2026-08-26），主路径迁 Responses/Conversations API，旧实现移入 history；company_dossier 补 OpenAI 平台收敛短评。"
flywheel_data: ["规则: 官方弃用 + 确认受影响文档 → update_current + move_to_history，不是 reject"]
```

理由：与 CH-011 的关键差异——此处 §4.1 impact_scan 命中**确有受影响文档**（doc-06 输入已确认用 Assistants API），故正确动作是 update 而非 reject。官方源 A 级、shutdown 日期明确（2026-08-26），confidence high。pm_transfer 命中 company_research + product_decision（OpenAI 平台从 Assistants 收敛到 Responses，影响 agent 产品的 build 选型），达 2/4 阈值，可附 company_dossier 短评。旧路径 move_to_history 而非删除，故 user_gate=notify 出 diff。

---

## CH-021 · Artificial Analysis 多轴榜（非单一 winner list）

```yaml
decision: accept_main
target_zone: benchmark
granularity: structured_card
freshness_policy: periodic_review
source_grade: A
risk_tier: low
risk_flags: ["multi_axis_caliber", "leaderboard_methodology"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 1
  company_research: 1
  product_decision: 1
  reusable_method: 1
impact_scan:
  required: true
  affected_docs_query: ["模型版图", "model landscape", "leaderboard", "top 10", "intelligence 排名", "model comparison"]
  affected_docs: [pending_scan]
  migration_action: update_current
benchmark_practice:
  practice: "多轴对比 + 口径标注（intelligence/price/speed/latency/context 各带 source+date+方法）"
  adopt_level: adapt
  local_mapping: "模型版图从单一 top10 intelligence 榜 → 多轴对比表 + 关键权衡短评，每列标 source+accessed_at"
  non_goals: "不照搬 100+ 模型全表；不做单一 winner 排名；不搬 AA 页面样式"
  validation_check: "每个数字可追到 AA 且有 accessed_at；至少覆盖 intelligence/price/speed/context 四轴"
task_lifecycle:
  owner: agent
  next_check_at: 2026-08-11
  promotion_condition: "n/a (已在主库)"
  close_condition: "多轴对比表上线，单轴排名版本废弃"
failure_mode: ["SL-06 违背: 不同口径粗暴排名", "单轴 overclaiming"]
changelog_note: "模型版图：单轴 top10 intelligence 榜 → 多轴对比（intelligence/price/speed/latency/context），每轴标 source+date，periodic_review。"
flywheel_data: ["规则: 榜单入库=多轴+口径，禁止压成单一名次"]
```

理由：benchmark 类必须出 benchmark_practice（§4.4）。隐藏陷阱是把多轴榜压成"top10 intelligence 单一排名"，直接违背 SL-06（数据必须有口径、不同口径不可粗暴排名）。模型选型是 AI PM 核心能力，pm_transfer 满 4/4（面试表达/竞品研究/产品选型/可复用选型框架），确入主库 benchmark 区，periodic_review + accessed_at 必填。adopt_level=adapt：吸收多轴+口径方法，不照搬其信息架构。
# run005 · 批2 (CH-031, CH-033, CH-041, CH-049, CH-057)

actor model = claude-opus-4-8 · dataset = challenge-v0.4 actor-pack · rubric = v2.0

---

## CH-031 · Lil'Log frontmatter（深度笔记状态元数据）

```yaml
decision: ops_only
target_zone: ops_protocol
granularity: structured_card
freshness_policy: none
source_grade: A
risk_tier: low
risk_flags: ["batch_backfill_downstream"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["frontmatter", "编号", "标题", "knowledge_type", "全部 md 文件"]
  affected_docs: [pending_scan]
  migration_action: add_metadata
benchmark_practice:
  practice: "深度笔记 frontmatter 状态元数据（date/author/reading_time/TOC + knowledge_type/last_reviewed/source/stale_after）"
  adopt_level: adapt
  local_mapping: "KB 文件从『编号+中文标题』升级为 frontmatter：knowledge_type/source_url/author/accessed_at/last_reviewed/stale_after/tags，配 frontmatter linter"
  non_goals: "不照搬 Lil'Log 博客视觉/reading-time 展示；旧文件不一次性回填（分批+人审）"
  validation_check: "linter 通过率；随机抽 10 文件均可判 type+溯源+保鲜状态"
task_lifecycle:
  owner: agent
  next_check_at: 2026-07-26
  promotion_condition: "n/a (schema/SOP)"
  close_condition: "frontmatter schema 定稿 + linter 落地 + 新文件强制、旧文件分批回填计划确认"
failure_mode: ["F-015 标杆泛化不足（须 local_mapping/non_goals/validation）", "F-008 无元数据难路由"]
changelog_note: "采纳 Lil'Log frontmatter：设计 topic-note 元数据 schema（type/source/accessed_at/last_reviewed/stale_after）+ linter；旧文件分批回填待确认。"
flywheel_data: ["规则: 新建/重构文件必须带 frontmatter，缺 type/source/保鲜字段进 linter 待办"]
```

理由：Lil'Log = G-01 标杆，故走 benchmark_practice（§4.4）。deliverable 是元数据 schema + linter，属维护资产（ops_protocol/tool_method），不入主库，pm_transfer 0/4。直接补"文件只有编号+标题"的 D1.2/D1.3/D3 短板，对齐 SL-01 与 tool-protocol「frontmatter linter 必须」。批量回填旧文件为 H2，故设计可 notify、回填需另行确认。

---

## CH-033 · Simon Willison 分粒度（三粒度收录政策）

```yaml
decision: ops_only
target_zone: ops_protocol
granularity: structured_card
freshness_policy: none
source_grade: A
risk_tier: low
risk_flags: ["core_sop_change"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["Curator SOP", "收录", "粒度", "markdown block", "等长"]
  affected_docs: [pending_scan]
  migration_action: update_current
benchmark_practice:
  practice: "分粒度收录：Entries/Links/Quotes/Notes/Guides → longform/structured_card/quote_takeaway/link_short_note/metadata_only"
  adopt_level: adopt
  local_mapping: "Curator 每条先判粒度再落盘：深度=longform；引文=quote_takeaway(出处+长度上限)；链接短评=link_short_note；标准卡=structured_card；仅元数据=metadata_only"
  non_goals: "不照搬 Simon 栏目命名/前端；不再等长 block 搬运"
  validation_check: "随机抽 10 条新收录，granularity 决策显式且可复核，无等长搬运"
task_lifecycle:
  owner: agent
  next_check_at: 2026-07-26
  promotion_condition: "n/a"
  close_condition: "三粒度收录政策写入 Curator SOP，每条收录必带 granularity 字段"
failure_mode: ["F-001 全文/等长搬运", "F-015 标杆泛化不足", "SL-02 粒度先行"]
changelog_note: "采纳 Simon 分粒度：Curator SOP 增 granularity 决策（longform/quote/link_note/card/metadata），废止等长 block。"
flywheel_data: ["规则: 收录前必须显式判粒度，等长 markdown block = 流程缺陷"]
```

理由：Simon Willison = G-03，且这是 D5 点名五大金实践之一「三粒度收录政策」，对应 SL-02（粒度先行）。deliverable 是 Curator 核心收录 SOP，属 ops_protocol。命中现有"所有来源写成等长 block"缺陷（F-001 风险）。adopt_level=adopt：粒度分层本就是 agent-v2 的 granularity 字段来源，直接采纳、本地化命名。

---

## CH-041 · AINews 高频源（source_log-first 管线）

```yaml
decision: ops_only
target_zone: source_log
granularity: link_short_note
freshness_policy: latest_only
source_grade: B
risk_tier: medium
risk_flags: ["high_frequency_noise", "direct_write_temptation"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["自动更新计划", "早报", "ingestion", "daily", "source funnel"]
  affected_docs: [pending_scan]
  migration_action: update_current
task_lifecycle:
  owner: agent
  next_check_at: 2026-07-19
  promotion_condition: "早报条目满足 pm_transfer≥2/4 或补齐一手源核实，才从 source_log 提升主库"
  close_condition: "daily 管线（crawled→candidate→accepted→rejected→pending + 人审 gate）写入 SOP，dashboard 出 funnel"
failure_mode: ["§3.3/F-003 高频源不直接入主库", "SL-07 来源漏斗+人审", "F-014 funnel 可观测"]
changelog_note: "AINews 每日早报：定义 source_log-first 管线（crawled→candidate→accepted/rejected/pending + 人审），禁止直接写主库，dashboard 出 funnel。"
flywheel_data: ["规则: 高频 newsletter 默认落 source_log，升主库需 pm_transfer≥2/4 或一手源核实"]
```

理由：命中隐藏陷阱——"自动计划想每天把早报直接写进知识库"，违背 §3.3（高频 newsletter 先入 source_log/candidate）与 SL-07（高频管线必须有人审+来源漏斗）。deliverable 是带 source funnel 的 ingestion SOP（ops_protocol），日条目默认落 source_log（link_short_note），多数 reject。AINews 为聚合二手源（B 级），单条事实仍需回一手源，故不自动升主库。

---

## CH-049 · 公开发布全库 secret 扫描（★★★★★，CH-003 升级版）

```yaml
decision: ops_only
target_zone: ops_protocol
granularity: structured_card
freshness_policy: none
source_grade: C
risk_tier: high
risk_flags: ["public_release_gate", "secret_scan", "irreversible_exposure", "standing_rule_change"]
confidence: high
user_gate: ask_before_write
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["公开化 checklist", "public release", "secret", "手机号", "git history", "env", "外链资源"]
  affected_docs: [pending_scan]
  migration_action: update_current
task_lifecycle:
  owner: user
  next_check_at: 2026-07-19
  promotion_condition: "用户确认后升级 public-release gate"
  close_condition: "gate 覆盖 git 历史 + env + 外链资源 + PII 全扫描；发布动作仍需用户最终确认(H4)"
failure_mode: ["若不升级→开源泄密(不可逆)", "tool-protocol『secret scanner 必须，开源前』", "H4 发布必须人审"]
changelog_note: "public-release gate 从『仅查正文手机号』升级为全库 secret scan（git 历史+env+外链资源+PII）；发布动作维持 H4 人审。"
flywheel_data: ["规则: 公开发布 gate = 全 repo 历史+env+外链 secret 扫描，单点正文检查=不合格 gate"]
```

理由：与 CH-003 同源 issue 的高危升级版——现有 checklist 仅查"正文手机号"，远不足以 gate 公开发布。属 §3.2 运维安全资产（ops_protocol），pm_transfer 0/4。发布=H4（禁止自动化、不可逆），故 risk_tier=high 且 user_gate=ask_before_write，升级后发布仍须用户最终确认。对齐 tool-protocol「secret scanner 必须，开源前」与 D8 清理要求。

---

## CH-057 · DeepSeek pricing（PM 成本证据，非仅开发者文档）

```yaml
decision: accept_main
target_zone: company_dossier
granularity: structured_card
freshness_policy: latest_only
source_grade: A
risk_tier: low
risk_flags: ["price_volatility", "accessed_at_required"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 1
  company_research: 1
  product_decision: 1
  reusable_method: 1
impact_scan:
  required: true
  affected_docs_query: ["DeepSeek", "R1", "pricing", "cost", "flash", "pro", "cache-hit"]
  affected_docs: [pending_scan]
  migration_action: update_current
task_lifecycle:
  owner: agent
  next_check_at: 2026-08-11
  promotion_condition: "n/a (直接入主库)"
  close_condition: "DeepSeek dossier 补 PM cost+positioning 卡；价格带 accessed_at + stale_after"
failure_mode: ["F-004 目标公司内容过浅(只有技术故事)", "SL-05 目标相关性", "§1 价格=latest_only"]
changelog_note: "DeepSeek company_dossier 新增 PM cost+positioning 卡（v4 flash/pro 价、cache-hit/miss、output、concurrency、竞品定位），价格 latest_only + accessed_at=2026-07-11。"
flywheel_data: ["规则: 目标公司档案须超越技术故事，含 cost/定位/面试问题；价格类 latest_only+accessed_at"]
```

理由：清晰的主库案例——DeepSeek pricing 是 PM 成本证据（SL-05），直接修复"DeepSeek 只讲 R1 技术故事"的 F-004 短板。pm_transfer 满 4/4（面试成本表达/公司研究/build 选型/可复用成本卡模板），入 company_dossier。价格属 product_version_data，主路径 latest_only + accessed_at，历史价入 changelog（§1）。source A 级一手官方页，confidence high。
# run005 · 批3 (CH-072, CH-073, CH-080, CH-081, CH-088)

actor model = claude-opus-4-8 · dataset = challenge-v0.4 actor-pack · rubric = v2.0

---

## CH-072 · CoT 演化（prompt trick → test-time compute → reasoning models）

```yaml
decision: accept_main
target_zone: theory
granularity: longform
freshness_policy: evolution_timeline
source_grade: A
risk_tier: medium
risk_flags: ["existing_note_refactor"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 1
  company_research: 1
  product_decision: 1
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["CoT", "chain of thought", "一步步想", "reasoning", "ToT", "test-time compute", "R1"]
  affected_docs: [pending_scan]
  migration_action: update_current
task_lifecycle:
  owner: agent
  next_check_at: 2026-10-11
  promotion_condition: "n/a (已主库)"
  close_condition: "CoT 笔记重构为演化链：CoT(prompt)→ToT→test-time compute→RL reasoning(R1)，每节点带论文源+日期"
failure_mode: ["F-002 演化知识当静态", "SL-04 看历史定位", "§5 reasoning=evolution_timeline"]
changelog_note: "CoT 笔记从『一步步想』重构为演化时间线：CoT(prompt)→ToT→test-time compute→RL reasoning(DeepSeek-R1 2025-01)，每节点带一手论文源。"
flywheel_data: ["规则: 理论类(CoT/agent/reasoning/RAG)用 evolution_timeline，保留 trick→能力→产品 脉络"]
```

理由：CoT/reasoning 属 §5 evolution_timeline，现有"只讲一步步想"是把演化知识做成静态点（F-002）。正确动作是重构为演化链，用 DeepSeek-R1（arxiv 一手 A 级）+ Lil'Log 解释层锚定 SL-04（看历史定位）。pm_transfer 3/4（reasoning 模型何时用=产品判断、DeepSeek/OpenAI reasoning=公司研究、演化叙事=面试），入 theory 主库。

---

## CH-073 · Agent 心智模型（AutoGPT demo → harnessed workflow）

```yaml
decision: accept_main
target_zone: theory
granularity: longform
freshness_policy: evolution_timeline
source_grade: B
risk_tier: medium
risk_flags: ["existing_doc_update", "outdated_mental_model"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 1
  company_research: 1
  product_decision: 1
  reusable_method: 1
impact_scan:
  required: true
  affected_docs_query: ["agent", "AutoGPT", "doc-06", "autonomous loop", "harness", "workflow", "mental model"]
  affected_docs: ["doc-06: 输入确认仍以 AutoGPT 式 loop 为中心；全文扫描 pending"]
  migration_action: update_current
task_lifecycle:
  owner: agent
  next_check_at: 2026-10-11
  promotion_condition: "n/a"
  close_condition: "doc-06 agent 心智模型从 AutoGPT loop 更新为 harnessed workflow（planning/memory/tools + tests/review/human-gate），旧框架标历史"
failure_mode: ["F-002 演化知识当静态", "§5 agent=evolution_timeline", "SL-01 建议补 Anthropic 一手源"]
changelog_note: "doc-06 agent 心智模型更新：AutoGPT 自主 loop→harnessed workflow（约束+测试+人审）；旧 loop 保留为演化历史，建议补 Anthropic『Building Effective Agents』一手源。"
flywheel_data: ["规则: agent 心智模型随 harness 范式更新，autonomy≠先进；保留 demo→harness 演化线"]
```

理由：与 CH-072 同为演化类（agent，§5 evolution_timeline），doc-06 现以 AutoGPT loop 为中心已过时（F-002）。更新为 harnessed workflow 范式，旧框架降为演化历史而非删除。源为 Lil'Log/Simon 博客（B 级），故建议补 Anthropic agent 一手文（SL-01）。pm_transfer 4/4（harness>autonomy 是可复用产品设计原则），入 theory 主库。

---

## CH-080 · Visualizer 显示 source funnel（非仅新增条数）

```yaml
decision: ops_only
target_zone: ops_protocol
granularity: structured_card
freshness_policy: none
source_grade: A
risk_tier: low
risk_flags: ["vanity_metric_trap"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["visualizer", "dashboard", "SPEC", "新增条目", "funnel", "build.py"]
  affected_docs: [pending_scan]
  migration_action: update_current
benchmark_practice:
  practice: "数据追踪+可视化：从『新增条目数』升级为 source funnel + 决策分布可观测"
  adopt_level: adapt
  local_mapping: "dashboard 增 source funnel(crawled/candidate/accepted/rejected/pending) + decision/target_zone/risk_tier/user_gate 分布 + prompt diff + 维度分 + 过拟合警报"
  non_goals: "不照搬 AI Index 报告体量/章节；不做仅『增长数』虚荣指标"
  validation_check: "dashboard 能回答『本轮收/拒/候选/改各多少、主库vs运维vs source_log 占比、是否降噪』"
task_lifecycle:
  owner: agent
  next_check_at: 2026-07-26
  promotion_condition: "n/a"
  close_condition: "visualizer SPEC+build.py 输出 source funnel + 决策分布面板，替换纯计数视图"
failure_mode: ["F-009 visualizer 只显示新增条数", "F-014 ops/main 不可观测", "SL-06 数据口径"]
changelog_note: "visualizer 指标：从『新增条目数』升级为 source funnel + decision/target_zone/risk_tier/user_gate 分布 + 过拟合警报（对标 AI Index）。"
flywheel_data: ["规则: dashboard 必须显示降噪/分流，而非增长虚荣指标"]
```

理由：直接命中 F-009（visualizer 只显示新增条数）与 F-014（ops/main 不可观测）。AI Index=G-08 数据可视化标杆，走 benchmark_practice。deliverable 是 dashboard 指标 spec（KB-Agent 基建，ops_protocol），pm_transfer 0/4。与 D13 已加的分流漏斗面板一致，本轮按 case 快照（草图仅计数）补齐 funnel+决策分布。

---

## CH-081 · 模型对比图多轴 + 单位护栏

```yaml
decision: accept_main
target_zone: benchmark
granularity: structured_card
freshness_policy: periodic_review
source_grade: A
risk_tier: low
risk_flags: ["mixed_units", "different_update_cadence", "composite_score_trap"]
confidence: high
user_gate: notify
pm_transfer_score:
  interview_expression: 1
  company_research: 1
  product_decision: 1
  reusable_method: 1
impact_scan:
  required: true
  affected_docs_query: ["模型版图", "model comparison", "总分榜单", "chart", "pricing", "unit", "口径"]
  affected_docs: [pending_scan]
  migration_action: update_current
benchmark_practice:
  practice: "多轴对比图 + 单位/口径护栏（intelligence/price/speed 各自单位、来源、update cadence 独立标注）"
  adopt_level: adapt
  local_mapping: "模型对比面板做成多轴（分面/分列表），每轴标 单位+source+accessed_at+更新频率；不合成单一总分"
  non_goals: "不画跨单位『总分榜单』；不把 price 与 intelligence 加权成单一名次"
  validation_check: "每轴单位+口径+accessed_at 齐全；无跨单位复合评分；不同 cadence 分别标注"
task_lifecycle:
  owner: agent
  next_check_at: 2026-08-11
  promotion_condition: "n/a"
  close_condition: "多轴对比面板上线，单一总分榜单方案废弃，各轴口径+cadence 完整"
failure_mode: ["SL-06 不同口径不可粗暴排名", "F-013 单一总分 overclaiming", "D4.3 图表口径"]
changelog_note: "模型对比面板：拒绝跨单位『总分榜单』，改多轴（intelligence/price/speed）+ 每轴单位/来源/accessed_at/cadence 护栏。"
flywheel_data: ["规则: 跨单位指标禁止合成单一总分；图表每轴必标单位+口径+日期+cadence"]
```

理由：隐藏陷阱是"想画一个总分榜单图"——把 AA 智能分与 OpenAI 定价（不同单位、不同更新频率）压成单一名次，违背 SL-06 与 D4.3（图表口径）。与 CH-021 同向（拒单轴排名），CH-081 额外加单位/cadence 护栏。模型选型属 AI PM 核心，pm_transfer 4/4，入 benchmark 主库、periodic_review。

---

## CH-088 · 自动写入需 risk tier + 人审门（★★★★★）

```yaml
decision: ops_only
target_zone: ops_protocol
granularity: structured_card
freshness_policy: none
source_grade: B
risk_tier: high
risk_flags: ["unbounded_autonomy_trap", "standing_rule_change", "governs_all_writes"]
confidence: high
user_gate: ask_before_write
pm_transfer_score:
  interview_expression: 0
  company_research: 0
  product_decision: 0
  reusable_method: 0
impact_scan:
  required: true
  affected_docs_query: ["autonomy", "自动运行", "叫停", "human review", "risk tier", "H0-H4", "gate"]
  affected_docs: ["protocols/03-human-review-protocol.md: 已有 H0-H4，须补 risk_tier→gate 映射", "auto-run 计划: 须废止『直到叫停』默认全自动"]
  migration_action: update_current
task_lifecycle:
  owner: user
  next_check_at: 2026-07-19
  promotion_condition: "用户确认 autonomy policy（risk_tier→H0-H4 gate 映射）"
  close_condition: "autonomy policy 写入 ops_protocol：low→自动 / medium→notify / high→ask_before_write / blocking→block；废止『自动运行直到叫停』"
failure_mode: ["F-010 人审触发点过晚", "§3.2 运维/HITL 边界", "H4 高危默认拒绝", "反『无限自主』陷阱"]
changelog_note: "autonomy policy：废止『自动运行直到叫停』，改 risk_tier→gate 映射（low 自动 / medium notify / high ask_before_write / blocking block），绑定 H0-H4 与 T0-T4。"
flywheel_data: ["规则: 自动化默认不是『直到叫停』，而是 risk_tier 门控；不可逆/发布/删除/密钥永远 H4 阻塞"]
```

理由：隐藏陷阱是现有"agent 目标是自动运行直到叫停"——无界自主，违背人审协议 H0-H4 与 F-010。正确动作是定义 risk_tier→gate 的 autonomy policy（ops_protocol），把 feed/issue 产生的不同风险候选映射到不同门控。此策略治理所有未来写入，属 H3 级治理，risk_tier=high、user_gate=ask_before_write；发布/删除/密钥类永远 H4 阻塞。pm_transfer 0/4（agent 治理非 PM 知识）。
