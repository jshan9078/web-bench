#!/usr/bin/env python3
"""Saturation check for the v2 set. A task is saturated when EVERY listed pilot config has a judged pass on it.
Usage: v2_saturation.py [--apply] [config ...]   (default configs: opus-low-val sonnet-low-val spark-low-val)
--apply writes `"saturated": True` into harness.TASKS registry lines for saturated tasks (and removes it from
tasks that are no longer saturated); tasks flagged `keep` stay in the sweep set regardless."""
import json, os, re, sys
import harness
args = [a for a in sys.argv[1:] if not a.startswith("--")]; apply = "--apply" in sys.argv
cfgs = args or ["opus-low-val", "sonnet-low-val", "spark-low-val"]
v = json.load(open("results/verdicts.json"))
def passed(t, c):
    f = f"results/{t}/{c}.json"; rawf = f"raw/{t}.{c}.json"; k = f"{t}.{c}"
    if not (os.path.exists(f) and os.path.exists(rawf)): return None
    b = json.load(open(rawf))
    if harness.TASKS[t]["kind"] == "appstate":
        return bool(json.load(open(f)).get("success")) and not harness.widget_bypass(b)
    return bool(v[k].get("pass")) if k in v else None
sat, unsat, pending = [], [], []
for t in harness.TASKS_V2:
    r = [passed(t, c) for c in cfgs]
    if any(x is None for x in r): pending.append(t)
    elif all(r): sat.append(t)
    else: unsat.append(t)
print("saturated (all pass):", sat); print("discriminating:", unsat); print("pending:", pending)
if apply:
    h = open("harness.py").read()
    for t in harness.TASKS_V2:
        line = re.search(rf'^    "{re.escape(t)}": \{{[^\n]*\}},\n', h, re.M)
        if not line: continue
        s = line.group(0); s2 = s.replace(', "saturated": True', "")
        if t in sat: s2 = s2.replace('"v2": True', '"v2": True, "saturated": True', 1)
        h = h.replace(s, s2)
    open("harness.py", "w").write(h); print("applied flags to harness.py")
