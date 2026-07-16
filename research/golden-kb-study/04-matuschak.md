# G-05 Andy Matuschak Evergreen Notes —— 原子化+概念命名+密集双链的"思考环境"型知识库

- 主站:https://notes.andymatuschak.org/
- 实际访问(2026-07-12):`About_these_notes`、`Evergreen_notes`、`Evergreen_notes_should_be_atomic`、`Evergreen_notes_should_be_concept-oriented`、`Evergreen_notes_should_be_densely_linked`、`Taxonomy_of_note_types`、`§What's top of mind`(标题 URL 返回 404,改用稳定 slug `zPKTSiU725W9WQCqoVPBcxm` 访问成功)、`Work with the garage door up`(slug `zCMhncA1iSE74MKKYQS5PBZ`)。共 8 条全部成功。
- 抓取方式说明:站点是 SPA,但每页内嵌 `notetower-initial-data` JSON,含每条笔记的 `slug / title / contentMarkdown / backlinkedNotes / linkedNoteSlugs / ctimeMillis / mtimeMillis` 全量结构化数据——本报告的链接计数即来自该字段。
- 局限:`ctimeMillis/mtimeMillis` 实测值为 0(1970 占位),**实际创建/修改时间不可考**,更新频率相关结论标 `TODO(研读缺口)`。

## a. 结构解剖

**信息架构:刻意没有架构**。无首页、无目录、无搜索入口,About 原文:"For now, there's no index or navigational aids: you'll need to follow a link to some starting point." 唯一推荐入口是一条 `§` 前缀的 outline 笔记(`§What's top of mind`,自述 "Sort of like a /now page… focused on what I'm thinking about")。整个库 = 一张纯链接驱动的概念网。

**条目格式**:每条笔记 = 一个概念 = 一个 URL(稳定随机 slug + 可读标题双寻址);正文用 `[[slug:::标题]]` 双链;尾部 `## References` 附文献与大段原文引块(Luhmann 1992、Ahrens 2017 反复出现)。链接密度实测:`Evergreen notes` 出链 15 / **反链 43**;`…densely linked` 出链 11 / 反链 22——反链数据是系统一等字段(`backlinkedNotes`)。

**样本 1:《Evergreen notes should be atomic》**
- 标题即完整论断(不是 "原子化" 这种话题词)。正文第一句就是命题的精确表述:"It's best to create notes which are only about one thing—but which, as much as possible, capture the entirety of that thing." 随后给出双向失败模式(太宽→链接浑浊;太碎→网络破碎)、软件工程类比(separation of concerns),并链到姊妹命题 `Evergreen note titles are like APIs`。References 引 zettelkasten.de 原文佐证。

**样本 2:《Taxonomy of note types》——笔记成熟度阶梯(本站最可移植的单页)**
- 开头公开挂着未完成标记:"**==TODO: flesh this out; write a note for each note type; etc==**"。
- 定义了一条"上升阶梯":Daily working log 的临时涂鸦 → writing inbox 的半成品 → Evergreen notes,而 evergreen 内部又分层:"stubs implicitly defined through backlinks" → "simple definitions for terms of art" → "precise, narrow declarative notes" →(证据不足时)问句笔记("To what extent is exceptional ability heritable?")→ "higher-level APIs" → "notes abstracting over many other notes" → outline notes(§)。
- 阶梯之外是 proper noun notes(文献笔记/人物笔记/公司笔记,例:Confluent),明确定性 "These note types are **weakly evergreen**… they're not as useful to build on"。
- 落地方式一句话:"Tactically speaking, I usually denote a note's 'type' with a tag."
- 收尾自我告诫:"Don't over-obsess or over-formalize this stuff."

**样本 3:《Work with the garage door up》(方法论自举)**
- 公开半成品思考本身就是方法论:"These notes are mostly written for myself… I'm sharing them publicly as an experiment"(About);本条论证公开过程的复利("creates more invested, interesting followings")。
- 维护痕迹实证:References 里 Robin Sloan 的邮件链接后标注 "**(link broken as of [[2024-12-17]])**"——死链不删除,就地打上带日期的失效标记,且日期本身是一条双链日记笔记。

## b. 维护工作流逆向

- **更新频率**:页面数据的时间戳字段为占位 0,无归档页,**无法从站内证据测出实际节奏**。`TODO(研读缺口):仅能从 About 的 "My morning writing practice" 链接推断存在每日晨间写作惯例,未能抓到该笔记正文验证。`
- **入库缓冲**:двух 级 inbox——`A reading inbox to capture possibly-useful references`(读到的东西先进读收件箱)与 `A writing inbox for transient and incomplete notes`(半成品笔记进写收件箱),经消化才升级为 evergreen(《Evergreen notes》"Implementing an evergreen note practice" 一节)。**收集与入库是两个动作**。
- **复检机制内生于链接行为**(《…densely linked》原文):"Finding the right links requires reading old notes, so it's also an **organic mechanism for intermittently reviewing** the notes we've written(Evergreen note maintenance approximates spaced repetition)"——写新笔记被迫重读旧笔记,维护是写作的副产品而非独立任务。
- **允许欠账**:链接可以指向尚不存在的笔记,"Backlinks can be used to implicitly define nodes"、"it's very freeing to be able to link to a stub"——节点由反链隐式定义,降低即时写作压力。
- **纠错**:死链带日期就地标注(见样本 3);TODO 公开可见(见样本 2)。
- **工具与把关**:自研私有系统,拒绝开放:"no, I haven't made this system available for others to use. It's still an early research environment, and [[Premature scaling can stunt system iteration]]." 把关人 = 本人;经济支撑 = Patreon 众筹研究金。

## c. 可移植实践提取(KB-Agent 应该……)

1. **KB-Agent 应该强制"概念导向 + 论断句标题":每条概念笔记按概念而非按来源(文章/公司/事件)组织,标题写成可独立引用的完整命题**。证据:《…concept-oriented》"factor by concept (rather than by author, book, event, project, topic)… there's no accumulation" ——按来源组织会导致同一概念散落多处、永不合流;这正是 AI 知识库月度迭代时"新文章进来就新建一篇"的病根。标题范例:"Evergreen notes should be atomic" 而非 "关于笔记原子化"。
2. **KB-Agent 应该给每条笔记加"成熟度/类型"元字段(stub / 定义 / 论断 / 问题 / 综合 / 索引§),Doctor 周检的核心 KPI 就是推动笔记沿阶梯上移**。证据:《Taxonomy of note types》完整阶梯 + "I usually denote a note's 'type' with a tag";证据不足的笔记降格为问句标题("To what extent is…?")是对"不确定性显式化"的优雅处理。
3. **KB-Agent(Curator)应该实现两级收件箱:reading inbox(原始链接/引用)与 writing inbox(半成品笔记)分离,只有经过消化改写的内容才能进正库**。证据:《Evergreen notes》列出的两条 inbox 实践 + "Most people take only transient notes" 的对立面设计。
4. **KB-Agent 应该把反链做成一等数据,并允许链接到尚不存在的笔记(stub 由反链隐式定义);Doctor 定期盘点高反链 stub,作为"下一篇该写什么"的选题信号**。证据:数据结构里的 `backlinkedNotes` 字段(Evergreen notes 反链 43 条)、"Backlinks can be used to implicitly define nodes"。
5. **KB-Agent(Doctor)处理死链/失效引用时,就地标注 "link broken as of YYYY-MM-DD" 而非静默删除**。证据:《Work with the garage door up》References 中 "(link broken as of [[2024-12-17]])"——保留证据链的同时声明失效,面试引用时不会踩坑。
6. **KB-Agent 生成新笔记时必须先检索旧笔记寻找链接点,把"找链接"设计成强制步骤**。证据:"Finding the right links requires reading old notes… may lead to surprising discoveries"——链接步骤同时承担复检和查重职能,天然适合 agent 自动化(这恰是人类做起来最累、agent 做起来最便宜的环节)。

## d. 不该抄的部分

- **"为自己写、无视读者" + 零导航**:About 明说 "If a note seems confusing or under-explained, it's probably because I didn't write it for you!"。用户的知识库有明确的第二读者场景(面试前 30 分钟的自己、模拟面试的提问者),必须有场景化入口和自解释性;照抄"无索引、跟着链接走"会让速查失败。
- **反标签、纯关联本体的立场**:Andy 明确主张 "Tags are an ineffective association structure"、"Prefer associative ontologies to hierarchical taxonomies"。这对"用自己大脑做检索引擎"的研究者成立;但 KB-Agent 的 Doctor 需要机器可枚举的结构(标签/目录/frontmatter)来做全库体检和覆盖率统计。应取折中:双链管语义关联,受控标签管机器盘点——两套并行,而非二选一。
- **"过早规模化会阻碍迭代"的研究节奏**:他拒绝把系统产品化、无交付期、靠 Patreon 供养开放式探索。KB-Agent 有硬死线(2026 秋招),eval 先行、快速定型 schema 比无限迭代形态更重要。
- **维护依赖本人写作冲动(晨间写作、间隔重复式重访)**:单人手工的冥想式维护不可自动化验证;KB-Agent 的 Doctor 就是要把"重访旧笔记"变成确定性的周度流程,而不是靠灵感。
