#!/usr/bin/env python3
"""184-queue-peak: a service-counter clip (canvas video, 2 min): people join a queue and are served (leave) at
random times. Task: the maximum number of people waiting at the same time at any moment. State that must be
tracked over the whole clip. complete = exact (last submission)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
DUR = 120
S = {"arrivals": [], "serve": [], "answer": 0, "submissions": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset():
    S["submissions"] = []
    while True:
        n = random.randint(12, 18); arr = sorted(random.uniform(3, 100) for _ in range(n)); t = 0; serve = []
        for a in arr:
            t = max(t, a) + random.uniform(3, 11); serve.append(min(t, DUR + 5))
        peak = 0
        for x in arr: peak = max(peak, sum(1 for a, s in zip(arr, serve) if a <= x < s))
        if 4 <= peak <= 7: break
    S["arrivals"] = [round(a, 1) for a in arr]; S["serve"] = [round(s, 1) for s in serve]; S["answer"] = peak


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"dur": DUR, "arr": S["arrivals"], "serve": S["serve"], "colors": [random.Random(i).choice(COLORS) for i in range(len(S["arrivals"]))]}), "application/json")
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
    return {"answer": S["answer"], "arrivals": S["arrivals"], "served": S["serve"], "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Service counter clip</title>
<style>body{font:14px system-ui;margin:0;background:#111827;color:#e5e7eb}#wrap{width:800px;margin:0 auto;padding:14px}h1{font-size:17px;margin:0 0 8px}canvas{display:block;background:#000}
#bar{display:flex;gap:8px;align-items:center;margin-top:8px}button,select{font:inherit;background:#374151;color:#e5e7eb;border:0;border-radius:6px;padding:6px 10px;cursor:pointer}input[type=range]{flex:1}
#ans{margin-top:16px;padding:12px;background:#1f2937;border-radius:8px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #4b5563;background:#111827;color:#e5e7eb}</style>
<div id=wrap><h1>Service counter camera (clip, 2:00)</h1><canvas id=v width=800 height=450></canvas>
<div id=bar><button id=pp>Play</button><button id=bm10>-10 s</button><button id=bm1>-1 s</button><button id=bp1>+1 s</button><button id=bp10>+10 s</button><span id=tm>0:00 / 2:00</span><input id=seek type=range min=0 max=120 step=0.5 value=0 aria-label="Seek"><select id=spd><option value=1>1x</option><option value=2>2x</option><option value=4>4x</option><option value=8>8x</option></select></div>
<div id=ans><label>Maximum number of people waiting in the queue at the same time: <input id=c type=text size=6></label> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>(function(){var D=null,pos=0,base=0,t0=Date.now(),playing=false,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d');
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function rr(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.arcTo(x+w,y,x+w,y+h,r);cx.arcTo(x+w,y+h,x,y+h,r);cx.arcTo(x,y+h,x,y,r);cx.arcTo(x,y,x+w,y,r);cx.closePath();cx.fill()}
function person(col,x,y){cx.fillStyle=col;cx.beginPath();cx.arc(x+12,y-60,11,0,6.28);cx.fill();rr(x+2,y-48,20,34,6);cx.fillRect(x+4,y-14,7,30);cx.fillRect(x+13,y-14,7,30)}
function scene(t){cx.fillStyle='#e5e7eb';cx.fillRect(0,0,800,450);cx.fillStyle='#d1d5db';cx.fillRect(0,300,800,150);cx.fillStyle='#374151';cx.fillRect(560,150,200,110);cx.fillStyle='#9ca3af';cx.fillRect(560,150,200,14);cx.fillStyle='#111827';cx.font='bold 14px system-ui';cx.fillText('COUNTER 2',610,205);
 var waiting=[];D.arr.forEach(function(a,i){var s=D.serve[i];if(t>=a-3&&t<s){var arriving=t<a,f=arriving?(t-(a-3))/3:1;waiting.push({i:i,x:arriving?-40+f*400:null})}});
 var q=0;waiting.forEach(function(w){var x=w.x!==null?w.x:520-q*46;if(w.x===null)q++;person(D.colors[w.i],x,340+((w.i%3)*6))});
 D.arr.forEach(function(a,i){var s=D.serve[i];if(t>=s&&t<s+3){var f=(t-s)/3;person(D.colors[i],600+f*260,330)}});
 cx.fillStyle='rgba(0,0,0,.65)';cx.fillRect(10,10,330,30);cx.fillStyle='#fff';cx.font='bold 18px ui-monospace,Menlo,monospace';cx.fillText('HALL-2  '+fmt(t),18,32);
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
    base.serve(sys.modules[__name__], 8867)
