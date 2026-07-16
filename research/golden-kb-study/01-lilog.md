# G-01 Lil'Log(Lilian Weng)—— 低频高深的综述式个人知识库

- 主站:https://lilianweng.github.io/
- 实际访问:首页、/faq/、/archives/、样本文 `posts/2023-06-23-agent/`(LLM-powered Autonomous Agents)、`posts/2025-05-01-thinking/`(Why We Think)均抓取成功(2026-07-11)。

## a. 结构解剖

**信息架构**:极简五入口导航 —— `Posts | Archive | Search | Tags | FAQ`。首页即文章流(全文摘要+元信息),无任何专题页、分类页、推荐位。

**条目元数据格式**(每篇统一):
> `Date: July 4, 2026 | Estimated Reading Time: 28 min | Author: Lilian Weng`

**样本 1:《LLM-powered Autonomous Agents》(2023-06-23,31 min)**
- 顶部目录(TOC 锚点),尾部固定四件套:**Citation 块**(纯文本引用格式 `Weng, Lilian. (Jun 2023). "LLM-powered Autonomous Agents". Lil'Log. https://...` + BibTeX `@article{weng2023agent,...}`)、**References 列表**、**标签**(Nlp / Language-Model / Agent / Steerability / Prompting)、上一篇/下一篇。
- 行文中引用一律 `(作者 et al. 年份)` 且链接直达 arXiv,如 `[Wei et al. 2022](https://arxiv.org/abs/2201.11903)`。
- **密集自引**:讲 CoT 时直接链到自己旧文的小节锚点 `posts/2023-03-15-prompt-engineering/#chain-of-thought-cot`;讲 UCB 链到 2018 年老虎机文章的锚点。旧文因此持续被赋能而不是沉底。

**样本 2:《Why We Think》(2025-05-01,40 min)**
- 开头声明外部评审:"Special thanks to John Schulman for a lot of super valuable feedback and **direct edits** on this post."——顶级从业者直接改稿。
- Citation 块同样存在(`@article{weng2025think,...}`)。

**样本 3(前置依赖声明)**:《Diffusion Models for Video Generation》(2024-04-12)正文首段有 "🥑 **Required Pre-read**: Please make sure you have read the previous blog on 'What are Diffusion Models?' … before continue here."——显式声明阅读前置,而非默默假设。

## b. 维护工作流逆向

- **频率**:Archive 页显示 2026 年 2 篇(7/4《Harness Engineering for Self-Improvement》28min、6/24《Scaling Laws, Carefully》25min)、2025 年 1 篇、2024 年 4 篇。**每年 1–5 篇,每篇 20–40 分钟阅读量**——用极低频换极高单篇密度,自 2017 年持续("I'm documenting my learning notes in this blog since 2017")。
- **旧文更新机制**(FAQ 原文):"Yes, I update my old posts periodically. Everytime I would add an **one-line update message in blue on top of that post**."——更新留痕:顶部一行蓝色更新说明。
- **纠错机制**(FAQ):发现错误发邮件;她明说单人时间有限,处理有延迟("time of one person is limited")。
- **完备性预期管理**(FAQ):承认综述不可能覆盖所有论文,欢迎邮件补充 pointer——把"漏了"变成正常协议而非事故。
- **工具**:Hugo + PaperMod 主题;图用 Google Presentation 画(FAQ 自述)。把关人 = 本人 + 特邀评审(如 Schulman)。
- **翻译治理**(FAQ):允许翻译但"please keep the original post link on top"——溯源链保护意识延伸到下游转载。

## c. 可移植实践提取(KB-Agent 应该……)

1. **KB-Agent 应该给每篇文档生成统一元信息行(创建日期/预计阅读时长/最后校订日期)**。证据:Lil'Log 每篇统一 `Date | Estimated Reading Time | Author`,阅读时长让"这篇值多少注意力"可预判。
2. **KB-Agent(Doctor)修订旧文档时,必须在文档顶部追加一行带日期的更新说明,而非静默改写**。证据:FAQ 明文"add an one-line update message in blue on top"。
3. **KB-Agent 应该维护文档间的细粒度互链(链接到小节锚点而非整篇),并在新文档写作时强制检索旧文档可链点**。证据:agent 文章链接自家旧文 `#chain-of-thought-cot`、`#upper-confidence-bounds` 锚点。
4. **KB-Agent 应该给每篇核心文档生成"引用块"(如何引用本文,含稳定 URL)**,把知识库当可被引用的正式出版物运营。证据:每篇尾部 Cited as + BibTeX。
5. **KB-Agent 应该支持"前置依赖"字段:阅读本文前应先读哪篇**。证据:视频扩散文的 "Required Pre-read" 声明。

## d. 不该抄的部分

- **年更 1–5 篇的节奏**:Lilian 的护城河是 OpenAI/前沿一线视角+全文献综述能力,单篇成本极高。用户的秋招场景需要月级甚至周级的行业动态更新,照抄此节奏会让知识库饿死。KB-Agent 应把"综述级长文"设为少数旗舰文档,日常靠更轻粒度(见 G-03)。
- **零导航层**:她只有时间轴+标签,因为读者是主动搜索的研究者。用户知识库要服务"面试前 30 分钟速查",必须有场景化入口(见 G-10/G-17)。
- **纯邮件纠错**:单人博客可以慢;KB-Agent 的 Doctor 就是为了替代"等作者有空"。
