# KB-Agent · 自主多轮迭代循环 Prompt（AUTONOMOUS LOOP）

> **这是什么**：一段**自包含、可复用**的执行剧本。任何新的 Claude Code 会话、或定时任务（见 §定时），只要读到本文件就能在**不依赖任何历史对话记忆**的前提下，安全地推进 KB-Agent 一整轮。
> **给定时任务的调用语**（复制进 scheduled task 的 prompt 即可）：
> *"读取并严格执行 `~/Documents/KB-Agent/work/AUTONOMOUS-LOOP-PROMPT.md`。你处于**无人值守模式（UNATTENDED）**：遵守其中所有安全边界，只体检/诊断/准备候选/上报，绝不自动修改知识正文、绝不自动 commit 正文。完成后把结果追加到 `进展.md §7`。"*

---

## 0. 两种运行模式（先判断自己属于哪种）
- **ATTENDED（用户在场，如用户手动开会话让你迭代）**：可以改知识正文、可本地原子 commit（遵循项目 commit-as-changelog 惯例），但**不 push、不开源**（那是 N8，需用户单独确认）。
- **UNATTENDED（定时任务触发，无人值守）**：**只读诊断 + 准备候选 + 上报**。禁止改 `AI知识库 V3` 的知识正文、禁止 commit 正文、禁止任何不可逆/对外动作。可以写 `_meta/reports/`、`_meta/flywheel/`、`KB-Agent/进展.md` 这类**元数据/报告**（可逆、非正文）。

> 判据：如果本轮由 scheduled task 或无用户交互触发 → UNATTENDED。默认从严：**拿不准就当 UNATTENDED**。

---

## 1. 开工必读（恢复上下文，按顺序）
1. `~/Documents/KB-Agent/进展.md` — 进度真相源（已完成/未决/迭代日志）。
2. `~/Documents/KB-Agent/work/ITERATION-TREE.md` — 选下一步。
3. `~/Documents/KB-Agent/evals/robustness-judge.md` — 收口验收标准 + 一票否决项。
4. `~/Documents/KB-Agent/protocols/0{1,2,3}-*.md` + `evals/failure-patterns.md` — 运行/工具/人审协议。
5. 记忆中的项目卡片（若可用）：`project-kb-agent`。

---

## 2. 一轮的标准流程（Loop）
**Step A · 诊断**
- 跑客观层：`python3 ~/Documents/KB-Agent/evals/robustness_audit.py`
- 跑库体检：`python3 "~/Documents/AI知识库 V3/_meta/pipeline/kb_ops.py" doctor --force`（只体检，不改正文）
- 读两者输出 + 进展.md §3 未决清单。

**Step B · 选节点**
- 从 ITERATION-TREE 里选"无 blocker、非 HITL、非 UNATTENDED 禁区"中 `价值/成本` 最高的节点。
- UNATTENDED 下若最高价值节点需改正文（如 N2）→ **不执行，改为"准备候选包 + 在进展.md 上报建议用户在场时做"**。

**Step C · 执行（一次只改一类变量）**
- 归因到单一主因（prompt/SOP/工具/数据/rubric 五选一），只动这一类。
- 若涉及内容：**先真实来源检索再落笔，禁止注水/占位/编造**（注水=self-deception，judger 一票否决）。
- ATTENDED 且改了正文：做**原子 commit**（一改动一 commit，message 写清 what+why），不 push。

**Step D · 判官（judger）**
- 按 `robustness-judge.md`：`[MECH]` 维度用 audit 脚本；`[JUDGE]` 维度（R2/R5/R6）**逐条写文字证据**打分，禁止机械代打。
- 检查 5 条一票否决项。任一触发 → 本轮**不许标 DONE**，把"修复该否决项"设为下一步。

**Step E · 记录 + 沉淀**
- 综合分与结论写 `evals/runs/robustness-run-<日期>.json`。
- 追加到 `进展.md §7 迭代日志`（归因/改动/judger分/下一轮方向）+ 更新 §3 未决表 + ITERATION-TREE 节点状态。
- 追加飞轮：`AI知识库 V3/_meta/flywheel/score-timeseries.jsonl`（kind=`robustness`）、`run-events.jsonl`。
- 若产出可复用资产（SOP/框架）→ 标注 topic 无关，记入 SOP 目录。

**Step F · 决定下一轮**
- 在 ITERATION-TREE 用同一选路规则确定下一节点，写进 §7 "下一轮方向"。
- 若全部非 HITL 节点已 DONE → 在进展.md 上报"待用户决策：是否进入 N8 开源 / 新 topic 库 / 叫停"，然后停。

---

## 3. 安全边界（硬红线，任何模式都不许破）
- 无人值守**绝不**改知识正文、**绝不**自动 commit 正文、**绝不** push/开源。
- API key 永不进对话/日志/文件/git。
- 对外/不可逆动作（开源、删除、改权限、发消息）= HITL，必须用户在场确认。
- 一切写操作优先可逆（git 可回滚）；拿不准就只上报不动手。

## 4. 数据飞轮（每轮都要喂）
持续收集这些高质量信号（都进 `AI知识库 V3/_meta/flywheel/`）：
- 分数序列（真实盲评/机械分分开记）、失败模式归因、候选取舍决策、用户反馈、手动 diff 偏好信号、SOP 补丁。
- **目的**：让 harness 产品越跑越准——这是设计这款产品的大前提。

## 5. 定时（时钟）
- 已配置：每周一次的"鲁棒性 + 进度推进"定时任务（scheduled-tasks），UNATTENDED 模式跑本剧本。
- 项目自带 launchd：curator 每日 09:10 / doctor 每周一 20:30（只体检）。
- 定时任务每次结束都必须在 `进展.md §7` 留一条带日期的记录，保证可观测。

---
*本剧本本身也是资产：换任意新 topic 知识库（如具身智能库）时，把路径变量替换即可复用。*
