# KB-Agent Eval Schemas

这些 schema 是 harness 产品化后的机器可读合同。执行脚本使用
`evals/schema.py` 中的同源常量；这里的 JSON Schema 用于文档、未来 UI
表单、外部 runner 和 CI 校验。

## 文件

- `actor-output.schema.json`：actor 盲考输出。不得包含 judge 分数字段。
- `judge-result.schema.json`：judge 对单条 case 的评分输出。
- `run-manifest.schema.json`：每轮 run 的元数据、版本三元组和聚合分。
- `failure-pattern.schema.json`：失败模式库条目的结构。

## 版本纪律

V5 是当前生产候选 actor schema。历史 run 可只满足 base actor 字段；新的
actor prompt 默认应满足 V5 schema，并在 `manifest.versions.agent_prompt`
中写清版本。
