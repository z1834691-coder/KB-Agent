#!/usr/bin/env python3
"""Summarize a KB-Agent eval run for data-driven prompt iteration."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def avg(items: list[float]) -> float:
    return round(sum(items) / len(items), 2) if items else 0.0


def grouped(rows: list[dict], index: int) -> list[tuple[str, float, int]]:
    groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        parts = str(row.get("category", "")).split("/")
        key = parts[index] if len(parts) > index else "unknown"
        groups[key].append(float(row["weighted"]))
    return sorted((key, avg(vals), len(vals)) for key, vals in groups.items())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--lowest", type=int, default=10)
    parser.add_argument("--highest", type=int, default=5)
    args = parser.parse_args()

    manifest = json.loads((args.run_dir / "manifest.json").read_text(encoding="utf-8"))
    rows = load_jsonl(args.run_dir / "results.jsonl")
    print(f"# {manifest['run_id']}")
    print(f"composite: {(manifest.get('aggregate') or {}).get('composite')}")
    print(f"dimensions: {json.dumps((manifest.get('aggregate') or {}).get('dimensions', {}), ensure_ascii=False)}")
    print(f"verdict_counts: {dict(Counter(row.get('verdict') for row in rows))}")
    print(f"decision_counts: {dict(Counter(row.get('decision') for row in rows))}")
    print(f"by_split: {grouped(rows, 0)}")
    print(f"by_source: {grouped(rows, 1)}")
    print(f"by_eval: {grouped(rows, 2)}")
    print("lowest:")
    for row in sorted(rows, key=lambda r: float(r["weighted"]))[: args.lowest]:
        print(f"- {row['case_id']} {row['weighted']} {row.get('category')} :: {row.get('judge_evidence', '')[:220]}")
    print("highest:")
    for row in sorted(rows, key=lambda r: float(r["weighted"]), reverse=True)[: args.highest]:
        print(f"- {row['case_id']} {row['weighted']} {row.get('category')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
