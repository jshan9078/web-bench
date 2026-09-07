#!/usr/bin/env python3
"""Recompute the v1 (44 live-site tasks, 36 configurations) rows for the personal site and README-v1.md from the local
per-run results (results/<task>/<label>.json) and raw bundles (raw/<task>.<label>.json; cost via run_cost.py).
Aggregates are per-task means over scored (non-blocked) runs. Haiku 4.5 ignores the effort setting, so its five sweeps
are pooled into one row. `python3 make_v1_site.py` prints the rows as TypeScript (site) and Markdown (README-v1)."""
import glob, json, os, statistics, sys
import harness, run_cost
agg = statistics.mean
V1 = [t for t in harness.TASKS if not harness.TASKS[t].get("v2") and not harness.TASKS[t].get("retired")]
FAM = {"opus": ("Opus 5", "Claude Code"), "sonnet": ("Sonnet 5", "Claude Code"), "haiku": ("Haiku 4.5", "Claude Code"), "gemini-3.7-flash": ("Gemini 3.7 Flash", "Antigravity"),
       "gemini-3.8-flash": ("Gemini 3.8 Flash", "Antigravity"), "luna": ("GPT-5.6 Luna", "Codex CLI"), "spark13": ("Muse Spark 1.3", "Muse Code"), "spark": ("Muse Spark 1.2", "Muse Code")}
EFF = ["low", "medium", "high", "xhigh", "max", "ultra"]
def split(label):
    c = label.replace("-val", "")
    for f in sorted(FAM, key=len, reverse=True):
        if c.startswith(f + "-"): return f, c[len(f) + 1:]
labels = set()
for t in V1:
    for p in glob.glob(f"results/{t}/*.json"):
        l = os.path.basename(p)[:-5]
        if l.startswith("._") or not split(l) or split(l)[1] not in EFF: continue
        if sum(os.path.exists(f"results/{tt}/{l}.json") for tt in V1) >= 40: labels.add(l)
def out_tokens(raw): return (raw.get("agent_usage_raw") or {}).get("output_tokens")
def reason_tokens(raw):
    u = raw.get("agent_usage_raw") or {}
    return (u.get("output_tokens_details") or {}).get("thinking_tokens") if "output_tokens_details" in u else u.get("reasoning_tokens", u.get("reasoning_output_tokens", u.get("thinking_tokens")))
groups = {}   # (family, effort) -> runs; Haiku pooled under effort "n/a"
for l in sorted(labels):
    f, e = split(l)
    for t in V1:
        p = f"results/{t}/{l}.json"
        if not os.path.exists(p): continue
        r = json.load(open(p))
        if r.get("blocked") or r.get("needs_judge"): continue
        rp = f"raw/{t}.{l}.json"; raw = json.load(open(rp)) if os.path.exists(rp) else {}
        groups.setdefault((f, "n/a" if f == "haiku" else e), []).append((r, raw, run_cost.cost(rp) if os.path.exists(rp) else None))
rows = []
for (f, e), runs in groups.items():
    name, h = FAM[f]; passes = sum(1 for r, _, _ in runs if r.get("success")); n = len(runs)
    col = lambda fn: [x for x in (fn(r, raw, c) for r, raw, c in runs) if x is not None]
    walls = col(lambda r, raw, c: r.get("wall_s")); wt = col(lambda r, raw, c: r.get("wall_total_s")); costs = col(lambda r, raw, c: c)
    steps = col(lambda r, raw, c: r.get("cli_calls")); ot = col(lambda r, raw, c: out_tokens(raw)); rt = col(lambda r, raw, c: reason_tokens(raw))
    rows.append({"model": name, "thinking": e, "harness": h, "score": round(100 * passes / n, 1), "time": round(agg(walls), 1), "cost": round(agg(costs), 3), "outTok": round(agg(ot)) if ot else 0,
                 "steps": round(agg(steps)), "passes": passes, "tasks": n, "wallTotal": round(agg(wt), 1), "reasonTok": round(agg(rt)) if rt else 0})
order = ["Haiku 4.5", "Gemini 3.7 Flash", "Gemini 3.8 Flash", "GPT-5.6 Luna", "Muse Spark 1.3", "Muse Spark 1.2", "Sonnet 5", "Opus 5"]
rows.sort(key=lambda r: (order.index(r["model"]), EFF.index(r["thinking"]) if r["thinking"] in EFF else -1))
print("// TypeScript rows (paste into WEBBENCH_V1.webRows)")
for r in rows:
    print("    { " + ", ".join(f"{k}: {json.dumps(v)}" for k, v in r.items()) + " },")
print("\n<!-- README-v1 table -->\n| model | thinking | pass | rate | mean time | mean cost |\n|---|---|---|---|---|---|")
for r in rows:
    th = "n/a (5 replicate sweeps)" if r["thinking"] == "n/a" else r["thinking"]
    print(f"| {r['model']} | {th} | {r['passes']}/{r['tasks']} | {r['score']:.1f}% | {r['time']:.0f}s | ${r['cost']:.3f} |")
json.dump(rows, open("results/v1_rows.json", "w"), indent=1)
