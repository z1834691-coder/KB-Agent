# G-06 Anthropic Docs + Cookbook —— 官方文档类型分层 + changelog + 可运行样例

- 主站：https://docs.anthropic.com/（当前重定向到 `platform.claude.com/docs/en/home`）
- Cookbook：https://github.com/anthropics/anthropic-cookbook（当前 GitHub 重定向到 `anthropics/claude-cookbooks`）
- 实际访问：Docs 首页、release notes、pricing、define success/build evaluations、cookbook repo。

## a. 结构解剖

Anthropic Docs 的首页不是“文档目录”，而是按开发者旅程组织：Get started → Build → Evaluate and ship → Operate。首页同时把产品面拆成 Messages、Managed Agents、Admin、API reference、Resources。对 KB-Agent 来说，这说明文档结构应服务任务流，而不是只按知识主题排。

“Evaluate and ship”下面单列 prompting best practices、run evals、batch testing、safety/guardrails、latency、price。这对 KB-Agent 的 harness 建设是直接范本：eval 不是附录，而是上线前的主路径。

Release notes 是一等页面，逐日记录 API、SDK、模型、内存、Managed Agents、webhooks 等变化。它给动态知识提供了标准结构：日期、影响面、迁移要求、相关链接。

Pricing 页面展示了另一个关键点：同一个模型的“价格”不是一个数，而是 base input、cache writes、cache hits、output、多云平台、地区端点等多个单位。KB-Agent 处理模型价格时必须拆单位，不能粗暴做一张总榜。

Cookbook/recipes 则承担“可运行示例层”：docs 讲概念与接口，cookbook 讲 runnable patterns。它实现了用户点名的 blog ↔ repo 配套思路在官方文档中的版本。

## b. 维护工作流逆向

- 文档首页按生命周期组织，说明官方认为“从 idea 到 production”是主流程。
- Release notes 承担变更事实源，动态知识不靠文章记忆。
- Eval 文档强调 success criteria 先于 prompt refinement，且建议边界场景、自动评分、LLM-as-judge 前先校验可靠性。
- Cookbook 与 docs 解耦：概念/参考/教程/样例分开，避免一篇文档同时承担所有任务。

## c. 可移植实践

1. KB-Agent 文档应分出 `concept / how-to / reference / cookbook` 四类，避免把概念讲解、操作步骤、API 事实和可运行示例混写。
2. 动态 API/模型/价格类信息必须进入 release-note/deprecation metadata，而不是直接覆盖正文。
3. 评测文档必须定义 success criteria、edge cases、评分方法、Judge 可靠性校验。
4. 可运行资产要和正文分离，并有版本/依赖/最后运行时间。
5. 价格、上下文窗口、tokenizer、数据保留等易变事实要有 `accessed_at`、`source_url`、`stale_after`。

## d. 不该抄的部分

- 官方文档默认读者是开发者，用户知识库还要服务 AI PM 面试和中文目标公司研究，不能只复制 API 导航。
- 官方文档可把最新事实作为唯一真相；个人知识库还要保留理论演化与学习路径。
