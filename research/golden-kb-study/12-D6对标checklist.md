# D6 对标 checklist v2.0

> 用法：D6 不再是“像某某一样好”的口号分，而是标杆实践采纳率。每项以 `已达成 / 部分 / 未达成 / 不适用` 记录，并要求证据。

## Checklist

| ID | 维度 | 标杆来源 | 检查项 |
|---|---|---|---|
| G01-C1 | D1 | Lil'Log | 核心文档有引用/参考文献块，关键结论可追到一手源 |
| G01-C2 | D3 | Lil'Log | 旧文更新在文档顶部留日期说明，不静默覆盖 |
| G01-C3 | D3 | Lil'Log | 文档间有小节级互链，而非只链整篇 |
| G01-C4 | D3 | Lil'Log | 有前置阅读/依赖关系字段 |
| G02-C1 | D2 | Chip Huyen | 撞题内容写明相对已有权威材料的增量 |
| G02-C2 | D3 | Chip Huyen | 正文与资源/代码/脚本分离互链 |
| G02-C3 | D5 | Chip Huyen | future work/待补清单被系统追踪 |
| G02-C4 | D1 | Chip Huyen | 口头信息标注人名、场合、日期 |
| G03-C1 | D2 | Simon Willison | 条目支持长文、链接短评、引文三粒度 |
| G03-C2 | D1 | Simon Willison | blogmark 同时记录原文链接和 via 发现渠道 |
| G03-C3 | D3 | Simon Willison | 标签含概念、人物、公司/产品，且可统计 |
| G03-C4 | D5 | Simon Willison | 周/月度十分钟压缩简报自动生成 |
| G05-C1 | D3 | Matuschak | 概念笔记采用论断句标题 |
| G05-C2 | D3 | Matuschak | 笔记有成熟度类型：stub/定义/论断/问题/综合/索引 |
| G05-C3 | D5 | Matuschak | reading inbox 与 writing inbox 分离 |
| G05-C4 | D3 | Matuschak | 反链和高反链 stub 作为维护信号 |
| G06-C1 | D3 | Anthropic Docs | 文档类型分离：概念/操作/参考/可运行示例 |
| G06-C2 | D1 | Anthropic Docs | release notes/deprecations 作为动态事实源 |
| G06-C3 | D5 | Anthropic Docs | eval 文档定义成功标准、边界 case、评分方法 |
| G06-C4 | D1 | Anthropic Docs | 价格/模型/API 易变信息带 accessed_at 与 stale_after |
| G08-C1 | D4 | AI Index | 关键数据优先图表化 |
| G08-C2 | D1 | AI Index | 数字有样本、口径、数据来源和章节/表格引用 |
| G08-C3 | D3 | AI Index | 年度/季度 snapshot 归档，支持纵向比较 |
| G10-C1 | D3 | WaytoAGI | 有面向不同读者身份的导航入口 |
| G10-C2 | D5 | WaytoAGI | 更新日志/精选入口是一等页面 |
| G10-C3 | D2 | WaytoAGI | 高频中文生态信息先进入候选池再核验 |
| G11-C1 | D2 | 拾象 | 目标公司档案按 thesis 组织，而非新闻堆叠 |
| G11-C2 | D2 | 拾象 | 公司研究覆盖技术、产品、商业、组织、风险、面试问题 |
| G12-C1 | D2 | a16z AI Canon | 入门/技术/实践/市场/经典论文分层策展 |
| G12-C2 | D1 | a16z AI Canon | 策展页有 last_reviewed、stale_after、review_status |
| G14-C1 | D5 | AI News | Curator 有 source funnel 统计 |
| G14-C2 | D5 | AI News | 高频摘要与正库 evergreen 分层 |
| G14-C3 | D3 | AI News | tag 支持话题演化回溯 |
| G17-C1 | D2 | Lenny's | 所有 PM 内容服务唯一目标读者画像 |
| G17-C2 | D3 | Lenny's | 人物/嘉宾作为一等索引 |
| G17-C3 | D4 | Lenny's | 访谈/播客可转成纪要、takeaway、面试弹药 |

## D6 计分

- 达成 = 1
- 部分 = 0.5
- 未达成 = 0
- 不适用 = 从分母移除，必须说明理由

D6 分数 = `1 + 9 × (得分 / 适用项总数)`，四舍五入到 0.1。

## Baseline-v0 粗评

基于 v0.1 baseline 证据，baseline-v0 只明显具备信源分级雏形、两大 Track、少量表格与 Research Log。多数 checklist 未达成。粗评约 2.8/10，后续 Doctor 全量评测需逐项打证据。
