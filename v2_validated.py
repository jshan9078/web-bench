#!/usr/bin/env python3
"""Recompute results/validated_set.json: a task is validated when ANY config (Spark 1.2 low, Sonnet 5 low, Opus 5
low) failed it on both pass@2 attempts, under the state-only rule of v2_pass2.passed. Retired and blocked_env
tasks are excluded. Usage: v2_validated.py [--write]"""
import os, glob, sys, json, harness
sys.argv, argv = ["x", "pairs"], sys.argv
ns = {}; exec(open("v2_pass2.py").read().split("mode = sys.argv[1]")[0], ns); passed = ns["passed"]
CFGS = ["spark-low-val", "sonnet-low-val", "opus-low-val"]
VERD = json.load(open("results/verdicts.json")) if os.path.exists("results/verdicts.json") else {}
def judged(t, r): return harness.TASKS[t]["kind"] != "judge" or f"{t}.{r}" in VERD
def ok(t, c):
    try: return bool(passed(t, c))
    except Exception: return False
out = {}
for t, meta in harness.TASKS.items():
    if meta.get("retired") or meta.get("blocked_env"): continue
    fails = [c for c in CFGS if os.path.exists(f"raw/{t}.{c}.json") and os.path.exists(f"raw/{t}.{c}2.json") and judged(t, c) and judged(t, c + "2") and not ok(t, c) and not ok(t, c + "2")]
    if fails: out[t] = fails
print(f"{len(out)} validated tasks (any config failed both attempts)")
from collections import Counter; print(Counter(c for v in out.values() for c in v))
if "--write" in argv: json.dump(out, open("results/validated_set.json", "w"), indent=1); print("written")
