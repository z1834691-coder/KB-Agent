# 工具协议 v0.1

## 核心判断

“用 Claude API / Claude Code”不等于天然拥有安全、完整、自动化的工具能力。

Claude API 支持 tool use：模型可以根据开发者提供的工具 schema 请求工具调用；Claude Code 则提供文件、shell、搜索、编辑等本地工具能力。但工具能做什么、能否联网、能否写文件、能否删除、是否需要用户批准，取决于我们定义的 harness。

因此 KB-Agent 必须补充工具协议。

## 工具分层

| 层级 | 工具类型 | 用途 | 默认权限 |
|---|---|---|---|
| T0 只读观察 | `rg`、`sed`、`git log`、`git diff`、目录列表 | 建立上下文、找证据 | 自动允许 |
| T1 受控写入 | `apply_patch`、生成报告、写 run 数据 | 修改 KB-Agent 或知识库 | 需先说明编辑目标 |
| T2 验证工具 | link check、JSONL schema check、rubric lint、dashboard build | 验证结果 | 自动允许 |
| T3 外部信息 | web search/fetch、官方 docs、论文、GitHub issue | 更新和核验 | 必须记录 URL 与 accessed_at |
| T4 高风险工具 | 删除、批量重命名、公开发布、上传 GitHub、读取密钥 | 不可逆或外部可见动作 | 必须人审 |

## 默认工具栈

### 本地检索

- 优先 `rg` / `rg --files`。
- 读取文件优先 `sed -n` 指定范围。
- 禁止为了“找相关信息”一次性 `cat` 全库。

### 文件修改

- 手动编辑用 `apply_patch`。
- 大批量机械生成可用受控脚本，但脚本必须保存在 `work/`，并在 run report 记录写入目标。
- 修改前必须读目标文件相关片段。

### Git

- 每个逻辑改动一个 commit。
- commit 前必须 `git status --short` 和必要验证。
- 禁止 reset/checkout/revert 用户未授权改动。
- 删除/重命名大量文件必须人审。

### Web / Source Fetch

- 时效或不确定事实必须查一手源。
- 来源优先级：官方文档 / 论文 / release note / repo maintainer / 高质量二手 / 社区讨论。
- 每个外部事实写入时记录 `source_url`、`accessed_at`、`source_type`。
- GitHub issue 只能作为发现或待核实来源，除非 maintainer 确认或有可复现证据。

### Eval / Visualizer

- 行为评测必须只给 actor-pack。
- Judge 才能读 gold。
- 每轮写 `manifest.json`、`results.jsonl`。
- dashboard build 失败不得忽略。

## 工具调用前检查

```yaml
tool_intent: ""
risk_level: low | medium | high
target_files: []
read_before_write_done: true
rollback_plan: ""
human_review_required: true | false
evidence_to_record: []
```

## 工具调用后检查

每次工具调用后，agent 必须判断：

- 输出是否支持原计划？
- 是否出现权限、网络、格式、解析失败？
- 是否需要降级为人工核查？
- 是否产生新的 failure pattern？

## 禁止工具行为

- 禁止输出 API key 或从 Keychain 打印 secret。
- 禁止无授权删除知识库内容。
- 禁止绕过平台规则发布内容。
- 禁止把 web 搜索结果当成事实源直接入库。
- 禁止批量改文件但不留下 diff/commit。
- 禁止让被测 actor 看到 gold 答案。

## 需要后续补的工具

| 工具 | 是否必须 | 说明 |
|---|---|---|
| link checker | 必须 | 检查外链有效性和 stale 链接 |
| frontmatter linter | 必须 | 检查 knowledge_type/source/accessed_at/stale_after |
| source funnel logger | 必须 | 记录 crawled/candidate/accepted/rejected/pending |
| eval runner | 必须 | 自动跑 smoke/regression 与 calibration |
| dashboard builder | 已有 v0 | 后续扩展 source funnel、calibration confidence |
| secret scanner | 必须，开源前 | 检查 repo 和历史中是否含 key/隐私 |
| scheduler | 后续 | launchd / Claude scheduled tasks，先手动 run 再自动化 |

## 用户需要做什么

1. API key 继续放在 macOS Keychain 或 Claude Code 登录态，不在聊天/文件里给 agent。
2. 授权高风险动作：删除、公开 GitHub、发布内容、读取密钥、批量改名。
3. 在工具协议升级时确认哪些工具可以自动运行，哪些必须每次询问。
