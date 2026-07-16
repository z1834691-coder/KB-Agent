# KB-Agent Failure Patterns v0.1

> 固定必读。每轮运行前读取，运行后如发现新失败模式则追加。

## F-001 · 直接把用户提供材料全文入库

表现：把公众号、小红书、博客长文完整复制进知识库。

风险：版权、文档膨胀、溯源缺失、知识低密度。

防护：先判 source_type 和收录粒度；外部内容默认“摘要 + 链接 + 必要短引”，不得全文搬运。

## F-002 · 不区分知识类型导致时效误判

表现：把经典论文当过时，或把旧 API/价格当当前事实。

防护：先标 `knowledge_type`，再按 rubric v2 保鲜策略处理。

## F-003 · GitHub issue / 社区帖子被当成事实

表现：未确认 issue 直接写入正文。

防护：issue 只能进入 candidate/verification，除非 maintainer 确认、官方文档支持或有可复现实验。

## F-004 · 目标公司内容过浅

表现：DeepSeek/阶跃/阿里/字节只写一句话定位，没有技术路线、产品、商业、组织、风险和面试问题。

防护：公司内容必须走 company_dossier 模板。

## F-005 · 只处理单条 case，知识库状态没有变好

表现：行为 eval 分数上升，但状态 eval 不动。

防护：每轮行为改进必须检查是否写回 SOP、结构、元数据或 regression。

## F-006 · Judge 打分漂亮但证据不足

表现：高分 case 没有引用具体 evidence。

防护：每个维度必须有证据；每轮抽查高分和低分 case；跑校准集。

## F-007 · 上下文过载后凭印象修改

表现：读了大量材料后直接改文件，无法说明证据来自哪里。

防护：70% 上下文写 snapshot，80% 主动 compact，长文必须输出事实摘要/判断依据/待确认点。

## F-008 · 跳过总览导致重复建档

表现：新建一个已有主题的文档，或把内容写到错误位置。

防护：修改前读总览、候选目标文件、相关历史条目。

## F-009 · visualizer 只显示新增条数

表现：dashboard 看起来有更新，但不能解释为什么收/拒/改。

防护：显示 source funnel、case-by-case、prompt diff、维度分、过拟合警报。

## F-010 · 人审触发点过晚

表现：低置信、版权、删除、大改已经执行后才告知用户。

防护：按 `protocols/03-human-review-protocol.md` 阻塞式确认。

## F-011 · 官方通知被高估为主知识

表现：看到 deprecation、alias shutdown、普通 release note 就准备写入 AI PM 主知识库。

风险：知识库被低学习价值通知污染；真正有价值的底层论文、产品方法论、公司战略被淹没。

防护：执行 `impact_scan`。先判断通知本身是否有 AI PM 学习价值，再扫描现有文档是否受影响。无受影响文档且无 PM 转译价值时，默认 reject 或 source_log；有受影响文档时才写 metadata、迁移提醒或更新任务。

## F-012 · verify/candidate 任务悬空

表现：把低置信内容放进“待核实”后没有 owner、next_check_at、promotion_condition、close_condition。

风险：候选池无限膨胀，agent 以为自己很谨慎，实际只是把噪音延期。

防护：任何 `verify`、`candidate`、`source_log` 都必须写任务生命周期字段。没有证据路径、无法验证或验证成本超过价值时，直接 reject。

## F-013 · 产品案例入主库阈值太宽

表现：只因为某产品/平台发生变化，就抽象出“产品教训”并放入主库。

风险：AI PM 主库变成产品新闻/平台生命周期记录，而不是求职和能力成长系统。

防护：使用 `pm_transfer_score`。求职/面试表达、公司研究、产品决策、方法论复用四项至少命中两项，才可进入 AI PM 主库。

## F-014 · ops_only 与 AI_PM_core 不可观测

表现：输出文字里说“这只进运维资产”，但结果文件和 dashboard 无法统计主库、运维、source log、reject 的比例。

风险：用户看不到 agent 是否真的在控制噪音；后续无法做数据飞轮。

防护：results.jsonl 必须含 `decision`、`target_zone`、`granularity`、`freshness_policy`、`risk_tier`、`user_gate`、`failure_mode` 等结构字段；visualizer 必须显示 funnel。

## F-015 · 标杆实践照搬或泛化不充分

表现：研读 Lil'Log、Simon Willison、AI Index 等标杆后，只说“学习元数据/图表/分层”，没有本地映射、非目标和验证方式。

风险：对标停留在口号，知识库结构没有真正变好。

防护：标杆实践必须输出 `practice`、`adopt_level`、`local_mapping`、`non_goals`、`validation_check`。只采用能解决当前 KB 短板的实践。
