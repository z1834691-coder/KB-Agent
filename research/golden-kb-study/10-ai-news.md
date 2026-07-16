# G-14 AI News（smol.ai）—— 高频自动策展 + 人工把关的动态管线

- 主站：https://news.smol.ai/
- 实际访问：首页、最近 30 天 issues、tags/search 入口。

## a. 结构解剖

AI News 首页说明它面向 AI engineers，每个工作日总结 top AI Discords、AI Reddit、AI X/Twitter。首页提供 issues、tags、搜索和最近 30 天列表。每条 issue 有大量 tag、来源账号和摘要。

它最有价值的不是单条事实，而是动态管线形态：多源聚合 → 日更摘要 → tag 化 → 可搜索归档。这正对应用户要的持续更新 agent。

## b. 维护工作流逆向

- 高频：weekday daily。
- 输入广：社交平台、社区、论坛、开发者讨论。
- 输出压缩：把大量信息压成可读 issue。
- 可观测：issues、tags、搜索让历史可回溯。

## c. 可移植实践

1. KB-Agent 的 Curator 应有 source funnel：crawled、candidate、accepted、rejected、pending verification、risk blocked、promoted to evergreen。
2. 高频源进入候选池，不直接写正库。
3. 每日/周度简报应成为知识库产品，而不是日志副产物。
4. tag 体系要支持同一话题演化回溯。
5. 自动摘要必须有人审抽查，尤其是模型发布、价格、benchmark、公司传闻。

## d. 不该抄的部分

- AI News 是资讯压缩产品，KB-Agent 的目标是 AI PM 知识库；不能把日更资讯当最终形态。
- 社交源摘要有传闻和噪音风险，必须回到官方/论文/一手源。
