# examples/ · 让这个仓库 clone-and-run

被维护的真实知识库是私有的（且完整 gold 答案集刻意不公开）。为了让**任何人 clone 下来就能真跑一遍**，这里放了一个**最小可跑的示例 vault** 和一个**示例挑战集**。

> ⚠️ 这些是**占位 demo**：内容是假的、分数偏低是**预期**的。它的目的是证明"管线能在全新 clone 上跑通并产出报告/仪表盘"，不是"内容有多好"。

## 目录

- `sample-vault/` —— 一个最小知识库骨架（几篇带 frontmatter 的文档 + 两份示例实体档案 + `_meta/` 脚手架 + 已内置的示例飞轮数据），并自带一份 sanitized 的 `kb_ops.py`。
- `sample-challenge.jsonl` —— 4 条**合成**挑战题（含 `gold`/`expected_action`，会在 blind actor 包里被自动剥除），用于演示盲评隔离。

## 一键试跑（在仓库根目录执行）

```bash
# 1) 元层客观机械审计（自动回退到 examples/sample-vault）
python3 evals/robustness_audit.py

# 2) 飞轮 digest → 下一轮聚焦建议（读示例飞轮数据，能看到真实趋势/慢性弱项）
python3 evals/flywheel_digest.py

# 3) 库体检（Doctor）：对示例 vault 打分并产出周报 + 仪表盘
python3 examples/sample-vault/_meta/pipeline/kb_ops.py doctor --force
#   → 生成 examples/sample-vault/_meta/reports/<date>-doctor-weekly.md
#   → 生成 examples/sample-vault/_meta/dashboard/index.html

# 4) 日常轻检 + 自主决策 + 重建仪表盘
python3 examples/sample-vault/_meta/pipeline/kb_ops.py run

# 5) 准备一次盲评 run（用示例挑战集；注意 gold 字段会被剥掉）
python3 evals/run_blind_eval.py prepare --actor agent-v5 --split smoke,regression --dataset examples/sample-challenge.jsonl
python3 evals/run_blind_eval.py status --run-dir evals/runs/<上一步打印的 run_id>
```

## 指向你自己的库

三个"库侧"脚本（`robustness_audit.py` / `flywheel_digest.py` / `kb_ops.py`）用这个顺序定位 vault：

1. 环境变量 `KB_VAULT`（最高优先）——`KB_VAULT=/path/to/your-vault python3 evals/flywheel_digest.py`
2. 同级目录的私有 vault（原作者的真实布局）
3. 本仓库内置的 `examples/sample-vault`（保证 clone 即可跑）

> 完整的 actor→judge 盲评（`validate`/`finalize`）需要在隔离会话里真正跑 actor 与 judge 两个模型步骤，属于"接了模型运行时之后"的步骤，示例只演示到 `prepare`/`status`。整套接入见根 README 的「迁移 10 步」。
