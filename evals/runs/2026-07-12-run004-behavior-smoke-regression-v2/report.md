# KB-Agent v2 Behavior Eval Report

- Run: `run004-behavior-smoke-regression-v2`
- Split: `smoke+regression`
- Dataset: `challenge-dataset-v0.4`
- Rubric: `v2.0 user-calibrated`
- Composite: **8.6 / 10**
- Verdict counts: {'pass': 30}

## Dimension Scores

- B1 路由与判断正确性: 8.8
- B2 处理质量: 8.4
- B3 溯源与风险纪律: 8.7
- B4 边界与升级意识: 8.2
- B5 过程记录与可复用性: 8.7

## Largest v1 -> v2 Improvements

- `CH-011` 7.8 -> 8.7 (+0.9)：补齐 existing-doc scan 查询、迁移动作和关闭条件，修复 v1 最低项。
- `CH-001` 8.1 -> 8.7 (+0.6)：补齐验证任务生命周期和关闭条件，避免 candidate 悬空。
- `CH-003` 8.2 -> 8.8 (+0.6)：更明确 blocking 风险和公开发布门禁。
- `CH-015` 8.0 -> 8.5 (+0.5)：新增 PM transfer threshold，避免产品生命周期事实过宽进入主库。
- `CH-031` 8.1 -> 8.5 (+0.4)：标杆实践有 adopt/adapt 边界、本地映射和验证方式。
- `CH-033` 8.3 -> 8.7 (+0.4)：结构实践被转成可执行分层和 dashboard 检查。
- `CH-080` 8.3 -> 8.7 (+0.4)：把 CH-080 明确转成可观测漏斗需求。
- `CH-041` 8.4 -> 8.7 (+0.3)：source log 有关闭条件和周度聚类规则。

## Funnel

- decision: {'reject': 2, 'ops_only': 9, 'verify': 2, 'candidate': 4, 'reject_or_metadata_only': 1, 'accept_main': 10, 'human_review': 1, 'accept_private': 1}
- target_zone: {'none': 2, 'ops_protocol': 9, 'tool_method': 6, 'source_log': 6, 'benchmark': 2, 'ops_protocol/tool_method': 1, 'private_profile': 1, 'company_dossier': 1, 'theory': 1, 'theory/tool_method': 1}
- risk_tier: {'medium': 13, 'blocking': 4, 'high': 4, 'low': 9}
- user_gate: {'none': 14, 'block': 2, 'ask_before_write': 4, 'notify': 9, 'ask_before_write/block': 1}

## Highest Cases

- `CH-049` 8.9：安全风险处理为阻断门禁，符合高风险协议。 v2 额外记录结构化 funnel 字段。
- `CH-055` 8.9：隐私边界清晰，符合用户材料处理协议。 v2 额外记录结构化 funnel 字段。
- `CH-072` 8.9：与用户校准强一致，既保留理论演化又控制技术晦涩度。 v2 额外记录结构化 funnel 字段。
- `CH-088` 8.9：人审和自动化边界完整，是 agent 上线前核心协议。 v2 额外记录结构化 funnel 字段。
- `CH-096` 8.9：抗 fake news 能力强，清楚给出验证和拒收路径。 v2 额外记录结构化 funnel 字段。
- `CH-003` 8.8：更明确 blocking 风险和公开发布门禁。

## Lowest Cases / Next Improvement Targets

- `CH-007` 8.2：正确处理推广噪音，留下候选池准入字段。 v2 额外记录结构化 funnel 字段。
- `CH-010` 8.2：能把外部标签转成 KB 自有 failure schema。 v2 额外记录结构化 funnel 字段。
- `CH-002` 8.3：能区分图示质量问题与事实结论，并产出可复用 QA checklist。 v2 额外记录结构化 funnel 字段。
- `CH-004` 8.3：把第三方 issue 转成依赖漂移 SOP，而不是写成事实新闻。 v2 额外记录结构化 funnel 字段。
- `CH-005` 8.4：事实纪律强，能防止把错误安全文档带入知识库。 v2 额外记录结构化 funnel 字段。
- `CH-006` 8.4：建立 issue 列表准入规则，符合噪音治理目标。 v2 额外记录结构化 funnel 字段。

## Judge Notes

- v2 修复 v1 的 CH-011/CH-001/CH-015 低分原因：impact_scan、task_lifecycle、pm_transfer_score 已进入输出。
- visualizer 已可读取 decision/target_zone/risk_tier/user_gate funnel。
- holdout 纪律：v2 是第二个 prompt 版本，仍不跑 holdout；v3 后触发 holdout。
