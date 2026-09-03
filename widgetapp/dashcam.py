#!/usr/bin/env python3
"""136-dashcam-speed: a dashcam clip (canvas video, 90 s) with a speed overlay that changes continuously and
roadside signs passing; the RED octagonal sign passes once. Task: the overlay speed at the moment the car
passes the red sign, within 3 km/h. Timing precision on a video plus reading. complete = within tolerance of
the speed during the 3 s the sign is beside the car."""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
DUR = 90
S = {"signs": [], "t_red": 0, "speed_params": [], "submissions": []}


def speed(t):
    a, b, c = S["speed_params"]; return 62 + 18 * math.sin(t / a + b) + 9 * math.sin(t / c)


def reset():
    S["submissions"] = []; S["speed_params"] = [random.uniform(9, 14), random.uniform(0, 6), random.uniform(3.5, 5.5)]
    while True:
        ts = sorted(random.uniform(8, 82) for _ in range(5))
        if all(y - x >= 7 for x, y in zip(ts, ts[1:])): break
    kinds = ["blue", "yellow", "red", "green", "blue"]; random.shuffle(kinds)
    S["signs"] = [{"t": round(t, 1), "kind": k} for t, k in zip(ts, kinds)]; S["t_red"] = next(s["t"] for s in S["signs"] if s["kind"] == "red")


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"dur": DUR, "signs": S["signs"], "sp": S["speed_params"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("speed") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    lo = min(speed(S["t_red"] + d / 10) for d in range(-15, 16)); hi = max(speed(S["t_red"] + d / 10) for d in range(-15, 16)); ok = False
    if S["submissions"]:
        try: v = float(S["submissions"][-1].replace("km/h", "").strip()); ok = lo - 3 <= v <= hi + 3
        except ValueError: ok = False
    return {"t_red": S["t_red"], "speed_at_red": round(speed(S["t_red"]), 1), "window": [round(lo, 1), round(hi, 1)], "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Dashcam clip review</title>
<style>body{font:14px system-ui;margin:0;background:#111827;color:#e5e7eb}#wrap{width:800px;margin:0 auto;padding:14px}h1{font-size:17px;margin:0 0 8px}canvas{display:block;background:#000}
#bar{display:flex;gap:8px;align-items:center;margin-top:8px}button,select{font:inherit;background:#374151;color:#e5e7eb;border:0;border-radius:6px;padding:6px 10px;cursor:pointer}input[type=range]{flex:1}
#ans{margin-top:16px;padding:12px;background:#1f2937;border-radius:8px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #4b5563;background:#111827;color:#e5e7eb}</style>
<div id=wrap><h1>Dashcam clip, claim #48213 (1:30)</h1><canvas id=v width=800 height=450></canvas>
<div id=bar><button id=pp>Play</button><button id=bm10>-10 s</button><button id=bm1>-1 s</button><button id=bp1>+1 s</button><button id=bp10>+10 s</button><span id=tm>0:00 / 1:30</span><input id=seek type=range min=0 max=90 step=0.1 value=0 aria-label="Seek"><select id=spd><option value=1>1x</option><option value=0.5>0.5x</option><option value=2>2x</option></select></div>
<div id=ans><label>Speed shown when the car passes the RED sign (km/h): <input id=s type=text size=8></label> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>(function(){var D=null,pos=0,base=0,t0=Date.now(),playing=false,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d');
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function speed(t){var a=D.sp[0],b=D.sp[1],c=D.sp[2];return 62+18*Math.sin(t/a+b)+9*Math.sin(t/c)}
function sign(kind,x,y,s){cx.fillStyle='#777';cx.fillRect(x-3,y,6,s*1.6);if(kind==='red'){cx.fillStyle='#c81e1e';cx.beginPath();for(var i=0;i<8;i++){var a=Math.PI/8+i*Math.PI/4;cx.lineTo(x+s*Math.cos(a),y-s*0.2+s*Math.sin(a))}cx.closePath();cx.fill()}
 else if(kind==='yellow'){cx.fillStyle='#f5c400';cx.beginPath();cx.moveTo(x,y-s*1.2);cx.lineTo(x+s,y+s*0.6);cx.lineTo(x-s,y+s*0.6);cx.closePath();cx.fill()}else{cx.fillStyle=kind==='blue'?'#1d4ed8':'#15803d';cx.fillRect(x-s,y-s*1.2,2*s,1.6*s)}}
function scene(t){cx.fillStyle='#8fb4d9';cx.fillRect(0,0,800,250);cx.fillStyle='#3f3f46';cx.fillRect(0,250,800,200);cx.fillStyle='#e5e7eb';var off=(t*40)%60;for(var y=250+off;y<450;y+=60)cx.fillRect(392,y,16,30);
 cx.strokeStyle='#e5e7eb';cx.lineWidth=3;cx.beginPath();cx.moveTo(400,250);cx.lineTo(60,450);cx.moveTo(400,250);cx.lineTo(740,450);cx.stroke();
 D.signs.forEach(function(sg){var dt=t-sg.t;if(dt<-6||dt>0.6)return;var f=(dt+6)/6.6;var s=6+f*f*60,x=420+f*f*360,y=250+f*f*120;sign(sg.kind,x,y,s)});
 cx.fillStyle='rgba(0,0,0,.6)';cx.fillRect(10,400,300,40);cx.fillStyle='#fff';cx.font='bold 20px ui-monospace,Menlo,monospace';cx.fillText(Math.round(speed(t))+' km/h   2026-08-30 17:0'+Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0'),18,428);
 if(!playing){cx.fillStyle='rgba(0,0,0,.55)';cx.fillRect(700,10,90,30);cx.fillStyle='#fff';cx.font='bold 15px system-ui';cx.fillText('PAUSED',714,31)}}
function draw(){if(!D)return;scene(pos);document.getElementById('tm').textContent=fmt(pos)+' / '+fmt(D.dur);document.getElementById('seek').value=pos}
function step(){if(playing){pos=base+rate*(Date.now()-t0)/1000;if(pos>=D.dur){pos=D.dur;base=pos;playing=false;document.getElementById('pp').textContent='Play'}}draw()}
function tick(){step();requestAnimationFrame(tick)}function seek(t){pos=Math.max(0,Math.min(D.dur,t));base=pos;t0=Date.now();draw()}
fetch('/__data').then(r=>r.json()).then(function(j){D=j;t0=Date.now();setInterval(step,100);requestAnimationFrame(tick)});
document.getElementById('pp').onclick=function(){base=pos;t0=Date.now();playing=!playing;this.textContent=playing?'Pause':'Play'};
document.getElementById('bm10').onclick=function(){seek(pos-10)};document.getElementById('bp10').onclick=function(){seek(pos+10)};document.getElementById('bm1').onclick=function(){seek(pos-1)};document.getElementById('bp1').onclick=function(){seek(pos+1)};
var sk=document.getElementById('seek');sk.oninput=sk.onchange=function(){seek(+this.value)};document.getElementById('spd').onchange=function(){base=pos;t0=Date.now();rate=+this.value};
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({speed:document.getElementById('s').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8843)
