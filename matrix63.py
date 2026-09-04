#!/usr/bin/env python3
"""Plan and shard the final-set matrix sweep (core tier + discriminating tier) over the requested configs.
Usage:
  matrix63.py plan                       print coverage per config and the run count still needed
  matrix63.py pairs [--attempts N]       print "task config" pairs still missing (one per line)
  matrix63.py shards K [--attempts N]    write results/shards/shard_<i>.txt (round-robin, tasks interleaved)
Configs: env MATRIX_CONFIGS overrides (space-separated), default is the 23 below.
A run counts as done when raw/<task>.<config>-val.json (attempt 1) or raw/<task>.<config>-val<a>.json exists."""
import json, os, sys
CONFIGS = os.environ.get("MATRIX_CONFIGS", "").split() or (
    [f"spark13-{e}" for e in ("low", "medium", "high", "xhigh", "ultra")] + [f"sonnet-{e}" for e in ("low", "medium", "high", "xhigh", "max")]
    + [f"opus-{e}" for e in ("low", "medium", "high", "xhigh", "max")] + [f"gemini-3.8-flash-{e}" for e in ("low", "medium", "high")]
    + [f"luna-{e}" for e in ("low", "medium", "high", "xhigh", "max")])
tasks = list(json.load(open("results/core_set.json"))) + list(json.load(open("results/validated_set.json")))
def label(cfg, a): return f"{cfg}-val" + ("" if a == 1 else str(a))
def done(t, cfg, a): return os.path.exists(f"raw/{t}.{label(cfg, a)}.json") or (a == 1 and os.path.exists(f"raw/{t}.{cfg}.json"))
att = int(sys.argv[sys.argv.index("--attempts") + 1]) if "--attempts" in sys.argv else 1
mode = sys.argv[1] if len(sys.argv) > 1 else "plan"
pairs = [(t, c, a) for a in range(1, att + 1) for t in tasks for c in CONFIGS if not done(t, c, a)]
if mode == "plan":
    print(f"{len(tasks)} tasks x {len(CONFIGS)} configs x {att} attempt(s)"); print(f"{'config':26} done  todo")
    for c in CONFIGS: d = sum(1 for t in tasks for a in range(1, att + 1) if done(t, c, a)); print(f"{c:26} {d:4}  {len(tasks) * att - d:4}")
    print("runs still needed:", len(pairs))
elif mode == "pairs":
    for t, c, a in pairs: print(t, label(c, a))
elif mode == "shards":
    k = int(sys.argv[2]); os.makedirs("results/shards", exist_ok=True)
    for i in range(k):
        with open(f"results/shards/shard_{i}.txt", "w") as f:
            for t, c, a in pairs[i::k]: f.write(f"{t} {label(c, a)}\n")
    print(f"wrote {k} shards, {len(pairs)} runs, ~{len(pairs) // k} each")
