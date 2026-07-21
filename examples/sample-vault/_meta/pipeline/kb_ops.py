#!/usr/bin/env python3
"""AI knowledge-base operations pipeline.

This script lives inside:
  <vault>/_meta/pipeline/kb_ops.py

It is intentionally stdlib-only so launchd can run it without a project
environment. The pipeline does three jobs:

1. Curator daily light run: inspect inbox + official source deltas, then decide
   whether a library update is worth doing.
2. Doctor weekly deep run: lint structure, wikilinks, freshness, metadata, and
   write a scored Obsidian-readable diagnosis report.
3. Dashboard build: render a static local HTML dashboard from git log,
   changelog, reports, scores, flywheel JSONL, source states, and file links.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


TZ = timezone(timedelta(hours=8))
SCRIPT = Path(__file__).resolve()
VAULT = SCRIPT.parents[2]
META = VAULT / "_meta"
REPORTS = META / "reports"
FLYWHEEL = META / "flywheel"
STATE = META / "state"
DASHBOARD = META / "dashboard"
SOURCES = META / "sources"
INBOX = META / "inbox"
SOP = META / "sop"
LOGS = META / "logs"

BRIEFING_DIR = VAULT.parent / "AI-HOT早报"  # 主动信息管线：外部每日早报目录

REQUIRED_FRONTMATTER = [
    "title",
    "type",
    "tags",
    "status",
    "last_reviewed",
    "maintainer",
    "related",
]

DOCTOR_WEIGHTS = {
    "D1 结构与导航": 0.25,
    "D2 内容覆盖": 0.25,
    "D3 时效与事实纪律": 0.15,
    "D4 元数据规范": 0.05,
    "D5 可面试/可行动性": 0.25,
    "D6 自动化与飞轮": 0.05,
}


def now() -> datetime:
    return datetime.now(TZ)


def today() -> str:
    return now().date().isoformat()


def ensure_dirs() -> None:
    for path in [REPORTS, FLYWHEEL, STATE, DASHBOARD, SOURCES, INBOX, LOGS]:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"_parse_error": line[:200]})
    return rows[-limit:] if limit else rows


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(VAULT))
    except ValueError:
        return str(path)


def as_file_url(path: Path) -> str:
    return path.resolve().as_uri()


def esc(x: Any) -> str:
    return html.escape(str(x))


def git(args: list[str], check: bool = False) -> str:
    proc = subprocess.run(
        ["git", "-C", str(VAULT), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout.strip()


def git_status() -> list[str]:
    out = git(["status", "--short"])
    return [ln for ln in out.splitlines() if ln.strip()]


def git_log(limit: int = 20) -> list[dict[str, str]]:
    out = git(["log", f"-{limit}", "--date=short", "--pretty=format:%h%x09%ad%x09%s"])
    rows = []
    for line in out.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            rows.append({"hash": parts[0], "date": parts[1], "subject": parts[2]})
    return rows


def latest_commit() -> str:
    return git(["rev-parse", "--short", "HEAD"]) or "unknown"


def content_docs() -> list[Path]:
    docs: list[Path] = []
    for path in VAULT.rglob("*.md"):
        rp = rel(path)
        if rp.startswith(".obsidian/"):
            continue
        if rp.startswith("_meta/archive/"):
            continue
        if rp.startswith("_meta/dashboard/"):
            continue
        docs.append(path)
    return sorted(docs)


def knowledge_docs() -> list[Path]:
    docs = []
    for path in VAULT.glob("*.md"):
        if path.name.startswith("."):
            continue
        docs.append(path)
    dossiers = sorted((VAULT / "company-dossiers").glob("*.md"))
    return sorted(docs) + dossiers


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip("\n")
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, body


def wikilink_missing(files: list[Path]) -> list[dict[str, str]]:
    all_files = list(VAULT.rglob("*.md"))
    stems = {p.stem: p for p in all_files}
    rel_no_ext = {rel(p).removesuffix(".md"): p for p in all_files}
    missing: list[dict[str, str]] = []
    for path in files:
        text = read_text(path)
        for raw in re.findall(r"\[\[([^\]]+)\]\]", text):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            ok = target in stems or target in rel_no_ext or (VAULT / f"{target}.md").exists()
            if not ok:
                missing.append({"file": rel(path), "target": raw})
    return missing


def frontmatter_issues(files: list[Path]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for path in files:
        fm, _ = parse_frontmatter(read_text(path))
        if not fm:
            issues.append({"file": rel(path), "issue": "missing_frontmatter"})
            continue
        missing = [key for key in REQUIRED_FRONTMATTER if not fm.get(key)]
        if missing:
            issues.append({"file": rel(path), "issue": "missing_keys", "keys": missing})
        if fm.get("type") in {"product_version_data", "news_dynamic"} and not fm.get("stale_after"):
            issues.append({"file": rel(path), "issue": "missing_stale_after"})
    return issues


def stale_docs(files: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    today_date = now().date()
    for path in files:
        fm, _ = parse_frontmatter(read_text(path))
        raw = fm.get("stale_after")
        if not raw or raw in {"无", "none", "None"}:
            continue
        try:
            stale_date = date.fromisoformat(raw[:10])
        except ValueError:
            rows.append({"file": rel(path), "stale_after": raw, "status": "invalid_date"})
            continue
        days = (stale_date - today_date).days
        if days < 0:
            rows.append({"file": rel(path), "stale_after": raw, "status": "expired"})
        elif days <= 7:
            rows.append({"file": rel(path), "stale_after": raw, "status": "due_soon"})
    return rows


COMPANY_VOLATILE_WINDOW_DAYS = 14  # 公司档案的融资/估值/股价/MAU/模型版本变化快


def volatile_review_due(window_days: int = COMPANY_VOLATILE_WINDOW_DAYS) -> list[dict[str, Any]]:
    """公司档案的快变事实（IPO/估值/股价/融资/MAU/模型版本）过期最隐蔽。

    document-level `stale_after` 常被设在一个月外，抓不到这类字段级过期——这正是
    2026-07 三家公司 IPO 被静默错标"待核"的根因。这里专门对 company-dossiers 用更短的
    volatile window，按 `volatile_review`（无则回退 `last_reviewed`）判定是否该重新核验
    快变事实，并进 Doctor 报告与 curator 决策，避免"看着不 stale 其实早已过时"。
    """
    rows: list[dict[str, Any]] = []
    today_date = now().date()
    for path in sorted((VAULT / "company-dossiers").glob("*.md")):
        if path.name.startswith("00-"):
            continue
        fm, _ = parse_frontmatter(read_text(path))
        raw = (fm.get("volatile_review") or fm.get("last_reviewed") or "")[:10]
        try:
            reviewed = date.fromisoformat(raw)
        except ValueError:
            rows.append({"file": rel(path), "reviewed": raw or "unknown", "age_days": None, "status": "no_date"})
            continue
        age = (today_date - reviewed).days
        if age >= window_days:
            rows.append({"file": rel(path), "reviewed": raw, "age_days": age, "status": "volatile_due"})
    return rows


def company_coverage() -> dict[str, Any]:
    expected = {
        "DeepSeek": "company-dossiers/DeepSeek.md",
        "StepFun": "company-dossiers/StepFun.md",
        "Alibaba": "company-dossiers/Alibaba.md",
        "Bytedance": "company-dossiers/Bytedance.md",
        "MiniMax": "company-dossiers/MiniMax.md",
        "Moonshot": "company-dossiers/Moonshot.md",
        "Zhipu": "company-dossiers/Zhipu.md",
    }
    missing = [name for name, p in expected.items() if not (VAULT / p).exists()]
    return {"expected": len(expected), "present": len(expected) - len(missing), "missing": missing}


def section_presence(path: Path, patterns: list[str]) -> bool:
    text = read_text(path)
    return all(re.search(pattern, text, re.M) for pattern in patterns)


def actionability_score() -> tuple[float, list[str]]:
    """MECHANICAL proxy only — hard-capped at 7.0.

    Honesty fix (2026-07-16): the old version returned 10.0 whenever every
    dossier merely *contained the heading string* "AI PM 面试角度". That is the
    Goodhart bug that inflated D5 to 10/10 even for half-depth dossiers. True
    interview-readiness is a quality judgment that needs an LLM/human judge, so
    here we (1) require a real interview block (heading AND Q&A structure), and
    (2) cap the auto-score at 7.0 — no mechanical run may claim full quality.
    """
    # 只算真正的公司档案；排除框架/索引文件（00-横向对比矩阵、01-面试题库 等数字前缀）
    files = [p for p in sorted((VAULT / "company-dossiers").glob("*.md")) if not p.name[0].isdigit()]
    missing = []
    for path in files:
        text = read_text(path)
        has_heading = any(m in text for m in ["AI PM 面试角度", "AI PM 面试视角", "面试角度", "面试视角"])
        has_qa = any(m in text for m in ["一句话答", "高频题", "追问", "面试题"])
        if not (has_heading and has_qa):
            missing.append(rel(path))
    if not files:
        return 4.0, missing
    score = max(3.0, 7.0 - len(missing) * 1.5)  # ceiling 7.0, not 10.0
    return score, missing


def dossier_depth_stats() -> tuple[float, list[str]]:
    """Line-count parity across company dossiers. Under-depth = < 60% of median.

    Feeds an honesty penalty into D2 so "all 7 dossiers exist" cannot hide the
    fact that some are half the depth of the rest.
    """
    files = [p for p in sorted((VAULT / "company-dossiers").glob("*.md")) if not p.name[0].isdigit()]
    lengths = [len(read_text(p).splitlines()) for p in files]
    if not lengths:
        return 0.0, []
    ordered = sorted(lengths)
    n = len(ordered)
    median = float(ordered[n // 2]) if n % 2 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2
    threshold = median * 0.6
    under = [rel(p) for p, ln in zip(files, lengths) if ln < threshold]
    return median, under


def source_manifest() -> list[dict[str, Any]]:
    data = read_json(SOURCES / "official-sources.json", {"sources": []})
    return data.get("sources", []) if isinstance(data, dict) else []


def fetch_url(url: str, timeout: int = 20) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "KB-Agent Curator/1.0 (+local vault maintenance)",
            "Accept": "text/html,application/json,text/plain;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read(500_000)
        text = raw.decode("utf-8", "ignore")
        digest = hashlib.sha256(raw).hexdigest()
        title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
        return {
            "ok": True,
            "status": getattr(resp, "status", None),
            "hash": digest,
            "bytes": len(raw),
            "title": title[:160],
        }


def check_sources(fetch: bool) -> dict[str, Any]:
    ensure_dirs()
    sources = source_manifest()
    state_path = STATE / "source_snapshots.json"
    previous = read_json(state_path, {})
    next_state = dict(previous)
    changed = []
    errors = []
    checked = []
    for source in sources:
        sid = source.get("id") or source.get("url")
        url = source.get("url")
        if not url:
            continue
        row = {
            "id": sid,
            "name": source.get("name", sid),
            "url": url,
            "tier": source.get("tier", ""),
            "checked_at": now().isoformat(timespec="seconds"),
        }
        if fetch:
            try:
                result = fetch_url(url)
                old_hash = (previous.get(sid) or {}).get("hash")
                row.update(result)
                row["changed"] = bool(old_hash and old_hash != result["hash"])
                row["first_seen"] = not bool(old_hash)
                if row["changed"]:
                    changed.append(row)
                next_state[sid] = row
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                row.update({"ok": False, "error": str(exc)[:220], "changed": False})
                errors.append(row)
                next_state[sid] = {**(previous.get(sid) or {}), **row}
        else:
            old = previous.get(sid) or {}
            row.update({
                "ok": old.get("ok"),
                "hash": old.get("hash"),
                "title": old.get("title"),
                "changed": False,
                "first_seen": not bool(old),
                "not_fetched": True,
            })
        checked.append(row)
    if fetch:
        write_text(state_path, json.dumps(next_state, ensure_ascii=False, indent=2, sort_keys=True))
    return {"checked": checked, "changed": changed, "errors": errors, "fetch": fetch}


def briefing_deltas() -> dict[str, Any]:
    """主动信息管线（N6）：扫描外部 AI-HOT早报 目录，检出上次基线以来的新简报，作为
    候选信号（**不自动入库**，走 candidate_review）。解决 L1 教训#5"用户是唯一信息泵"。

    首次运行建立基线（记录当前全部早报的 hash，report 0 new），此后只报真正新增的简报，
    直到 curator 把它们处理成候选包时才更新基线（避免未经处理就标记已读）。
    """
    state_path = STATE / "briefing_state.json"
    prev = read_json(state_path, None)
    curr: dict[str, str] = {}
    files = sorted(BRIEFING_DIR.glob("*.md")) if BRIEFING_DIR.exists() else []
    for p in files:
        try:
            curr[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
        except OSError:
            continue
    if prev is None:
        STATE.mkdir(parents=True, exist_ok=True)
        write_text(state_path, json.dumps(curr, ensure_ascii=False, indent=2, sort_keys=True))
        return {"available": BRIEFING_DIR.exists(), "dir": str(BRIEFING_DIR),
                "baseline_initialized": True, "new": [], "new_count": 0, "known": len(curr)}
    new = [{"file": n, "sha12": h} for n, h in curr.items() if prev.get(n) != h]
    new.sort(key=lambda r: r["file"], reverse=True)
    return {"available": BRIEFING_DIR.exists(), "dir": str(BRIEFING_DIR),
            "baseline_initialized": False, "new": new[:15], "new_count": len(new), "known": len(curr)}


def inbox_items() -> list[dict[str, Any]]:
    INBOX.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(INBOX.glob("*")):
        if path.name.startswith(".") or path.name == "README.md" or path.is_dir():
            continue
        if path.suffix.lower() not in {".md", ".txt", ".json", ".jsonl"}:
            continue
        text = read_text(path)
        rows.append({
            "file": rel(path),
            "bytes": path.stat().st_size,
            "lines": len(text.splitlines()),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })
    return rows


def days_since_latest_score() -> int | None:
    rows = read_jsonl(FLYWHEEL / "score-timeseries.jsonl")
    if not rows:
        return None
    dates = []
    for row in rows:
        raw = str(row.get("date") or "")[:10]
        try:
            dates.append(date.fromisoformat(raw))
        except ValueError:
            pass
    if not dates:
        return None
    return (now().date() - max(dates)).days


def doctor_due() -> bool:
    delta = days_since_latest_score()
    return delta is None or delta >= 7


def run_checks(fetch: bool = False) -> dict[str, Any]:
    docs = knowledge_docs()
    all_md = content_docs()
    source = check_sources(fetch=fetch)
    fm_issues = frontmatter_issues(docs)
    # Doctor D1 focuses on user-facing knowledge objects. Historical reports and
    # SOP examples may intentionally contain placeholder wikilinks such as
    # [[双链]]; those should not drag down the live vault score.
    missing_links = wikilink_missing(docs)
    stale = stale_docs(docs)
    coverage = company_coverage()
    action_score, action_missing = actionability_score()
    volatile_due = volatile_review_due()
    dirty = git_status()
    inbox = inbox_items()
    briefings = briefing_deltas()
    automation_files = [
        META / "pipeline/kb_ops.py",
        META / "automation/launchd/com.kb-agent.curator.plist",
        META / "automation/launchd/com.kb-agent.doctor.plist",
        META / "dashboard/index.html",
        FLYWHEEL / "run-events.jsonl",
    ]
    automation_present = [rel(p) for p in automation_files if p.exists()]
    return {
        "generated_at": now().isoformat(timespec="seconds"),
        "commit": latest_commit(),
        "doc_count": len(docs),
        "all_md_count": len(all_md),
        "frontmatter_issues": fm_issues,
        "missing_links": missing_links,
        "stale_docs": stale,
        "company_coverage": coverage,
        "actionability": {"score": action_score, "missing_ai_pm_sections": action_missing},
        "volatile_review_due": volatile_due,
        "dirty_status": dirty,
        "inbox": inbox,
        "briefings": briefings,
        "sources": source,
        "doctor_due": doctor_due(),
        "automation_present": automation_present,
    }


def decide_library_action(checks: dict[str, Any]) -> dict[str, Any]:
    reasons = []
    depth = "none"
    action = "no_library_update"
    if checks["frontmatter_issues"] or checks["missing_links"]:
        depth = "deep"
        action = "repair_required"
        reasons.append("metadata_or_link_breakage")
    if any(row["status"] == "expired" for row in checks["stale_docs"]):
        depth = "deep"
        action = "refresh_required"
        reasons.append("expired_docs")
    if checks["sources"]["changed"] or checks["inbox"]:
        if depth == "none":
            depth = "light"
            action = "candidate_review_required"
        reasons.append("new_source_or_inbox_delta")
    if checks.get("volatile_review_due"):
        if depth == "none":
            depth = "light"
            action = "candidate_review_required"
        reasons.append("company_volatile_facts_due")
    if (checks.get("briefings") or {}).get("new_count"):
        if depth == "none":
            depth = "light"
            action = "candidate_review_required"
        reasons.append("new_briefing_delta")
    if checks["doctor_due"]:
        reasons.append("doctor_due")
    if checks["dirty_status"]:
        reasons.append("manual_edit_signal_dirty_git")
    if not reasons:
        reasons.append("no_material_signal")
    return {
        "action": action,
        "depth": depth,
        "reasons": reasons,
        "should_touch_main_library": action in {"repair_required", "refresh_required"},
    }


def render_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "<p class='muted'>暂无</p>"
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def curator_report(checks: dict[str, Any], decision: dict[str, Any]) -> Path:
    path = REPORTS / f"{today()}-curator-light.md"
    changed_rows = []
    for row in checks["sources"]["changed"]:
        changed_rows.append(f"- `{row['id']}`：{row.get('name')} · {row.get('url')}")
    inbox_rows = [f"- `{item['file']}` · {item['lines']} lines · `{item['sha256'][:12]}`" for item in checks["inbox"]]
    errors = [f"- `{row['id']}`：{row.get('error')}" for row in checks["sources"]["errors"]]
    report = f"""\
---
title: "Curator Daily Light Run · {today()}"
type: run_report
tags: [meta, curator, automation]
status: active
created: {today()}
last_reviewed: {today()}
maintainer: KB-Agent
related: ["[[00-框架总览]]", "[[16-前沿快报]]", "[[11-模型版图与选型]]"]
---

# Curator Daily Light Run · {today()}

> **run_id**：`curator-{now().strftime('%Y%m%d-%H%M%S')}`  
> **commit**：`{checks['commit']}`  
> **fetch_official_sources**：`{checks['sources']['fetch']}`  
> **自主决策**：`{decision['action']}` / depth = `{decision['depth']}`  

## 1. 本次是否值得动库？

**结论**：{'需要进入更新/修复队列' if decision['action'] != 'no_library_update' else '不动主库，只记录心跳与信号'}。

**理由**：{', '.join(decision['reasons'])}

## 2. 官方源增量

{chr(10).join(changed_rows) if changed_rows else '- 未检测到官方源 hash 变化，或本次未启用 fetch。'}

## 3. Inbox / 早报

{chr(10).join(inbox_rows) if inbox_rows else '- `_meta/inbox/` 暂无待消化早报或候选资料。'}

### 3.1 主动信息管线 · AI-HOT早报增量（N6）

{briefing_report_lines(checks.get('briefings') or {})}

## 4. 异常

{chr(10).join(errors) if errors else '- 无 fetch 异常。'}

## 5. 结构健康快照

- frontmatter issues：{len(checks['frontmatter_issues'])}
- wikilink missing：{len(checks['missing_links'])}
- stale / due-soon docs：{len(checks['stale_docs'])}
- git dirty lines：{len(checks['dirty_status'])}

## 6. 下一步

{next_step_for_decision(decision)}
"""
    write_text(path, report)
    return path


def briefing_report_lines(briefings: dict[str, Any]) -> str:
    if not briefings.get("available"):
        return f"- 未找到早报目录 `{briefings.get('dir', '')}`。"
    if briefings.get("baseline_initialized"):
        return f"- 首次运行：已建立早报基线（{briefings.get('known', 0)} 篇），此后只报新增。"
    new = briefings.get("new") or []
    if not new:
        return f"- 已知 {briefings.get('known', 0)} 篇早报，无新增。"
    lines = [f"- **{briefings.get('new_count')} 篇新早报待消化**（不自动入库，走 candidate_review）："]
    lines += [f"  - `{row['file']}`" for row in new]
    return "\n".join(lines)


def next_step_for_decision(decision: dict[str, Any]) -> str:
    action = decision["action"]
    if action == "no_library_update":
        return "- 维持主库不变；dashboard 与 flywheel 记录本次心跳。"
    if action == "candidate_review_required":
        return "- Curator 应先生成候选更新包；若信息价值足够，再交 Actor 写入主库，Doctor 复核。"
    if action == "repair_required":
        return "- 优先修断链/frontmatter；不要在结构损坏时叠加内容更新。"
    if action == "refresh_required":
        return "- 优先刷新过期高价值文档，尤其 `16-前沿快报` 与公司档案。"
    return "- 人工复核决策。"


def score_doctor(checks: dict[str, Any]) -> dict[str, Any]:
    docs = max(checks["doc_count"], 1)
    fm_penalty = min(4.0, len(checks["frontmatter_issues"]) / docs * 20)
    link_penalty = min(5.0, len(checks["missing_links"]) * 0.8)
    expired = sum(1 for row in checks["stale_docs"] if row["status"] == "expired")
    due_soon = sum(1 for row in checks["stale_docs"] if row["status"] == "due_soon")
    coverage = checks["company_coverage"]
    automation_score = min(10.0, 4.0 + len(checks["automation_present"]) * 1.2)

    # HONESTY FIX (2026-07-16): coverage-only D2 hid that some dossiers are
    # half-depth. Penalize under-depth dossiers so "all 7 exist" can't inflate.
    median_lines, under_depth = dossier_depth_stats()
    depth_penalty = min(3.0, len(under_depth) * 1.0)
    d2_coverage = min(10.0, 5.0 + coverage["present"] / max(coverage["expected"], 1) * 4.0 + 0.8)

    dims = {
        "D1 结构与导航": max(0.0, 8.0 - link_penalty - (0.4 if checks["doc_count"] < 26 else 0)),
        "D2 内容覆盖": max(0.0, d2_coverage - depth_penalty),
        "D3 时效与事实纪律": max(0.0, 8.0 - expired * 1.4 - due_soon * 0.35 - min(2.0, len(checks.get("volatile_review_due") or []) * 0.4)),
        "D4 元数据规范": max(0.0, 9.0 - fm_penalty),
        "D5 可面试/可行动性": checks["actionability"]["score"],
        "D6 自动化与飞轮": automation_score,
    }
    composite = sum(dims[k] * DOCTOR_WEIGHTS[k] for k in DOCTOR_WEIGHTS)
    return {
        "dimensions": {k: round(v, 1) for k, v in dims.items()},
        "composite": round(composite, 1),
        "score_type": "mechanical_structural_gate",
        "honesty_note": "机械结构分，非质量分。D2 含 under-depth 惩罚；D5 为封顶机械代理(<=7)；真实可面试性/深度需 LLM 或人工盲评。",
        "under_depth_dossiers": under_depth,
        "median_dossier_lines": median_lines,
        "requires_judge": ["D2 内容覆盖", "D5 可面试/可行动性"],
    }


def doctor_report(checks: dict[str, Any], score: dict[str, Any]) -> Path:
    path = REPORTS / f"{today()}-doctor-weekly.md"
    dims = score["dimensions"]
    rows = "\n".join(
        f"| {name} | {DOCTOR_WEIGHTS[name] * 100:.0f}% | {value:.1f} | {doctor_dim_note(name, value, checks)} |"
        for name, value in dims.items()
    )
    stale_lines = "\n".join(
        f"- `{row['file']}` · {row['status']} · stale_after={row['stale_after']}"
        for row in checks["stale_docs"][:30]
    )
    missing_links = "\n".join(
        f"- `{row['file']}` → `{row['target']}`"
        for row in checks["missing_links"][:30]
    )
    fm_lines = "\n".join(
        f"- `{row['file']}` · {row['issue']} {row.get('keys', '')}"
        for row in checks["frontmatter_issues"][:30]
    )
    report = f"""\
---
title: "Doctor Weekly Deep Check · {today()}"
type: diagnostic_report
tags: [meta, doctor, automation, flywheel]
status: active
created: {today()}
last_reviewed: {today()}
maintainer: KB-Agent
related: ["[[00-框架总览]]", "[[09-评测与Evals]]", "[[16-前沿快报]]"]
---

# Doctor Weekly Deep Check · {today()}

> **commit**：`{checks['commit']}`
> **机械结构分（非质量分）**：**{score['composite']}/10**
> ⚠️ **诚实性声明**：本分是机械结构门分（lint gate），**不代表内容质量**。D2/D5 需 LLM/人工盲评方为真实质量分；under-depth 档案：{', '.join(score.get('under_depth_dossiers') or []) or '无'}。
> **目标**：每周深度体检结构、时效、元数据、双链、自动化飞轮，并把低分项反写到 SOP 队列。

## 1. 维度评分

| 维度 | 权重 | 分数 | 诊断 |
|---|---:|---:|---|
{rows}

## 2. 关键检查

- knowledge docs：{checks['doc_count']}
- all markdown checked：{checks['all_md_count']}
- company dossier coverage：{checks['company_coverage']['present']}/{checks['company_coverage']['expected']}
- frontmatter issues：{len(checks['frontmatter_issues'])}
- wikilink missing：{len(checks['missing_links'])}
- stale/due-soon docs：{len(checks['stale_docs'])}
- dashboard：{'present' if (DASHBOARD / 'index.html').exists() else 'missing'}

## 3. Stale / Due Soon

{stale_lines if stale_lines else '- 暂无过期或 7 天内到期文档。'}

## 4. Wikilink Missing

{missing_links if missing_links else '- 0 断链。'}

## 4.5 公司档案快变事实复核队列（IPO/估值/股价/融资/MAU/模型版本）

{chr(10).join(f"- `{row['file']}` · {row['status']} · last_reviewed={row['reviewed']} · {row['age_days']} 天未复核" for row in checks.get('volatile_review_due') or []) if (checks.get('volatile_review_due')) else f'- 无公司档案超过 {COMPANY_VOLATILE_WINDOW_DAYS} 天未复核快变事实。'}

## 5. Frontmatter Issues

{fm_lines if fm_lines else '- 0 frontmatter blocker。'}

## 6. Doctor → SOP 修正

{low_score_sop_text(score)}

## 7. 结论

当前系统状态：**{'可自动维护，但需继续补横向矩阵与反馈采集' if score['composite'] >= 7 else '可用，但自动化与结构治理仍需优先修复'}**。

下一轮优先级：

1. 过期/临期文档优先于新增内容；
2. 用户手动编辑 diff 优先作为偏好信号；
3. 公司横向矩阵优先于继续扩写单家公司；
4. 每次 Actor 写库后必须跑 Doctor + dashboard。
"""
    write_text(path, report)
    return path


def doctor_dim_note(name: str, value: float, checks: dict[str, Any]) -> str:
    if name == "D1 结构与导航":
        return f"{len(checks['missing_links'])} missing wikilinks"
    if name == "D2 内容覆盖":
        c = checks["company_coverage"]
        return f"company dossiers {c['present']}/{c['expected']}"
    if name == "D3 时效与事实纪律":
        return f"{len(checks['stale_docs'])} stale/due-soon docs"
    if name == "D4 元数据规范":
        return f"{len(checks['frontmatter_issues'])} metadata issues"
    if name == "D5 可面试/可行动性":
        return "AI PM sections present" if not checks["actionability"]["missing_ai_pm_sections"] else "missing AI PM sections"
    if name == "D6 自动化与飞轮":
        return f"{len(checks['automation_present'])} automation artifacts present"
    return ""


def low_score_sop_text(score: dict[str, Any]) -> str:
    low = [(k, v) for k, v in score["dimensions"].items() if v < 7.0]
    if not low:
        return "- 无 <7.0 维度；下一轮保持现有 SOP。"
    lines = []
    for name, value in low:
        lines.append(f"- `{name}` = {value:.1f}：下一轮 Actor/Curator prompt 必须先处理该维度，不得继续扩写低优先级内容。")
    return "\n".join(lines)


def update_sop_queue(score: dict[str, Any]) -> None:
    path = SOP / "SOP-03-automation-loop.md"
    text = read_text(path)
    start = "<!-- AUTO-SOP-QUEUE:START -->"
    end = "<!-- AUTO-SOP-QUEUE:END -->"
    block = f"""{start}
## 自动修正队列（Doctor 自动维护）

更新时间：{now().isoformat(timespec="seconds")}

{low_score_sop_text(score)}

{end}"""
    if start in text and end in text:
        text = re.sub(f"{re.escape(start)}.*?{re.escape(end)}", block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    write_text(path, text)
    for name, value in score["dimensions"].items():
        if value < 7.0:
            append_jsonl(FLYWHEEL / "sop-patches.jsonl", {
                "date": now().isoformat(timespec="seconds"),
                "dimension": name,
                "score": value,
                "rule": "下一轮 Actor/Curator prompt 必须先处理该维度，不得继续扩写低优先级内容。",
                "sop": rel(path),
            })


def record_run(kind: str, checks: dict[str, Any], decision: dict[str, Any] | None = None, score: dict[str, Any] | None = None, report: Path | None = None) -> None:
    row = {
        "date": now().isoformat(timespec="seconds"),
        "kind": kind,
        "commit": checks.get("commit"),
        "decision": decision,
        "score": score,
        "report": rel(report) if report else None,
        "dirty_status_count": len(checks.get("dirty_status") or []),
        "frontmatter_issues": len(checks.get("frontmatter_issues") or []),
        "missing_links": len(checks.get("missing_links") or []),
        "stale_docs": len(checks.get("stale_docs") or []),
    }
    append_jsonl(FLYWHEEL / "run-events.jsonl", row)
    if decision:
        append_jsonl(FLYWHEEL / "candidate-decisions.jsonl", {
            "date": row["date"],
            "kind": kind,
            "action": decision["action"],
            "depth": decision["depth"],
            "reasons": decision["reasons"],
            "should_touch_main_library": decision["should_touch_main_library"],
            "source_changes": [r.get("id") for r in checks["sources"]["changed"]],
            "inbox": [r.get("file") for r in checks["inbox"]],
        })
    if score:
        append_jsonl(FLYWHEEL / "score-timeseries.jsonl", {
            "date": row["date"],
            "kind": kind,
            "commit": checks.get("commit"),
            "composite": score["composite"],
            "dimensions": score["dimensions"],
            "report": rel(report) if report else None,
        })


def render_dashboard(checks: dict[str, Any] | None = None) -> Path:
    ensure_dirs()
    checks = checks or run_checks(fetch=False)
    logs = git_log(18)
    changelog = read_text(META / "CHANGELOG.md")
    reports = sorted(REPORTS.glob("*.md"), key=lambda p: p.name, reverse=True)
    run_events = read_jsonl(FLYWHEEL / "run-events.jsonl", limit=40)
    decisions = read_jsonl(FLYWHEEL / "candidate-decisions.jsonl", limit=40)
    scores = read_jsonl(FLYWHEEL / "score-timeseries.jsonl", limit=40)
    source_state = read_json(STATE / "source_snapshots.json", {})

    latest_score = scores[-1] if scores else None
    score_cards = ""
    if latest_score:
        dim_rows = [
            [esc(k), f"{float(v):.1f}", bar(float(v))]
            for k, v in latest_score.get("dimensions", {}).items()
        ]
        score_cards = f"""
        <div class="card wide">
          <h2>Doctor Score</h2>
          <div class="big">{esc(latest_score.get('composite'))}/10</div>
          {render_table(['Dimension','Score','Bar'], dim_rows)}
        </div>
        """
    else:
        score_cards = "<div class='card wide'><h2>Doctor Score</h2><p class='muted'>暂无分数</p></div>"

    report_rows = [
        [
            f"<a href='{esc(as_file_url(p))}'>{esc(p.name)}</a>",
            esc(datetime.fromtimestamp(p.stat().st_mtime, TZ).strftime("%Y-%m-%d %H:%M")),
        ]
        for p in reports[:14]
    ]
    git_rows = [[f"<code>{esc(r['hash'])}</code>", esc(r["date"]), esc(r["subject"])] for r in logs]
    decision_rows = [
        [
            esc(str(r.get("date", ""))[:19]),
            esc(r.get("action")),
            esc(r.get("depth")),
            esc(", ".join(r.get("reasons") or [])),
        ]
        for r in reversed(decisions[-12:])
    ]
    score_rows = [
        [
            esc(str(r.get("date", ""))[:19]),
            esc(r.get("kind")),
            esc(r.get("composite")),
            f"<a href='{esc(as_file_url(VAULT / r['report']))}'>{esc(r.get('report'))}</a>" if r.get("report") else "",
        ]
        for r in reversed(scores[-12:])
    ]
    source_rows = []
    for sid, row in sorted(source_state.items()):
        source_rows.append([
            esc(sid),
            esc(row.get("name", "")),
            f"<a href='{esc(row.get('url', ''))}'>{esc(row.get('url', ''))}</a>",
            esc(row.get("checked_at", "")),
            esc(row.get("title", "")),
            esc("changed" if row.get("changed") else "stable"),
        ])

    paths = [
        ("Vault root", VAULT),
        ("Dashboard", DASHBOARD / "index.html"),
        ("Changelog", META / "CHANGELOG.md"),
        ("Reports", REPORTS),
        ("Flywheel", FLYWHEEL),
        ("Inbox", INBOX),
        ("Pipeline", META / "pipeline/kb_ops.py"),
        ("LaunchAgents", META / "automation/launchd"),
    ]
    path_rows = [[esc(name), f"<a href='{esc(as_file_url(path))}'>{esc(str(path))}</a>"] for name, path in paths]
    changelog_excerpt = "\n".join(changelog.splitlines()[:80])

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 知识库 Harness Dashboard</title>
  <style>
    :root {{
      --bg:#f6f7f9; --panel:#ffffff; --text:#17202a; --muted:#667085;
      --line:#d8dee8; --accent:#1f7a8c; --accent2:#b7791f; --bad:#b42318;
      --good:#16803c; --code:#eef2f6;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--text); background:var(--bg); }}
    header {{ position:sticky; top:0; z-index:5; background:rgba(255,255,255,.94); border-bottom:1px solid var(--line); backdrop-filter: blur(8px); }}
    .top {{ max-width:1280px; margin:0 auto; padding:14px 20px 10px; display:flex; gap:16px; align-items:center; justify-content:space-between; }}
    h1 {{ margin:0; font-size:20px; font-weight:720; letter-spacing:0; }}
    nav {{ display:flex; flex-wrap:wrap; gap:6px; }}
    nav a {{ color:var(--text); text-decoration:none; border:1px solid var(--line); padding:6px 10px; border-radius:6px; background:#fff; }}
    main {{ max-width:1280px; margin:0 auto; padding:18px 20px 40px; }}
    section {{ margin:18px 0 28px; }}
    h2 {{ font-size:16px; margin:0 0 10px; }}
    h3 {{ font-size:14px; margin:10px 0 8px; }}
    .grid {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }}
    .card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px; min-height:112px; }}
    .wide {{ grid-column:span 2; }}
    .full {{ grid-column:1/-1; }}
    .big {{ font-size:34px; font-weight:760; margin:8px 0; color:var(--accent); }}
    .muted {{ color:var(--muted); }}
    .pill {{ display:inline-block; border:1px solid var(--line); border-radius:999px; padding:3px 8px; background:#fff; margin:2px 4px 2px 0; }}
    .ok {{ color:var(--good); }} .warn {{ color:var(--accent2); }} .bad {{ color:var(--bad); }}
    table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
    th,td {{ text-align:left; vertical-align:top; border-bottom:1px solid var(--line); padding:8px 10px; }}
    th {{ background:#f0f3f7; font-size:12px; color:#344054; }}
    tr:last-child td {{ border-bottom:0; }}
    code {{ background:var(--code); padding:1px 4px; border-radius:4px; }}
    a {{ color:#0b6575; }}
    .barwrap {{ width:100%; height:10px; background:#eef2f6; border-radius:999px; overflow:hidden; }}
    .bar {{ height:10px; background:linear-gradient(90deg,var(--accent),#2f9e44); }}
    pre {{ white-space:pre-wrap; background:#101828; color:#f2f4f7; border-radius:8px; padding:12px; overflow:auto; }}
    @media (max-width:900px) {{ .grid {{ grid-template-columns:1fr 1fr; }} .wide {{ grid-column:1/-1; }} }}
    @media (max-width:640px) {{ .grid {{ grid-template-columns:1fr; }} .top {{ align-items:flex-start; flex-direction:column; }} }}
  </style>
</head>
<body>
<header>
  <div class="top">
    <div>
      <h1>AI 知识库 Harness Dashboard</h1>
      <div class="muted">generated {esc(checks['generated_at'])} · commit <code>{esc(checks['commit'])}</code></div>
    </div>
    <nav>
      <a href="#overview">Overview</a><a href="#doctor">Doctor</a><a href="#reports">Reports</a>
      <a href="#flywheel">Flywheel</a><a href="#sources">Sources</a><a href="#paths">Paths</a>
    </nav>
  </div>
</header>
<main>
  <section id="overview">
    <div class="grid">
      <div class="card"><h2>Knowledge Docs</h2><div class="big">{checks['doc_count']}</div><p class="muted">19 主文档 + company dossiers</p></div>
      <div class="card"><h2>Company Dossiers</h2><div class="big">{checks['company_coverage']['present']}/{checks['company_coverage']['expected']}</div><p class="muted">{esc(', '.join(checks['company_coverage']['missing']) or 'complete')}</p></div>
      <div class="card"><h2>Broken Links</h2><div class="big {'bad' if checks['missing_links'] else 'ok'}">{len(checks['missing_links'])}</div><p class="muted">wikilink missing</p></div>
      <div class="card"><h2>Stale Queue</h2><div class="big {'warn' if checks['stale_docs'] else 'ok'}">{len(checks['stale_docs'])}</div><p class="muted">expired or due in 7 days</p></div>
      {score_cards}
      <div class="card wide"><h2>Automation</h2>
        <p>{''.join(f"<span class='pill'>{esc(x)}</span>" for x in checks['automation_present'])}</p>
        <p class="muted">Daily Curator and Weekly Doctor run through launchd when installed.</p>
      </div>
    </div>
  </section>
  <section id="doctor">
    <h2>Doctor Score Time Series</h2>
    {render_table(['Date','Kind','Composite','Report'], score_rows)}
  </section>
  <section id="reports">
    <h2>Reports</h2>
    {render_table(['Report','Modified'], report_rows)}
    <h2>Git Log</h2>
    {render_table(['Commit','Date','Subject'], git_rows)}
  </section>
  <section id="flywheel">
    <h2>Candidate Decisions</h2>
    {render_table(['Date','Action','Depth','Reasons'], decision_rows)}
    <h2>Recent Run Events</h2>
    <pre>{esc(json.dumps(run_events[-8:], ensure_ascii=False, indent=2))}</pre>
  </section>
  <section id="sources">
    <h2>Official Source State</h2>
    {render_table(['ID','Name','URL','Checked At','Title','State'], source_rows)}
  </section>
  <section id="paths">
    <h2>Path Links</h2>
    {render_table(['Name','Path'], path_rows)}
    <h2>Manual Commands</h2>
    <pre>python3 "{META / 'pipeline/kb_ops.py'}" run --fetch
python3 "{META / 'pipeline/kb_ops.py'}" doctor --force
python3 "{META / 'pipeline/kb_ops.py'}" dashboard</pre>
  </section>
  <section>
    <h2>Changelog Excerpt</h2>
    <pre>{esc(changelog_excerpt)}</pre>
  </section>
</main>
</body>
</html>"""
    out = DASHBOARD / "index.html"
    write_text(out, html_doc)
    return out


def bar(value: float) -> str:
    pct = max(0, min(100, value * 10))
    return f"<div class='barwrap'><div class='bar' style='width:{pct:.0f}%'></div></div>"


def command_curator(args: argparse.Namespace) -> None:
    ensure_dirs()
    checks = run_checks(fetch=args.fetch)
    decision = decide_library_action(checks)
    report = curator_report(checks, decision)
    record_run("curator", checks, decision=decision, report=report)
    render_dashboard(checks)
    print(f"curator_report={report}")
    print(f"decision={decision['action']} depth={decision['depth']}")


def command_doctor(args: argparse.Namespace) -> None:
    ensure_dirs()
    checks = run_checks(fetch=args.fetch)
    score = score_doctor(checks)
    report = doctor_report(checks, score)
    update_sop_queue(score)
    record_run("doctor", checks, score=score, report=report)
    render_dashboard(checks)
    print(f"doctor_report={report}")
    print(f"score={score['composite']}")


def command_dashboard(args: argparse.Namespace) -> None:
    ensure_dirs()
    checks = run_checks(fetch=False)
    out = render_dashboard(checks)
    print(f"dashboard={out}")


def command_run(args: argparse.Namespace) -> None:
    ensure_dirs()
    checks = run_checks(fetch=args.fetch)
    decision = decide_library_action(checks)
    report = curator_report(checks, decision)
    record_run("curator", checks, decision=decision, report=report)
    if args.force_doctor or checks["doctor_due"]:
        score = score_doctor(checks)
        doctor = doctor_report(checks, score)
        update_sop_queue(score)
        record_run("doctor", checks, score=score, report=doctor)
    out = render_dashboard(checks)
    print(f"curator_report={report}")
    print(f"dashboard={out}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI knowledge-base operations pipeline")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("curator", help="daily light source/inbox check")
    p.add_argument("--fetch", action="store_true", help="fetch official source URLs and compare hashes")
    p.set_defaults(func=command_curator)

    p = sub.add_parser("doctor", help="weekly deep health check")
    p.add_argument("--fetch", action="store_true", help="also fetch official source URLs")
    p.add_argument("--force", action="store_true", help="accepted for launchd/manual symmetry")
    p.set_defaults(func=command_doctor)

    p = sub.add_parser("dashboard", help="rebuild static dashboard")
    p.set_defaults(func=command_dashboard)

    p = sub.add_parser("run", help="curator, optional doctor if due, then dashboard")
    p.add_argument("--fetch", action="store_true", help="fetch official source URLs and compare hashes")
    p.add_argument("--force-doctor", action="store_true", help="force doctor during this run")
    p.set_defaults(func=command_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
