#!/usr/bin/env python3
"""Validate KB-Agent behavior eval run artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from schema import (  # noqa: E402 - local eval harness module
    ACTOR_FORBIDDEN,
    B_WEIGHTS,
    DECISIONS,
    MANIFEST_REQUIRED,
    RESULT_REQUIRED,
    RISK_TIERS,
    TARGET_ZONES,
    USER_GATES,
    actor_required_fields,
    load_jsonl,
    weighted,
)


def load_manifest(run_dir: Path, errors: list[str]) -> dict:
    path = run_dir / "manifest.json"
    if not path.exists():
        errors.append("missing manifest.json")
        return {}
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"manifest.json invalid JSON: {exc}")
        return {}
    missing = sorted(MANIFEST_REQUIRED - manifest.keys())
    if missing:
        errors.append(f"manifest missing {missing}")
    return manifest


def check_actor(run_dir: Path, expected_cases: int, manifest: dict, errors: list[str]) -> list[dict]:
    path = run_dir / "actor-output.jsonl"
    if not path.exists():
        errors.append("missing actor-output.jsonl")
        return []
    rows = load_jsonl(path)
    if len(rows) != expected_cases:
        errors.append(f"actor rows={len(rows)} expected={expected_cases}")
    ids = [r.get("case_id") for r in rows]
    if len(set(ids)) != len(ids):
        errors.append("actor has duplicate case_id")
    agent_prompt = (manifest.get("versions") or {}).get("agent_prompt")
    required = actor_required_fields(agent_prompt)
    for row in rows:
        cid = row.get("case_id", "<missing>")
        missing = sorted(required - row.keys())
        forbidden = sorted(ACTOR_FORBIDDEN & row.keys())
        if missing:
            errors.append(f"{cid}: actor missing {missing}")
        if forbidden:
            errors.append(f"{cid}: actor contains judge-only fields {forbidden}")
        if row.get("decision") not in DECISIONS:
            errors.append(f"{cid}: unknown decision={row.get('decision')!r}")
        if row.get("target_zone") not in TARGET_ZONES:
            errors.append(f"{cid}: unknown target_zone={row.get('target_zone')!r}")
        if row.get("risk_tier") not in RISK_TIERS:
            errors.append(f"{cid}: unknown risk_tier={row.get('risk_tier')!r}")
        if row.get("user_gate") not in USER_GATES:
            errors.append(f"{cid}: unknown user_gate={row.get('user_gate')!r}")
    return rows


def check_results(run_dir: Path, actor_rows: list[dict], expected_cases: int, errors: list[str]) -> list[dict]:
    path = run_dir / "results.jsonl"
    if not path.exists():
        errors.append("missing results.jsonl")
        return []
    rows = load_jsonl(path)
    if len(rows) != expected_cases:
        errors.append(f"results rows={len(rows)} expected={expected_cases}")
    actor_ids = {r.get("case_id") for r in actor_rows}
    result_ids = {r.get("case_id") for r in rows}
    if actor_rows and actor_ids != result_ids:
        errors.append(f"actor/results case_id mismatch: actor_only={sorted(actor_ids - result_ids)[:5]} result_only={sorted(result_ids - actor_ids)[:5]}")
    for row in rows:
        cid = row.get("case_id", "<missing>")
        missing = sorted(RESULT_REQUIRED - row.keys())
        if missing:
            errors.append(f"{cid}: results missing {missing}")
            continue
        scores = row.get("scores") or {}
        if sorted(scores) != sorted(B_WEIGHTS):
            errors.append(f"{cid}: score keys must be {sorted(B_WEIGHTS)}")
            continue
        got = round(float(row.get("weighted")), 1)
        want = weighted(scores)
        if got != want:
            errors.append(f"{cid}: weighted={got} expected={want}")
        if row.get("decision") not in DECISIONS:
            errors.append(f"{cid}: results unknown decision={row.get('decision')!r}")
        if row.get("target_zone") not in TARGET_ZONES:
            errors.append(f"{cid}: results unknown target_zone={row.get('target_zone')!r}")
        if row.get("risk_tier") not in RISK_TIERS:
            errors.append(f"{cid}: results unknown risk_tier={row.get('risk_tier')!r}")
        if row.get("user_gate") not in USER_GATES:
            errors.append(f"{cid}: results unknown user_gate={row.get('user_gate')!r}")
    return rows


def check_manifest(manifest: dict, result_rows: list[dict], errors: list[str]) -> None:
    if not manifest:
        return
    if manifest.get("type") != "behavior":
        errors.append("manifest.type should be behavior")
    if result_rows:
        want = round(sum(float(r["weighted"]) for r in result_rows) / len(result_rows), 1)
        got = round(float((manifest.get("aggregate") or {}).get("composite")), 1)
        if got != want:
            errors.append(f"manifest composite={got} expected={want}")
        dims = (manifest.get("aggregate") or {}).get("dimensions") or {}
        if len(dims) < 5:
            errors.append("manifest aggregate.dimensions should contain five behavior dimensions")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--expected-cases", type=int, default=100)
    args = parser.parse_args()

    errors: list[str] = []
    if not args.run_dir.exists():
        errors.append(f"run directory does not exist: {args.run_dir}")
    else:
        manifest = load_manifest(args.run_dir, errors)
        actor_rows = check_actor(args.run_dir, args.expected_cases, manifest, errors)
        result_rows = check_results(args.run_dir, actor_rows, args.expected_cases, errors)
        check_manifest(manifest, result_rows, errors)

    if errors:
        print("Eval run lint failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"OK: {args.run_dir} passed eval run lint")
    return 0


if __name__ == "__main__":
    sys.exit(main())
