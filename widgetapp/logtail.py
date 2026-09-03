#!/usr/bin/env python3
"""92-log-stream: a live log tail (Datadog / kubectl-logs style) streaming about four lines per second.
The viewer keeps a bounded history and shows the last 40 lines matching the level filter and search box;
Pause freezes the display. Task: report the order id and reason code of the FIRST ERROR-level line from
the `payments` service. It arrives 25 to 55 s after the page opens; an unfiltered screenshot shows only the
last ~10 s of lines, so a sampling agent misses it unless it uses the filter, search, or Pause (or polls
often enough). Traps: payments WARN lines containing "error=", an earlier ERROR from `checkout` with its own
order id, and a SECOND payments ERROR 45 s after the first. complete = submitted order id and reason match."""
import json, random, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base

LEVEL = int(os.environ.get("WIDGET_LEVEL", "1"))
RATE = 4
SVCS = ["api", "checkout", "payments", "auth", "search", "cdn", "inventory"]
MSGS = ["GET /v1/orders 200", "POST /v1/cart 201", "GET /v1/search 200", "token refreshed", "cache hit", "GET /v1/products 200", "session validated",
        "PUT /v1/address 200", "stock check ok", "GET /v1/me 200", "edge purge scheduled", "POST /v1/login 200"]
REASONS = ["card_declined", "insufficient_funds", "gateway_timeout", "fraud_hold", "expired_card", "3ds_failed"]
S = {"seed": 0, "t0": None, "k_target": 0, "k_second": 0, "k_checkout": 0, "k_first": -1, "k_third": -1, "k_corr": -1, "target": None, "submissions": [], "start_wall": 0.0}


def reset():
    S["seed"] = random.randint(1, 10 ** 9); S["t0"] = None; S["submissions"] = []
    rng = random.Random(S["seed"] * 31 + 7)
    S["target"] = {"order": f"ORD-{rng.randint(10000, 99999)}", "reason": rng.choice(REASONS), "req": f"req_{rng.randrange(16 ** 6):06x}"}
    if LEVEL >= 2:
        # three payments ERRORs; only the middle one's req id also appears in an EARLIER checkout WARN
        S["k_first"] = int(RATE * random.uniform(25, 40)); S["k_target"] = int(RATE * random.uniform(55, 75))
        S["k_third"] = S["k_target"] + int(RATE * random.uniform(30, 45)); S["k_second"] = -1
        S["k_corr"] = S["k_target"] - int(RATE * random.uniform(10, 20))
        S["k_checkout"] = S["k_first"] - random.randint(20, 60)
    else:
        S["k_target"] = int(RATE * random.uniform(25, 55)); S["k_second"] = S["k_target"] + 45 * RATE
        S["k_checkout"] = S["k_target"] - random.randint(20, 60); S["k_first"] = S["k_third"] = S["k_corr"] = -1


def line(k):
    rng = random.Random(S["seed"] * 7919 + k)
    ts = time.strftime("%H:%M:%S", time.localtime(S["start_wall"] + k / RATE)) + f".{int((k % RATE) * 1000 / RATE):03d}"
    rid = f"req_{rng.randrange(16 ** 6):06x}"
    if k == S["k_target"]:
        return {"k": k, "ts": ts, "lvl": "ERROR", "svc": "payments", "msg": f"charge failed order={S['target']['order']} reason={S['target']['reason']} req={S['target']['req']}"}
    if k == S["k_corr"]:
        return {"k": k, "ts": ts, "lvl": "WARN", "svc": "checkout", "msg": f"payment pending, will retry order={S['target']['order']} req={S['target']['req']}"}
    if k in (S["k_first"], S["k_third"]) and k >= 0:
        return {"k": k, "ts": ts, "lvl": "ERROR", "svc": "payments", "msg": f"charge failed order=ORD-{rng.randint(10000, 99999)} reason={rng.choice(REASONS)} req={rid}"}
    if LEVEL >= 2 and k % 29 == 3:
        return {"k": k, "ts": ts, "lvl": "WARN", "svc": "checkout", "msg": f"payment pending, will retry order=ORD-{rng.randint(10000, 99999)} req={rid}"}
    if k == S["k_second"]:
        return {"k": k, "ts": ts, "lvl": "ERROR", "svc": "payments", "msg": f"charge failed order=ORD-{rng.randint(10000, 99999)} reason={rng.choice(REASONS)} req={rid}"}
    if k == S["k_checkout"]:
        return {"k": k, "ts": ts, "lvl": "ERROR", "svc": "checkout", "msg": f"cart lock failed order=ORD-{rng.randint(10000, 99999)} reason=lock_timeout req={rid}"}
    if k % 23 == 5:
        return {"k": k, "ts": ts, "lvl": "WARN", "svc": "payments", "msg": f"gateway retry error=timeout attempt={rng.randint(1, 3)} order=ORD-{rng.randint(10000, 99999)} req={rid}"}
    if k % 17 == 11:
        return {"k": k, "ts": ts, "lvl": "WARN", "svc": rng.choice(SVCS), "msg": f"slow response {rng.randint(800, 2400)}ms req={rid}"}
    return {"k": k, "ts": ts, "lvl": "INFO", "svc": rng.choice(SVCS), "msg": f"{rng.choice(MSGS)} user=u{rng.randint(1000, 9999)} {rng.randint(8, 240)}ms req={rid}"}


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path, full):
    if path == "/__lines":
        now = time.time()
        if S["t0"] is None: S["t0"] = now; S["start_wall"] = now
        try: since = int(full.split("since=")[1].split("&")[0])
        except Exception: since = 0
        kmax = int((now - S["t0"]) * RATE)
        ks = range(max(since, kmax - 200), kmax)
        return (json.dumps({"lines": [line(k) for k in ks], "next": kmax}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append({"order": str(data.get("order") or "").strip(), "reason": str(data.get("reason") or "").strip()}); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    t = S["target"]; digits = lambda s: "".join(ch for ch in s if ch.isdigit())
    ok = any(digits(s["order"]) == digits(t["order"]) and s["reason"].lower().replace("-", "_") == t["reason"] for s in S["submissions"])
    return {"level": LEVEL, "target": t, "target_at_s": S["k_target"] / RATE, "second_error_at_s": S["k_second"] / RATE, "checkout_decoy_at_s": S["k_checkout"] / RATE,
            "l2_decoy_errors_at_s": [S["k_first"] / RATE, S["k_third"] / RATE], "l2_correlated_warn_at_s": S["k_corr"] / RATE,
            "opened": S["t0"] is not None, "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Live Tail: prod-web</title>
<style>body{font:13px ui-monospace,Menlo,monospace;margin:0;background:#0b1020;color:#cbd5e1}header{display:flex;gap:12px;align-items:center;padding:10px 14px;background:#111a33;border-bottom:1px solid #1e293b;font-family:system-ui}
select,input,button{font:inherit;background:#0b1020;color:#e2e8f0;border:1px solid #334155;border-radius:6px;padding:5px 8px}button{cursor:pointer}button.on{background:#f59e0b;color:#000;border-color:#f59e0b}
#log{height:560px;overflow:auto;padding:6px 14px}.l{white-space:pre;line-height:1.5}.INFO .lvl{color:#60a5fa}.WARN .lvl{color:#fbbf24}.ERROR .lvl{color:#f87171;font-weight:700}.ERROR{background:rgba(248,113,113,.08)}
.ts{color:#64748b}.svc{color:#a5b4fc}#foot{padding:8px 14px;color:#64748b;font-family:system-ui;display:flex;gap:16px}#ans{padding:12px 14px;border-top:1px solid #1e293b;font-family:system-ui}</style>
<header><b>Live Tail</b> <span>service: prod-web (all pods)</span>
<label>Level <select id=lvl><option>ALL</option><option>INFO</option><option>WARN</option><option>ERROR</option></select></label>
<label>Search <input id=q placeholder="substring" size=18></label><button id=pause>Pause</button><span id=rate></span></header>
<div id=log role=log aria-live=off></div>
<div id=foot><span id=cnt></span><span>showing the latest 40 matching lines</span></div>
<div id=ans><label>Order id <input id=ord size=12></label> <label>Reason <input id=rsn size=18></label> <button id=go>Submit</button> <span id=msg></span></div>
<script>
(function(){
var hist=[],next=0,paused=false,seen=0,t0=Date.now();
function poll(){fetch('/__lines?since='+next).then(r=>r.json()).then(function(j){j.lines.forEach(function(l){hist.push(l)});next=j.next;seen+=j.lines.length;if(hist.length>800)hist=hist.slice(-800);if(!paused)render();
 document.getElementById('rate').textContent=(seen/Math.max(1,(Date.now()-t0)/1000)).toFixed(1)+' lines/s'})}
function render(){var lvl=document.getElementById('lvl').value,q=document.getElementById('q').value.toLowerCase();
 var m=hist.filter(function(l){return (lvl==='ALL'||l.lvl===lvl)&&(!q||(l.ts+' '+l.lvl+' '+l.svc+' '+l.msg).toLowerCase().indexOf(q)>=0)});
 var show=m.slice(-40),el=document.getElementById('log');el.innerHTML=show.map(function(l){return '<div class="l '+l.lvl+'"><span class=ts>'+l.ts+'</span> <span class=lvl>'+l.lvl.padEnd(5)+'</span> <span class=svc>'+l.svc.padEnd(9)+'</span> '+l.msg+'</div>'}).join('');
 el.scrollTop=el.scrollHeight;document.getElementById('cnt').textContent=m.length+' matching of '+hist.length+' buffered'}
document.getElementById('lvl').onchange=render;document.getElementById('q').oninput=render;
document.getElementById('pause').onclick=function(){paused=!paused;this.textContent=paused?'Resume':'Pause';this.className=paused?'on':'';if(!paused)render()};
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({order:document.getElementById('ord').value,reason:document.getElementById('rsn').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
poll();setInterval(poll,400);
})();
</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8812)
