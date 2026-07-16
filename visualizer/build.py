#!/usr/bin/env python3
"""KB-Agent 迭代可视化 dashboard 生成器（零依赖）。

用法：python3 visualizer/build.py
输入：evals/runs/*/manifest.json（+ 可选 results.jsonl）、evals/prompts/agent-v*.md
输出：evals/dashboard.html（静态单文件，离线可看）

schema 维度无关：manifest.aggregate.dimensions 是任意 key->分数 映射，
rubric 升级改维度不需要改本脚本。详见 visualizer/SPEC.md。
"""
import difflib
import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
RUNS_DIR = EVALS / "runs"
PROMPTS_DIR = EVALS / "prompts"
OUT = EVALS / "dashboard.html"


def esc(x):
    return html.escape(str(x))


def split_of(r):
    return (r.get("meta") or {}).get("split")


def load_runs():
    runs = []
    if RUNS_DIR.exists():
        for d in sorted(p for p in RUNS_DIR.iterdir() if p.is_dir()):
            mf = d / "manifest.json"
            if not mf.exists():
                continue
            r = json.loads(mf.read_text(encoding="utf-8"))
            r["_cases"] = []
            rl = d / "results.jsonl"
            if rl.exists():
                for ln in rl.read_text(encoding="utf-8").splitlines():
                    if ln.strip():
                        r["_cases"].append(json.loads(ln))
            runs.append(r)
    runs.sort(key=lambda r: (r.get("timestamp", ""), r.get("run_id", "")))
    return runs


def trend_svg(runs):
    pts = [
        r for r in runs
        if r.get("type") in {"state", "behavior"}
        and (r.get("aggregate") or {}).get("composite") is not None
    ]
    if not pts:
        return "<p class='muted'>暂无评测数据</p>"
    W, H, P = 780, 250, 46
    n = len(pts)
    xstep = (W - 2 * P) / max(n - 1, 1)

    def x_of(i):
        return P + i * xstep if n > 1 else W / 2

    def y_of(v):
        return H - P - (v / 10.0) * (H - 2 * P)

    parts = []
    for g in range(0, 11, 2):
        y = y_of(g)
        parts.append(f"<line x1='{P}' y1='{y:.1f}' x2='{W - P}' y2='{y:.1f}' class='grid'/>")
        parts.append(f"<text x='{P - 8}' y='{y + 4:.1f}' class='axis' text-anchor='end'>{g}</text>")
    colors = {"state": "#4f7cff", "behavior": "#2fa36b"}
    poly = []
    for i, r in enumerate(pts):
        v = r["aggregate"]["composite"]
        x, y = x_of(i), y_of(v)
        poly.append(f"{x:.1f},{y:.1f}")
        c = colors.get(r.get("type"), "#999")
        if split_of(r) == "holdout":
            parts.append(f"<rect x='{x - 5:.1f}' y='{y - 5:.1f}' width='10' height='10' fill='{c}'/>")
        else:
            parts.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='5' fill='{c}'/>")
        parts.append(f"<text x='{x:.1f}' y='{y - 10:.1f}' class='pt' text-anchor='middle'>{v}</text>")
        rid = str(r.get("run_id", ""))[:18]
        parts.append(f"<text x='{x:.1f}' y='{H - P + 18}' class='axis' text-anchor='middle'>{esc(rid)}</text>")
    line = ""
    if len(poly) > 1:
        line = f"<polyline points='{' '.join(poly)}' fill='none' stroke='#c5c5c5' stroke-dasharray='4,3'/>"
    legend = (
        f"<circle cx='{W - 270}' cy='18' r='5' fill='#4f7cff'/><text x='{W - 260}' y='22' class='axis'>状态评测</text>"
        f"<circle cx='{W - 185}' cy='18' r='5' fill='#2fa36b'/><text x='{W - 175}' y='22' class='axis'>行为评测</text>"
        f"<rect x='{W - 100}' y='13' width='10' height='10' fill='#2fa36b'/><text x='{W - 86}' y='22' class='axis'>holdout</text>"
    )
    return f"<svg viewBox='0 0 {W} {H}'>{''.join(parts)}{line}{legend}</svg>"


def dim_bars(runs):
    series = [r for r in runs if r.get("type") == "behavior"]
    label = "行为评测"
    if not series:
        series = [r for r in runs if r.get("type") == "state"]
        label = "状态评测"
    if not series:
        return "<p class='muted'>暂无状态/行为评测</p>"
    cur = series[-1]
    prev = series[-2] if len(series) > 1 else None
    rows = []
    for k, v in (cur["aggregate"].get("dimensions") or {}).items():
        pv = (prev["aggregate"].get("dimensions") or {}).get(k) if prev else None
        delta_html, prev_html = "", ""
        if pv is not None:
            d = v - pv
            cls = "up" if d >= 0 else "down"
            delta_html = f" <span class='{cls}'>({d:+.1f})</span>"
            prev_html = f"<div class='bar prev' style='width:{pv * 10:.0f}%'></div>"
        rows.append(
            "<div class='dim'>"
            f"<span class='dlabel'>{esc(k)}</span>"
            f"<div class='barwrap'>{prev_html}<div class='bar cur' style='width:{v * 10:.0f}%'></div></div>"
            f"<span class='dval'>{v}{delta_html}</span>"
            "</div>"
        )
    cap = f"当前{label}：{esc(cur.get('run_id'))}"
    if prev:
        cap += f" ｜ 灰色底条为上一版：{esc(prev.get('run_id'))}"
    return f"<p class='muted'>{cap}</p>" + "".join(rows)


def calibration_section(runs):
    cals = [r for r in runs if r.get("type") == "calibration"]
    if not cals:
        return "<p class='muted'>暂无 Judge 校准 run。用户校准后，这里会显示 agent 分数与用户分数的一致性。</p>"
    cur = cals[-1]
    dims = (cur.get("aggregate") or {}).get("dimensions") or {}
    cases = cur.get("_cases") or []
    review = [c for c in cases if c.get("verdict") != "aligned"]
    rows = []
    for c in cases:
        err = (c.get("scores") or {}).get("abs_error")
        rows.append(
            f"<tr><td><code>{esc(c.get('case_id'))}</code></td>"
            f"<td>{esc((c.get('scores') or {}).get('user_source_value', '-'))}</td>"
            f"<td>{esc((c.get('scores') or {}).get('agent_source_value', '-'))}</td>"
            f"<td>{esc(err)}</td><td>{esc(c.get('verdict', ''))}</td></tr>"
        )
    summary = (
        f"<p>最新校准：<code>{esc(cur.get('run_id'))}</code> ｜ "
        f"对齐分 <b>{esc((cur.get('aggregate') or {}).get('composite', '-'))}</b> ｜ "
        f"需复核 case：<b>{len(review)}</b></p>"
        f"<p class='muted'>"
        + " ｜ ".join(f"{esc(k)}: {esc(v)}" for k, v in dims.items())
        + "</p>"
    )
    table = (
        "<table><tr><th>case</th><th>用户分</th><th>agent 分</th><th>偏差</th><th>状态</th></tr>"
        + "".join(rows)
        + "</table>"
    )
    return summary + table


def count_from_cases(cases, key):
    counts = {}
    for c in cases:
        v = c.get(key)
        if not v:
            continue
        counts[str(v)] = counts.get(str(v), 0) + 1
    return counts


def funnel_table(title, counts, prev_counts=None):
    if not counts:
        return f"<div class='fblock'><h3>{esc(title)}</h3><p class='muted'>暂无结构化字段</p></div>"
    total = max(sum(counts.values()), 1)
    rows = []
    for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        pct = v / total * 100
        pv = (prev_counts or {}).get(k)
        delta = ""
        if pv is not None:
            d = v - pv
            cls = "up" if d >= 0 else "down"
            delta = f" <span class='{cls}'>({d:+d})</span>"
        rows.append(
            "<div class='frow'>"
            f"<span class='fname'>{esc(k)}</span>"
            f"<div class='fbarwrap'><div class='fbar' style='width:{pct:.0f}%'></div></div>"
            f"<span class='fval'>{v}{delta}</span>"
            "</div>"
        )
    return f"<div class='fblock'><h3>{esc(title)}</h3>{''.join(rows)}</div>"


def funnel_section(runs):
    beh = [r for r in runs if r.get("type") == "behavior" and r.get("_cases")]
    if not beh:
        return "<p class='muted'>暂无行为评测漏斗。v2 起 results.jsonl 会记录 decision/target_zone/risk_tier/user_gate。</p>"
    cur = beh[-1]
    prev = beh[-2] if len(beh) > 1 else None
    cur_meta = (cur.get("meta") or {}).get("funnel") or {}
    prev_meta = (prev.get("meta") or {}).get("funnel") if prev else {}

    def counts_for(run, meta, key):
        return (meta or {}).get(key) or count_from_cases(run.get("_cases") or [], key)

    parts = [
        f"<p class='muted'>当前行为评测：{esc(cur.get('run_id'))}"
        + (f" ｜ 对比上一版：{esc(prev.get('run_id'))}" if prev else "")
        + "</p>"
    ]
    for key, title in [
        ("decision", "Decision 分布"),
        ("target_zone", "Target Zone 分布"),
        ("risk_tier", "Risk Tier 分布"),
        ("user_gate", "User Gate 分布"),
    ]:
        parts.append(funnel_table(title, counts_for(cur, cur_meta, key), counts_for(prev, prev_meta, key) if prev else None))
    return "<div class='fgrid'>" + "".join(parts) + "</div>"


def overfit(runs):
    beh = [r for r in runs if r.get("type") == "behavior"]
    train = [r for r in beh if split_of(r) and split_of(r) != "holdout"]
    hold = [r for r in beh if split_of(r) == "holdout"]
    if not train or not hold:
        return ("<p class='muted'>需要至少各一轮 训练侧（smoke/regression）与 holdout 行为评测后激活。"
                "监控逻辑：训练侧分持续上升而 holdout 不升 = agent 在背题而非变强（过拟合）。</p>")
    d = train[-1]["aggregate"]["composite"]
    h = hold[-1]["aggregate"]["composite"]
    gap = d - h
    cls = "alert" if gap > 1.0 else "ok"
    verdict = "⚠️ 分差超过 1.0，过拟合警报" if gap > 1.0 else "✅ 正常"
    return (f"<p>最新训练侧（{esc(split_of(train[-1]))}）：<b>{d}</b>（{esc(train[-1]['run_id'])}） ｜ "
            f"最新 holdout：<b>{h}</b>（{esc(hold[-1]['run_id'])}） ｜ "
            f"分差：<b class='{cls}'>{gap:+.1f}</b>　{verdict}</p>")


def cases_section(runs):
    beh = [r for r in runs if r["_cases"]]
    if not beh:
        return ("<p class='muted'>暂无 case 级数据——第一轮行为评测后，这里会出现每条挑战的"
                "输入/输出/得分/Judge 证据，以及同一 case 的跨版本对比。</p>")
    per, cats = {}, set()
    run_order = [r["run_id"] for r in beh]
    for r in beh:
        for c in r["_cases"]:
            per.setdefault(c.get("case_id", "?"), {})[r["run_id"]] = c
            cats.add(c.get("category", "未分类"))
    opts = "".join(f"<option>{esc(c)}</option>" for c in sorted(cats))
    rows = []
    for cid in sorted(per):
        by = per[cid]
        seen = [rid for rid in run_order if rid in by]
        latest = by[seen[-1]]
        hist = []
        for rid in seen:
            c = by[rid]
            meta_bits = []
            for k in ["decision", "target_zone", "granularity", "freshness_policy", "risk_tier", "user_gate"]:
                if c.get(k):
                    meta_bits.append(f"{k}={c.get(k)}")
            meta = ""
            if meta_bits:
                meta = f"<div class='chips'>{''.join(f'<code>{esc(x)}</code>' for x in meta_bits)}</div>"
            hist.append(
                f"<div class='hist'><b>{esc(rid)}</b> · 得分 <b>{esc(c.get('weighted', '-'))}</b>"
                f" · {esc(c.get('verdict', ''))}"
                f"{meta}"
                f"<div><b>输出：</b>{esc(c.get('output', ''))}</div>"
                f"<div class='muted'><b>Judge 证据：</b>{esc(c.get('judge_evidence', ''))}</div></div>"
            )
        rows.append(
            f"<details class='case' data-cat='{esc(latest.get('category', '未分类'))}'>"
            f"<summary><code>{esc(cid)}</code> · {esc(latest.get('category', '未分类'))}"
            f" · 最新得分 <b>{esc(latest.get('weighted', '-'))}</b>（{esc(seen[-1])}，共 {len(seen)} 轮）</summary>"
            f"<div class='cbody'><p><b>输入：</b>{esc(latest.get('input_excerpt') or latest.get('input_ref', ''))}</p>"
            f"{''.join(hist)}</div></details>"
        )
    controls = (
        "<div class='controls'>"
        "<input id='q' placeholder='搜索 case…' oninput='flt()'>"
        f"<select id='cat' onchange='flt()'><option value=''>全部类别</option>{opts}</select>"
        "</div>"
    )
    return controls + "".join(rows)


def prompt_diffs():
    files = sorted(PROMPTS_DIR.glob("agent-v*.md")) if PROMPTS_DIR.exists() else []
    if not files:
        return "<p class='muted'>暂无 agent prompt 版本快照（第一版落盘为 evals/prompts/agent-v1.md）</p>"
    out = [f"<p class='muted'>现有版本：{', '.join(esc(f.stem) for f in files)}</p>"]
    for a, b in zip(files, files[1:]):
        diff = difflib.unified_diff(
            a.read_text(encoding="utf-8").splitlines(),
            b.read_text(encoding="utf-8").splitlines(),
            fromfile=a.stem, tofile=b.stem, lineterm="")
        lines = []
        for l in diff:
            cls = "ctx"
            if l.startswith("+") and not l.startswith("+++"):
                cls = "add"
            elif l.startswith("-") and not l.startswith("---"):
                cls = "del"
            lines.append(f"<div class='dl {cls}'>{esc(l)}</div>")
        out.append(f"<details class='pd'><summary>{esc(a.stem)} → {esc(b.stem)}</summary>"
                   f"<div class='diff'>{''.join(lines)}</div></details>")
    return "".join(out)


def runs_table(runs):
    if not runs:
        return "<p class='muted'>暂无</p>"
    head = ("<tr><th>run</th><th>类型</th><th>split</th><th>agent prompt</th><th>数据集</th>"
            "<th>rubric</th><th>综合分</th><th>case 数</th><th>备注</th></tr>")
    body = []
    for r in reversed(runs):
        ver = r.get("versions") or {}
        body.append(
            f"<tr><td><code>{esc(r.get('run_id'))}</code></td><td>{esc(r.get('type', ''))}</td>"
            f"<td>{esc(split_of(r) or '-')}</td>"
            f"<td>{esc(ver.get('agent_prompt', '-'))}</td><td>{esc(ver.get('dataset', '-'))}</td>"
            f"<td>{esc(ver.get('rubric', '-'))}</td>"
            f"<td><b>{esc((r.get('aggregate') or {}).get('composite', '-'))}</b></td>"
            f"<td>{len(r['_cases'])}</td>"
            f"<td class='muted'>{esc((r.get('meta') or {}).get('notes', ''))}</td></tr>"
        )
    return f"<table>{head}{''.join(body)}</table>"


CSS = """<style>
:root{color-scheme:light}
body{font-family:-apple-system,'PingFang SC','Helvetica Neue',sans-serif;margin:0;background:#f6f7f9;color:#1f2328}
main{max-width:1000px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:22px;margin:0 0 4px}
section{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:16px 20px;margin:16px 0}
h2{font-size:15px;margin:0 0 10px;color:#333}
svg{width:100%;height:auto}
.grid{stroke:#eee}.axis{fill:#8a8f98;font-size:11px}.pt{fill:#333;font-size:11px;font-weight:600}
.muted{color:#8a8f98;font-size:13px}
.dim{display:flex;align-items:center;gap:10px;margin:7px 0}
.dlabel{width:210px;font-size:13px}.dval{width:100px;font-size:13px;font-weight:600}
.barwrap{position:relative;flex:1;background:#f0f1f4;height:14px;border-radius:7px;overflow:hidden}
.bar{position:absolute;left:0;top:0;bottom:0;border-radius:7px}
.bar.prev{background:#d4d7dd}.bar.cur{background:#4f7cff;opacity:.85}
.up{color:#1a7f37}.down{color:#c0392b}.alert{color:#c0392b}.ok{color:#1a7f37}
details.case,details.pd{border:1px solid #e5e7eb;border-radius:8px;margin:8px 0;padding:8px 12px;background:#fff}
details summary{cursor:pointer;font-size:13px}
.cbody{font-size:13px;margin-top:8px}
.hist{border-left:3px solid #dfe3e8;margin:8px 0;padding:6px 10px;background:#fafbfc;font-size:13px}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border:1px solid #e5e7eb;padding:6px 8px;text-align:left}
th{background:#fafbfc}
.controls{margin:4px 0 10px}
.controls input,.controls select{padding:6px 10px;margin-right:8px;border:1px solid #d0d7de;border-radius:6px;font-size:13px}
.diff{max-height:420px;overflow:auto;margin-top:8px}
.dl{font-family:ui-monospace,SFMono-Regular,monospace;font-size:12px;white-space:pre-wrap;padding:0 6px}
.dl.add{background:#e6ffec;color:#116329}.dl.del{background:#ffebe9;color:#82071e}.dl.ctx{color:#57606a}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.fgrid>p{grid-column:1/-1}
.fblock{border:1px solid #e5e7eb;border-radius:8px;padding:10px;background:#fafbfc}
.fblock h3{font-size:13px;margin:0 0 8px;color:#333}
.frow{display:flex;align-items:center;gap:8px;margin:6px 0}
.fname{width:145px;font-size:12px}.fval{width:48px;font-size:12px;font-weight:600}
.fbarwrap{flex:1;background:#eef0f3;height:12px;border-radius:6px;overflow:hidden}
.fbar{height:100%;background:#2fa36b;border-radius:6px}
.chips{margin:4px 0 6px;display:flex;gap:4px;flex-wrap:wrap}
code{background:#f0f1f4;padding:1px 5px;border-radius:4px;font-size:12px}
</style>"""

JS = """<script>
function flt(){
  var q=(document.getElementById('q')||{}).value||'';q=q.toLowerCase();
  var c=(document.getElementById('cat')||{}).value||'';
  document.querySelectorAll('.case').forEach(function(e){
    var okq=!q||e.textContent.toLowerCase().indexOf(q)>=0;
    var okc=!c||e.getAttribute('data-cat')===c;
    e.style.display=(okq&&okc)?'':'none';
  });
}
</script>"""


def section(title, body):
    return f"<section><h2>{title}</h2>{body}</section>"


def build():
    runs = load_runs()
    gen = datetime.now().strftime("%Y-%m-%d %H:%M")
    page = (
        "<!DOCTYPE html><html lang='zh'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>KB-Agent 迭代 Dashboard</title>" + CSS + "</head><body><main>"
        + f"<h1>KB-Agent 迭代 Dashboard</h1>"
        + f"<p class='muted'>生成于 {gen} ｜ 数据源 evals/runs/ ｜ 重新生成：python3 visualizer/build.py</p>"
        + section("① 版本趋势（状态/行为综合分，1–10）", trend_svg(runs))
        + section("② Judge 校准（用户分 vs agent 分）", calibration_section(runs))
        + section("③ 维度对比（当前 vs 上一版）", dim_bars(runs))
        + section("④ 分流漏斗（decision / target_zone / risk）", funnel_section(runs))
        + section("⑤ 过拟合监控（dev vs holdout）", overfit(runs))
        + section("⑥ Case 浏览器（输入 → 输出 → 评分 → Judge 证据，跨版本）", cases_section(runs))
        + section("⑦ Prompt 版本演化（unified diff）", prompt_diffs())
        + section("⑧ 全部评测轮次（版本三元组）", runs_table(runs))
        + "</main>" + JS + "</body></html>"
    )
    OUT.write_text(page, encoding="utf-8")
    print(f"OK: dashboard -> {OUT} ({len(runs)} runs)")


if __name__ == "__main__":
    build()
