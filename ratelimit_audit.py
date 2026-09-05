#!/usr/bin/env python3
"""Audit fleet runs for provider rate limits (rule: such runs are void). Scans done markers written by fleet workers
whose stream has not been checked yet, downloads the stream from S3, and on a hit: moves the run's artifacts to
voided/ratelimited/, removes the done marker and any verdict, and re-adds the item to pending. State in
results/ratelimit_audit.json. Usage: ratelimit_audit.py [--loop]"""
import os, sys, json, time, datetime, tempfile
sys.path.insert(0, "."); import matrix_queue as mq, ratelimit, harness
S = mq.store(); STATE = "results/ratelimit_audit.json"; LOG = "results/ratelimit_audit.log"
def log(m): line = f"{datetime.datetime.now().strftime('%H:%M:%S')} {m}"; print(line, flush=True); open(LOG, "a").write(line + "\n")
def void(k, t, l, marks):
    kk = mq.key(t, l)
    for key in S.list(f"raw/{t}.{l}.") + S.list(f"results/{t}/{l}."):
        data = S.get(key)
        if data is not None and not key.endswith(".mp4"): S.put(f"voided/ratelimited/{key}", data)
        S.delete(key)
    S.delete(k); S.delete(f"verdicts/{kk}"); S.put(f"pending/{kk}", mq.j({"task": t, "label": l, "lane": mq.lane_of(t)}))
    v = harness._verdicts()
    if f"{t}.{l}" in v: del v[f"{t}.{l}"]; harness.VERDICTS.write_text(json.dumps(v, indent=1))
    for f in (f"raw/{t}.{l}.json", f"results/{t}/{l}.json"):
        if os.path.exists(f): os.remove(f)
    log(f"VOID {t} {l}: rate limit in stream {marks[:2]}; requeued")
def once():
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"checked": {}}
    n = v = 0
    for k in S.list("done/"):
        d = json.loads(S.get(k) or b"{}")
        if not str(d.get("worker", "")).startswith("i-") or k in st["checked"]: continue
        t, l = d["task"], d["label"]; key = f"raw/{t}.{l}.stream.txt"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tf: path = tf.name
        try:
            S.get_file(key, path); marks = ratelimit.hits(path)
            if not marks and d.get("cost_usd") is None:   # backfill the run's cost while the stream is at hand
                import run_cost; rp = f"raw/{t}.{l}.json"
                if not os.path.exists(rp): S.get_file(rp, rp)
                c = run_cost.cost(rp, path)
                if c is not None: d["cost_usd"] = c; S.put(k, mq.j(d))
        except Exception as e: marks = []; log(f"no stream for {t} {l}: {type(e).__name__}")
        finally:
            try: os.remove(path)
            except OSError: pass
        st["checked"][k] = {"ts": time.time(), "hits": marks}; n += 1
        if marks: void(k, t, l, marks); v += 1
        json.dump(st, open(STATE, "w"))
    return n, v
if __name__ == "__main__":
    log("audit start")
    while True:
        n, v = once(); log(f"checked {n} new runs, voided {v}")
        if "--loop" not in sys.argv: break
        time.sleep(600)
