# G-12 a16z AI Canon —— 分层策展 + 维护腐烂的反面教材

- 链接：https://a16z.com/ai-canon/
- 实际访问：AI Canon 页面。

## a. 结构解剖

AI Canon 发布于 2023-05-25，目标是给 AI 初学者和实践者一个现代 AI 阅读路径。它的结构非常清晰：gentle introduction、foundational learning、technical deep dive、practical guides、market analysis、landmark research results。

它最强的地方是读者深度分层：入门解释、技术课程、实践指南、市场分析、里程碑论文各归其位。Landmark research results 还给论文标年份，例如 Attention Is All You Need (2017)、BERT (2018)、GPT (2018)、GPT-3 (2020)、InstructGPT (2022) 等，这对“经典知识历史定位”非常有价值。

## b. 维护工作流逆向

AI Canon 更像一次大型策展，而不是持续维护的动态知识库。页面仍包含很多 2023 时点的 AI app stack 和 benchmark 入口。它的价值因此是正反两面：

- 正面：分层策展、学习路径、经典论文时间线。
- 反面：策展型知识库如果没有 review cadence，会在产品/API/工具层快速过期。

## c. 可移植实践

1. KB-Agent 应给入门/技术/实践/市场/经典论文分别设入口。
2. 经典论文要保留年份、开创点、后续演化，而不是按“最新”排序。
3. 策展页必须有 `last_reviewed`、`stale_after`、`review_status`。
4. 工具/API/实践指南要比经典论文更频繁复检。

## d. 不该抄的部分

- 不要把一次性 canon 当作长期正确。
- 不要让过时工具页继续占据主路径。
