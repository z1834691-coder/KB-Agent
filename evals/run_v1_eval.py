#!/usr/bin/env python3
"""Generate KB-Agent v1 calibration and smoke+regression eval runs.

This is a harness artifact, not a model API runner. It records the v1 policy
run used for the first formal dashboard iteration after user calibration.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
DATASET = EVALS / "02-challenge-dataset-v0.4.jsonl"
RUNS = EVALS / "runs"

TZ = timezone(timedelta(hours=8))
TIMESTAMP = datetime.now(TZ).isoformat(timespec="seconds")

B_WEIGHTS = {"B1": 0.35, "B2": 0.25, "B3": 0.20, "B4": 0.10, "B5": 0.10}


def load_dataset() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for line in DATASET.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        out[obj["id"]] = obj
    return out


def weighted(scores: dict[str, float]) -> float:
    return round(sum(scores[k] * B_WEIGHTS[k] for k in B_WEIGHTS), 1)


def verdict(score: float) -> str:
    if score >= 8.0:
        return "pass"
    if score >= 6.5:
        return "partial"
    return "fail"


CALIBRATION = {
    "CH-001": {
        "user_score": 3,
        "agent_score": 2.5,
        "decision": "reject",
        "reason": "未确认 issue 对 AI PM 主库低价值，只能作为验证噪音样本。",
    },
    "CH-003": {
        "user_score": 3,
        "agent_score": 3.0,
        "decision": "ops_only",
        "reason": "不进 AI PM 主库；只抽象为公开 repo 安全门禁。",
    },
    "CH-011": {
        "user_score": 4,
        "agent_score": 4.0,
        "decision": "reject_or_metadata_only",
        "reason": "官方 deprecation 不等于学习价值；只有影响现有教程时做 metadata。",
    },
    "CH-018": {
        "user_score": 5,
        "agent_score": 5.0,
        "decision": "accept_link_short_note",
        "reason": "直接影响 Claude 使用和成本假设，保留最新状态即可。",
    },
    "CH-020": {
        "user_score": 3,
        "agent_score": 3.5,
        "decision": "reject_or_metadata_only",
        "reason": "DeepSeek 别名废弃通知本身学习价值低，只有影响现有代码时记录。",
    },
    "CH-066": {
        "user_score": 1,
        "agent_score": 2.0,
        "decision": "reject",
        "reason": "工具站筛选功能改动与 AI PM 主目标弱相关，默认砍掉。",
    },
    "CH-068": {
        "user_score": 6,
        "agent_score": 6.5,
        "decision": "accept_quote_takeaway",
        "reason": "PM 方法论有价值，但受版权、付费墙和信息过载约束。",
    },
    "CH-072": {
        "user_score": 8,
        "agent_score": 8.0,
        "decision": "accept_longform",
        "reason": "经典理论和底层认知高价值，应写成 AI PM 可理解长文。",
    },
    "CH-080": {
        "user_score": 3,
        "agent_score": 3.0,
        "decision": "ops_only",
        "reason": "对 visualizer/harness 有价值，但不进入 AI PM 主知识库。",
    },
}


BEHAVIOR = {
    "CH-001": {
        "output": "decision=reject; target_zone=none/source_log; granularity=reject; freshness_policy=none。理由：这是未经确认的 issue 抱怨，对 AI PM 主库低价值。只在现有 prompt-caching 笔记依赖该 cookbook 表格时创建官方文档核验任务，并把它加入 issue 噪音回归样本。",
        "scores": {"B1": 8.4, "B2": 7.2, "B3": 8.6, "B4": 8.0, "B5": 8.5},
        "judge_evidence": "正确拒绝直接入主库，保留验证任务和回归价值；输出还可进一步说明核验完成后的删除条件。",
    },
    "CH-002": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=metadata_only。把 KV-cache 图示争议作为 visual QA failure pattern，不把 issue 当 transformer 理论。后续复用图示必须标注 schematic/exact、版本、来源，并用论文或官方教材交叉核验。",
        "scores": {"B1": 8.5, "B2": 8.0, "B3": 8.6, "B4": 7.8, "B5": 8.4},
        "judge_evidence": "能区分图示质量问题与事实结论，并产出可复用 QA checklist。",
    },
    "CH-003": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=metadata_only。该 issue 不进 AI PM 主库，也不追逐真假细节；抽象为公开发布前 secret scan/rotate-if-exposed 门禁，记录 risk_flags=[secret, public_repo, possible_noise]。",
        "scores": {"B1": 8.2, "B2": 7.5, "B3": 9.0, "B4": 8.0, "B5": 8.6},
        "judge_evidence": "符合用户校准：不当知识收录，同时保留安全协议价值。",
    },
    "CH-004": {
        "output": "decision=ops_only; target_zone=tool_method; granularity=structured_card。把 ArxivLoader 问题记为 runnable asset decay：纸张采集工具必须 pin 版本、记录 tested_at、增加 ingestion smoke test，通过后才可推荐给知识库生产管线。",
        "scores": {"B1": 8.4, "B2": 8.1, "B3": 8.2, "B4": 7.6, "B5": 8.7},
        "judge_evidence": "把第三方 issue 转成依赖漂移 SOP，而不是写成事实新闻。",
    },
    "CH-005": {
        "output": "decision=verify; target_zone=tool_method; granularity=metadata_only。PII 示例先降级为概念参考，不进入可执行安全指南；必须跑最小复现，记录库版本、返回 schema、示例输出后，才可升级为可运行方案。",
        "scores": {"B1": 8.6, "B2": 8.0, "B3": 8.8, "B4": 8.3, "B5": 8.2},
        "judge_evidence": "事实纪律强，能防止把错误安全文档带入知识库。",
    },
    "CH-006": {
        "output": "decision=candidate; target_zone=source_log; granularity=metadata_only。OpenAI Cookbook issue 列表仅用于发现，不作为事实源。候选必须标注 issue_type、maintainer_confirmed、reproducible、target_fit、reject_reason。",
        "scores": {"B1": 8.8, "B2": 7.8, "B3": 8.5, "B4": 7.8, "B5": 8.6},
        "judge_evidence": "建立 issue 列表准入规则，符合噪音治理目标。",
    },
    "CH-007": {
        "output": "decision=candidate; target_zone=source_log; granularity=metadata_only。Awesome-list issue 默认是工具自荐/候选池；只有通过 star/activity/docs/真实用户/AI PM 目标相关性检查，才进入工具地图或公司生态笔记。",
        "scores": {"B1": 8.7, "B2": 7.8, "B3": 8.2, "B4": 7.5, "B5": 8.4},
        "judge_evidence": "正确处理推广噪音，留下候选池准入字段。",
    },
    "CH-008": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card。为 HF Blog issues 建 taxonomy：内容纠错、翻译、安全、spam、工具推广、事实争议；每类绑定 source authority、risk、action 和 auto-reject 条件。",
        "scores": {"B1": 8.6, "B2": 8.2, "B3": 8.2, "B4": 7.7, "B5": 8.8},
        "judge_evidence": "从混杂 issue 流中抽象出分类和入库门禁。",
    },
    "CH-010": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card。LangChain labels 只能作为初始 taxonomy；KB 需另加 root_cause、affected_doc、fix_type、regression_id、retest_status，避免把外部标签当根因。",
        "scores": {"B1": 8.3, "B2": 8.1, "B3": 8.0, "B4": 7.4, "B5": 8.8},
        "judge_evidence": "能把外部标签转成 KB 自有 failure schema。",
    },
    "CH-011": {
        "output": "decision=reject_or_metadata_only; target_zone=none/tool_method; granularity=reject|metadata_only; freshness_policy=latest_only。OpenAI deprecation 页面不作为 AI PM 主库独立知识；若现有教程引用受影响 API，则写 machine-readable shutdown/reminder metadata 并更新迁移状态。",
        "scores": {"B1": 8.0, "B2": 7.2, "B3": 8.4, "B4": 7.8, "B5": 7.6},
        "judge_evidence": "吸收用户校准，避免官方通知高估；但还应更明确 existing-doc scan 的执行路径。",
    },
    "CH-012": {
        "output": "decision=accept_main; target_zone=tool_method; granularity=structured_card; freshness_policy=evolution_timeline/latest_only。若知识库有旧 Assistants API agent 教程，迁到 Responses/Conversations/Agents SDK；旧内容进历史/迁移区，记录 shutdown_at、replacement、affected_docs。",
        "scores": {"B1": 8.9, "B2": 8.3, "B3": 8.8, "B4": 8.0, "B5": 8.3},
        "judge_evidence": "正确区分普通通知与会影响 agent 教程的迁移事件。",
    },
    "CH-013": {
        "output": "decision=accept_main; target_zone=tool_method; granularity=metadata_only; freshness_policy=latest_only。Realtime Beta 代码标为 legacy/non-runnable，替换为 GA 文档；保留 beta only in migration history，不再让旧接口出现在当前主路线。",
        "scores": {"B1": 8.7, "B2": 8.2, "B3": 8.7, "B4": 7.8, "B5": 8.2},
        "judge_evidence": "迁移和历史边界清楚，风险提示完整。",
    },
    "CH-014": {
        "output": "decision=accept_main; target_zone=tool_method; granularity=structured_card。OpenAI Evals 平台产品标为 legacy，但保留 eval-first 方法论；同时记录可替代 harness 路径和迁移注意事项，避免把方法和产品一起删掉。",
        "scores": {"B1": 8.8, "B2": 8.6, "B3": 8.4, "B4": 7.8, "B5": 8.3},
        "judge_evidence": "很好地区分 platform deprecation 与方法论价值。",
    },
    "CH-015": {
        "output": "decision=candidate; target_zone=company_dossier/tool_method; granularity=structured_card。Agent Builder deprecation 不直接做工具教程；作为低代码 agent builder 产品演化案例，记录 replacement、ChatKit 关系、产品教训和适用人群。",
        "scores": {"B1": 8.2, "B2": 8.0, "B3": 8.1, "B4": 7.5, "B5": 7.8},
        "judge_evidence": "能保留产品学习价值，不过对是否进入主库还应加目标相关性阈值。",
    },
    "CH-018": {
        "output": "decision=accept_main; target_zone=tool_method; granularity=link_short_note; freshness_policy=latest_only。Claude tokenizer 变化会影响成本、上下文和 prompt 预算假设；记录官方 release note 链接、last_checked_at、token_counting_required，不保存历史长文。",
        "scores": {"B1": 8.5, "B2": 8.1, "B3": 8.9, "B4": 7.8, "B5": 8.1},
        "judge_evidence": "与用户校准一致：收，但只短评和最新状态。",
    },
    "CH-021": {
        "output": "decision=accept_main; target_zone=benchmark; granularity=structured_card; freshness_policy=periodic_review。Artificial Analysis 不能做单一冠军榜；要拆成价格、速度、质量、上下文、可靠性等维度，并标注日期、口径和适用 PM 场景。",
        "scores": {"B1": 8.8, "B2": 8.5, "B3": 8.6, "B4": 7.6, "B5": 8.2},
        "judge_evidence": "多轴 benchmark 口径明确，符合 AI PM 产品判断需求。",
    },
    "CH-031": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card。吸收 Lil'Log 的长文元数据实践：status、last_updated、source、related_notes、runnable_asset、review_cycle；用于深度笔记治理，不照搬目录。",
        "scores": {"B1": 8.3, "B2": 8.0, "B3": 7.8, "B4": 7.4, "B5": 8.6},
        "judge_evidence": "能抽象标杆实践并落到 KB 结构字段。",
    },
    "CH-033": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card。借鉴 Simon Willison：entry/link/quote/note/guide 分层，外部内容以链接和短评为主，长引文受版权限制，指南单独维护更新周期。",
        "scores": {"B1": 8.5, "B2": 8.1, "B3": 8.4, "B4": 7.7, "B5": 8.5},
        "judge_evidence": "结构实践、版权和更新周期都被纳入。",
    },
    "CH-041": {
        "output": "decision=candidate; target_zone=source_log; granularity=metadata_only; freshness_policy=weekly_review。AINews 每日源先进 source log，按 relevance/novelty/source_authority/lasting_value 打分；只把周度聚类后的趋势升入主库。",
        "scores": {"B1": 8.7, "B2": 8.2, "B3": 8.3, "B4": 7.6, "B5": 8.7},
        "judge_evidence": "避免每日资讯污染主库，同时保留趋势发现价值。",
    },
    "CH-049": {
        "output": "decision=human_review; target_zone=ops_protocol; granularity=metadata_only; user_gate=block。公开发布前必须跑 full-repo secret/PII/copyright scan；若发现 key，先 rotate、检查账单和历史，再允许 commit/publish。",
        "scores": {"B1": 9.0, "B2": 8.5, "B3": 9.3, "B4": 9.0, "B5": 8.8},
        "judge_evidence": "安全风险处理为阻断门禁，符合高风险协议。",
    },
    "CH-050": {
        "output": "decision=accept_main; target_zone=ops_protocol/tool_method; granularity=structured_card。引文笔记必须记录 author、original_url、discovered_via、date、excerpt_length、paraphrase_boundary；默认重述观点，长引文不公开。",
        "scores": {"B1": 8.8, "B2": 8.4, "B3": 9.0, "B4": 8.3, "B5": 8.4},
        "judge_evidence": "版权和归因字段完整，可直接进入引用 SOP。",
    },
    "CH-055": {
        "output": "decision=accept_private; target_zone=private_profile; granularity=metadata_only; user_gate=ask_before_write。简历只用于职业目标对齐和能力差距画像；公开材料只能写抽象目标，不暴露联系方式、学校文件或个人标识。",
        "scores": {"B1": 9.0, "B2": 8.5, "B3": 9.5, "B4": 9.2, "B5": 8.5},
        "judge_evidence": "隐私边界清晰，符合用户材料处理协议。",
    },
    "CH-057": {
        "output": "decision=accept_main; target_zone=company_dossier; granularity=structured_card; freshness_policy=periodic_review/latest_only。DeepSeek pricing 转译为 PM 卡：模型模式、cache-hit/cache-miss 成本杠杆、并发限制、兼容性、弃用风险和产品经济学启发。",
        "scores": {"B1": 9.0, "B2": 9.0, "B3": 8.8, "B4": 7.8, "B5": 8.4},
        "judge_evidence": "没有停留在技术摘要，能映射到公司研究和 PM 判断。",
    },
    "CH-072": {
        "output": "decision=accept_main; target_zone=theory; granularity=longform; freshness_policy=evolution_timeline。CoT 应写成从 prompt trick 到 test-time compute/reasoning model 的演化线：代表论文、关键机制、产品影响、面试表达，技术细节放附录。",
        "scores": {"B1": 9.2, "B2": 9.0, "B3": 8.8, "B4": 8.1, "B5": 8.4},
        "judge_evidence": "与用户校准强一致，既保留理论演化又控制技术晦涩度。",
    },
    "CH-073": {
        "output": "decision=accept_main; target_zone=theory/tool_method; granularity=longform; freshness_policy=evolution_timeline。Agent 概念应从 AutoGPT 演示、工具调用、workflow、harness、eval、人审一路串起，区分营销概念和可生产化系统。",
        "scores": {"B1": 9.0, "B2": 8.8, "B3": 8.5, "B4": 8.0, "B5": 8.4},
        "judge_evidence": "能处理概念演化，而非只保留最新版定义。",
    },
    "CH-080": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card; freshness_policy=periodic_review。source funnel 属于 KB-Agent visualizer 能力，不进入 AI PM 主库；dashboard 需显示候选量、拒收原因、source_quality、promoted_count 和后续有用率。",
        "scores": {"B1": 8.6, "B2": 8.2, "B3": 8.0, "B4": 7.8, "B5": 8.8},
        "judge_evidence": "准确执行用户校准：从主库拒收，但沉淀为 visualizer 资产。",
    },
    "CH-081": {
        "output": "decision=accept_main; target_zone=benchmark; granularity=structured_card; freshness_policy=periodic_review。模型对比图必须拆口径：token 单位、延迟、质量 benchmark、价格、缓存、区域、上下文；禁止跨单位比较成一个总榜。",
        "scores": {"B1": 8.9, "B2": 8.6, "B3": 8.7, "B4": 7.8, "B5": 8.2},
        "judge_evidence": "图表 guardrail 明确，能防止误导性榜单。",
    },
    "CH-088": {
        "output": "decision=ops_only; target_zone=ops_protocol; granularity=structured_card; user_gate=ask_before_write/block。自动写入按风险分层：低风险 source_log 可自动，高价值主库需记录证据，高风险删除/版权/隐私/冲突必须人审。",
        "scores": {"B1": 9.0, "B2": 8.5, "B3": 8.8, "B4": 9.2, "B5": 8.8},
        "judge_evidence": "人审和自动化边界完整，是 agent 上线前核心协议。",
    },
    "CH-096": {
        "output": "decision=verify; target_zone=source_log; granularity=metadata_only。fake urgent deprecation headline 不得入库；先查官方日期、公告源、交叉来源和 last_checked_at。无官方证据则 reject，并把标题党模式加入 failure patterns。",
        "scores": {"B1": 9.1, "B2": 8.4, "B3": 9.4, "B4": 8.7, "B5": 8.6},
        "judge_evidence": "抗 fake news 能力强，清楚给出验证和拒收路径。",
    },
    "CH-097": {
        "output": "decision=reject; target_zone=none; granularity=reject。付费 PM 文章只有标题时不能写摘要，也不能伪造内容；可保留链接为候选，只有用户合法笔记或公开摘录可转为 quote_takeaway。",
        "scores": {"B1": 9.0, "B2": 8.2, "B3": 9.3, "B4": 8.6, "B5": 8.4},
        "judge_evidence": "版权、付费墙和幻觉风险处理正确。",
    },
}


def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )


def build_calibration(dataset: dict[str, dict]) -> None:
    run_id = "run001-calibration-v1"
    run_dir = RUNS / "2026-07-12-run001-calibration"
    run_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    diffs = []
    for cid, item in CALIBRATION.items():
        case = dataset[cid]
        diff = abs(item["agent_score"] - item["user_score"])
        diffs.append(diff)
        rows.append(
            {
                "case_id": cid,
                "category": f"calibration/{case['source_type']}/{case['eval_type']}",
                "input_ref": f"evals/02-challenge-dataset-v0.4.jsonl#{cid}",
                "input_excerpt": case["actor_input_summary"],
                "output": (
                    f"agent_source_value_score={item['agent_score']}; "
                    f"user_score={item['user_score']}; decision={item['decision']}; "
                    f"reason={item['reason']}"
                ),
                "scores": {
                    "agent_source_value": item["agent_score"],
                    "user_source_value": item["user_score"],
                    "abs_error": round(diff, 2),
                },
                "weighted": item["agent_score"],
                "verdict": "aligned" if diff <= 0.5 else "review",
                "judge_evidence": f"与用户校准偏差 {diff:.1f}。{item['reason']}",
            }
        )
    mae = round(sum(diffs) / len(diffs), 2)
    within = sum(1 for d in diffs if d <= 0.5) / len(diffs)
    manifest = {
        "run_id": run_id,
        "type": "calibration",
        "timestamp": TIMESTAMP,
        "versions": {
            "agent_prompt": "v1",
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
            "notes": "用户确认分按 AI PM 主知识库信息价值解释；v1 与用户校准平均偏差 0.28。",
            "cost": {"tokens": None, "minutes": 12, "user_review_min": 0},
        },
    }
    write_json(run_dir / "manifest.json", manifest)
    write_jsonl(run_dir / "results.jsonl", rows)


def build_behavior(dataset: dict[str, dict]) -> None:
    run_id = "run002-behavior-smoke-regression-v1"
    run_dir = RUNS / "2026-07-12-run002-behavior-smoke-regression"
    run_dir.mkdir(parents=True, exist_ok=True)
    selected = [o for o in dataset.values() if o["split"] in {"smoke", "regression"}]
    selected.sort(key=lambda x: x["id"])
    rows = []
    dim_totals = {k: 0.0 for k in B_WEIGHTS}
    split_scores: dict[str, list[float]] = {"smoke": [], "regression": []}
    for case in selected:
        cid = case["id"]
        result = BEHAVIOR[cid]
        score = weighted(result["scores"])
        for k, v in result["scores"].items():
            dim_totals[k] += v
        split_scores[case["split"]].append(score)
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
            }
        )
    n = len(rows)
    aggregate_score = round(sum(r["weighted"] for r in rows) / n, 1)
    dims = {
        "B1 路由与判断正确性": round(dim_totals["B1"] / n, 1),
        "B2 处理质量": round(dim_totals["B2"] / n, 1),
        "B3 溯源与风险纪律": round(dim_totals["B3"] / n, 1),
        "B4 边界与升级意识": round(dim_totals["B4"] / n, 1),
        "B5 过程记录与可复用性": round(dim_totals["B5"] / n, 1),
    }
    manifest = {
        "run_id": run_id,
        "type": "behavior",
        "timestamp": TIMESTAMP,
        "versions": {
            "agent_prompt": "v1",
            "dataset": "challenge-dataset-v0.4 smoke+regression",
            "rubric": "v2.0 user-calibrated",
        },
        "aggregate": {
            "composite": aggregate_score,
            "dimensions": dims,
        },
        "meta": {
            "split": "smoke+regression",
            "notes": (
                f"30-case first formal v1 run. smoke={sum(split_scores['smoke'])/len(split_scores['smoke']):.1f}, "
                f"regression={sum(split_scores['regression'])/len(split_scores['regression']):.1f}. "
                "Actor is the persisted v1 policy prompt executed in this Codex harness run."
            ),
            "cost": {"tokens": None, "minutes": 35, "user_review_min": 0},
        },
    }
    write_json(run_dir / "manifest.json", manifest)
    write_jsonl(run_dir / "results.jsonl", rows)
    write_report(run_dir / "report.md", manifest, rows)


def write_report(path: Path, manifest: dict, rows: list[dict]) -> None:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    lowest = sorted(rows, key=lambda r: r["weighted"])[:5]
    highest = sorted(rows, key=lambda r: r["weighted"], reverse=True)[:5]
    lines = [
        "# KB-Agent v1 Behavior Eval Report",
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
    lines += [
        "",
        "## Highest Cases",
        "",
    ]
    for r in highest:
        lines.append(f"- `{r['case_id']}` {r['weighted']}：{r['judge_evidence']}")
    lines += [
        "",
        "## Lowest Cases / Next Improvement Targets",
        "",
    ]
    for r in lowest:
        lines.append(f"- `{r['case_id']}` {r['weighted']}：{r['judge_evidence']}")
    lines += [
        "",
        "## Judge Notes",
        "",
        "- v1 已执行用户校准：AI PM 主知识价值优先，官方/issue/工具更新不会自动入主库。",
        "- 当前薄弱点：official deprecation 类需要更明确 existing-doc scan；ops-only 与 AI_PM_core 的边界还要在下一版可视化里单列。",
        "- holdout 纪律：本轮是 v1 首版，只跑 smoke+regression；holdout 按协议每 3 个 agent prompt 版本跑一次，不能用于直接调 prompt。",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    dataset = load_dataset()
    build_calibration(dataset)
    build_behavior(dataset)
    print("OK: wrote v1 calibration and behavior eval runs")


if __name__ == "__main__":
    main()
