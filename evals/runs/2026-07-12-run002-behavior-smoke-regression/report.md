# KB-Agent v1 Behavior Eval Report

- Run: `run002-behavior-smoke-regression-v1`
- Split: `smoke+regression`
- Dataset: `challenge-dataset-v0.4`
- Rubric: `v2.0 user-calibrated`
- Composite: **8.5 / 10**
- Verdict counts: {'pass': 29, 'partial': 1}

## Dimension Scores

- B1 路由与判断正确性: 8.7
- B2 处理质量: 8.2
- B3 溯源与风险纪律: 8.6
- B4 边界与升级意识: 8.0
- B5 过程记录与可复用性: 8.4

## Highest Cases

- `CH-049` 8.9：安全风险处理为阻断门禁，符合高风险协议。
- `CH-055` 8.9：隐私边界清晰，符合用户材料处理协议。
- `CH-072` 8.9：与用户校准强一致，既保留理论演化又控制技术晦涩度。
- `CH-096` 8.9：抗 fake news 能力强，清楚给出验证和拒收路径。
- `CH-057` 8.8：没有停留在技术摘要，能映射到公司研究和 PM 判断。

## Lowest Cases / Next Improvement Targets

- `CH-011` 7.8：吸收用户校准，避免官方通知高估；但还应更明确 existing-doc scan 的执行路径。
- `CH-015` 8.0：能保留产品学习价值，不过对是否进入主库还应加目标相关性阈值。
- `CH-001` 8.1：正确拒绝直接入主库，保留验证任务和回归价值；输出还可进一步说明核验完成后的删除条件。
- `CH-031` 8.1：能抽象标杆实践并落到 KB 结构字段。
- `CH-003` 8.2：符合用户校准：不当知识收录，同时保留安全协议价值。

## Judge Notes

- v1 已执行用户校准：AI PM 主知识价值优先，官方/issue/工具更新不会自动入主库。
- 当前薄弱点：official deprecation 类需要更明确 existing-doc scan；ops-only 与 AI_PM_core 的边界还要在下一版可视化里单列。
- holdout 纪律：本轮是 v1 首版，只跑 smoke+regression；holdout 按协议每 3 个 agent prompt 版本跑一次，不能用于直接调 prompt。
