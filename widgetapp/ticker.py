#!/usr/bin/env python3
"""93-ticker-tape: a markets page with a continuously scrolling canvas ticker (24 symbols, ~40 s per loop,
about six symbols visible at once; hovering pauses it, like most web tickers). Task: name the symbol with
the LARGEST percentage gain on the ticker and its percentage. Reading the answer needs coverage of the
whole loop (the two best gainers sit far apart on the tape and differ by under half a point) or the hover
pause. Trap: a "Watchlist (delayed 15 min)" table on the page lists a symbol with a bigger stale gain.
complete = submitted symbol is the true top gainer (percentage within 0.15)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base

SYMS = ["ACME", "BRKT", "CNDL", "DLTA", "EQNX", "FRGE", "GLXY", "HRBR", "IONQ", "JNPR", "KTLA", "LMNR", "MRDN", "NBLE", "ORCH", "PLTF", "QNTM", "RVRA", "SLTN", "TRNT", "ULTR", "VRTX", "WLDN", "ZPHR"]
S = {"tape": [], "answer": None, "watch": [], "submissions": []}


def reset():
    S["submissions"] = []
    while True:
        tape = [{"sym": s, "px": round(random.uniform(4, 900), 2), "pct": round(random.uniform(-5.5, 4.0), 2)} for s in SYMS]
        i, j = random.sample(range(len(SYMS)), 2)
        if min(abs(i - j), len(SYMS) - abs(i - j)) < 8: continue
        top = round(random.uniform(4.5, 7.9), 2); tape[i]["pct"] = top; tape[j]["pct"] = round(top - random.uniform(0.2, 0.45), 2)
        if all(t["pct"] < tape[j]["pct"] for k, t in enumerate(tape) if k not in (i, j)): break
    S["tape"] = tape; S["answer"] = tape[i]
    # delayed watchlist: six symbols with stale numbers, one of them showing a bigger (stale) gain than the true top
    ws = random.sample([t for k, t in enumerate(tape) if k not in (i, j)], 5) + [tape[j]]
    random.shuffle(ws)
    S["watch"] = [{"sym": t["sym"], "px": round(t["px"] * random.uniform(0.97, 1.03), 2), "pct": round(t["pct"] + random.uniform(-1.5, 1.5), 2)} for t in ws]
    S["watch"][random.randrange(6)]["pct"] = round(top + random.uniform(0.6, 1.8), 2)


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"tape": S["tape"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append({"sym": str(data.get("sym") or "").strip().upper(), "pct": str(data.get("pct") or "").strip()}); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    a = S["answer"]; ok = False
    for s in S["submissions"]:
        try: p = float(s["pct"].replace("%", "").replace("+", ""))
        except ValueError: continue
        if s["sym"] == a["sym"] and abs(p - a["pct"]) <= 0.15: ok = True
    return {"answer": a, "runner_up": sorted(S["tape"], key=lambda t: -t["pct"])[1], "watchlist": S["watch"], "submissions": S["submissions"], "complete": ok}


def page():
    rows = "".join(f"<tr><td>{w['sym']}</td><td>{w['px']:.2f}</td><td class={'up' if w['pct'] >= 0 else 'dn'}>{w['pct']:+.2f}%</td></tr>" for w in S["watch"])
    return PAGE.replace("__ROWS__", rows)


PAGE = r"""<!doctype html><meta charset=utf-8><title>Harbor Markets</title>
<style>body{font:15px system-ui;margin:0;background:#fff;color:#111}#tape{display:block;width:1280px;height:64px;background:#0b1020;cursor:default}
main{max-width:1100px;margin:0 auto;padding:20px}h1{font-size:22px}table{border-collapse:collapse;margin-top:8px}td,th{padding:6px 14px;border-bottom:1px solid #e5e7eb;text-align:right;font-variant-numeric:tabular-nums}th:first-child,td:first-child{text-align:left}
.up{color:#15803d}.dn{color:#b91c1c}.note{color:#6b7280;font-size:13px}article{margin-top:24px;max-width:70ch;color:#374151}#ans{margin-top:24px;padding:14px;background:#f3f4f6;border-radius:8px}input,button{font:inherit;padding:6px 8px}</style>
<canvas id=tape width=1280 height=64 aria-label="live ticker"></canvas>
<main><h1>Harbor Markets</h1><p class=note>The tape above is live. Hover over it to pause.</p>
<h2 style="font-size:17px">Watchlist <span class=note>(delayed 15 min)</span></h2><table><tr><th>Symbol</th><th>Last</th><th>Chg</th></tr>__ROWS__</table>
<article><h2 style="font-size:17px">Midday note</h2><p>Stocks were mixed through the morning session as traders weighed the latest inventory data against a softer services print. Volume ran slightly below the 20-day average. Energy names lagged while a handful of small caps posted outsized moves on earnings.</p></article>
<div id=ans><b>Top gainer on the tape:</b> <label>Symbol <input id=sym size=6></label> <label>% change <input id=pct size=8></label> <button id=go>Submit</button> <span id=msg></span></div></main>
<script>
(function(){var cv=document.getElementById('tape'),cx=cv.getContext('2d'),tape=null,off=0,base=0,t0=Date.now(),paused=false,W=200;
function draw(){if(tape){if(!paused)off=(base+120*(Date.now()-t0)/1000)%(tape.length*W);cx.fillStyle='#0b1020';cx.fillRect(0,0,1280,64);cx.font='bold 20px system-ui';cx.textBaseline='middle';
 for(var i=0;i<tape.length;i++){var x=i*W-off;if(x<-W)x+=tape.length*W;if(x>1280)continue;var t=tape[i],up=t.pct>=0;cx.fillStyle='#e5e7eb';cx.fillText(t.sym,x+10,24);cx.fillStyle='#cbd5e1';cx.font='18px system-ui';cx.fillText(t.px.toFixed(2),x+10,46);
 cx.fillStyle=up?'#22c55e':'#ef4444';cx.font='bold 18px system-ui';cx.fillText((up?'▲ +':'▼ ')+t.pct.toFixed(2)+'%',x+90,46);cx.font='bold 20px system-ui';cx.fillStyle='#1e293b';cx.fillRect(x+W-2,8,1,48)}}
 }
fetch('/__data').then(r=>r.json()).then(function(j){tape=j.tape;t0=Date.now();setInterval(draw,40)});
cv.onmouseenter=function(){base=off;paused=true};cv.onmouseleave=function(){base=off;t0=Date.now();paused=false};
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sym:document.getElementById('sym').value,pct:document.getElementById('pct').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
})();
</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8813)
