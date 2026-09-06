#!/usr/bin/env python3
"""One-shot fairness audit of every fleet run recorded so far: a run is void (artifacts moved to voided/, done marker
and verdict removed, item requeued) if its stream shows a provider rate/usage limit marker, or if the harness failed
around it (empty browser session id, or no CLI calls with a zero wall clock). Log: results/audit_all.log"""
import os, sys, json, time, datetime, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "."); import matrix_queue as mq, ratelimit
S = mq.store(); LOG = "results/audit_all.log"
def log(m): line = f"{datetime.datetime.now().strftime('%H:%M:%S')} {m}"; print(line, flush=True); open(LOG, "a").write(line + "\n")
def check(k):
    d = json.loads(S.get(k) or b"{}")
    if not str(d.get("worker", "")).startswith("i-"): return None
    t, l = d["task"], d["label"]; reasons = []
    raw = S.get(f"raw/{t}.{l}.json")
    if not raw: reasons.append("no raw bundle recorded")
    if raw:
        r = json.loads(raw)
        if not r.get("sid"): reasons.append("empty session id")
        if not (r.get("requests_log") or []) and not r.get("blocked"): reasons.append("no CLI calls recorded")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tf: path = tf.name
    try:
        S.get_file(f"raw/{t}.{l}.stream.txt", path); marks = ratelimit.hits(path)
        if marks: reasons.append("rate/usage limit: " + ", ".join(marks[:2]))
    except Exception: pass
    finally:
        try: os.remove(path)
        except OSError: pass
    return (k, t, l, d, reasons)
def void(k, t, l, reasons):
    kk = mq.key(t, l)
    for key in S.list(f"raw/{t}.{l}.") + S.list(f"results/{t}/{l}."):
        data = S.get(key)
        if data is not None and not key.endswith(".mp4"): S.put(f"voided/audit/{key}", data)
        S.delete(key)
    S.delete(k); S.delete(f"verdicts/{kk}"); S.put(f"pending/{kk}", mq.j({"task": t, "label": l, "lane": mq.lane_of(t)}))
keys = S.list("done/"); log(f"audit start: {len(keys)} done markers")
n = v = 0; by = {}
with ThreadPoolExecutor(8) as ex:
    for res in ex.map(check, keys):
        if res is None: continue
        k, t, l, d, reasons = res; n += 1
        if reasons:
            void(k, t, l, reasons); v += 1; c = mq.cfg_of(l); by[c] = by.get(c, 0) + 1
            log(f"VOID {t} {l} (was {'pass' if d.get('success') else 'fail/pending'}): {'; '.join(reasons)}")
        if n % 100 == 0: log(f"... {n} checked, {v} voided")
log(f"audit done: checked {n} fleet runs, voided {v}; by config: {json.dumps(by, sort_keys=True)}")
