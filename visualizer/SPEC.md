# Visualizer 规格（D8）

**形态**：`python3 visualizer/build.py` → 生成 `evals/dashboard.html`（静态单文件，零依赖，离线可看）。每轮评测后重跑一次即刷新。

## 数据 schema（维度无关——rubric 改版不破坏 dashboard）

```
evals/runs/<run-id>/manifest.json      # 每轮一个目录
{
  "run_id": "run003-behavior-dev",
  "type": "state" | "behavior" | "calibration",
  "timestamp": "2026-07-18T21:00:00+08:00",
  "versions": {"agent_prompt": "v2", "dataset": "v0.3-dev", "rubric": "v2.0"},
  "aggregate": {"composite": 6.8, "dimensions": {"B1 判断正确性": 7.1, "...": 0}},
  "meta": {
    "split": "smoke" | "regression" | "holdout" | "full" | "calibration" | null,
    "notes": "…",
    "funnel": {"decision": {"accept_main": 0}, "target_zone": {}, "risk_tier": {}, "user_gate": {}},
    "cost": {"tokens": 0, "minutes": 0, "user_review_min": 0}
  }
}

evals/runs/<run-id>/results.jsonl      # 行为评测逐 case 一行
{"case_id":"CH-07","category":"时效陷阱","input_ref":"02-challenge-dataset-v0.3.md#CH-07",
 "input_excerpt":"…","output":"agent 的处理结论…","scores":{"B1":8,"B2":7,"B3":9,"B4":8},
 "weighted":7.9,"verdict":"pass","judge_evidence":"…",
 "decision":"accept_main","target_zone":"AI_PM_core","granularity":"structured_card",
 "freshness_policy":"periodic_review","risk_tier":"medium","user_gate":"notify",
 "failure_mode":["F-011"]}

evals/prompts/agent-vN.md              # 每个 agent prompt 版本快照（diff 数据源）
```

## 八个视图 ↔ 用户三需求

| 视图 | 满足 |
|---|---|
| ① 版本趋势折线（状态/行为分色、holdout 方块） | 需求3：整体指标逐版本真提升 |
| ② Judge 校准（用户分 vs agent 分） | 人工校准闭环 |
| ③ 维度对比条形（当前 vs 上一版，带 Δ） | 需求3 |
| ④ 分流漏斗（decision / target_zone / risk_tier / user_gate） | 可观测：agent 是否真的在减少噪音、分流主库/运维/source log |
| ⑤ 过拟合监控（dev vs holdout 分差，>1.0 红色警报） | 需求3 的"防过拟合" |
| ⑥ Case 浏览器（输入/输出/评分/Judge 证据 + 同 case 跨版本历史，可搜索/按类别筛） | 需求1：case-by-case |
| ⑦ Prompt diff（相邻版本 unified diff） | 需求2：prompt 变化 |
| ⑧ 全轮次表（版本三元组 + 成本备注） | 可追溯 |

## 使用约定

- 每轮评测的执行者（Judge 会话）负责写 `runs/<run-id>/` 数据并重跑 build.py，然后 git 提交（数据与 dashboard 一起版本化）
- run-id 命名：`runNNN-<type>[-smoke|-regression|-holdout|-full]`，NNN 递增
- split 纪律遵循挑战集 v0.4（smoke/regression 每轮，holdout 每 3 个 agent 版本且不用于调优，full 里程碑跑；见 DECISIONS D7/D9）
- ⑤ 过拟合监控取"最新训练侧（smoke/regression）综合分 − 最新 holdout 综合分"，>1.0 红色警报
- v2 起，行为评测 results 必须写结构化 funnel 字段；旧 run 缺字段时，dashboard 可回退显示文本，不作为协议合格样本。
