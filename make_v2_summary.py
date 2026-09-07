#!/usr/bin/env python3
"""Rebuild results/v2_summary.json from the fleet queue's done markers (s3://.../final63/done/), the authoritative
pass/fail, wall-clock, step and cost record of every scored run. The task list is carried over from the existing summary.
Usage: MATRIX_STORE=s3://webbench-matrix-966239516827/final63 python3 make_v2_summary.py"""
import json, os, statistics, time, collections
import matrix_queue as mq
S = mq.store(); old = json.load(open("results/v2_summary.json")); tasks = old["tasks"]; tids = {t["id"] for t in tasks}
from concurrent.futures import ThreadPoolExecutor
keys = S.list("done/")
with ThreadPoolExecutor(16) as ex: markers = list(ex.map(lambda k: json.loads(S.get(k) or b"{}"), keys))
per = collections.defaultdict(dict)
for k, d in zip(keys, markers):
    t, l = k.split("/", 1)[1].split("__"); cfg = mq.cfg_of(l)
    if t not in tids or l != mq.label(cfg, 1): continue
    if d.get("blocked"): continue
    per[cfg][t] = {"pass": None if d.get("needs_judge") else bool(d.get("success")), "wall_s": d.get("wall_s"), "cli_calls": d.get("cli_calls"), "cost_usd": d.get("cost_usd"), "judge_pending": bool(d.get("needs_judge"))}
NAMES = {"spark13": "Muse Spark 1.3", "sonnet": "Claude Sonnet 5", "opus": "Claude Opus 5", "gemini-3.8-flash": "Gemini 3.8 Flash", "luna": "GPT-5.6 Luna", "astra": "GPT-6 Astra", "fable": "Claude Fable 5.1"}
configs = []
for cfg in mq.CONFIGS:
    p = per.get(cfg, {}); fam, eff = cfg.rsplit("-", 1); scored = [v for v in p.values() if v["pass"] is not None]
    ws = [v["wall_s"] for v in p.values() if v.get("wall_s")]; cs = [v["cost_usd"] for v in p.values() if v.get("cost_usd") is not None]
    configs.append({"config": cfg, "family": fam, "model": NAMES.get(fam, fam), "effort": eff, "runs": len(p), "scored": len(scored), "pass": sum(1 for v in scored if v["pass"]),
                    "mean_wall_s": round(statistics.mean(ws), 1) if ws else None, "mean_cost_usd": round(statistics.mean(cs), 3) if cs else None, "total_cost_usd": round(sum(cs), 2) if cs else None,
                    "complete": len(scored) == len(tasks), "per_task": dict(sorted(p.items()))})
out = {"generated": time.strftime("%Y-%m-%dT%H:%M"), "tasks": tasks, "configs": configs, "notes": old.get("notes")}
json.dump(out, open("results/v2_summary.json", "w"), indent=1)
for c in configs:
    if c["runs"]: print(f"{c['config']:24} runs {c['runs']:3} scored {c['scored']:3} pass {c['pass']:3} mean wall {c['mean_wall_s']} mean cost {c['mean_cost_usd']} {'complete' if c['complete'] else ''}")
