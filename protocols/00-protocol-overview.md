# KB-Agent 协议总纲 v0.1

更新时间：2026-07-12

## 结论：三项都必须补

用户提出的三项补充——上下文协议、工具协议、人把关协议——不是额外文档，而是 KB-Agent 从“会写内容的助手”升级为“可持续运行的 AI harness”的必要护栏。

| 协议 | 必要性判断 | 如果没有会发生什么 |
|---|---|---|
| 上下文协议 | 必须 | agent 读太多、读错重点、凭印象改文件、上下文漂移，最后不可复现 |
| 工具协议 | 必须 | Claude API/Claude Code 有工具能力，但不会自动安全地使用工具；必须定义工具边界、权限、证据和失败回滚 |
| 人把关协议 | 必须 | 自动化会在低置信、版权、删除、大改、Judge 失准时放大风险 |

## 协议位置

- `protocols/01-context-protocol.md`
- `protocols/02-tool-protocol.md`
- `protocols/03-human-review-protocol.md`
- `evals/failure-patterns.md`

## 协议如何进入每轮 loop

每轮 KB-Agent 运行前必须构造一个 **Run Context Packet**：

```text
固定必读 → 动态上下文 → 工具计划 → 风险/人审判断 → 执行 → 压缩摘要 → 写 run report
```

运行后必须写入：

- 本轮读取了哪些上下文
- 调用了哪些工具
- 哪些地方触发了人审或本应触发人审
- 是否有新的 failure pattern
- 是否需要更新 SOP / prompt / rubric / dataset

## 外部依据

本协议参考了以下公开实践：

1. Claude Code 官方文档：强调 context window 管理、自动 compact、`/compact` 和 `/context` 等命令。
2. Anthropic “Effective Context Engineering for AI Agents”：长任务 agent 需要把上下文拆成压缩、结构化、可恢复的单元。
3. Anthropic Tool Use 文档：Claude API 支持 tool use，但工具必须由开发者定义 schema、执行环境和结果回传。
4. Anthropic “Building Effective Agents”：高风险工作流应优先使用简单、可控、可评估的 patterns，并在需要时加入 human review。

## v0.1 的边界

- 协议先服务 KB-Agent harness，不扩展到 IP agent。
- 不新增自动发布、自动删除、自动公开仓库等对外动作。
- 不把 API key、密码、cookie、个人隐私写入任何协议或日志。
