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
