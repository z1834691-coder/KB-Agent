#!/usr/bin/env python3
"""Prepare and validate blind behavior eval runs.

This runner deliberately separates deterministic harness work from model
execution. It can prepare blind actor/judge task packets and validate completed
artifacts. The actual actor and judge passes must run in isolated Codex/Claude
sessions, or through a future adapter that preserves the same file boundaries.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from schema import case_category, load_jsonl, normalize_agent_version, safe_actor_case, split_slug, write_json, write_jsonl

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
DATASET = EVALS / "02-challenge-dataset-v0.4.jsonl"
RUNS = EVALS / "runs"
RUBRIC = EVALS / "03-rubric-v2.0.md"
ACTOR_PACK = EVALS / "02-challenge-dataset-v0.4-actor-pack.md"
GOLD = EVALS / "02-challenge-dataset-v0.4-gold.md"
TZ = timezone(timedelta(hours=8))


def load_dataset(path: Path = DATASET) -> list[dict[str, Any]]:
    return load_jsonl(path)


def dataset_display(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def expand_splits(raw: str) -> list[str]:
    parts = [part.strip().lower().replace("_", "-") for part in raw.split(",") if part.strip()]
    if not parts:
        raise ValueError("--split cannot be empty")
    if "dev" in parts:
        parts = [p for p in parts if p != "dev"] + ["smoke", "regression"]
    return list(dict.fromkeys(parts))


def select_cases(cases: list[dict[str, Any]], splits: list[str]) -> list[dict[str, Any]]:
    if "all" in splits or "full" in splits:
        return cases
    selected = []
    wanted = {"full" if split == "full-only" else split for split in splits}
    for case in cases:
        if str(case.get("split", "")).lower() in wanted:
            selected.append(case)
    return selected


def next_run_number(runs_root: Path) -> int:
    current = 0
    if not runs_root.exists():
        return 0
    for path in runs_root.iterdir():
        match = re.search(r"run(\d+)", path.name)
        if match:
            current = max(current, int(match.group(1)))
    return current + 1


def default_run_id(actor: str, splits: list[str], runs_root: Path) -> str:
    today = datetime.now(TZ).date().isoformat()
    actor_version = normalize_agent_version(actor).replace("v", "v")
    return f"{today}-run{next_run_number(runs_root):03d}-behavior-{split_slug(splits)}-{actor_version}-blind"


def actor_task_text(run_id: str, actor: str, selected: list[dict[str, Any]]) -> str:
    safe_rows = [safe_actor_case(case) for case in selected]
    case_lines = "\n".join(json.dumps(row, ensure_ascii=False) for row in safe_rows)
    return f"""# Blind Actor Task: {run_id}

你是被测 actor。请严格按照 `{actor}` prompt 执行行为评测。

## 可读文件

- `evals/prompts/{actor}.md`
- `evals/02-challenge-dataset-v0.4-actor-pack.md`
- `README.md`
- `DECISIONS.md`
- `protocols/*.md`
- `evals/03-rubric-v2.0.md`
- `evals/failure-patterns.md`

## 禁止读取

- `evals/02-challenge-dataset-v0.4-gold.md`
- `evals/02-challenge-dataset-v0.4.jsonl`
- `evals/runs/*`
- `evals/run_v1_eval.py`
- `evals/run_v2_eval.py`
- 任何包含 JUDGE、results、expected_action、gold、score、override 的材料

## 输出位置

只写：

```text
evals/runs/{run_id}/actor-output.jsonl
```

每行一个 JSON object。不得包含 `scores`、`weighted`、`verdict`、
`judge_evidence`、`expected_action`。

## Case Pack

下面是 actor 可见字段，已移除答案与 judge 字段：

```jsonl
{case_lines}
```
"""


def judge_task_text(run_id: str, selected: list[dict[str, Any]]) -> str:
    case_ids = ", ".join(case["id"] for case in selected)
    return f"""# Independent Judge Task: {run_id}

你是独立 judge。请读取 actor-output、gold、JSONL、rubric 与校准集后评分。

## 可读文件

- `evals/runs/{run_id}/actor-output.jsonl`
- `evals/02-challenge-dataset-v0.4-gold.md`
- `evals/02-challenge-dataset-v0.4.jsonl`
- `evals/03-rubric-v2.0.md`
- `evals/judge-calibration-set.md`

## 禁止事项

- 不得修改 `actor-output.jsonl`
- 不得使用 `evals/run_v1_eval.py` 或 `evals/run_v2_eval.py` 的 hard-coded OVERRIDES
- 不得把 holdout 单题答案写进 prompt 建议

## 必写文件

```text
evals/runs/{run_id}/manifest.json
evals/runs/{run_id}/results.jsonl
evals/runs/{run_id}/report.md
```

## Case IDs

{case_ids}
"""


def prepare(args: argparse.Namespace) -> int:
    splits = expand_splits(args.split)
    dataset_path = Path(args.dataset).expanduser().resolve()
    if not dataset_path.exists():
        print(f"Dataset not found: {dataset_path}", file=sys.stderr)
        print("The full gold dataset is private; pass --dataset examples/sample-challenge.jsonl for a demo run.", file=sys.stderr)
        return 1
    cases = select_cases(load_dataset(dataset_path), splits)
    if not cases:
        print(f"No cases selected for split={args.split}", file=sys.stderr)
        return 1

    runs_root = Path(args.runs_root).resolve()
    run_id = args.run_id or default_run_id(args.actor, splits, runs_root)
    run_dir = runs_root / run_id
    if run_dir.exists() and not args.force:
        print(f"Run directory already exists: {run_dir}", file=sys.stderr)
        print("Use --force only if you intend to overwrite task packet files.", file=sys.stderr)
        return 1
    run_dir.mkdir(parents=True, exist_ok=True)

    actor_task = actor_task_text(run_id, args.actor, cases)
    judge_task = judge_task_text(run_id, cases)
    safe_cases = [safe_actor_case(case) for case in cases]
    config = {
        "schema_version": "kb-agent.blind-run-config.v1",
        "run_id": run_id,
        "created_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "actor_prompt": args.actor,
        "dataset": dataset_display(dataset_path),
        "rubric": str(RUBRIC.relative_to(ROOT)),
        "splits_requested": splits,
        "case_count": len(cases),
        "case_ids": [case["id"] for case in cases],
        "blind_boundaries": {
            "actor_allowed": [
                f"evals/prompts/{args.actor}.md",
                str(ACTOR_PACK.relative_to(ROOT)),
                "README.md",
                "DECISIONS.md",
                "protocols/*.md",
                str(RUBRIC.relative_to(ROOT)),
                "evals/failure-patterns.md"
            ],
            "actor_forbidden": [
                str(GOLD.relative_to(ROOT)),
                str(DATASET.relative_to(ROOT)),
                "evals/runs/*",
                "evals/run_v1_eval.py",
                "evals/run_v2_eval.py",
                "JUDGE/results/expected_action/gold/score/override materials"
            ],
            "judge_writes": ["manifest.json", "results.jsonl", "report.md"]
        }
    }

    (run_dir / "actor-task.md").write_text(actor_task, encoding="utf-8")
    (run_dir / "judge-task.md").write_text(judge_task, encoding="utf-8")
    write_json(run_dir / "run_config.json", config)
    write_jsonl(run_dir / "actor-visible-cases.jsonl", safe_cases)
    print(f"Prepared blind eval packet: {run_dir}")
    print(f"Cases: {len(cases)}")
    print("Next: run actor in an isolated session, then run judge in a separate isolated session.")
    return 0


def expected_cases(run_dir: Path) -> int:
    config = run_dir / "run_config.json"
    if config.exists():
        return int(json.loads(config.read_text(encoding="utf-8"))["case_count"])
    manifest = run_dir / "manifest.json"
    if manifest.exists():
        obj = json.loads(manifest.read_text(encoding="utf-8"))
        return int((obj.get("inputs") or {}).get("case_count") or 0)
    actor = run_dir / "actor-output.jsonl"
    if actor.exists():
        return len(load_jsonl(actor))
    return 0


def run_command(cmd: list[str], capture: bool = True) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=capture, check=False)
    output = ""
    if capture:
        output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def validate(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not run_dir.exists():
        print(f"Run directory does not exist: {run_dir}", file=sys.stderr)
        return 1
    cases = args.expected_cases if args.expected_cases is not None else expected_cases(run_dir)
    if not cases:
        print("Could not infer expected case count. Pass --expected-cases.", file=sys.stderr)
        return 1

    checks = [
        ("eval lint", [sys.executable, str(EVALS / "lint_eval_run.py"), str(run_dir), "--expected-cases", str(cases)]),
        ("summary", [sys.executable, str(EVALS / "summarize_eval_run.py"), str(run_dir)]),
        ("dashboard", [sys.executable, str(ROOT / "visualizer" / "build.py")]),
        ("protocol lint", [sys.executable, str(ROOT / "visualizer" / "protocol_lint.py")]),
    ]
    report_lines = [f"# Runner Validation: {run_dir.name}", ""]
    failed = False
    for label, cmd in checks:
        code, output = run_command(cmd)
        status = "OK" if code == 0 else "FAIL"
        print(f"{status}: {label}")
        if output.strip():
            print(output.strip())
        report_lines.extend([f"## {label}", "", f"status: {status}", "", "```text", output.strip(), "```", ""])
        if code != 0:
            failed = True
            if not args.keep_going:
                break
    if args.write_report:
        (run_dir / "runner-validation.md").write_text("\n".join(report_lines).rstrip() + "\n", encoding="utf-8")
        print(f"Wrote {run_dir / 'runner-validation.md'}")
    return 1 if failed else 0


def status(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    files = ["run_config.json", "actor-task.md", "judge-task.md", "actor-output.jsonl", "manifest.json", "results.jsonl", "report.md"]
    print(f"# {run_dir}")
    for name in files:
        print(f"{'OK' if (run_dir / name).exists() else 'MISSING'} {name}")
    inferred = expected_cases(run_dir) if run_dir.exists() else 0
    print(f"expected_cases={inferred or 'unknown'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare", help="create a blind actor/judge task packet")
    p_prepare.add_argument("--actor", required=True, help="prompt version, for example agent-v5")
    p_prepare.add_argument("--split", default="smoke,regression", help="comma list: smoke,regression,holdout,dev,full,full-only,all")
    p_prepare.add_argument("--dataset", default=str(DATASET), help="path to a challenge dataset jsonl (gold set is private; use examples/sample-challenge.jsonl for a demo)")
    p_prepare.add_argument("--run-id")
    p_prepare.add_argument("--runs-root", default=str(RUNS))
    p_prepare.add_argument("--force", action="store_true")
    p_prepare.set_defaults(func=prepare)

    p_validate = sub.add_parser("validate", help="validate a completed blind run")
    p_validate.add_argument("--run-dir", required=True)
    p_validate.add_argument("--expected-cases", type=int)
    p_validate.add_argument("--keep-going", action="store_true")
    p_validate.add_argument("--write-report", action="store_true")
    p_validate.set_defaults(func=validate)

    p_finalize = sub.add_parser("finalize", help="alias for validate --write-report")
    p_finalize.add_argument("--run-dir", required=True)
    p_finalize.add_argument("--expected-cases", type=int)
    p_finalize.add_argument("--keep-going", action="store_true")
    p_finalize.set_defaults(func=lambda args: validate(argparse.Namespace(**vars(args), write_report=True)))

    p_status = sub.add_parser("status", help="show run packet/artifact status")
    p_status.add_argument("--run-dir", required=True)
    p_status.set_defaults(func=status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
