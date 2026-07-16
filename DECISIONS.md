# 决策日志

> 记录 KB-Agent 项目的关键决策、理由和可复用教训。倒序排列。

---

## 2026-07-12 · D13：v2 数据驱动迭代完成，分流漏斗成为 harness 指标

用户确认 CH-066 可给 1.5 分，表示“极低价值但不是绝对零分”。本轮基于 v1 eval 数据做失败模式分析，并据此生成 `agent-v2`。

新增/更新：
- `evals/analysis/2026-07-12-v1-failure-pattern-analysis.md`：从 v1 最低分、类别均分、case judge 证据中提炼 5 个失败模式
- `evals/failure-patterns.md`：追加 F-011~F-015，包括官方通知高估、verify 悬空、产品案例阈值过宽、ops/main 不可观测、标杆实践泛化不足
- `evals/prompts/agent-v2.md`：新增 `impact_scan`、`task_lifecycle`、`pm_transfer_score`、`benchmark_practice`、结构化 funnel 字段
- `evals/runs/2026-07-12-run003-calibration-v2/`：校准分 10.0，CH-066 用户分更新为 1.5
- `evals/runs/2026-07-12-run004-behavior-smoke-regression-v2/`：30 条 smoke+regression 行为评测，综合分 8.6
- `visualizer/build.py` 和 `visualizer/SPEC.md`：新增分流漏斗面板，展示 decision / target_zone / risk_tier / user_gate

关键结果：
- v1 -> v2 综合分：8.5 -> 8.6，30 条全部 pass。
- 重点修复 case：CH-011 7.8 -> 8.7，CH-001 8.1 -> 8.7，CH-015 8.0 -> 8.5，CH-031 8.1 -> 8.5，CH-080 8.3 -> 8.7。
- v2 的主要收益不是刷分，而是让 agent 的分流、风险和人审边界变成可观测数据。
- holdout 纪律保持：v2 是第二个 prompt 版本，不跑 holdout；v3 后触发 holdout，且不得用 holdout 结果直接调 prompt。

## 2026-07-12 · D12：v1 首轮正式行为评测完成

用户完成 rubric v2 与 judge calibration 人工核查后，本轮执行 `agent-v1` 的正式 smoke+regression 评测。

产出：
- `evals/prompts/agent-v1.md`：selection-calibrated actor prompt，明确 AI PM 主知识价值、KB-Agent 运维价值、噪音/风险三分法
- `evals/judge-calibration-set.md`：升级为 v0.2，确认用户分数口径 = AI PM 知识库信息价值/收录优先级
- `evals/runs/2026-07-12-run001-calibration/`：9 条人工校准对齐记录，平均偏差 0.28
- `evals/runs/2026-07-12-run002-behavior-smoke-regression/`：30 条 smoke+regression 行为评测，综合分 8.5

关键结果：
- v1 已把“官方/issue/工具更新不自动入主库”作为硬规则，能正确分流到 `AI_PM_core`、`source_log`、`ops_protocol`、`private_profile` 或拒收。
- 最强项：隐私/安全阻断、fake news 验证、理论演化、DeepSeek pricing 的 PM 转译。
- 待改进：official deprecation 类需要更明确的 existing-doc scan；ops-only 与 AI_PM_core 的分流应在下一版 visualizer 中单列成 funnel 指标。
- holdout 纪律保持：v1 首版只跑 smoke+regression；holdout 每 3 个 prompt 版本跑一次，且不得用于直接调 prompt。


## 2026-07-12 · D11：三大运行协议成为 KB-Agent harness 硬约束

用户补充了三项关键要求：上下文协议、工具协议、人把关协议。本轮判断为“必须补”，并落地为可执行协议：

- `protocols/01-context-protocol.md`：固定必读、动态上下文、禁止行为、上下文压缩、70/80/90 保守阈值、Run Context Packet
- `protocols/02-tool-protocol.md`：工具分层、读写/验证/git/web/eval 工具规则、高风险动作边界
- `protocols/03-human-review-protocol.md`：H0-H4 人审等级、必须问用户的触发条件、eval 后抽查流程、baseline 大改协议
- `evals/failure-patterns.md`：每轮固定必读的失败模式库
- `evals/protocol-compliance-checklist.md`：每轮 run report 末尾必须勾选的执行清单

关键决定：
- Claude Code/Claude API 的工具能力不是“自动安全”的，必须由 harness 定义工具 schema、权限和人审边界。
- Claude Code 官方未公开固定自动 compact 百分比，KB-Agent 采用保守工程阈值：70% 写 snapshot，80% 主动 compact，90% 禁止继续读长文或动库。
- 用户将作为 Judge 校准与高/低分 case 抽查的关键裁判，相关覆写进入数据飞轮。


## 2026-07-12 · D10：Rubric v2.0 执行完成 + 黄金研读闭环

用户确认 `evals/rubric-v2-upgrade-prompt.md`，本轮执行 v2 升级。

产出：
- `research/golden-kb-study/00-总纲.md`：11 个黄金标杆研读总纲与选择眼光判据 SL-01~SL-10
- `research/golden-kb-study/05-11*.md`：补齐 Anthropic Docs、AI Index、WaytoAGI、拾象、a16z AI Canon、AI News、Lenny's
- `research/golden-kb-study/12-D6对标checklist.md`：D6 从口号化对标改为 checklist 采纳率
- `evals/03-rubric-v2.0.md`：状态/行为 rubric v2，含类型化保鲜、子指标独立计分、B1 可辩护性通道、split 纪律、效率门槛、Judge 校准
- `evals/04-baseline-report-v2.0.md`：baseline-v0 从 v0.1 的 4.7 桥接为 v2 口径 4.1
- `evals/judge-calibration-set.md`：用户待确认校准集候选

关键决策：
- D6 权重降为 5%，变成标杆实践采纳率；释放权重并入 D5，以符合建设期“先把维护系统做起来”的阶段目标。
- v2 默认使用建设期权重；连续两轮状态分 >= 7.5 且 D5 >= 8 后切到稳态权重。
- Judge 每轮正式评分前必须跑用户确认过的校准集。用户确认前，校准集只作为候选。

## 2026-07-11 · D9：迭代可视化 Visualizer = 本地静态 dashboard（零依赖）

形态（由 Claude 定夺）：**`visualizer/build.py`（Python 标准库，零外部依赖）→ 生成 `evals/dashboard.html`**，浏览器直接打开，离线可用。

三层视图对应用户的三条需求：
1. **Case 浏览器**：每条挑战 case 的输入 / agent 输出 / 得分 / Judge 证据，同一 case 的跨版本历史并排（case-by-case 变化可观测）
2. **Prompt diff 视图**：`evals/prompts/agent-vN.md` 相邻版本 unified diff（prompt 演化可追溯）
3. **版本趋势**：综合分折线（状态/行为分色，holdout 方块标记）+ 维度对比条形图（当前 vs 上一版带 Δ）+ 全轮次版本三元组表

防过拟合设计（对应"像训练模型"的要求，与 D7 的 v0.4 split 机制配合）：
- 遵守 v0.4 split 纪律：smoke/regression 每轮可跑，**holdout（10 条）每 3 个 agent 版本测一次且绝不用于 prompt 调优**，full 只在里程碑跑
- 每轮追加 3–5 条**当周早报新鲜条目**做活体测试（agent 从未见过）
- dashboard 监控 训练侧（smoke/regression）与 holdout 的分差，**>1.0 触发红色过拟合警报**
- 数据 schema 维度无关（dimensions 为 key→分数映射），rubric 改版不破坏 dashboard

---

## 2026-07-11 · D8：公开化两轨决策

1. **KB-Agent 开源到 GitHub：确定执行**。时机 = agent 完全建成后；届时按开源标准整理（README / LICENSE / 目录规范 / 敏感信息清理，gold 答案包等防泄露资产单独评估是否公开），发布到用户的 GitHub（账号邮箱 <redacted-email>）。执行时需用户完成 `gh` 登录授权，发布动作届时需用户最终确认（对外发布惯例）。
2. **内容公开 = 未来独立的新 agent（本项目不做执行）**。阵地：微信公众号（文字原发）+ 小红书（公众号内容截图分发，两端内容一致）；内容定位：**观点/认知类**（非资讯速递——资讯更新不符合两平台吸粉调性），目标是个人 IP 与 AI 知识社区。将以本项目全部交互为 context 另行立项"AI 认知 IP agent"。
   - 本 agent 预留的接口：知识库内容分区时给"认知/观点类"条目打 `#insight` 标签，供未来 IP agent 筛选导出。
   - 状态：**待定**（等新 agent 立项）。

---

## 2026-07-11 · D7：挑战数据集从题目清单升级为 harness 数据库 v0.4

用户要求按照 v0.4 prompt 慢慢做，但尽可能解决所有问题。核心升级不是继续堆题，而是把挑战数据集改造成可运行、可判分、可复现、可拆分、可防答案泄露的 AI harness 数据库。

本次决策：
- v0.4 固定为 100 条，覆盖真实信源噪音、官方文档演化、benchmark、知识库结构、动态管线、风险、AI PM 求职、理论演化、visualizer、自动化飞轮和抗幻觉。
- 数据拆成四份：人类主读版、actor-pack、gold、JSONL。被测 agent 只看 actor-pack，Judge 才看 gold。
- 每条挑战必须包含 source_type、eval_type、capability_tags、difficulty_vector、split、realness、snapshot_policy、Actor Input、Task、Hidden Trap、Gold Behavior、Acceptance Criteria。
- split 固定为 smoke 15 条、regression 15 条、holdout 10 条、full-only 60 条；全量集为 100 条。
- v0.3 保留为历史版本；v0.4 作为当前行为评测主集。

这条决策把 eval-first 从“有题可测”推进到“有 harness 可迭代”。

---

## 2026-07-11 · D6：挑战数据集改为真实来源版 v0.3

用户进一步要求：挑战数据集尽可能来自真实 AI 知识库、官方文档、开源 issue、榜单、论文、行业媒体和社区资料，而不是抽象编造场景；同时覆盖更广范围与更高难度。

本次决策：
- `02-challenge-dataset-v0.2.md` 保留为历史版本，不再作为主评测集。
- 新增 `02-challenge-dataset-v0.3.md`，扩充为 80 条真实来源锚定挑战，作为当前行为评测主集。
- 每条挑战都必须显式写出来源锚点、测试能力、输入样本、期望动作、判分重点，避免"看起来合理但无法追溯"。
- 来源类型必须覆盖：官方文档演化、GitHub issue/PR、公开榜单、研究论文、个人/团队知识库、行业 newsletter、中文 AI 社区与公开报告。

这条决策服务于 agent 的两项底层能力：一是识别真实世界信息噪声、版本漂移和低价值内容；二是把知识库评测从"模型编故事"升级为"贴近真实维护现场"。

---

## 2026-07-11 · D5：黄金数据集选定 + 五条重点实践成为 agent 硬性构建需求

用户从 17 个候选中选定 11 个标杆：G-01/02/03/05/06/08/10/11/12/14/17。

用户点名重点吸收、并要求纳入 agent 构建需求的五条实践：
1. **文字与可运行资源分离互链**（G-02）→ 知识文档与配套资产（prompt、脚本、评测集）分仓存放、双向链接
2. **三粒度收录政策**（G-03）→ Curator 对每条信息必须显式做粒度决策：深度长文 / 引文摘录 / 链接短评，且判定标准成文进 SOP
3. **公开可浏览 + 方法论自举**（G-05）→ 知识库按"可公开/私有存档"分区建设，公开化方案待用户定（开源 agent / 数字花园 / 社媒半自动分发）
4. **图表表达 + 数据口径标注**（G-08）→ 呈现规范：关键数字必须带口径与日期，重要对比优先图表
5. **hybrid 管线：自动策展 + 人工把关**（G-14）→ 明确分级：哪类改动 agent 自动执行、哪类需用户确认后执行

后台 agent 对 11 个标杆做深度研读，产出物在 `research/golden-kb-study/`（含 rubric D6 对标 checklist 草案）。

**待定**：知识库公开化的具体方案（用户 review 建议后决定）；用户将提供修订版评测标准。

---

## 2026-07-11 · D4：运行时 = Claude Code 本身（取代 D2 的 API Key 方案）

用户指示：「你调用 cc api 就可以」——agent 直接以 Claude Code 为运行时，不再需要单独的 Anthropic API key。

- **执行形态**：交互会话（与用户协作时）+ scheduled tasks（App 打开时自动运行）+ `claude -p` headless（配 launchd 可完全无人值守）。计费走用户已登录的 Claude 订阅。
- **模型选择**：通过 `claude --model` / 任务配置实现——sonnet-5（日常 Curator）、opus-4-8（周度 Doctor + Judge）。
- **运行约束（需让用户知情）**：scheduled tasks 在 Claude 桌面 App 打开时执行，错过的任务在下次启动时补跑。
- D2 的钥匙串方案**归档为备选**：若日后迁移到 Agent SDK 独立部署再启用。

---

## 2026-07-11 · D3：评测先行（Eval-first）

用户决定：在 Phase 0 基建之前先建立评测体系，用于对 agent 本身做多版本迭代。

评测三件套：
1. **黄金数据集**：市面顶尖 AI 知识库范例（用户从候选中筛选）→ 定义"10 分长什么样"
2. **挑战数据集**：五花八门、连最先进 LLM 都觉得难的知识库输入数据 → 驱动行为评测
3. **Baseline**：当前「AI知识库 V3」→ 状态评测基线（v0.1 = 4.7/10）

评测两种模式（详见 `evals/03-rubric-v0.1.md`）：
- **状态评测**：给知识库快照打分（六维度）
- **行为评测**：给 agent 单次处理挑战条目的表现打分（四维度）

---

## 2026-07-11 · D2：API Key 安全方案 = macOS 钥匙串

用户不愿把 API key 直接给 agent（正确的安全直觉）。方案：

- **不装第三方密码管理器**，用 macOS 自带钥匙串（Keychain）：本地加密、免费、有 CLI（`security`）。
  新版"密码"App 不适用——没有 CLI，agent 运行时读不到。
- **存入方式（用户自己操作，key 不经过对话）**：
  - GUI：钥匙串访问 → 菜单栏 文件 → 新建密码项目 → 名称 `anthropic-api-key`、账户名任意、密码栏粘贴 key
  - 或终端（输入时隐藏）：`security add-generic-password -a "$USER" -s anthropic-api-key -w`
- **agent 读取方式**：运行脚本在启动时执行
  `export ANTHROPIC_API_KEY="$(security find-generic-password -s anthropic-api-key -w)"`
  首次读取 macOS 会弹窗，点"始终允许"一次后即可无人值守运行。
- **硬性规则**：agent（含 Claude Code 会话）永远不得把 key 打印到对话、日志、文件或 git。
  禁止在交互会话中运行 `security find-generic-password -w` 并输出结果。

---

## 2026-07-11 · D1：模型配置

- 日常管线（Curator 每日收集更新）：**claude-sonnet-5**
- 周度深度诊断（Doctor 全库体检）：**claude-opus-4-8**
- 评测 Judge：**claude-opus-4-8**，与 actor 分离运行（详见 rubric Judge 协议）

（用户对初版方案的修订：周度诊断由 fable-5 改为 opus-4.8。）

---

## 2026-07-11 · L1：从原始生成流程中提取的教训（用户提供了当时的完整 prompt 记录）

原流程 = 网页对话贴文章 → Claude 整理成 Artifacts → 用户手动下载落盘。六条教训，全部转化为本 agent 的设计约束：

1. **生产环境错位**：对话环境无文件系统权限 → 人工下载 → 文件名漂移（`doc-01-pm-interview.md` vs 索引里的 `01-PM-面试与选人`）、Artifacts 与本地文件形成"两套真相"。
   → 约束：agent 必须直接读写本地文件，git 为唯一真相源。
2. **"原文完整保留"政策不加区分**：版权风险（公众号全文搬运）+ 文档膨胀（doc-01 达 60KB）+ 溯源缺失（整篇转载却无作者无链接）。
   → 约束：分级收录政策——官方/外部内容一律"重述精华 + 链接"；用户私有收藏（录音纪要等）可全文存档但入独立档案目录。
3. **无入库前验证关卡**：含明显技术错误的文章（Fine-Tuning Claude 一文把闭源模型当开源本地训练）先入库、数批之后才被发现补注。
   → 约束：Curator 入库前必须过核实 checklist（信源级别、关键事实交叉验证、utility 判断）。
4. **变更记录靠人工叙述**：框架总览的"第 N 批"日志出现"第 3 批"重复记录。
   → 约束：changelog 由 git commit 自动生成，人只写摘要。
5. **用户是唯一信息泵**：用户不贴文章，知识库就停止生长；且用户贴什么就收什么，缺乏主动的信息面覆盖。
   → 约束：Curator 必须有主动信息管线（官方源 + 复用 AI-HOT早报）。
6. **状态存在对话里**：靠超长对话维持上下文，模型自己都发出"对话已非常长，赶紧下载备份"的警告。
   → 约束：一切状态（SOP、进度、评测结果）持久化在文件系统，任何新会话可从文件恢复全部上下文。
