#!/usr/bin/env python3
"""KB-Agent robustness audit — OBJECTIVE structural signals only.

Philosophy (project soul): mechanical-measurable != quality.
This script computes ONLY the [MECH] dimensions of robustness-judge.md
(R1 recoverability, R3 traceability, R4 safety-boundary, R7 reuse) and emits a
clearly-labelled *mechanical integrity score*. It DELIBERATELY refuses to score
the [JUDGE] dimensions (R2 eval-honesty, R5 depth-honesty, R6 attribution) —
those require an LLM/human with evidence. Printing a single pretty composite as
"the system is good" is exactly the Goodhart trap this project exists to avoid.

Usage:
    python3 evals/robustness_audit.py            # human-readable report
    python3 evals/robustness_audit.py --json     # machine-readable
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TZ = timezone(timedelta(hours=8))
SCRIPT = Path(__file__).resolve()
KB_AGENT = SCRIPT.parents[1]
VAULT = KB_AGENT.parent / "AI知识库 V3"
DOSSIERS = VAULT / "company-dossiers"
FLYWHEEL = VAULT / "_meta" / "flywheel"

STATE_FILES = [
    KB_AGENT / "进展.md",
    KB_AGENT / "work" / "ITERATION-TREE.md",
    KB_AGENT / "work" / "AUTONOMOUS-LOOP-PROMPT.md",
]
PROTOCOL_FILES = [
    KB_AGENT / "protocols" / "01-context-protocol.md",
    KB_AGENT / "protocols" / "02-tool-protocol.md",
    KB_AGENT / "protocols" / "03-human-review-protocol.md",
]


def now() -> datetime:
    return datetime.now(TZ)


def git(repo: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return proc.stdout.strip()


def mtime_days(path: Path) -> float | None:
    if not path.exists():
        return None
    dt = datetime.fromtimestamp(path.stat().st_mtime, TZ)
    return round((now() - dt).total_seconds() / 86400, 2)


def r1_recoverability() -> dict:
    present = {p.name: p.exists() for p in STATE_FILES}
    ages = {p.name: mtime_days(p) for p in STATE_FILES}
    all_present = all(present.values())
    # fresh if the freshest state file was touched within 8 days
    fresh_ages = [a for a in ages.values() if a is not None]
    freshest = min(fresh_ages) if fresh_ages else None
    fresh = freshest is not None and freshest <= 8
    score = 10.0 if all_present and fresh else (6.0 if all_present else 2.0)
    return {"score": score, "present": present, "age_days": ages,
            "note": "state files present+fresh" if score == 10 else "missing or stale state files"}


def r3_traceability() -> dict:
    kb_log = git(VAULT, ["log", "-1", "--pretty=format:%h %ad %s", "--date=short"])
    agent_log = git(KB_AGENT, ["log", "-1", "--pretty=format:%h %ad %s", "--date=short"])
    fw = FLYWHEEL / "run-events.jsonl"
    fw_age = mtime_days(fw)
    score = 10.0
    if not kb_log or not agent_log:
        score -= 4.0
    if fw_age is None or fw_age > 14:
        score -= 3.0
    return {"score": max(0.0, round(score, 1)),
            "vault_head": kb_log, "agent_head": agent_log,
            "flywheel_run_events_age_days": fw_age}


def r4_safety_boundary() -> dict:
    """Objective checks only: is the vault working tree unexpectedly rewritten by
    an unattended process? We flag but cannot fully judge intent — hence [MECH] partial."""
    dirty = [ln for ln in git(VAULT, ["status", "--short"]).splitlines() if ln.strip()]
    protocols_present = all(p.exists() for p in PROTOCOL_FILES)
    human_review = KB_AGENT / "protocols" / "03-human-review-protocol.md"
    score = 10.0 if protocols_present else 5.0
    return {"score": score, "protocols_present": protocols_present,
            "human_review_protocol": human_review.exists(),
            "vault_dirty_lines": len(dirty),
            "note": "HITL/tool/context protocols present" if protocols_present else "missing protocol files"}


def r7_reuse() -> dict:
    sop_dir = VAULT / "_meta" / "sop"
    sops = sorted(sop_dir.glob("SOP-*.md")) if sop_dir.exists() else []
    return {"score": 10.0 if len(sops) >= 3 else round(3.0 + len(sops) * 2.0, 1),
            "sop_count": len(sops), "sops": [p.name for p in sops]}


def dossier_depth_parity() -> dict:
    """Objective signal feeding R5 [JUDGE] — reports the numbers, does NOT judge quality."""
    if not DOSSIERS.exists():
        return {"available": False}
    rows = []
    for p in sorted(DOSSIERS.glob("*.md")):
        if p.name.startswith("00-"):
            continue
        rows.append((p.name, len(p.read_text(encoding="utf-8").splitlines())))
    if not rows:
        return {"available": False}
    lengths = [n for _, n in rows]
    med = statistics.median(lengths)
    threshold = med * 0.6
    under = [{"file": f, "lines": n} for f, n in rows if n < threshold]
    return {"available": True, "median_lines": med,
            "under_depth_threshold": round(threshold, 1),
            "under_depth": under,
            "all": [{"file": f, "lines": n} for f, n in rows]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    mech = {"R1_recoverability": r1_recoverability(),
            "R3_traceability": r3_traceability(),
            "R4_safety_boundary": r4_safety_boundary(),
            "R7_reuse": r7_reuse()}
    weights = {"R1_recoverability": 0.15, "R3_traceability": 0.15,
               "R4_safety_boundary": 0.15, "R7_reuse": 0.05}
    wsum = sum(weights.values())
    mech_composite = round(sum(mech[k]["score"] * w for k, w in weights.items()) / wsum, 2)

    parity = dossier_depth_parity()
    result = {
        "generated_at": now().isoformat(timespec="seconds"),
        "kind": "robustness_audit_MECHANICAL_ONLY",
        "mechanical_dimensions": mech,
        "mechanical_integrity_score": mech_composite,
        "dossier_depth_parity_signal": parity,
        "REQUIRES_JUDGE": {
            "R2_eval_honesty": "LLM/human must score with evidence — NOT auto-scored",
            "R5_depth_honesty": "use dossier_depth_parity_signal as INPUT, then judge",
            "R6_attribution": "LLM/human must verify single-cause attribution",
        },
        "DISCLAIMER": "此为机械结构分，非质量分。综合鲁棒性必须叠加 robustness-judge.md 的 [JUDGE] 维度证据。",
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"=== KB-Agent Robustness Audit (MECHANICAL ONLY) · {result['generated_at']} ===")
    for k, v in mech.items():
        print(f"  {k}: {v['score']}/10  — {v.get('note', '')}")
    print(f"  → 机械结构完整性分: {mech_composite}/10  (⚠ 非质量分，不代表系统好坏)")
    if parity.get("available"):
        print(f"\n  Dossier depth: median={parity['median_lines']} 行, under-depth 阈值={parity['under_depth_threshold']}")
        if parity["under_depth"]:
            for u in parity["under_depth"]:
                print(f"    ❗ under-depth: {u['file']} = {u['lines']} 行 (< 阈值)")
        else:
            print("    ✅ 无 under-depth 档案")
    print("\n  ⚠ R2 评测诚实性 / R5 深度诚实 / R6 归因有效性 = [JUDGE]，必须由 LLM/人工带证据打分，本脚本拒绝机械代打。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
