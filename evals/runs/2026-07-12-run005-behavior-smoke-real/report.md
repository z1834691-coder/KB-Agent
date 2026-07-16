# Run005 · 真实闭卷行为评测 · 独立 Judge 报告

- run_id: run005-behavior-smoke-real
- 三元组: agent-v2 × challenge-dataset-v0.4/smoke × rubric v2.0
- Judge: claude-opus-4-8（独立盲评，未参与 actor 决策；仅依 rubric v2.0 + gold + 用户校准打分）
- actor: agent-v2，claude-opus-4-8，闭卷（仅读 actor-pack，未碰 gold），运行 11 分钟
- 打分纪律: 锚点先行 + 证据强制（见 results.jsonl 各 judge_evidence）+ B1 可辩护性通道

## 1. 综合分与五维分
| 指标 | 分数 | 旧硬编码 run004 | Δ |
|---|---:|---:|---:|
| 综合 composite | 8.3 | 8.6(硬编码 OVERRIDES) | −0.3 |
| B1 路由与判断正确性(35%) | 8.6 | 8.8 | −0.2 |
| B2 处理质量(25%) | 8.1 | 8.4 | −0.3 |
| B3 溯源与风险纪律(20%) | 8.2 | 8.7 | −0.5 |
| B4 边界与升级意识(10%) | 8.0 | 8.2 | −0.2 |
| B5 过程记录与可复用性(10%) | 8.5 | 8.7 | −0.2 |

首个真实行为分。旧 8.6 是写死的 OVERRIDES 非真实评分；本轮 8.3 为逐条盲评结果。掉分集中在 B3(−0.5)/B2(−0.3)：impact_scan 普遍 pending_scan、具体溯源字段未落结构。B1 几乎无损=判断真实可靠。15 条全部 pass，无 auto-fail。weighted 区间 7.8–8.6，方差小。

## 2. 最高分/最低分 3 条
最高(并列 8.6)：CH-012(唯一 impact_scan 命中真实 doc-06,正确区分 update vs SOP)、CH-057(pm_transfer 4/4,定价转 PM 成本卡,修 F-004)、CH-072(CoT evolution_timeline 重构,一手论文源)；另 CH-073 亦 8.6。
最低：CH-011(7.8,定义 schema 但 pending_scan 未落 metadata)、CH-001(8.0,无纪要+pending_scan+溯源字段缺)、CH-021(8.0,缺 China-availability 轴+未标 contamination/Goodhart)。

## 3. 与 gold 分歧·可辩护性裁定
本轮无方向相反、无 auto-fail，分歧均为「同向但执行度不足」，全部 7+：
1. CH-011 走 SOP 而非直接落 metadata → 可辩护(用户要求更新 SOP+与 CH-012 区分),扣分落 B2/B3。
2. CH-003/049 risk_tier 梯度(medium/high+ask_before_write vs 旧 blocking/block)→ 可辩护(都未泄密、发布 behind H4);★★★★★ 场景 blocking 会更保守,故 B4 未满分。
3. CH-041 ops_only→source_log 定义管线(vs candidate)→ 目的地一致,无扣分。
4. CH-021 缺 China 轴 → 目标对齐缺口(B2),非失败。

## 4. Judge 校准偏差
对 judge-calibration-set v0.2 独立评信息价值 vs 用户确认分：
CH-001 3/3、CH-003 3/3、CH-011 3/4、CH-018 5/5、CH-020 3/3、CH-066 2/1.5、CH-068 6/6、CH-072 8/8、CH-080 3/3。
平均偏差 = 1.5/9 = 0.17(≤0.5 正常置信,本轮不标低置信)。唯一 1.0 在 CH-011(方向一致仅程度差)。校准证明对用户主库信息价值口径对齐。

## 5. 效率门槛(§7)
时长 11 分钟(≤45)✅、运行中用户确认 0(≤3)✅、把关耗时 0 ✅ → 非 cost-fail。
tokens/工具调用次数未采集(null)⚠️ = §7/D5.6 报告完整性欠账,建议 harness 补齐。
注:actor 的 3 处 ask_before_write 是建议门,非运行中真实确认。

## 6. 三条改进方向(只写失败模式,不含 gold 答案)
1.【首要】impact_scan 系统性 pending_scan——声明扫描但不执行(13/15)。使 B1 建立在未验证意图上,压住 B2/B3。归因:harness 未给可查询 KB 文件索引 → 让 impact_scan 真正可执行。
2. 具体溯源字段(URL/标题/日期/状态)未落结构。归因:schema 未把 provenance 设为非 reject 决策的强制项 → 设必填+linter。
3. standing-rule/核心 SOP 变更 user_gate 偏宽(用 notify)。归因:gate 只绑 risk_tier → 扩为「风险等级 ∨ 是否改治理性规则」。

Judge 认为最该修的一个:第 1 条 impact_scan 的 pending_scan 化——判断力已到位,但扫描没真正跑,好判断无法兑现成可信处理与溯源。

## 7. 状态↔行为联动(§8)
13/15 处理停在 pending_scan(计划而非落库)。若下轮状态评测显示库内容未变,即触发「无效运行」。建议 v3 同时观测状态分,把落库执行率作为联动指标。
