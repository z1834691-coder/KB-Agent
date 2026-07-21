#!/usr/bin/env python3
"""Flywheel digest — close the data-flywheel loop (Task 3).

The project already *records* rich flywheel JSONL (score series, candidate
decisions, sop patches, run events). This script *uses* them: it reads the
flywheel and emits a NEXT-ROUND BRIEFING (trends, chronic weak dimensions,
pending candidates, recommended focus) that the loop's node-selection step
(AUTONOMOUS-LOOP-PROMPT Step B) consumes — so data informs selection, not just
gets logged. That is the flywheel actually turning.

Usage:
    python3 evals/flywheel_digest.py            # human-readable briefing
    python3 evals/flywheel_digest.py --json
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path

SCRIPT = Path(__file__).resolve()
KB_AGENT = SCRIPT.parents[1]


def resolve_vault() -> Path:
    """Locate the maintained vault. Order: $KB_VAULT → sibling private vault →
    bundled examples/sample-vault (so a fresh clone runs out of the box)."""
    env = os.environ.get("KB_VAULT")
    if env:
        return Path(env).expanduser()
    sibling = KB_AGENT.parent / "AI知识库 V3"
    if sibling.exists():
        return sibling
    bundled = KB_AGENT / "examples" / "sample-vault"
    if bundled.exists():
        return bundled
    return sibling


VAULT = resolve_vault()
FW = VAULT / "_meta" / "flywheel"


def read_jsonl(name: str) -> list[dict]:
    p = FW / name
    rows = []
    if not p.exists():
        return rows
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows


def score_trends() -> dict:
    rows = read_jsonl("score-timeseries.jsonl")
    by_kind: dict[str, list[dict]] = {}
    for r in rows:
        by_kind.setdefault(r.get("kind", "?"), []).append(r)
    out = {}
    for kind, series in by_kind.items():
        series = [s for s in series if isinstance(s.get("composite"), (int, float))]
        if not series:
            continue
        first, last = series[0]["composite"], series[-1]["composite"]
        # lowest current dimension from the latest entry
        dims = series[-1].get("dimensions", {}) or {}
        lowest = min(dims.items(), key=lambda kv: kv[1]) if dims else None
        out[kind] = {
            "n": len(series), "first": first, "last": last,
            "delta": round(last - first, 2),
            "direction": "↑" if last > first else ("↓" if last < first else "→"),
            "lowest_dim_now": {"name": lowest[0], "score": lowest[1]} if lowest else None,
        }
    return out


def chronic_weak_dims() -> list[dict]:
    """Dimensions repeatedly written to sop-patches (<7.0) = chronic weak spots."""
    rows = read_jsonl("sop-patches.jsonl")
    c = Counter(r.get("dimension") for r in rows if r.get("dimension"))
    return [{"dimension": d, "flagged_times": n} for d, n in c.most_common(5)]


def pending_candidates() -> dict:
    rows = read_jsonl("candidate-decisions.jsonl")
    recent = rows[-8:]
    touch = [r for r in recent if r.get("should_touch_main_library")]
    reasons = Counter()
    for r in recent:
        for reason in (r.get("reasons") or []):
            reasons[reason] += 1
    return {"recent_n": len(recent),
            "pending_touch_main_library": len(touch),
            "top_reasons": reasons.most_common(5)}


def recommend(trends: dict, weak: list[dict], cands: dict) -> list[str]:
    recs = []
    # 1) regressing score kind
    for kind, t in trends.items():
        if t["direction"] == "↓":
            recs.append(f"⚠️ `{kind}` 分在下降({t['first']}→{t['last']})——下一轮优先查回归原因，不要叠新内容。")
    # 2) lowest current dimension
    doc = trends.get("doctor") or trends.get("robustness")
    if doc and doc.get("lowest_dim_now"):
        ld = doc["lowest_dim_now"]
        recs.append(f"📉 当前最低维度 = {ld['name']}({ld['score']})——下一轮把它作为首选修复目标。")
    # 3) chronic weak
    if weak:
        top = weak[0]
        recs.append(f"🔁 慢性弱项 = {top['dimension']}(被 SOP 队列标记 {top['flagged_times']} 次)——需结构性修复而非反复打补丁。")
    # 4) pending candidates
    if cands.get("top_reasons"):
        r0 = cands["top_reasons"][0]
        recs.append(f"📥 候选信号最多来自 `{r0[0]}`({r0[1]}次)——检查是否有该类待消化信号(如新早报/快变事实)。")
    if not recs:
        recs.append("✅ 无回归、无慢性弱项、无积压候选——可按 ITERATION-TREE 正常选下一节点。")
    return recs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    trends = score_trends()
    weak = chronic_weak_dims()
    cands = pending_candidates()
    recs = recommend(trends, weak, cands)
    result = {"score_trends": trends, "chronic_weak_dims": weak,
              "pending_candidates": cands, "next_round_focus": recs}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print("=== 飞轮 Digest · 下一轮聚焦建议（数据反哺选路）===\n")
    print("· 分数趋势:")
    for kind, t in trends.items():
        low = f" · 最低维 {t['lowest_dim_now']['name']}={t['lowest_dim_now']['score']}" if t.get("lowest_dim_now") else ""
        print(f"    {kind}: {t['first']}→{t['last']} {t['direction']}(Δ{t['delta']}, n={t['n']}){low}")
    print("· 慢性弱项(SOP队列反复标记):", weak or "无")
    print(f"· 候选信号: 近{cands['recent_n']}条, 待动主库 {cands['pending_touch_main_library']}, top={cands['top_reasons']}")
    print("\n· 下一轮聚焦建议:")
    for r in recs:
        print("   ", r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
