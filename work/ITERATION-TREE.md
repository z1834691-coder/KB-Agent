# KB-Agent · 进程推进树（Iteration Tree）

> **用途**：把剩余工作拆成**优先级 + 依赖排序**的节点树，让每一轮迭代都能"最短路径挑到最高价值的下一步"。
> **配套**：进度真相 = [../进展.md](../进展.md)；执行循环 = [AUTONOMOUS-LOOP-PROMPT.md](AUTONOMOUS-LOOP-PROMPT.md)；验收 = [../evals/robustness-judge.md](../evals/robustness-judge.md)。
> **节点状态**：`TODO` 待办 · `DOING` 进行中 · `DONE` 已闭 · `BLOCKED` 阻塞（列出 blocker）· `HITL` 需用户确认才能动。
> **选路规则**：每轮从"无 blocker 且非 HITL"的节点里，选 `价值/成本` 最高者。价值 = 求职弹药 + 系统鲁棒性 + 可复用资产 三者加权。

```
KB-Agent 总目标：自主维护 AI 知识库 + 产出 AI PM 求职弹药
│
├─ A. 系统鲁棒性 / 诚实性（agent 本体质量）
│   ├─ N1  Doctor 评分诚实化 ................................. DONE  (Round 1)
│   ├─ N3  鲁棒性 judger（rubric + audit 脚本）............... DONE  (本次)
│   ├─ N4  快变事实 stale-checker + source manifest .......... DONE  (Round 5)
│   └─ N9  定时任务安全审计（确认无人值守不改正文）.......... DONE  (本次·loop-prompt 内建边界)
│
├─ B. 内容深度 / 求职弹药（KB 质量）
│   ├─ N2  后 3 家档案补齐到样板深度 ........................ DONE  (Round 2-4)
│   │      MiniMax 247→300 / Moonshot 252→292 / Zhipu 251→289；均清 under-depth
│   │      并纠正三家"已上市/高估值"静默过期错误；全程真实检索、judger 判无注水
│   ├─ N5  旧文档 frontmatter 批量对齐 ...................... DONE  (Round 8·验证达标)
│   └─ N6  主动信息管线（curator 复用 AI-HOT早报）........... DONE  (Round 7)
│
├─ C. 泛化 / 可复用（资产杠杆）
│   └─ N7  具身智能库复用验证 ............................... DONE  (Round 6·只读验证)
│          把 SOP + 评测框架迁移到 Desktop/韶音实习/具身智能PM知识库/
│
└─ D. 发布（对外，HITL 高风险，压轴）
    └─ N8  开源 KB-Agent 到 GitHub ......................... HITL  需用户确认
           前置：敏感信息扫描 + gh 授权 + 清理未提交 harness 改动
```

---

## 节点卡片（可执行规格）

### N2 · 后 3 家档案补齐到样板深度　【下一轮首选】
- **为什么高价值**：MiniMax/Moonshot/Zhipu 都是用户目标公司；深度不足=面试弹药缺口；同时兑现"覆盖≠质量、完成的定义要绑质量"这条项目核心教训。
- **验收标准（judger 会查）**：
  1. 三家行数各 ≥ 480×0.85 ≈ **408 行**（对齐样板 Alibaba/Bytedance/DeepSeek/StepFun）；
  2. 八大板块齐全（速览/技术路线/产品矩阵/商业化/组织与人/战略叙事/风险争议/AI PM 面试角度）**且每板块有实质内容非占位**；
  3. **每条关键事实带信源**（tier + accessed_at），无信源的估计数标 `待核`；
  4. 面试块含"高频题 + 一句话答 + 追问"结构。
- **红线**：禁止为凑行数注水/复读。宁可少写，不可假写。每家先做真实来源检索（官方 + 权威二手）再落笔。
- **依赖**：无。**成本**：中（3 家 × 检索+撰写）。**建议**：可拆成 3 个子轮，每家一轮，边做边 commit。

### N4 · 快变事实 stale-checker + source manifest
- **验收**：`_meta/sources/official-sources.json` 补全各公司官方源；kb_ops 增 stale 检查报告（价格/模型版本/融资/MAU 字段级 `stale_after`）；Doctor 报告列出临期字段。
- **依赖**：无。**成本**：中。

### N5 · 旧文档 frontmatter 批量对齐
- **验收**：`frontmatter_issues` 归零；19 篇主文档字段与 REQUIRED_FRONTMATTER 一致。**成本**：低。

### N6 · 主动信息管线
- **验收**：curator 能从 `~/Documents/AI-HOT早报` 读增量并生成候选包（不自动入库，走 candidate_review）。**成本**：中。

### N7 · 具身智能库复用验证
- **验收**：在 `Desktop/韶音实习/具身智能PM知识库/` 跑通同一套 SOP/评测框架，产出一份迁移报告，证明 topic 无关。**这是简历"可复用"卖点的实证。**
- **依赖**：建议在 N2 之后（先把主库打磨成可复制的样板）。**成本**：中。

### N8 · 开源（HITL）
- **必须先问用户**。前置：敏感信息扫描（钥匙串引用/个人路径/简历隐私）、`gh` 授权、清理 repo。**不得在无人值守/未确认下执行。**

---

## 依赖图（拓扑）
```
N1 ─┐
N3 ─┼─► (系统诚实底座就绪) ─► N2 ─► N7 ─► N8(HITL)
N9 ─┘                         │
N4 ────────────────────────────┤ (可与 N2 并行)
N5 ───────────────────────────►┘ (随手清扫)
N6 ──► (依赖 N4 的 source manifest)
```

## 进度结论（2026-07-16 更新）
- 系统诚实底座（N1/N3/N9）已就绪；**N2 已全闭**（Round 2-4，MiniMax/Moonshot/Zhipu 均清 under-depth 并纠错）。
- **下一轮 = N4 快变事实 stale-checker**：本轮暴露所有档案的"融资/股价/估值"都是高频静默过期字段（三家 IPO 都曾被错标"待核"），正需 source manifest + 字段级 stale checker 系统化。
- 其后：N7 具身库复用验证（泛化实证）→ N8 开源（HITL，需用户确认）。
