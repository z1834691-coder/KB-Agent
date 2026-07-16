#!/usr/bin/env python3
"""Lightweight protocol lint for KB-Agent harness docs."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "protocols/01-context-protocol.md": [
        "固定必读",
        "禁止一次性读取完整知识库",
        "最大泛化的最短程序",
        "70-80%",
        "80-90%",
        "> 90%",
        "Run Context Packet",
    ],
    "protocols/02-tool-protocol.md": [
        "Claude API 支持 tool use",
        "T0 只读观察",
        "T4 高风险工具",
        "禁止工具行为",
        "需要后续补的工具",
    ],
    "protocols/03-human-review-protocol.md": [
        "用户已确认参与的环节",
        "H0",
        "H4",
        "必须问用户的触发条件",
        "第一轮 baseline 大改协议",
        "用户的覆写是最高价值数据",
    ],
    "evals/failure-patterns.md": [
        "F-001",
        "F-010",
        "固定必读",
    ],
    "evals/protocol-compliance-checklist.md": [
        "Context",
        "Tools",
        "Human Review",
        "Eval",
    ],
}


def main() -> int:
    errors: list[str] = []
    for rel, needles in REQUIRED.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing phrase {needle!r}")

    if errors:
        print("Protocol lint failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("OK: protocol docs contain required guardrails")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
