#!/usr/bin/env python3
"""Per-task verdict table for the v2 task set. Usage: v2_table.py [config ...] (default: the three pilot configs).
Widget tasks are objective (server state + endpoint-bypass guard); judged tasks read results/verdicts.json.
Annotations: (bypass) = failed by the endpoint guard, (budget) = 10-minute budget hit, (missing) = no bundle."""
import json, os, sys, statistics as st
import harness
cfgs = sys.argv[1:] or ["sonnet-low-val", "gemini-3.7-flash-low", "spark-low-val"]
v = json.load(open("results/verdicts.json"))
rows = []; tot = {c: [0, 0, 0] for c in cfgs}; eff = {c: [] for c in cfgs}
for t in harness.TASKS_V2:
    r = [t]
    for c in cfgs:
        f = f"results/{t}/{c}.json"; rawf = f"raw/{t}.{c}.json"; k = f"{t}.{c}"
        if not os.path.exists(f) or not os.path.exists(rawf):
            r.append("(missing)"); tot[c][2] += 1; continue
        b = json.load(open(rawf)); res = json.load(open(f)); ann = []
        if b.get("budget_hit"): ann.append("budget")
        if harness.TASKS[t]["kind"] == "appstate":
            if harness.widget_bypass(b): ann.append("bypass")
            ok = bool(res.get("success"))
        elif k in v:
            ok = bool(v[k].get("pass"))
            if v[k].get("blocked"): ann.append("blocked")
        else:
            r.append("pending"); tot[c][2] += 1; continue
        eff[c].append(b["t1"] - b["t0"])
        r.append(("PASS" if ok else "FAIL") + (f" ({', '.join(ann)})" if ann else ""))
        tot[c][0 if ok else 1] += 1
    rows.append(r)
w = max(len(t) for t in harness.TASKS_V2)
print(f"{'task':{w}} " + " ".join(f"{c[:22]:>24}" for c in cfgs))
for r in rows: print(f"{r[0]:{w}} " + " ".join(f"{x:>24}" for x in r[1:]))
print(f"{'score (pass/judged)':{w}} " + " ".join(f"{str(tot[c][0])+'/'+str(tot[c][0]+tot[c][1]):>24}" for c in cfgs))
print(f"{'pending/missing':{w}} " + " ".join(f"{tot[c][2]:>24}" for c in cfgs))
print(f"{'median s / max s':{w}} " + " ".join(f"{(str(round(st.median(eff[c])))+' / '+str(round(max(eff[c])))) if eff[c] else '-':>24}" for c in cfgs))
scores = {c: (tot[c][0], tot[c][0] + tot[c][1]) for c in cfgs}
rates = {c: (p / n if n else None) for c, (p, n) in scores.items()}
print("\ncriteria: no config at 100%:", all(x is not None and x < 1 for x in rates.values()), "| all scores distinct:", len({round(x, 4) for x in rates.values() if x is not None}) == len([x for x in rates.values() if x is not None]))
