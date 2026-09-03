#!/usr/bin/env python3
"""139-traffic-count: a 2-minute traffic-camera clip (canvas video); vehicles pass in both directions at random
times, some close together, and a few pedestrians. Task: how many vehicles passed in total (exact). Counting over
time requires watching or stepping through the whole clip; the timeline has NO motion markers this time.
complete = exact count."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
DUR = 120
S = {"events": [], "answer": 0, "submissions": []}


def reset():
    S["submissions"] = []; n = random.randint(9, 14); ts = sorted(random.uniform(4, 114) for _ in range(n))
    ev = [{"t": round(t, 1), "kind": random.choice(["car", "car", "van"]), "dir": random.choice([1, -1]), "color": random.choice(["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280"])} for t in ts]
    for _ in range(3): ev.append({"t": round(random.uniform(4, 114), 1), "kind": "person", "dir": random.choice([1, -1]), "color": "#9ca3af"})
    ev.sort(key=lambda e: e["t"]); S["events"] = ev; S["answer"] = n


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


PAGE = r"""<!doctype html><meta charset=utf-8><title>Traffic camera clip</title>
<style>body{font:14px system-ui;margin:0;background:#111827;color:#e5e7eb}#wrap{width:800px;margin:0 auto;padding:14px}h1{font-size:17px;margin:0 0 8px}canvas{display:block;background:#000}
#bar{display:flex;gap:8px;align-items:center;margin-top:8px}button,select{font:inherit;background:#374151;color:#e5e7eb;border:0;border-radius:6px;padding:6px 10px;cursor:pointer}input[type=range]{flex:1}
#ans{margin-top:16px;padding:12px;background:#1f2937;border-radius:8px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #4b5563;background:#111827;color:#e5e7eb}</style>
<div id=wrap><h1>Traffic camera, Mill Rd (clip, 2:00)</h1><canvas id=v width=800 height=450></canvas>
<div id=bar><button id=pp>Play</button><button id=bm10>-10 s</button><button id=bm1>-1 s</button><button id=bp1>+1 s</button><button id=bp10>+10 s</button><span id=tm>0:00 / 2:00</span><input id=seek type=range min=0 max=120 step=0.5 value=0 aria-label="Seek"><select id=spd><option value=1>1x</option><option value=2>2x</option><option value=4>4x</option><option value=8>8x</option></select></div>
<div id=ans><label>How many vehicles (cars and vans, not pedestrians) passed during the clip? <input id=c type=text size=6></label> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>(function(){var D=null,pos=0,base=0,t0=Date.now(),playing=false,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d');var LEN={car:120,van:150,person:24},PASS={car:5,van:6,person:12};
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function rr(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.arcTo(x+w,y,x+w,y+h,r);cx.arcTo(x+w,y+h,x,y+h,r);cx.arcTo(x,y+h,x,y,r);cx.arcTo(x,y,x+w,y,r);cx.closePath();cx.fill()}
function wheel(x,y){cx.fillStyle='#111';cx.beginPath();cx.arc(x,y,12,0,6.28);cx.fill();cx.fillStyle='#9ca3af';cx.beginPath();cx.arc(x,y,5,0,6.28);cx.fill()}
function vehicle(e,x,y){cx.fillStyle=e.color;if(e.kind==='car'){rr(x,y,120,38,8);rr(x+28,y-26,60,30,8);cx.fillStyle='#93c5fd';cx.fillRect(x+34,y-20,20,18);cx.fillRect(x+62,y-20,20,18);wheel(x+26,y+40);wheel(x+94,y+40)}else if(e.kind==='van'){rr(x,y-30,150,68,6);cx.fillStyle='#93c5fd';cx.fillRect(x+110,y-20,28,18);wheel(x+30,y+40);wheel(x+120,y+40)}else{cx.fillStyle=e.color;cx.beginPath();cx.arc(x+12,y-12,10,0,6.28);cx.fill();rr(x+3,y,18,34,5);cx.fillRect(x+5,y+34,6,22);cx.fillRect(x+14,y+34,6,22)}}
function scene(t){var g=cx.createLinearGradient(0,0,0,450);g.addColorStop(0,'#1e293b');g.addColorStop(1,'#334155');cx.fillStyle=g;cx.fillRect(0,0,800,450);cx.fillStyle='#475569';[[20,120,110,160],[150,90,90,190],[260,140,140,140],[420,100,120,180],[560,130,100,150],[680,110,110,170]].forEach(function(b){cx.fillRect(b[0],b[1],b[2],b[3])});
 cx.fillStyle='#6b7280';cx.fillRect(0,280,800,20);cx.fillStyle='#374151';cx.fillRect(0,300,800,150);cx.fillStyle='#e5e7eb';for(var x=0;x<800;x+=80)cx.fillRect(x,372,40,4);
 D.events.forEach(function(e){var L=LEN[e.kind],P=PASS[e.kind],dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x=e.dir>0?-L+f*(800+2*L):800-f*(800+2*L);vehicle(e,x,e.dir>0?345:315)});
 cx.fillStyle='rgba(0,0,0,.65)';cx.fillRect(10,10,330,30);cx.fillStyle='#fff';cx.font='bold 18px ui-monospace,Menlo,monospace';cx.fillText('CAM-09 MILL RD  '+fmt(t),18,32);
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
    base.serve(sys.modules[__name__], 8846)
