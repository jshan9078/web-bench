#!/usr/bin/env python3
"""pass@2 bookkeeping for a set of tasks.
  v2_pass2.py pairs <task...>    -> prints "<task> <config>" for every attempt-1 failure (appstate tasks only)
  v2_pass2.py summary <task...>  -> per-task table and VALID/INVALID lists; --apply flags pass2_invalid / keeps valid"""
import json, os, re, sys, harness
CFGS = ["spark-low-val", "sonnet-low-val", "opus-low-val"]


def passed(t, r):
    f = f"results/{t}/{r}.json"; rawf = f"raw/{t}.{r}.json"
    if not (os.path.exists(f) and os.path.exists(rawf)): return None
    b = json.load(open(rawf)); res = json.load(open(f))
    if harness.TASKS[t]["kind"] == "appstate": return bool(res.get("success")) and not harness.widget_bypass(b)
    v = json.load(open("results/verdicts.json")); return v.get(f"{t}.{r}", {}).get("pass")


mode = sys.argv[1]; tasks = [a for a in sys.argv[2:] if not a.startswith("--")]
if mode == "pairs":
    for t in tasks:
        for c in CFGS:
            if passed(t, c) is False: print(t, c)
elif mode == "summary":
    valid, invalid, pending = [], [], []
    print(f"{'task':26} " + " ".join(f"{c[:6]:>9}" for c in CFGS) + "   (attempt1/attempt2)")
    for t in tasks:
        cells = []; hold = []; pend = False
        for c in CFGS:
            a1 = passed(t, c); a2 = passed(t, c + "2") if a1 is False else None
            if a1 is None or (a1 is False and a2 is None): pend = True
            if a1 is False and a2 is False: hold.append(c)
            cells.append(("P" if a1 else "F" if a1 is False else "?") + "/" + ("-" if a1 is not False else "P" if a2 else "F" if a2 is False else "?"))
        print(f"{t:26} " + " ".join(f"{x:>9}" for x in cells))
        (pending if pend else valid if hold else invalid).append(t)
    print("\nVALID (fails both attempts for some config):", valid); print("INVALID (all failures cleared on retry):", invalid); print("PENDING:", pending)
    if "--apply" in sys.argv:
        h = open("harness.py").read()
        for t in invalid:
            m = re.search(rf'^    "{re.escape(t)}": \{{[^\n]*\}},\n', h, re.M)
            if m and "pass2_invalid" not in m.group(0): h = h.replace(m.group(0), m.group(0).replace('"v2": True', '"v2": True, "pass2_invalid": True', 1))
        open("harness.py", "w").write(h); print("flags applied")
