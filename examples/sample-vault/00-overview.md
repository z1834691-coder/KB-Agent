---
title: "示例知识库 · 框架总览"
type: framework_overview
tags: [meta, overview, sample]
status: active
last_reviewed: 2026-07-21
maintainer: KB-Agent
related: ["[[01-example-topic]]", "[[ExampleCorp]]"]
---

# 示例知识库 · 框架总览

> 这是一个**最小可跑的示例 vault**，用来演示 KB-Agent 管线（Curator / Doctor / Dashboard）在一个全新 clone 上能真实运行并产出报告。它**不含真实内容**，分数偏低是预期的——它的作用是"证明脚本能跑通"，不是"内容有多好"。

## 这是什么

- 一个 topic-agnostic 的知识库骨架：几篇带规范 frontmatter 的主文档 + 两份示例实体档案（[[ExampleCorp]] / [[SampleAI]]）+ `_meta/` 脚手架。
- 跑 `kb_ops.py doctor` 会对它做结构/时效/元数据/双链体检并打机械结构分，产出 `_meta/reports/` 周报与 `_meta/dashboard/index.html`。

## 导航

- 主题占位页：[[01-example-topic]]
- 实体档案：[[ExampleCorp]]、[[SampleAI]]
- 横向对比：见 `company-dossiers/00-comparison-matrix.md`

> 想把这套用到你自己的真实主题？见仓库根 README 的「迁移到你自己的知识库（10 步）」。
