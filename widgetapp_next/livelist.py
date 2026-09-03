#!/usr/bin/env python3
"""80-live-list: a fleet dashboard whose rows REORDER every TICK seconds as CPU figures update (like any
live ops console). Task: restart the server that is using the MOST CPU at the moment you act. The server
records, for each Restart click, which host was top-ranked at that instant. A click from a stale screenshot
lands on a row that has moved; a fresh snapshot + ref click, or reading the current top row and acting
immediately, succeeds. complete = exactly one restart, and its host was the top-CPU host at click time.
Level 2: TICK 4 s and a transient "Restart" confirmation that must be confirmed within 6 s."""
import json, random, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base

LEVEL = int(os.environ.get("WIDGET_LEVEL", "2"))
TICK = 6 if LEVEL == 1 else 4
HOSTS = ["api-01", "api-02", "api-03", "db-primary", "db-replica", "cache-01", "cache-02", "worker-01", "worker-02", "worker-03", "ingest-01", "edge-01"]
S = {"seed": 0, "t0": 0.0, "restarts": [], "confirm_open": None}


def reset():
    S["seed"] = random.randint(1, 10 ** 9); S["t0"] = time.time(); S["restarts"] = []; S["confirm_open"] = None


def _snapshot(t=None):
    """Deterministic CPU figures for the tick containing time t (so client and server agree exactly)."""
    t = time.time() if t is None else t
    tick = int((t - S["t0"]) // TICK)
    rng = random.Random(S["seed"] * 1000003 + tick)
    rows = [{"host": h, "cpu": rng.randint(5, 97), "mem": rng.randint(20, 90), "uptime_d": rng.randint(1, 400)} for h in HOSTS]
    # two hosts always within 3 points of each other at the top, so the max must be read, not guessed
    top2 = rng.sample(range(len(rows)), 2); rows[top2[0]]["cpu"] = 96; rows[top2[1]]["cpu"] = 96 - rng.randint(1, 3)
    rng.shuffle(rows)              # row ORDER is random each tick: position is never a stable handle
    return tick, rows


def render():
    return b""


def click(x, y):
    return {"ignored": True}


def get(path):
    if path == "/__rows":
        tick, rows = _snapshot()
        return (json.dumps({"tick": tick, "tick_s": TICK, "rows": rows}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__restart":
        host = str(data.get("host", "")); tick, rows = _snapshot()
        top = max(rows, key=lambda r: r["cpu"])["host"]
        S["restarts"].append({"host": host, "top_at_click": top, "tick": tick, "cpu_of_host": next((r["cpu"] for r in rows if r["host"] == host), None)})
        return (json.dumps({"ok": True, "restarted": host}), "application/json")
    return None


def state():
    r = S["restarts"]
    return {"level": LEVEL, "tick_s": TICK, "restarts": r,
            "complete": len(r) == 1 and r[0]["host"] == r[0]["top_at_click"]}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Fleet Console</title>
<style>body{font:14px system-ui;margin:0;background:#0f172a;color:#e2e8f0}header{padding:12px 20px;border-bottom:1px solid #1e293b;display:flex;justify-content:space-between}
table{width:100%;border-collapse:collapse}th,td{padding:8px 14px;text-align:left;border-bottom:1px solid #1e293b}th{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#94a3b8}
tr.row{transition:background .2s}tr.row:hover{background:#1e293b}.bar{display:inline-block;height:8px;background:#38bdf8;border-radius:4px;vertical-align:middle;margin-right:8px}.hot{color:#f87171;font-weight:600}
button{font:inherit;padding:4px 10px;border-radius:6px;border:1px solid #475569;background:#1e293b;color:#e2e8f0;cursor:pointer}#confirm{position:fixed;inset:0;background:rgba(0,0,0,.5);display:none}
#confirm .box{background:#0f172a;border:1px solid #334155;width:360px;margin:16% auto;padding:20px;border-radius:8px}#toast{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#1e293b;padding:10px 16px;border-radius:8px;display:none}
.note{color:#94a3b8;font-size:12px}</style>
<header><b>Fleet Console</b><span class=note>Live: metrics refresh every <span id=tick></span> s and the table reorders. <span id=age></span></span></header>
<table><thead><tr><th>#</th><th>Host</th><th>CPU</th><th>Mem</th><th>Uptime</th><th></th></tr></thead><tbody id=tb></tbody></table>
<div id=confirm role=dialog><div class=box><h3 style="margin-top:0">Restart <span id=chost></span>?</h3><p class=note>This dialog closes on its own after 6 seconds.</p><button id=cyes>Confirm restart</button> <button id=cno>Cancel</button></div></div>
<div id=toast role=status></div>
<script>
var LEVEL=__LEVEL__,cur=null,pending=null,ctimer=null,lastTick=-1,lastAt=0;
function load(){fetch('/__rows').then(r=>r.json()).then(j=>{document.getElementById('tick').textContent=j.tick_s;if(j.tick!==lastTick){lastTick=j.tick;lastAt=Date.now();render(j.rows)}})}
function render(rows){var tb=document.getElementById('tb');tb.innerHTML='';rows.forEach((r,i)=>{var tr=document.createElement('tr');tr.className='row';tr.innerHTML='<td>'+(i+1)+'</td><td>'+r.host+'</td><td><span class=bar style="width:'+r.cpu+'px"></span><span class="'+(r.cpu>=80?'hot':'')+'">'+r.cpu+'%</span></td><td>'+r.mem+'%</td><td>'+r.uptime_d+' d</td><td><button data-h="'+r.host+'" aria-label="Restart '+r.host+'">Restart</button></td>';tb.appendChild(tr)});
 tb.querySelectorAll('button').forEach(b=>b.onclick=function(){var h=this.dataset.h;if(LEVEL<2){restart(h);return}pending=h;document.getElementById('chost').textContent=h;document.getElementById('confirm').style.display='block';clearTimeout(ctimer);ctimer=setTimeout(function(){document.getElementById('confirm').style.display='none';pending=null},6000)})}
function restart(h){fetch('/__restart',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({host:h})}).then(r=>r.json()).then(j=>{var t=document.getElementById('toast');t.textContent='Restart requested for '+j.restarted;t.style.display='block';setTimeout(()=>t.style.display='none',3000)})}
document.getElementById('cyes').onclick=function(){if(pending){restart(pending)}document.getElementById('confirm').style.display='none';pending=null;clearTimeout(ctimer)};
document.getElementById('cno').onclick=function(){document.getElementById('confirm').style.display='none';pending=null;clearTimeout(ctimer)};
setInterval(function(){document.getElementById('age').textContent='(last refresh '+Math.round((Date.now()-lastAt)/1000)+' s ago)'},500);
load();setInterval(load,700);
</script>"""


def page():
    return PAGE.replace("__LEVEL__", str(LEVEL))


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8800)
