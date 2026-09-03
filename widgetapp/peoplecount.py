#!/usr/bin/env python3
"""179-people-count: a 2-minute lobby camera clip (canvas video) with 16-24 people crossing in both directions,
several within a second of each other, plus a cleaning cart. Task: exact number of people who crossed. Counting
over time with overlaps. complete = exact (last submission)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
DUR = 120
S = {"events": [], "answer": 0, "submissions": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset():
    S["submissions"] = []; n = random.randint(16, 24); ts = [random.uniform(3, 112) for _ in range(n)]
    for _ in range(4): ts.append(random.choice(ts) + random.uniform(0.4, 1.2))     # near-simultaneous crossings
    ts = sorted(t for t in ts if t < 114)[:n]
    ev = [{"t": round(t, 1), "kind": "person", "dir": random.choice([1, -1]), "color": random.choice(COLORS), "h": random.randint(60, 84)} for t in ts]
    ev.append({"t": round(random.uniform(20, 100), 1), "kind": "cart", "dir": random.choice([1, -1]), "color": "#9ca3af", "h": 50})
    ev.sort(key=lambda e: e["t"]); S["events"] = ev; S["answer"] = sum(1 for e in ev if e["kind"] == "person")


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"dur": DUR, "events": S["events"]}), "application/json")
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
    return {"answer": S["answer"], "events": S["events"], "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Lobby camera clip</title>
<style>body{font:14px system-ui;margin:0;background:#111827;color:#e5e7eb}#wrap{width:800px;margin:0 auto;padding:14px}h1{font-size:17px;margin:0 0 8px}canvas{display:block;background:#000}
#bar{display:flex;gap:8px;align-items:center;margin-top:8px}button,select{font:inherit;background:#374151;color:#e5e7eb;border:0;border-radius:6px;padding:6px 10px;cursor:pointer}input[type=range]{flex:1}
#ans{margin-top:16px;padding:12px;background:#1f2937;border-radius:8px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #4b5563;background:#111827;color:#e5e7eb}</style>
<div id=wrap><h1>Lobby camera, east corridor (clip, 2:00)</h1><canvas id=v width=800 height=450></canvas>
<div id=bar><button id=pp>Play</button><button id=bm10>-10 s</button><button id=bm1>-1 s</button><button id=bp1>+1 s</button><button id=bp10>+10 s</button><span id=tm>0:00 / 2:00</span><input id=seek type=range min=0 max=120 step=0.5 value=0 aria-label="Seek"><select id=spd><option value=1>1x</option><option value=2>2x</option><option value=4>4x</option><option value=0.5>0.5x</option></select></div>
<div id=ans><label>How many PEOPLE crossed the corridor during the clip (not the cart)? <input id=c type=text size=6></label> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>(function(){var D=null,pos=0,base=0,t0=Date.now(),playing=false,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d');var PASS={person:4.5,cart:9};
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function rr(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.arcTo(x+w,y,x+w,y+h,r);cx.arcTo(x+w,y+h,x,y+h,r);cx.arcTo(x,y+h,x,y,r);cx.arcTo(x,y,x+w,y,r);cx.closePath();cx.fill()}
function person(e,x,y,t){cx.fillStyle=e.color;cx.beginPath();cx.arc(x+12,y-e.h+12,11,0,6.28);cx.fill();rr(x+2,y-e.h+24,20,e.h*0.5,6);var sw=Math.sin(t*8)*6;cx.fillRect(x+4,y-e.h*0.5+24,7,e.h*0.45+sw);cx.fillRect(x+13,y-e.h*0.5+24,7,e.h*0.45-sw)}
function cart(e,x,y){cx.fillStyle=e.color;cx.fillRect(x,y-50,70,40);cx.fillStyle='#374151';cx.beginPath();cx.arc(x+12,y-6,8,0,6.28);cx.arc(x+58,y-6,8,0,6.28);cx.fill();cx.fillStyle='#fbbf24';cx.fillRect(x+20,y-70,6,20);cx.fillRect(x+44,y-70,6,20)}
function scene(t){var g=cx.createLinearGradient(0,0,0,450);g.addColorStop(0,'#e5e7eb');g.addColorStop(1,'#9ca3af');cx.fillStyle=g;cx.fillRect(0,0,800,450);cx.fillStyle='#d1d5db';cx.fillRect(0,250,800,200);cx.fillStyle='#6b7280';for(var x=0;x<800;x+=100)cx.fillRect(x,250,2,200);
 cx.fillStyle='#374151';cx.fillRect(120,60,90,190);cx.fillRect(590,60,90,190);cx.fillStyle='#93c5fd';cx.fillRect(130,70,70,120);cx.fillRect(600,70,70,120);
 D.events.forEach(function(e){var P=PASS[e.kind],dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x=e.dir>0?-40+f*880:840-f*880;if(e.kind==='person')person(e,x,380+(e.h%3)*12,t);else cart(e,x,400)});
 cx.fillStyle='rgba(0,0,0,.65)';cx.fillRect(10,10,330,30);cx.fillStyle='#fff';cx.font='bold 18px ui-monospace,Menlo,monospace';cx.fillText('LOBBY-E  '+fmt(t),18,32);
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
    base.serve(sys.modules[__name__], 8863)
