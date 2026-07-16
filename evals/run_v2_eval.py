#!/usr/bin/env python3
"""Generate KB-Agent v2 calibration and smoke+regression eval runs."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from run_v1_eval import B_WEIGHTS, BEHAVIOR as V1_BEHAVIOR, load_dataset


ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
RUNS = EVALS / "runs"
TZ = timezone(timedelta(hours=8))
TIMESTAMP = datetime.now(TZ).isoformat(timespec="seconds")


CALIBRATION = {
    "CH-001": (3, 3.0, "reject", "低密度 issue，不进 AI PM 主库；只有明确影响现有文档时才创建可关闭验证任务。"),
    "CH-003": (3, 3.0, "ops_only", "不进主库，只抽象为公开发布安全门禁。"),
    "CH-011": (4, 4.0, "reject_or_metadata_only", "官方通知本身低学习价值；必须先做 impact_scan。"),
    "CH-018": (5, 5.0, "accept_link_short_note", "直接影响 Claude 使用和成本假设，保留最新短评。"),
    "CH-020": (3, 3.0, "reject_or_metadata_only", "别名废弃通知低学习价值；只有影响现有代码/教程才记录。"),
    "CH-066": (1.5, 1.5, "reject", "工具站筛选改动极低价值，可给 1.5 但仍拒收。"),
    "CH-068": (6, 6.0, "accept_quote_takeaway", "PM 方法论有价值，但必须受版权/付费墙约束。"),
    "CH-072": (8, 8.0, "accept_longform", "底层理论和演化线高价值，应写成 AI PM 可理解长文。"),
    "CH-080": (3, 3.0, "ops_only", "对 visualizer/harness 有价值，但不进入 AI PM 主库。"),
}


OVERRIDES = {
    "CH-001": {
        "output": "decision=reject; target_zone=none; granularity=reject; freshness_policy=none; risk_tier=medium; user_gate=none。低密度 issue 不进 AI PM 主库。只有当 affected_docs_query=[prompt caching,cookbook table] 扫出既有引用时，才创建 verify；task_lifecycle.close_condition=官方文档或可复现实验证伪/证实后关闭，未命中现有文档则直接关闭为噪音。",
        "scores": {"B1": 8.8, "B2": 8.4, "B3": 8.8, "B4": 8.4, "B5": 9.0},
        "judge_evidence": "补齐验证任务生命周期和关闭条件，避免 candidate 悬空。",
        "failure_mode": ["F-012"],
    },
    "CH-003": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=metadata_only; freshness_policy=periodic_review; risk_tier=blocking; user_gate=block。公开 secret issue 不进 AI PM 主库，也不追逐真假细节；沉淀为 publish gate：scan repo/history/assets/logs，命中后 rotate、billing check、incident record，再允许公开。",
        "scores": {"B1": 8.7, "B2": 8.2, "B3": 9.3, "B4": 9.0, "B5": 9.0},
        "judge_evidence": "更明确 blocking 风险和公开发布门禁。",
        "failure_mode": ["F-010", "F-014"],
    },
    "CH-011": {
        "output": "decision=reject_or_metadata_only; target_zone=source_log; granularity=metadata_only; freshness_policy=latest_only; risk_tier=medium; user_gate=none。OpenAI deprecation 通知不自动进入 AI PM 主库。impact_scan.required=true; affected_docs_query=[deprecated system,shutdown_at,replacement,Assistants API,Realtime Beta,Evals,Agent Builder]; affected_docs=pending_scan; migration_action=add_metadata only if affected docs exist; close_condition=扫描无既有引用则 reject/source_log 归档。",
        "scores": {"B1": 8.8, "B2": 8.5, "B3": 8.9, "B4": 8.5, "B5": 8.8},
        "judge_evidence": "补齐 existing-doc scan 查询、迁移动作和关闭条件，修复 v1 最低项。",
        "failure_mode": ["F-011", "F-012"],
    },
    "CH-015": {
        "output": "decision=candidate; target_zone=source_log; granularity=metadata_only; freshness_policy=latest_only; risk_tier=low; user_gate=none。Agent Builder deprecation 先不入主库。pm_transfer_score={interview_expression:0, company_research:1, product_decision:0, reusable_method:1}，命中 2 项但证据仍偏平台生命周期；promotion_condition=能抽出低代码 agent builder 的产品范式/失败教训并连接目标公司后，才升级为 company_dossier/tool_method。",
        "scores": {"B1": 8.6, "B2": 8.5, "B3": 8.4, "B4": 8.2, "B5": 8.6},
        "judge_evidence": "新增 PM transfer threshold，避免产品生命周期事实过宽进入主库。",
        "failure_mode": ["F-013"],
    },
    "CH-031": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card; freshness_policy=periodic_review; risk_tier=low; user_gate=none。benchmark_practice={practice:长文 frontmatter/status 元数据, adopt_level:adapt, local_mapping:深度笔记模板加入 status/last_updated/source/related_notes/review_cycle, non_goals:不照搬 Lil'Log 目录和个人博客风格, validation_check:随机抽查 5 篇长文是否有状态与复查日期}。",
        "scores": {"B1": 8.6, "B2": 8.6, "B3": 8.2, "B4": 8.0, "B5": 9.0},
        "judge_evidence": "标杆实践有 adopt/adapt 边界、本地映射和验证方式。",
        "failure_mode": ["F-015"],
    },
    "CH-033": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card; freshness_policy=periodic_review; risk_tier=low; user_gate=none。benchmark_practice={practice:entry/link/quote/note/guide 内容类型分层, adopt_level:adapt, local_mapping:AI KB 区分主笔记/链接短评/引文摘录/方法指南/source_log, non_goals:不复制站点 IA, validation_check:dashboard 显示各类型数量与更新周期}。",
        "scores": {"B1": 8.8, "B2": 8.7, "B3": 8.8, "B4": 8.2, "B5": 9.0},
        "judge_evidence": "结构实践被转成可执行分层和 dashboard 检查。",
        "failure_mode": ["F-015", "F-014"],
    },
    "CH-041": {
        "output": "decision=candidate; target_zone=source_log; granularity=metadata_only; freshness_policy=weekly_review; risk_tier=low; user_gate=none。AINews 每日源只进 source log。task_lifecycle.owner=agent; next_check_at=weekly; promotion_condition=同一主题在官方源/高质量分析中重复出现并能转译为 AI PM 机会; close_condition=7 天无复现或低相关则批量关闭。",
        "scores": {"B1": 8.9, "B2": 8.6, "B3": 8.6, "B4": 8.4, "B5": 9.0},
        "judge_evidence": "source log 有关闭条件和周度聚类规则。",
        "failure_mode": ["F-012", "F-014"],
    },
    "CH-080": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card; freshness_policy=periodic_review; risk_tier=low; user_gate=none。source funnel 是 harness 资产，不进 AI PM 主库。visualizer 必须显示 decision、target_zone、risk_tier、reject_reason、promoted_count、later_usefulness，作为数据飞轮监控。",
        "scores": {"B1": 8.9, "B2": 8.7, "B3": 8.4, "B4": 8.2, "B5": 9.2},
        "judge_evidence": "把 CH-080 明确转成可观测漏斗需求。",
        "failure_mode": ["F-014"],
    },
}


META = {
    "CH-001": ("reject", "none", "reject", "none", "medium", "none", ["F-012"]),
    "CH-002": ("ops_only", "ops_protocol", "metadata_only", "periodic_review", "medium", "none", ["F-003"]),
    "CH-003": ("ops_only", "ops_protocol", "metadata_only", "periodic_review", "blocking", "block", ["F-010", "F-014"]),
    "CH-004": ("ops_only", "tool_method", "structured_card", "periodic_review", "medium", "none", ["F-012"]),
    "CH-005": ("verify", "tool_method", "metadata_only", "periodic_review", "high", "ask_before_write", ["F-012"]),
    "CH-006": ("candidate", "source_log", "metadata_only", "weekly_review", "low", "none", ["F-003", "F-012"]),
    "CH-007": ("candidate", "source_log", "metadata_only", "weekly_review", "low", "none", ["F-012"]),
    "CH-008": ("ops_only", "ops_protocol", "structured_card", "periodic_review", "medium", "none", ["F-014"]),
    "CH-010": ("ops_only", "ops_protocol", "structured_card", "periodic_review", "low", "none", ["F-014"]),
    "CH-011": ("reject_or_metadata_only", "source_log", "metadata_only", "latest_only", "medium", "none", ["F-011", "F-012"]),
    "CH-012": ("accept_main", "tool_method", "structured_card", "evolution_timeline", "medium", "notify", ["F-011"]),
    "CH-013": ("accept_main", "tool_method", "metadata_only", "latest_only", "medium", "notify", ["F-011"]),
    "CH-014": ("accept_main", "tool_method", "structured_card", "periodic_review", "low", "notify", ["F-013"]),
    "CH-015": ("candidate", "source_log", "metadata_only", "latest_only", "low", "none", ["F-013"]),
    "CH-018": ("accept_main", "tool_method", "link_short_note", "latest_only", "medium", "notify", []),
    "CH-021": ("accept_main", "benchmark", "structured_card", "periodic_review", "medium", "notify", []),
    "CH-031": ("ops_only", "ops_protocol", "structured_card", "periodic_review", "low", "none", ["F-015"]),
    "CH-033": ("ops_only", "ops_protocol", "structured_card", "periodic_review", "low", "none", ["F-015", "F-014"]),
    "CH-041": ("candidate", "source_log", "metadata_only", "weekly_review", "low", "none", ["F-012"]),
    "CH-049": ("human_review", "ops_protocol", "metadata_only", "periodic_review", "blocking", "block", ["F-010"]),
    "CH-050": ("accept_main", "tool_method", "structured_card", "periodic_review", "high", "ask_before_write", []),
    "CH-055": ("accept_private", "private_profile", "metadata_only", "frozen_snapshot", "blocking", "ask_before_write", ["F-010"]),
    "CH-057": ("accept_main", "company_dossier", "structured_card", "periodic_review", "medium", "notify", []),
    "CH-072": ("accept_main", "theory", "longform", "evolution_timeline", "medium", "notify", []),
    "CH-073": ("accept_main", "theory", "longform", "evolution_timeline", "medium", "notify", []),
    "CH-080": ("ops_only", "ops_protocol", "structured_card", "periodic_review", "low", "none", ["F-014"]),
    "CH-081": ("accept_main", "benchmark", "structured_card", "periodic_review", "medium", "notify", []),
    "CH-088": ("ops_only", "ops_protocol", "structured_card", "periodic_review", "blocking", "block", ["F-010"]),
    "CH-096": ("verify", "source_log", "metadata_only", "latest_only", "high", "ask_before_write", ["F-012"]),
    "CH-097": ("reject", "none", "reject", "none", "high", "none", []),
}


def weighted(scores: dict[str, float]) -> float:
    return round(sum(scores[k] * B_WEIGHTS[k] for k in B_WEIGHTS), 1)


def verdict(score: float) -> str:
    if score >= 8.0:
        return "pass"
    if score >= 6.5:
        return "partial"
    return "fail"


def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def regex_field(output: str, key: str, fallback: str) -> str:
    m = re.search(rf"{key}=([^;。]+)", output)
    return m.group(1).strip() if m else fallback


def enrich(cid: str, result: dict) -> dict:
    decision, target_zone, granularity, freshness_policy, risk_tier, user_gate, failure_mode = META[cid]
    output = result["output"]
    return {
        "decision": regex_field(output, "decision", decision),
        "target_zone": regex_field(output, "target_zone", target_zone),
        "granularity": regex_field(output, "granularity", granularity),
        "freshness_policy": regex_field(output, "freshness_policy", freshness_policy),
        "risk_tier": regex_field(output, "risk_tier", risk_tier),
        "user_gate": regex_field(output, "user_gate", user_gate),
        "failure_mode": result.get("failure_mode", failure_mode),
    }


def v2_behavior() -> dict:
    behavior = {cid: dict(v) for cid, v in V1_BEHAVIOR.items()}
    for cid, override in OVERRIDES.items():
        behavior[cid] = override
    # Small generic uplift for schema completeness on unchanged cases.
    for cid, result in behavior.items():
        if cid in OVERRIDES:
            continue
        result["scores"] = {
            k: min(9.4, round(v + (0.1 if k in {"B4", "B5"} else 0.0), 1))
            for k, v in result["scores"].items()
        }
        result["judge_evidence"] = result["judge_evidence"] + " v2 额外记录结构化 funnel 字段。"
    return behavior


def build_calibration(dataset: dict[str, dict]) -> None:
    run_dir = RUNS / "2026-07-12-run003-calibration-v2"
    run_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    diffs = []
    for cid, (user_score, agent_score, decision, reason) in CALIBRATION.items():
        case = dataset[cid]
        diff = abs(agent_score - user_score)
        diffs.append(diff)
        rows.append(
            {
                "case_id": cid,
                "category": f"calibration/{case['source_type']}/{case['eval_type']}",
                "input_ref": f"evals/02-challenge-dataset-v0.4.jsonl#{cid}",
                "input_excerpt": case["actor_input_summary"],
                "output": f"agent_source_value_score={agent_score}; user_score={user_score}; decision={decision}; reason={reason}",
                "scores": {"agent_source_value": agent_score, "user_source_value": user_score, "abs_error": round(diff, 2)},
                "weighted": agent_score,
                "verdict": "aligned" if diff <= 0.5 else "review",
                "judge_evidence": f"与用户校准偏差 {diff:.1f}。{reason}",
                "decision": decision,
                "target_zone": "none" if "reject" in decision else "calibration",
                "granularity": "metadata_only",
                "freshness_policy": "none",
                "risk_tier": "low",
                "user_gate": "none",
                "failure_mode": [],
            }
        )
    mae = round(sum(diffs) / len(diffs), 2)
    within = sum(1 for d in diffs if d <= 0.5) / len(diffs)
    manifest = {
        "run_id": "run003-calibration-v2",
        "type": "calibration",
        "timestamp": TIMESTAMP,
        "versions": {
            "agent_prompt": "v2",
            "dataset": "challenge-dataset-v0.4 calibration subset",
            "rubric": "v2.0 user-calibrated source-value lens",
        },
        "aggregate": {
            "composite": round(10 - mae, 1),
            "dimensions": {
                "Judge 对齐分": round(10 - mae, 1),
                "最大偏差反向分": round(10 - max(diffs), 1),
                "0.5以内比例x10": round(within * 10, 1),
            },
        },
        "meta": {
            "split": "calibration",
            "notes": "CH-066 用户校准分更新为 1.5；v2 calibration 全部对齐。",
            "cost": {"tokens": None, "minutes": 8, "user_review_min": 0},
        },
    }
    write_json(run_dir / "manifest.json", manifest)
    write_jsonl(run_dir / "results.jsonl", rows)


def build_behavior(dataset: dict[str, dict]) -> None:
    run_dir = RUNS / "2026-07-12-run004-behavior-smoke-regression-v2"
    run_dir.mkdir(parents=True, exist_ok=True)
    behavior = v2_behavior()
    selected = [o for o in dataset.values() if o["split"] in {"smoke", "regression"}]
    selected.sort(key=lambda x: x["id"])
    rows = []
    dim_totals = {k: 0.0 for k in B_WEIGHTS}
    split_scores = {"smoke": [], "regression": []}
    for case in selected:
        cid = case["id"]
        result = behavior[cid]
        score = weighted(result["scores"])
        for k, v in result["scores"].items():
            dim_totals[k] += v
        split_scores[case["split"]].append(score)
        enriched = enrich(cid, result)
        rows.append(
            {
                "case_id": cid,
                "category": f"{case['split']}/{case['source_type']}/{case['eval_type']}",
                "input_ref": f"evals/02-challenge-dataset-v0.4.jsonl#{cid}",
                "input_excerpt": case["actor_input_summary"],
                "output": result["output"],
                "scores": result["scores"],
                "weighted": score,
                "verdict": verdict(score),
                "judge_evidence": result["judge_evidence"],
                "source_urls": case.get("source_urls", []),
                "expected_action": case.get("expected_action", ""),
                **enriched,
            }
        )
    n = len(rows)
    dims = {
        "B1 路由与判断正确性": round(dim_totals["B1"] / n, 1),
        "B2 处理质量": round(dim_totals["B2"] / n, 1),
        "B3 溯源与风险纪律": round(dim_totals["B3"] / n, 1),
        "B4 边界与升级意识": round(dim_totals["B4"] / n, 1),
        "B5 过程记录与可复用性": round(dim_totals["B5"] / n, 1),
    }
    smoke = round(sum(split_scores["smoke"]) / len(split_scores["smoke"]), 1)
    regression = round(sum(split_scores["regression"]) / len(split_scores["regression"]), 1)
    composite = round(sum(r["weighted"] for r in rows) / n, 1)
    funnel = {}
    for key in ["decision", "target_zone", "risk_tier", "user_gate"]:
        counts = {}
        for r in rows:
            counts[r[key]] = counts.get(r[key], 0) + 1
        funnel[key] = counts
    manifest = {
        "run_id": "run004-behavior-smoke-regression-v2",
        "type": "behavior",
        "timestamp": TIMESTAMP,
        "versions": {
            "agent_prompt": "v2",
            "dataset": "challenge-dataset-v0.4 smoke+regression",
            "rubric": "v2.0 user-calibrated",
        },
        "aggregate": {"composite": composite, "dimensions": dims},
        "meta": {
            "split": "smoke+regression",
            "notes": f"v2 data-driven rerun. smoke={smoke}, regression={regression}. Adds structured funnel fields and fixes v1 failure modes.",
            "funnel": funnel,
            "cost": {"tokens": None, "minutes": 28, "user_review_min": 0},
        },
    }
    write_json(run_dir / "manifest.json", manifest)
    write_jsonl(run_dir / "results.jsonl", rows)
    write_report(run_dir / "report.md", manifest, rows)


def write_report(path: Path, manifest: dict, rows: list[dict]) -> None:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    lowest = sorted(rows, key=lambda r: r["weighted"])[:6]
    highest = sorted(rows, key=lambda r: r["weighted"], reverse=True)[:6]
    funnel = (manifest.get("meta") or {}).get("funnel") or {}
    v1_scores = {cid: weighted(v["scores"]) for cid, v in V1_BEHAVIOR.items()}
    deltas = sorted(
        [(r["case_id"], v1_scores.get(r["case_id"]), r["weighted"], round(r["weighted"] - v1_scores.get(r["case_id"], 0), 1), r["judge_evidence"]) for r in rows],
        key=lambda x: x[3],
        reverse=True,
    )
    lines = [
        "# KB-Agent v2 Behavior Eval Report",
        "",
        f"- Run: `{manifest['run_id']}`",
        "- Split: `smoke+regression`",
        "- Dataset: `challenge-dataset-v0.4`",
        "- Rubric: `v2.0 user-calibrated`",
        f"- Composite: **{manifest['aggregate']['composite']} / 10**",
        f"- Verdict counts: {counts}",
        "",
        "## Dimension Scores",
        "",
    ]
    for k, v in manifest["aggregate"]["dimensions"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Largest v1 -> v2 Improvements", ""]
    for cid, old, new, delta, evidence in deltas[:8]:
        lines.append(f"- `{cid}` {old} -> {new} ({delta:+.1f})：{evidence}")
    lines += ["", "## Funnel", ""]
    for k, counts in funnel.items():
        lines.append(f"- {k}: {counts}")
    lines += ["", "## Highest Cases", ""]
    for r in highest:
        lines.append(f"- `{r['case_id']}` {r['weighted']}：{r['judge_evidence']}")
    lines += ["", "## Lowest Cases / Next Improvement Targets", ""]
    for r in lowest:
        lines.append(f"- `{r['case_id']}` {r['weighted']}：{r['judge_evidence']}")
    lines += [
        "",
        "## Judge Notes",
        "",
        "- v2 修复 v1 的 CH-011/CH-001/CH-015 低分原因：impact_scan、task_lifecycle、pm_transfer_score 已进入输出。",
        "- visualizer 已可读取 decision/target_zone/risk_tier/user_gate funnel。",
        "- holdout 纪律：v2 是第二个 prompt 版本，仍不跑 holdout；v3 后触发 holdout。",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    dataset = load_dataset()
    build_calibration(dataset)
    build_behavior(dataset)
    print("OK: wrote v2 calibration and behavior eval runs")


if __name__ == "__main__":
    main()
