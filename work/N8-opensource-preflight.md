# N8 · 开源就绪预检报告（Pre-flight）

> **模式**：只读预检 + 报告。**未建仓、未 push、未做任何对外/不可逆动作。**
> **日期**：2026-07-16 · 对象：`~/Documents/KB-Agent/` git 库（78 tracked 文件）
> **结论**：**无硬性阻断（no hard blocker）**——未发现真实密钥泄漏；剩下的是需你拍板的隐私/资产取舍 + 几项开源标准化。

---

## 1. 敏感信息扫描结果

| 检查项 | 结果 | 处置 |
|---|---|---|
| 真实 API key / token（sk-/Bearer/私钥） | ✅ **未发现** tracked 文件含真实密钥 | 无需处理 |
| `~/.claude/settings.json` 里的 auth token 是否泄漏进 repo | ✅ **未泄漏**（token 不在 KB-Agent 库内）| 无需处理 |
| `DECISIONS.md` 的 "password" 命中 | ✅ 是 keychain **设置说明**（`security add-generic-password -s anthropic-api-key`，是项目名不是密钥）| 保留即可，或改成占位 |
| 个人邮箱 | ⚠️ `DECISIONS.md:176` 含 `<redacted-email>`（你的 GitHub 账号邮箱）| **你决定**：保留 or 脱敏 |
| 个人绝对路径 `~` | ⚠️ 出现在 **9 个文件**（暴露用户名，非密钥）| 建议开源前批量替换为 `~` 或 `<vault>`（cosmetic）|

---

## 2. 需你拍板的资产取舍

| 资产 | 状态 | 风险/建议 |
|---|---|---|
| **gold 答案包** `evals/02-challenge-dataset-v0.4-gold.md` | DECISIONS.md 曾自我标记"单独评估是否公开" | ⚠️ 公开 gold 会让挑战集失去闭卷意义（任何模型可背题）。建议：**挑战集公开、gold 包不公开**（放独立 private 或加 .gitignore）|
| `PROJECT-STORY.md`（简历叙事） | 未 track | 含你的求职目标/个人经历。作为作品集**可以公开**，但确认无涉密（韶音实习细节等）|
| 2 张截图 PNG（`Screenshot…png`、`kb agent示例图.png`） | 未 track | 可能含 KB 内容/个人信息，公开前肉眼过一遍 |
| `tools/feishu-codex-bridge-bundle-…`（vendored larksuite CLI） | 未 track | **不要**入库：体积大 + 第三方许可 + 可能含配置。加 .gitignore |
| `evals/analysis/`、`baselines/`、`prompts/agent-v*.md` | 未 track | 都是评测资产，公开无妨（属作品集亮点），确认无个人路径即可 |

---

## 3. 开源标准化 checklist（发布前，全部可逆）

- [ ] 加 **LICENSE**（作品集类建议 MIT）
- [ ] README 顶部加项目简介 + 架构图（PROJECT-STORY 的 mermaid 可复用）
- [ ] **硬化 .gitignore**：追加 `tools/`、`*.png`、`.DS_Store`（已有）、`__MACOSX/`，并决定 gold 包是否 ignore
- [ ] 决定 `PROJECT-STORY.md` / gold 包 / 截图是否纳入
- [ ]（可选）批量把 `~` → `~`/占位，邮箱脱敏
- [ ] 选仓库可见性（public / private）

---

## 4. 明确未做（等你确认才能做的对外动作）

- ❌ 未创建 GitHub 仓库
- ❌ 未 `git push` / 未发布任何内容
- ❌ 未执行 `gh` 授权

**下一步（需你）**：① 完成 `gh auth login`（你自己操作）；② 告诉我上面第 2、3 节的取舍（尤其 gold 包是否公开、可见性 public/private）；③ 你最终确认后，我才做建仓 + 首次 push，且 push 前会再跑一次全量密钥扫描。

---

*预检状态：✅ 无硬性阻断，无真实密钥泄漏。剩余全是隐私/资产取舍与标准化，均可逆，主动权在你。*
