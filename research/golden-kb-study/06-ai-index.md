# G-08 Stanford HAI AI Index —— 数据口径、年度快照与图表规范

- 主站：https://hai.stanford.edu/ai-index/2026-ai-index-report
- 访问页面：2026 AI Index Report、2025 AI Index Report、past reports/public data 入口。

## a. 结构解剖

AI Index 的核心不是“观点”，而是按年度生产的结构化数据产品。2026 报告页面把全书分成 Research and Development、Technical Performance、Responsible AI、Economy、Science、Medicine、Education、Policy and Governance、Public Opinion 九章。

页面明确提供 full report、past reports、public data。2025 页面同样提供 report、public data、policy highlights、chapter lineup。重要的是，它把“结论”和“数据口径/数据集”拆开：读者可以看 top takeaways，也可以回到 public data。

2026 top takeaways 展示了数据表达的形式：每条结论后接 “See: Chapter X”。这是一种优秀的可追溯摘要：摘要不是悬空观点，而是指向可核查章节。

## b. 维护工作流逆向

- 年度固定节奏，适合做宏观行业 snapshot。
- 每年保留 past reports，形成趋势纵向比较。
- 章节按社会、经济、技术、政策等大维度分层，避免把 AI 只当技术榜单。
- 对关键数字使用章节和 public data 兜底，允许读者追到数据表。

## c. 可移植实践

1. KB-Agent 需要 `data_claim` 规范：数字必须有来源、日期、样本、口径、不可比提醒。
2. 图表不是装饰，而是对趋势、对比、漏斗、矩阵的首选表达。
3. 年度/季度 snapshot 要归档，不能被最新数据静默覆盖。
4. 任何总结型内容都应能追到来源章节或数据行。
5. AI PM 面试常用数字应单独维护“数据弹药卡”，每条卡有 last_reviewed。

## d. 不该抄的部分

- AI Index 是宏观报告，不适合直接承担每日更新。
- 它的章节粒度很大，用户知识库还需要目标公司、产品形态、面试问题等更细入口。
