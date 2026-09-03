#!/usr/bin/env python3
"""185-belt-defects: a conveyor-belt inspection clip (canvas video, 2 min): 30-40 bottles pass; some have a visible
defect (a missing cap). Task: how many defective bottles passed. Counting a visual detail over time. complete =
exact (last submission)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
DUR = 120
S = {"items": [], "answer": 0, "submissions": []}


def reset():
    S["submissions"] = []; n = random.randint(30, 40); ts = sorted(random.uniform(2, 115) for _ in range(n))
    items = [{"t": round(t, 1), "bad": random.random() < 0.25} for t in ts]; S["items"] = items; S["answer"] = sum(1 for i in items if i["bad"])


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"dur": DUR, "items": S["items"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("count") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    ok = False
    if S["submissions"]:
        try: ok = int(float(S["submissions"][-1])) == S["answer"]
        except ValueError: ok = False
    return {"answer": S["answer"], "total": len(S["items"]), "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Line 3 inspection clip</title>
<style>body{font:14px system-ui;margin:0;background:#111827;color:#e5e7eb}#wrap{width:800px;margin:0 auto;padding:14px}h1{font-size:17px;margin:0 0 8px}canvas{display:block;background:#000}
#bar{display:flex;gap:8px;align-items:center;margin-top:8px}button,select{font:inherit;background:#374151;color:#e5e7eb;border:0;border-radius:6px;padding:6px 10px;cursor:pointer}input[type=range]{flex:1}
#ans{margin-top:16px;padding:12px;background:#1f2937;border-radius:8px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #4b5563;background:#111827;color:#e5e7eb}</style>
<div id=wrap><h1>Bottling line 3, capper outfeed (clip, 2:00)</h1><canvas id=v width=800 height=450></canvas>
<div id=bar><button id=pp>Play</button><button id=bm10>-10 s</button><button id=bm1>-1 s</button><button id=bp1>+1 s</button><button id=bp10>+10 s</button><span id=tm>0:00 / 2:00</span><input id=seek type=range min=0 max=120 step=0.5 value=0 aria-label="Seek"><select id=spd><option value=1>1x</option><option value=2>2x</option><option value=4>4x</option><option value=0.5>0.5x</option></select></div>
<div id=ans><label>How many bottles passed WITHOUT a cap (defective)? <input id=c type=text size=6></label> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>(function(){var D=null,pos=0,base=0,t0=Date.now(),playing=false,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d');var P=5;
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function bottle(x,bad){cx.fillStyle='#93c5fd';cx.fillRect(x,230,44,120);cx.fillRect(x+12,200,20,34);cx.fillStyle='#1d4ed8';cx.fillRect(x+4,290,36,40);if(!bad){cx.fillStyle='#dc2626';cx.fillRect(x+10,190,24,14)}}
function scene(t){cx.fillStyle='#374151';cx.fillRect(0,0,800,450);cx.fillStyle='#6b7280';cx.fillRect(0,350,800,40);cx.fillStyle='#9ca3af';var off=(t*160)%40;for(var x=-40+off;x<800;x+=40)cx.fillRect(x,352,20,36);cx.fillStyle='#1f2937';cx.fillRect(0,390,800,60);
 D.items.forEach(function(it){var dt=t-it.t;if(dt<0||dt>P)return;bottle(-60+(dt/P)*900,it.bad)});
 cx.fillStyle='rgba(0,0,0,.65)';cx.fillRect(10,10,330,30);cx.fillStyle='#fff';cx.font='bold 18px ui-monospace,Menlo,monospace';cx.fillText('LINE-3 CAPPER  '+fmt(t),18,32);
 if(!playing){cx.fillStyle='rgba(0,0,0,.55)';cx.fillRect(700,10,90,30);cx.fillStyle='#fff';cx.font='bold 15px system-ui';cx.fillText('PAUSED',714,31)}}
function draw(){if(!D)return;scene(pos);document.getElementById('tm').textContent=fmt(pos)+' / '+fmt(D.dur);document.getElementById('seek').value=pos}
function step(){if(playing){pos=base+rate*(Date.now()-t0)/1000;if(pos>=D.dur){pos=D.dur;base=pos;playing=false;document.getElementById('pp').textContent='Play'}}draw()}
function tick(){step();requestAnimationFrame(tick)}function seek(t){pos=Math.max(0,Math.min(D.dur,t));base=pos;t0=Date.now();draw()}
fetch('/__data').then(r=>r.json()).then(function(j){D=j;t0=Date.now();setInterval(step,100);requestAnimationFrame(tick)});
document.getElementById('pp').onclick=function(){base=pos;t0=Date.now();playing=!playing;this.textContent=playing?'Pause':'Play'};
document.getElementById('bm10').onclick=function(){seek(pos-10)};document.getElementById('bp10').onclick=function(){seek(pos+10)};document.getElementById('bm1').onclick=function(){seek(pos-1)};document.getElementById('bp1').onclick=function(){seek(pos+1)};
var sk=document.getElementById('seek');sk.oninput=sk.onchange=function(){seek(+this.value)};document.getElementById('spd').onchange=function(){base=pos;t0=Date.now();rate=+this.value};
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({count:document.getElementById('c').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8868)
