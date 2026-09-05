#!/usr/bin/env python3
"""Localhost dashboard for the final-set matrix sweep. Refreshes a snapshot of the S3 queue every 30 s (cached done
markers; only unjudged ones are re-read) and serves: per-config scoreboard, running runs, task x config grid,
recent completions, failures/blocked, judge log. http://127.0.0.1:8600/  (JSON at /api)"""
import os, sys, json, time, threading, html
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ".")
os.environ.setdefault("MATRIX_STORE", "s3://webbench-matrix-966239516827/final63")
import matrix_queue as mq
S = mq.store(); CONFIGS = mq.CONFIGS; TASKS = mq.final_tasks(); LEASE_S = mq.LEASE_S
SNAP = {"ts": 0, "cells": {}, "workers": [], "recent": [], "failed": [], "blocked": [], "summary": {}}; CACHE = {}
def getj(k):
    try: return json.loads(S.get(k) or b"{}")
    except Exception: return {}
def refresh():
    pend = {k.split("/", 1)[1] for k in S.list("pending/")}; claims = {k.split("/", 1)[1]: k for k in S.list("claims/")}
    done_keys = S.list("done/"); failed = S.list("failed/"); blocked = S.list("blocked/")
    todo = [k for k in done_keys if k not in CACHE or (CACHE[k].get("needs_judge") and CACHE[k].get("success") is None)]
    with ThreadPoolExecutor(16) as ex:
        for k, d in zip(todo, ex.map(getj, todo)): CACHE[k] = d
        claim_d = dict(zip(claims.values(), ex.map(getj, list(claims.values()))))
        fb = dict(zip(failed + blocked, ex.map(getj, failed + blocked)))
    now = time.time(); cells = {}; workers = []
    for kk in pend:
        t, l = kk.split("__"); c = mq.cfg_of(l); st = "pending"
        if kk in claims and now - claim_d[claims[kk]].get("ts", 0) <= LEASE_S:
            st = "running"; cd = claim_d[claims[kk]]; workers.append({"worker": cd.get("worker"), "host": cd.get("host"), "task": t, "config": c, "age": int(now - cd.get("ts", now))})
        cells[(t, c)] = {"state": st}
    for k in done_keys:
        d = CACHE.get(k, {}); t, l = k.split("/", 1)[1].split("__"); c = mq.cfg_of(l)
        st = "pass" if d.get("success") is True else ("judge" if (d.get("needs_judge") and d.get("success") is None) else ("blocked" if d.get("blocked") else "fail"))
        cells[(t, c)] = {"state": st, "cli": d.get("cli_calls"), "wall": d.get("wall_s"), "worker": d.get("worker"), "ts": d.get("ts"), "note": d.get("judge_note", "")}
    fl = []; bl = []
    for k in failed:
        t, l = k.split("/", 1)[1].split("__"); d = fb.get(k, {})
        if d.get("attempts", 0) >= mq.MAX_TRIES: cells[(t, mq.cfg_of(l))] = {"state": "failed"}; fl.append({"task": t, "config": mq.cfg_of(l), **d})
        else: cells.setdefault((t, mq.cfg_of(l)), {"state": "pending"})["retries"] = d.get("attempts")
    for k in blocked: t, l = k.split("/", 1)[1].split("__"); bl.append({"task": t, "config": mq.cfg_of(l), **fb.get(k, {})}); cells.setdefault((t, mq.cfg_of(l)), {"state": "pending"})["blk"] = fb.get(k, {}).get("count")
    summary = {}
    for c in CONFIGS:
        s = {"pass": 0, "fail": 0, "judge": 0, "running": 0, "pending": 0, "failed": 0, "blocked": 0}
        for t in TASKS: s[cells.get((t, c), {"state": "pending"})["state"]] = s.get(cells.get((t, c), {"state": "pending"})["state"], 0) + 1
        s["done"] = s["pass"] + s["fail"] + s["judge"] + s["blocked"]; s["rate"] = (100 * s["pass"] / (s["pass"] + s["fail"])) if (s["pass"] + s["fail"]) else None; summary[c] = s
    recent = sorted([{"task": t, "config": c, **v} for (t, c), v in cells.items() if v.get("ts")], key=lambda x: -x["ts"])[:40]
    SNAP.update(ts=now, cells={f"{t}|{c}": v for (t, c), v in cells.items()}, workers=sorted(workers, key=lambda w: w["config"]), recent=recent, failed=fl, blocked=bl, summary=summary)
def loop():
    while True:
        try: refresh()
        except Exception as e: SNAP["error"] = f"{type(e).__name__}: {e}"
        time.sleep(30)
COLORS = {"pass": "#22c55e", "fail": "#ef4444", "judge": "#a78bfa", "running": "#f59e0b", "pending": "#e5e7eb", "failed": "#7f1d1d", "blocked": "#0ea5e9"}
def page():
    s = SNAP; e = html.escape; age = int(time.time() - s["ts"]) if s["ts"] else None
    tot = {k: sum(v[k] for v in s["summary"].values()) for k in ("pass", "fail", "judge", "running", "pending", "failed", "blocked", "done")} if s["summary"] else {}
    out = [f"""<!doctype html><meta charset=utf-8><meta http-equiv=refresh content=30><title>Matrix sweep</title>
<style>body{{font:13px system-ui;margin:16px;color:#111;background:#fff}}h1{{font-size:18px;margin:0 0 4px}}h2{{font-size:15px;margin:18px 0 6px}}table{{border-collapse:collapse}}td,th{{padding:3px 8px;border-bottom:1px solid #eee;text-align:right;white-space:nowrap}}th{{background:#f8fafc;position:sticky;top:0}}td:first-child,th:first-child{{text-align:left}}
.grid td{{padding:0;width:16px;height:16px;border:1px solid #fff}}.grid th{{font-size:10px;padding:2px}}.grid td:first-child{{width:auto;font-size:11px;padding:0 6px;text-align:left}}.legend span{{display:inline-block;padding:2px 8px;margin-right:6px;border-radius:3px;color:#fff}}small{{color:#666}}</style>
<h1>Final-set matrix sweep <small>{len(TASKS)} tasks x {len(CONFIGS)} configs, pass@1</small></h1><small>snapshot {age if age is not None else '?'} s ago, refreshes every 30 s. {e(s.get('error',''))}</small>
<h2>Totals</h2><p>done <b>{tot.get('done',0)}</b> (pass {tot.get('pass',0)}, fail {tot.get('fail',0)}, awaiting judge {tot.get('judge',0)}, blocked {tot.get('blocked',0)}) · running <b>{tot.get('running',0)}</b> · pending {tot.get('pending',0)} · gave up {tot.get('failed',0)}</p>
<h2>Per config</h2><table><tr><th>config</th><th>done</th><th>pass</th><th>fail</th><th>judge</th><th>pass rate</th><th>running</th><th>pending</th><th>gave up</th></tr>"""]
    for c, v in s["summary"].items(): out.append(f"<tr><td>{c}</td><td>{v['done']}</td><td style=color:#15803d>{v['pass']}</td><td style=color:#b91c1c>{v['fail']}</td><td>{v['judge']}</td><td><b>{'' if v['rate'] is None else f'{v['rate']:.0f}%'}</b></td><td>{v['running']}</td><td>{v['pending']}</td><td>{v['failed']}</td></tr>")
    out.append("</table><h2>Running now</h2><table><tr><th>worker</th><th>task</th><th>config</th><th>lease age</th></tr>")
    for w in s["workers"]: out.append(f"<tr><td>{e(str(w['worker']))}</td><td style=text-align:left>{e(w['task'])}</td><td style=text-align:left>{e(w['config'])}</td><td>{w['age']} s</td></tr>")
    out.append("</table><h2>Task x config</h2><div class=legend>" + "".join(f"<span style=background:{COLORS[k]}>{k}</span>" for k in COLORS) + "</div><table class=grid><tr><th></th>" + "".join(f"<th>{c.replace('gemini-3.8-flash','gem').replace('spark13','sp13')}</th>" for c in CONFIGS) + "</tr>")
    for t in TASKS:
        out.append(f"<tr><td>{e(t)}</td>")
        for c in CONFIGS:
            v = s["cells"].get(f"{t}|{c}", {"state": "pending"}); tip = f"{t} / {c}: {v['state']}" + (f", {v.get('cli')} cli calls, {v.get('wall')} s" if v.get("cli") is not None else "") + (f", {v.get('note')}" if v.get("note") else "")
            out.append(f"<td style=background:{COLORS[v['state']]} title=\"{e(tip)}\"></td>")
        out.append("</tr>")
    out.append("</table><h2>Recent completions</h2><table><tr><th>when</th><th>task</th><th>config</th><th>result</th><th>cli calls</th><th>wall s</th><th>worker</th></tr>")
    for r in s["recent"]: out.append(f"<tr><td>{time.strftime('%H:%M:%S', time.localtime(r['ts']))}</td><td style=text-align:left>{e(r['task'])}</td><td style=text-align:left>{e(r['config'])}</td><td style=color:{COLORS[r['state']]}><b>{r['state']}</b></td><td>{r.get('cli','')}</td><td>{r.get('wall','')}</td><td>{e(str(r.get('worker','')))}</td></tr>")
    out.append("</table>")
    if s["failed"] or s["blocked"]:
        out.append("<h2>Gave up / blocked</h2><table><tr><th>task</th><th>config</th><th>attempts</th><th>last</th></tr>")
        for r in s["failed"] + s["blocked"]: out.append(f"<tr><td>{e(r['task'])}</td><td style=text-align:left>{e(r['config'])}</td><td>{r.get('attempts', r.get('count'))}</td><td style=text-align:left>{e(str(r.get('last_error','')))[:120]}</td></tr>")
        out.append("</table>")
    try: jl = open("results/judge_daemon.log").read().splitlines()[-25:]
    except FileNotFoundError: jl = ["(judge daemon log not found)"]
    out.append("<h2>Judge daemon</h2><pre style=font-size:12px>" + e("\n".join(jl)) + "</pre>")
    return "".join(out)
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        body = (json.dumps(SNAP, default=str) if self.path.startswith("/api") else page()).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json" if self.path.startswith("/api") else "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
if __name__ == "__main__":
    threading.Thread(target=loop, daemon=True).start(); port = int(os.environ.get("PORT", "8600")); print(f"dashboard on http://127.0.0.1:{port}/", flush=True); HTTPServer(("127.0.0.1", port), H).serve_forever()
