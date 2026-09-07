#!/usr/bin/env python3
"""Build the personal site's WebBench v2 data (src/data/webbench-v2.json) from results/v2_summary.json (pass/fail per run,
authoritative from the fleet queue) plus the synced results/<task>/<label>.json and raw/<task>.<label>.json (metrics).
Only complete configurations (all 70 tasks scored) become rows; partial families are named in the description."""
import json, os, statistics, sys
summ = json.load(open("results/v2_summary.json")); tasks = [t["id"] for t in summ["tasks"]]; core = [t["id"] for t in summ["tasks"] if t["tier"] == "core"]; disc = [t["id"] for t in summ["tasks"] if t["tier"] != "core"]
NAMES = {"spark13": ("Muse Spark 1.3", "Muse Code"), "sonnet": ("Sonnet 5", "Claude Code"), "opus": ("Opus 5", "Claude Code"), "gemini-3.8-flash": ("Gemini 3.8 Flash", "Antigravity"), "luna": ("GPT-5.6 Luna", "Codex CLI"), "astra": ("GPT-6 Astra", "Codex CLI"), "fable": ("Fable 5.1", "Claude Code")}
def load(t, l):
    r = raw = {}
    for cand in (f"results/{t}/{l}.json", f"results/{t}/{l.replace('-val','')}.json"):
        if os.path.exists(cand): r = json.load(open(cand)); break
    for cand in (f"raw/{t}.{l}.json", f"raw/{t}.{l.replace('-val','')}.json"):
        if os.path.exists(cand): raw = json.load(open(cand)); break
    return r, raw
def out_tokens(raw):
    u = raw.get("agent_usage_raw") or {}; return u.get("output_tokens")
def reason_tokens(raw):
    u = raw.get("agent_usage_raw") or {}
    return (u.get("output_tokens_details") or {}).get("thinking_tokens", None) if "output_tokens_details" in u else u.get("reasoning_tokens", u.get("reasoning_output_tokens", u.get("thinking_tokens")))
mean = lambda xs: round(statistics.mean(xs), 1) if xs else None
rows = []; partial = []
for c in summ["configs"]:
    fam, eff = c["family"], c["effort"]; per = c["per_task"]; scored = {t: v for t, v in per.items() if v["pass"] is not None}
    if len(scored) < len(tasks): partial.append((fam, eff, len(scored))); continue
    metrics = []
    for t, v in scored.items():
        r, raw = load(t, f"{c['config']}-val"); metrics.append((v, r, raw))
    passes = sum(1 for v in scored.values() if v["pass"])
    walls = [r.get("wall_s") for v, r, raw in metrics if r.get("wall_s")]; wt = [r.get("wall_total_s") for v, r, raw in metrics if r.get("wall_total_s")]
    costs = [v["cost_usd"] for v in scored.values() if v.get("cost_usd") is not None]; steps = [v["cli_calls"] for v in scored.values() if v.get("cli_calls")]
    ot = [x for x in (out_tokens(raw) for v, r, raw in metrics) if x]; rt = [x for x in (reason_tokens(raw) for v, r, raw in metrics) if x is not None]
    name, harness = NAMES[fam]
    rows.append({"model": name, "thinking": eff, "harness": harness, "score": round(100 * passes / len(scored), 1), "time": mean(walls) or 0, "cost": round(statistics.mean(costs), 3) if costs else 0,
                 "outTok": round(statistics.mean(ot)) if ot else 0, "steps": round(statistics.mean(steps)) if steps else 0, "passes": passes, "tasks": len(scored), "wallTotal": mean(wt), "reasonTok": round(statistics.mean(rt)) if rt else None})
order = ["GPT-6 Astra", "Fable 5.1", "Opus 5", "Sonnet 5", "Gemini 3.8 Flash", "Muse Spark 1.3", "GPT-5.6 Luna"]; EFF = ["low", "medium", "high", "xhigh", "max", "ultra"]
rows.sort(key=lambda r: (order.index(r["model"]), EFF.index(r["thinking"])))
vid = sum(1 for t in summ["tasks"] if t["video"]); real = sum(1 for t in summ["tasks"] if t["site"] == "real")
from collections import defaultdict
pf = defaultdict(list)
for f, e, n in partial: pf[NAMES[f][0]].append(e)
partial_txt = "; ".join(f"{m} {', '.join(sorted(es, key=lambda x: ['low','medium','high','xhigh','max','ultra'].index(x)))}" for m, es in pf.items())
desc = ""   # v2 explains itself in the bullet points rendered after the charts
caption = [f"{len(tasks)} tasks per configuration at pass@1, same browser tool, 10-minute budget; time, cost, tokens and steps are per-task means.",
           "Tasks were written in batches and run on Claude Sonnet 5, Claude Opus 5 and Muse Spark 1.2 at low thinking; a task was kept when a configuration failed it on two independent attempts (pass@2), or when it covered browser-control work the set would otherwise lack; every kept failure was checked by hand.",
           f"{vid} tasks count or track something in a rendered video clip: occupancy peaks, events attributed to actors, direction-filtered crossings, defects on a belt.",
           f"The rest are exact visual work on generated images (rotated or occluded shapes, a line traced through crossings, an angle, a gauge, an unnumbered clock), browser workflows on local web apps (multi-page checkout, password reset through an in-app inbox, keyboard-only and hover-only UIs, a form inside a shadow root inside an iframe, table editing with conflicts), and {real} read-only tasks on live GitHub, Wikipedia and JS Paint.",
           f"Scoring: the {len(tasks) - real} local-app tasks are scored from the server's state after the run (their private endpoints are gated, so calling the API instead of using the page yields nothing); the {real} live-site tasks are judged by a Claude Sonnet judge against API ground truth. Runs that hit a provider rate or usage limit were voided and rerun.",
           "Cost is the CLI's reported cost for Claude and list prices applied to captured token usage for the others; runs took place one per AWS instance.",
           f"Partial and not shown: {partial_txt}.",
           "[Tasks](https://github.com/jshan9078/web-bench/tree/main/tasks) · [design log](https://github.com/jshan9078/web-bench/blob/main/tasks/V2-DESIGN.md) · [per-run results](https://github.com/jshan9078/web-bench/tree/main/results)"]
out = {"tableDesc": desc, "webRows": rows, "tableCaption": caption, "defaultOff": []}
dst = "/Users/jonathan/Desktop/personal-site/jshan9078.github.io/src/data/webbench-v2.json"; json.dump(out, open(dst, "w"), indent=1)
print(f"{len(rows)} complete configurations written; partial: {partial_txt}")
for r in rows: print(f"  {r['model']:16} {r['thinking']:6} score {r['score']:5} time {r['time']} wallTotal {r['wallTotal']} cost {r['cost']} outTok {r['outTok']} reason {r['reasonTok']} steps {r['steps']}")
