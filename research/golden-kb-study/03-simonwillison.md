# G-03 Simon Willison —— 多粒度高频流水线 + 全站可查询的工业级个人知识库

- 主站:https://simonwillison.net/
- 实际访问(2026-07-12,全部成功):首页 `/`、`/about/`(含 Colophon+Disclosures)、`/tags/` 全量标签索引、年度归档 `/2026/`、blogmark 样本 `/2026/Jul/8/rewriting-bun-in-rust/`、quotation 样本 `/2026/Jul/3/josh-w-comeau/`、方法论自述文 `/2026/Feb/20/beats/`、TIL 子站 https://til.simonwillison.net/ 首页。
- 未访问:Datasette 后台实例 datasette.simonwillison.net、simonw/til repo 内部 —— 相关结论标 `TODO(研读缺口)`。

## a. 结构解剖

**信息架构**:首页导航即粒度分层声明——`Entries | Links | Quotes | Notes | Guides | Elsewhere`,外加 Highlights(近期长文精选)、按标签的快捷入口、逐年归档(2002–2026 连续 25 年)。2026-02 起又加了 "beats" 层(Elsewhere):Release / TIL / Museum / Tool / Research / Sighting 等站外活动的徽章式短条目。

**粒度分层的量化证据**(/2026/ 归档页原文):"February - **10 entries, 47 links, 21 quotes, 13 notes, 6 chapters**"——链接短评(blogmark)和引语(quotation)数量是正式长文(entry)的 6–8 倍。粒度金字塔:大量轻条目供养少量重条目。

**样本 1:blogmark《Rewriting Bun in Rust》(2026-07-08)**
- 结构 = 指向原文的标题链接 + **via 溯源**("(via [news.ycombinator.com/item?id=48837877])")+ 数百词自有评论。
- 评论绝不只是转述:补历史坐标("Joel Spolsky highlighted that in Things You Should Never Do, Part I back in April 2000!")、提炼核心问题("How do you review a PR with +1 million lines added?")、并**内链自己的标签页**(正文里 `conformance suite` 一词直接链到 `/tags/conformance-suites/`)。
- 尾部标签 11 个,混合了概念(agentic-engineering)、公司(anthropic)、语言(rust/zig)、产品(bun)。

**样本 2:quotation《A quote from Josh W. Comeau》(2026-07-03)**
- 结构 = 纯引文 + 署名行 "— Josh W. Comeau [bsky 原帖链接], **via** Salma Alam-Naylor [发现渠道链接]"——引文的"作者链"与"发现链"是两个独立字段。
- 标签含**人物标签** `josh-comeau 5`——同一个人的言论可被聚合追踪。每个标签页都有独立 Atom feed(about 页:"Every tag on my blog has its own feed… adding .atom to the URL")。

**标签体系**:`/tags/` 页实测 1,845 个唯一标签,每个带条目计数(`ai 2,090`、`ai-assisted-programming 381`、`sqlite-utils 232`)。标签四大类混用:概念 / 人物(armin-ronacher, andrej-karpathy 43)/ 产品项目 / 私有梗(pelican-riding-a-bicycle)。

**TILs**:独立子站,自述 "Things I've learned, collected in simonw/til"——按主题目录组织(python 66 · github-actions 29 · macos 26…),内容为"今天学会的一个小操作",发布门槛远低于 blog entry;2026-02 起通过 beats 回灌主站时间线。

**其他一等结构**:series(《beats》一文尾部 "Part of series How I blog",串起 4 篇方法论文);月度归档页每月同时列出各粒度计数;文内更新留痕(2026-07-02 条目内 "**Update 10th July**: here's Geoffrey's talk on YouTube")。

## b. 维护工作流逆向

- **频率实测**(/2026/ 归档):月均 9–14 篇 entry + 20–47 条 link + 14–21 条 quote + 若干 note,合计**每月约 60–100 条、日均 2–3 条**,且自 2002 年连续 25 年。这是"高频轻粒度"路线的极限样本。
- **旧文更新机制**:条目内追加带日期的 Update 行(见上);产品发布类条目之间前后互链("The first dot-release since 4.0 a few days ago [链接]")形成事件链。
- **工具链**(about 页 Colophon 原文):"a custom web application built using Django… content in PostgreSQL, which is **backed up to JSON files in simonw/simonwillisonblog-backup. These are then deployed to a Datasette instance**"——知识库本体是结构化数据库,支持 faceted search 和任意 SQL 查询,git 里存 JSON 快照。
- **站外内容自动回灌**:beats 文详述 5 条自动化管道(GitHub releases 从 Actions 生成的 JSON 导入、TIL 用 SQL over HTTP 导入、Research 用 regex 解析 README),自评 "I'm fine with a brittle solution that would be too risky against a source that I don't control myself"——对自控源允许脆弱脚本,风险分级明确。
- **压缩产品化**:免费周报(自动从博客生成,另有专文《How I automate my Substack newsletter》)+ 付费月报 "It's intended to be a **ten minute read that catches you up** on the most important developments from the past month"、口号 "**Pay me to send you less!**"——月度压缩摘要本身是最高价值产出。
- **利益披露纪律**:about 页 Disclosures 一节逐项声明("I have not accepted payments from LLM vendors… often under NDA",连 OpenAI 付过一次出场费都单列)。
- **方法论自举**:怎么运营这个博客本身就是博客的 series(How I blog:link blog 方法、首页改版、newsletter 自动化、beats),每次基础设施改动都发文并链 PR("the most interesting PRs are Beats #592…")。
- **把关人**:本人;纠错靠读者社交渠道反馈 + 文内 Update。

## c. 可移植实践提取(KB-Agent 应该……)

1. **KB-Agent 应该建立三档条目 schema——entry(长文)/ blogmark(链接+短评)/ quotation(引语+出处),Curator 收集时强制归类,禁止把所有东西都写成同一种"笔记"**。证据:导航六分区 + 归档页计数(Feb 2026:10 entries vs 47 links vs 21 quotes)——高频动态天然应该以轻粒度入库,这正是秋招"周级动态"需要的形态。
2. **blogmark 类条目必须同时有"原文链接"和"via 发现渠道"两个溯源字段,且短评必须含至少一条自有增量(个人判断/历史对照/与库内旧条目的关联)**。证据:Bun blogmark 的 `(via HN)` + Joel Spolsky 2000 年对照 + 内链自家 `/tags/conformance-suites/`;quotation 的 "— 作者, via 发现者" 双链。
3. **KB-Agent 应该把"人物"作为一等标签类型,聚合同一人的历次观点**。证据:`josh-comeau 5`、`andrej-karpathy 43` 等人物标签——对求职者,"某公司 CTO/CEO 历次公开表态"聚合页就是面试弹药库。
4. **KB-Agent(Doctor)每周/每月产出一份"十分钟读完"的压缩简报,把它当作知识库的第一产品而非副产品**。证据:Simon 把月度压缩做成付费产品("Pay me to send you less!"),说明在高频流水线上,**压缩层比采集层更稀缺**。
5. **KB-Agent 应该把知识库当结构化数据维护:条目元数据(类型/日期/标签/via)机器可查询,归档页自动生成各粒度计数**。证据:Colophon 的 PostgreSQL→JSON git 备份→Datasette 管道;月度归档的 "10 entries, 47 links, 21 quotes" 自动计数——KB-Agent 用本地 frontmatter + git 完全可以复刻,这也是 Doctor 做全库体检的前提。
6. **KB-Agent 的自动化管道行为要自我文档化:每次改采集/入库规则,生成一条方法论记录**。证据:beats 文详述五条导入管道并链到具体代码行和 PR;"How I blog" series 把方法论沉淀为可回溯的公开文档。

## d. 不该抄的部分

- **全行业火力全开的采集广度(日均 2–3 条、1,845 个标签)**:Simon 是全职独立开发者,博客即职业。用户是秋招候选人,时间预算完全不同;Curator 必须按"具身智能 PM 相关度"做强过滤,宁可漏掉泛 AI 新闻,不可让库变成第二个 Hacker News。
- **自建 Django+PostgreSQL+Datasette 的重基础设施**:那是 22 年演化出来的定制系统。KB-Agent 的运行时是 Claude Code + 本地 markdown + git,应该用 frontmatter 模拟结构化,而不是引入数据库。
- **无治理的标签自由生长**:1,845 个标签里有大量 3–5 条的长尾和私有梗标签(pelican-riding-a-bicycle 可行,因为 Simon 自己就是全部的写入方和主要读者,记得住)。KB-Agent 自动打标签时若不加受控词表 + Doctor 定期合并同义标签,长尾会迅速失控。
- **Sighting/Museum 等生活流内容类型**:多粒度不等于什么都收;KB-Agent 的类型系统应封闭在求职场景相关的类型内。
