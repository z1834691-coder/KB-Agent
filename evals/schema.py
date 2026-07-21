#!/usr/bin/env python3
"""Shared schema constants and helpers for KB-Agent eval artifacts.

This module is intentionally standard-library only. JSON Schema files in
`evals/schemas/` are the public contract; this file is the executable contract
used by local harness scripts.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

B_WEIGHTS: dict[str, float] = {"B1": 0.35, "B2": 0.25, "B3": 0.20, "B4": 0.10, "B5": 0.10}

ACTOR_BASE_REQUIRED: set[str] = {
    "case_id",
    "output",
    "decision",
    "target_zone",
    "granularity",
    "freshness_policy",
    "source_grade",
    "risk_tier",
    "risk_flags",
    "confidence",
    "user_gate",
    "pm_transfer_score",
    "impact_scan",
    "task_lifecycle",
    "failure_mode",
    "changelog_note",
    "flywheel_data",
}

ACTOR_V5_REQUIRED: set[str] = ACTOR_BASE_REQUIRED | {
    "artifact_type",
    "applicable_blocks",
    "provenance",
    "gate_detail",
    "candidate_admission",
    "triage_record",
    "required_fields_check",
    "chart_schema",
    "migration_record",
    "theory_caveats",
    "quotation_policy",
    "execution_template",
}

ACTOR_FORBIDDEN: set[str] = {"scores", "weighted", "verdict", "judge_evidence", "expected_action"}

RESULT_REQUIRED: set[str] = {
    "case_id",
    "category",
    "input_ref",
    "input_excerpt",
    "output",
    "scores",
    "weighted",
    "verdict",
    "judge_evidence",
    "decision",
    "target_zone",
    "granularity",
    "freshness_policy",
    "risk_tier",
    "user_gate",
    "failure_mode",
}

MANIFEST_REQUIRED: set[str] = {"run_id", "type", "versions", "inputs", "aggregate", "meta"}

DECISIONS = {
    "accept_main",
    "accept_private",
    "ops_only",
    "candidate",
    "verify",
    "reject",
    "human_review",
    "reject_or_metadata_only",
}

TARGET_ZONES = {
    "AI_PM_core",
    "company_dossier",
    "theory",
    "benchmark",
    "tool_method",
    "source_log",
    "ops_protocol",
    "private_profile",
    "none",
}

USER_GATES = {"none", "notify", "ask_before_write", "block"}

RISK_TIERS = {"low", "medium", "high", "blocking"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{idx}: invalid JSON: {exc}") from exc
        if not isinstance(obj, dict):
            raise ValueError(f"{path.name}:{idx}: row must be a JSON object")
        rows.append(obj)
    return rows


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def weighted(scores: dict[str, Any]) -> float:
    return round(sum(float(scores[k]) * weight for k, weight in B_WEIGHTS.items()), 1)


def normalize_agent_version(raw: Any) -> str:
    text = str(raw or "").lower()
    match = re.search(r"v\d+", text)
    return match.group(0) if match else text


def actor_required_fields(agent_prompt_version: Any) -> set[str]:
    version = normalize_agent_version(agent_prompt_version)
    match = re.search(r"v(\d+)", version)
    if match and int(match.group(1)) >= 5:
        return ACTOR_V5_REQUIRED
    return ACTOR_BASE_REQUIRED


def split_slug(splits: list[str]) -> str:
    return "-".join(split.replace("_", "-") for split in splits)


def case_category(case: dict[str, Any]) -> str:
    return f"{case.get('split', 'unknown')}/{case.get('source_type', 'unknown')}/{case.get('eval_type', 'unknown')}"


def safe_actor_case(case: dict[str, Any]) -> dict[str, Any]:
    """Return only fields an actor may see during blind eval."""
    allowed = [
        "id",
        "title",
        "version",
        "source_type",
        "eval_type",
        "capability_tags",
        "source_urls",
        "accessed_at",
        "snapshot_policy",
        "realness",
        "difficulty",
        "difficulty_vector",
        "split",
        "actor_input_summary",
    ]
    return {key: case.get(key) for key in allowed if key in case}
