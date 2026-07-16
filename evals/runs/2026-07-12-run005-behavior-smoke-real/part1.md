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
