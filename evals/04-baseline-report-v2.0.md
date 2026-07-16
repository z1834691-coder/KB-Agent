# Baseline 报告 v2.0 —— 用 rubric v2 重打 baseline-v0

评测对象：`AI知识库 V3` baseline-v0 快照（沿用 v0.1 baseline 取证，不重新跑全库 Doctor）

Rubric：`03-rubric-v2.0.md`

## 桥接结论

v0.1 总分：4.7 / 10

v2.0 建设期口径总分：**4.1 / 10**

分数下降不是知识库变差，而是 v2 口径更严格：它把“类型化保鲜、知识分层、标杆 checklist、SOP/flywheel、成本可观测”显式计入。

## 维度评分

| 维度 | 建设期权重 | v2 分数 | 加权 | 口径变化 |
|---|---:|---:|---:|---|
| D1 信息质量 | 20% | 4.8 | 0.96 | 过去只看时效，现在按知识类型、source metadata、冲突处理评分 |
| D2 内容价值与目标对齐 | 25% | 4.6 | 1.15 | 新增信息密度、洞察深度、知识分层分类型 |
| D3 结构与组织 | 15% | 5.3 | 0.80 | 两大 Track 仍加分，但双链/标签/演化链缺失被更明确扣分 |
| D4 呈现与体验 | 10% | 4.2 | 0.42 | 零图表、口径标注缺失、超长文档继续扣分 |
| D5 可维护性与流程 | 25% | 2.5 | 0.63 | baseline-v0 仍按 Phase 0 前状态评分：无 git/SOP/flywheel |
| D6 标杆实践采纳率 | 5% | 2.8 | 0.14 | 多数 checklist 未达成 |
| **综合** | 100% |  | **4.10 → 4.1** |  |

## 子指标证据摘要

### D1 = 4.8

已有四级信源分级和部分核实说明；但无 `accessed_at / stale_after / knowledge_type`，公众号全文转载有溯源风险，动态模型/价格/新闻未按类型管理。

### D2 = 4.6

覆盖面广，PM takeaway 有雏形；但目标公司深度档案缺失，知识类型没有定制选择标准，前沿快报断更，信息密度和洞察深度不稳定。

### D3 = 5.3

总目录和两大 Track 成立；但 Obsidian 双链/标签/人物/公司索引基本缺失，演化链靠人工叙述，不能支撑自动 Doctor。

### D4 = 4.2

表格和 emoji 有基本分层；但全库零图表，数据口径不成体系，doc-01 过长，旧对话遗留内容影响体验。

### D5 = 2.5

v2 baseline 仍评估 baseline-v0，不把后续 Phase 0 git 化计入。baseline-v0 无 git、无自动 changelog、无 SOP、无飞轮、无运行报告。

### D6 = 2.8

基线只部分具备信源分级、两大 Track、少量表格和 Research Log。三粒度收录、资源分离互链、反链、source funnel、公司 dossier、数据口径、校准集等均未达成。

## Phase 1 v2 提分优先级

1. D5：把 Phase 0 已完成的 git/_meta/SOP 纳入状态评测，并补 flywheel schema。
2. D2：建立目标公司 dossier 模板和中国公司深度板块。
3. D1：给所有动态/产品数据类条目补 `knowledge_type / accessed_at / stale_after`。
4. D3：引入 tags、wiki-links、人物/公司索引。
5. D4：为关键模型/公司/指标补图表与数据口径。
