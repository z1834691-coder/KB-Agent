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
