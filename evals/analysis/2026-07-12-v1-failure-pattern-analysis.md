# v1 数据驱动失败模式分析

> 输入：`run001-calibration-v1`、`run002-behavior-smoke-regression-v1`、用户对 CH-066 的补充校准。  
> 目的：把 v1 的分数、低分 case、judge 证据转成 v2 prompt 和 visualizer 指标。

## 1. 总览

- calibration：9 条，v1 平均偏差 0.28。用户确认 CH-066 可从 1 调整为 1.5，表示“极低价值但不是绝对零分”。
- behavior：30 条 smoke+regression，综合 8.5。
- 维度分：B1 8.7、B2 8.2、B3 8.6、B4 8.0、B5 8.4。
- 最低 5 条：CH-011 7.8、CH-015 8.0、CH-001 8.1、CH-031 8.1、CH-003 8.2。
- 类别平均：github_issue 8.32、official_doc 8.35、benchmark 8.47、blog 8.52、newsletter 8.60、paper 8.90。

v1 已解决的关键问题：

- 不再把 GitHub issue、官方通知、工具站更新自动塞进 AI PM 主知识库。
- 能区分 AI PM 主知识价值、KB-Agent 运维价值、纯噪音/风险信息。
- 对隐私、安全、fake news、付费墙有明确阻断或降级动作。

v1 未完全解决的关键问题：

- 分流动作仍主要写在自然语言里，dashboard 无法量化主库/运维/source log/reject 的 funnel。
- official deprecation 类只说“如果影响现有教程”，但没有规定如何扫描现有文档、如何关闭验证任务。
- 产品演化类 case 还容易“保留产品教训”，但没有硬阈值判定是否值得进入 AI PM 主库。
- 标杆知识库结构类 case 能抽象字段，但还没有形成“结构资产 vs 主知识内容”的明确落盘边界。

## 2. 失败模式

### FM-v1-01：official update 影响面扫描不足

证据：

- CH-011 得分 7.8，是本轮最低分。
- Judge 证据：吸收用户校准，避免官方通知高估；但还应更明确 existing-doc scan 的执行路径。

根因：

- v1 只定义“官方通知不自动高价值”，但缺少二段式流程：
  1. 判断通知本身是否有 AI PM 学习价值。
  2. 扫描现有知识库是否有受影响教程、代码、模型卡、成本表或链接。

v2 改法：

- 增加 `impact_scan` 规则：必须输出 `affected_docs_query`、`affected_docs`、`migration_action`、`close_condition`。
- 若无受影响文档，deprecation/alias/shutdown 只能进入 `source_log` 或 reject。
- 若有受影响文档，才升级为 `metadata_only` 或 `structured_card`。

### FM-v1-02：验证任务缺少关闭条件

证据：

- CH-001 得分 8.1。
- Judge 证据：输出还可进一步说明核验完成后的删除条件。

根因：

- v1 能创建 verify/candidate，但没有要求每个任务带 `owner`、`next_check_at`、`close_condition`、`promotion_condition`。

v2 改法：

- 所有 `verify`、`candidate`、`source_log` 都必须给出任务生命周期字段。
- 没有下一步证据路径的信息应直接 reject，不创建永远悬空的待办。

### FM-v1-03：产品案例入主库阈值不够硬

证据：

- CH-015 得分 8.0。
- Judge 证据：能保留产品学习价值，不过对是否进入主库还应加目标相关性阈值。

根因：

- v1 对“产品演化案例”偏宽松，只要有产品教训就可能 candidate。
- 用户目标是 AI PM 求职，产品案例必须能转译成公司研究、方法论、面试表达或设计判断。

v2 改法：

- 增加 `pm_transfer_score`：求职/面试表达、公司研究、产品决策、方法论复用四项至少命中两项，才可进入 AI PM 主库。
- 只具备平台生命周期事实的内容，默认 `source_log` 或 `ops_protocol`。

### FM-v1-04：ops_only 与 AI_PM_core 边界缺少可观测漏斗

证据：

- v1 输出中 `accept_main` 10 条、`ops_only` 9 条、`candidate` 4 条、`reject` 2 条、`verify` 2 条。
- target_zone 中 `ops_protocol` 9 条、`source_log` 4 条、`tool_method` 6 条，但 dashboard 原本只能展示文本，不能总览分流。

根因：

- v1 结果没有结构化字段，visualizer 只能从 output 文本里读。

v2 改法：

- results.jsonl 增加结构化字段：`decision`、`target_zone`、`granularity`、`freshness_policy`、`risk_tier`、`user_gate`、`failure_mode`。
- visualizer 增加 funnel 面板，显示 decision/target_zone/risk_tier 分布。

### FM-v1-05：标杆结构类容易“学到结构”，但缺少采用边界

证据：

- CH-031 得分 8.1，Judge 说能抽象字段，但仍在最低组。
- CH-033 得分 8.3，说明结构抽象可行但还需更可执行。

根因：

- v1 只说“不照搬目录”，但没有要求输出 `adopt / adapt / reject` 级别。

v2 改法：

- 对黄金标杆实践强制输出：`practice`、`adopt_level`、`local_mapping`、`non_goals`、`validation_check`。
- 只有能映射到本 KB 当前短板的实践才进入 `ops_protocol`。

## 3. v2 目标

v2 不追求大幅抬高所有分数，而是提高可观测性、分流纪律和任务闭环：

- CH-011：从 7.8 提升到 >= 8.5。
- CH-001：从 8.1 提升到 >= 8.5。
- CH-015：从 8.0 提升到 >= 8.4。
- CH-031/033：结构实践输出更可执行。
- dashboard：显示 decision/target_zone/risk_tier funnel。

## 4. 防过拟合纪律

- 本轮仍只跑 smoke+regression，因为 v2 是第二个 prompt 版本；holdout 按协议每 3 个 prompt 版本跑一次。
- v2 prompt 只能吸收失败模式层面的规则，不允许硬编码 case id。
- CH-011、CH-001、CH-015 的改进必须以通用字段体现，而不是写成单题答案。
