#!/usr/bin/env python3
"""94-cctv-review: security-camera playback (NVR style) of a 4-minute recording rendered on a canvas, with
a burned-in camera clock, a timeline that marks motion events, play/pause, a fine seek bar, 1 s and 10 s
steps and playback speed. Four motion events (blue car, red truck, red car, pedestrian) occur in random
order at random times. Task: report the camera clock reading (HH:MM:SS) while the RED CAR is fully in
frame. The clock start is random, so the time must be read off the frame, not computed. Traps: the red
truck (same colour, wrong vehicle), the blue car (right shape, wrong colour), and reading the clock while
the car is only partly in frame. complete = a submitted time within the fully-visible window (+-1 s)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base

LEVEL = int(os.environ.get("WIDGET_LEVEL", "1"))
DUR = 240; W = 800
KINDS = [("car", "#2563eb", "blue car"), ("truck", "#dc2626", "red truck"), ("car", "#dc2626", "red car"), ("person", "#6b7280", "pedestrian")]
# Level 2: a SECOND red car in the opposite direction; the target is the one travelling right-to-left.
# Direction is not visible in a single frame, so the agent must compare two frames (or watch it move).
LEN = {"car": 120, "truck": 210, "person": 24}; PASS = {"car": 9.0, "truck": 11.0, "person": 14.0}
S = {"clock0": 0, "events": [], "target": None, "submissions": []}


def reset():
    S["submissions"] = []; S["clock0"] = random.randint(0, 86400 - 600)
    kinds = KINDS[:] + ([("car", "#dc2626", "red car")] if LEVEL >= 2 else [])
    while True:
        ts = sorted(random.uniform(15, 215) for _ in range(len(kinds)))
        if all(b - a >= 25 for a, b in zip(ts, ts[1:])): break
    random.shuffle(kinds)
    S["events"] = [{"t": round(t, 1), "kind": k[0], "color": k[1], "label": k[2], "dir": random.choice([1, -1])} for t, k in zip(ts, kinds)]
    reds = [e for e in S["events"] if e["label"] == "red car"]
    if LEVEL >= 2:
        reds[0]["dir"], reds[1]["dir"] = random.choice([(1, -1), (-1, 1)])
    tgt = next(e for e in reds if LEVEL < 2 or e["dir"] == -1)
    L, P = LEN["car"], PASS["car"]; travel = W + 2 * L      # x runs from -L to W+L over P seconds
    fin = tgt["t"] + P * (L / travel); fout = tgt["t"] + P * ((W) / travel)   # fully visible while 0 <= x and x+L <= W
    S["target"] = {"event": tgt, "full_in": round(fin, 2), "full_out": round(fout, 2)}


def clock(t):
    s = int(S["clock0"] + t); return f"{s // 3600 % 24:02d}:{s // 60 % 60:02d}:{s % 60:02d}"


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"dur": DUR, "clock0": S["clock0"], "events": S["events"], "len": LEN, "pass": PASS}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("time") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    tg = S["target"]; lo, hi = S["clock0"] + tg["full_in"] - 1, S["clock0"] + tg["full_out"] + 1; ok = False
    for s in S["submissions"]:
        try:
            h, m, sec = [int(x) for x in s.split(":")[:3]]; v = h * 3600 + m * 60 + sec
        except Exception: continue
        if lo <= v <= hi or lo <= v + 86400 <= hi: ok = True
    return {"level": LEVEL, "target": tg, "clock_window": [clock(tg["full_in"]), clock(tg["full_out"])], "events": [{**e, "clock": clock(e["t"])} for e in S["events"]],
            "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>NVR Playback: CAM-04</title>
<style>body{font:14px system-ui;margin:0;background:#111827;color:#e5e7eb}#wrap{width:800px;margin:0 auto;padding:14px}h1{font-size:17px;margin:0 0 8px}
canvas{display:block}#v{background:#000}#tl{background:#1f2937;margin-top:6px;cursor:pointer}#bar{display:flex;gap:8px;align-items:center;margin-top:8px}
button,select{font:inherit;background:#374151;color:#e5e7eb;border:0;border-radius:6px;padding:6px 10px;cursor:pointer}input[type=range]{flex:1}
#ans{margin-top:16px;padding:12px;background:#1f2937;border-radius:8px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #4b5563;background:#111827;color:#e5e7eb}.note{color:#9ca3af;font-size:12px}</style>
<div id=wrap><h1>NVR Playback, CAM-04 Front St (recording, 4:00)</h1>
<canvas id=v width=800 height=450 aria-label="camera playback"></canvas>
<canvas id=tl width=800 height=28 aria-label="timeline with motion markers"></canvas><div class=note>Orange marks on the timeline are motion events. Click the timeline to jump.</div>
<div id=bar><button id=pp>Play</button><button id=bm10>-10 s</button><button id=bm1>-1 s</button><button id=bp1>+1 s</button><button id=bp10>+10 s</button><span id=tm>0:00 / 4:00</span>
<input id=seek type=range min=0 max=240 step=0.5 value=0 aria-label="Seek"><select id=spd><option value=1>1x</option><option value=2>2x</option><option value=4>4x</option><option value=8>8x</option></select></div>
<div id=ans><label>Camera clock while the red car__L2__ is fully in frame (HH:MM:SS): <input id=t type=text size=10 placeholder="00:00:00"></label> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>
(function(){var D=null,pos=0,base=0,t0=Date.now(),playing=false,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d'),tl=document.getElementById('tl'),tx=tl.getContext('2d');
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function clock(t){var s=Math.floor(D.clock0+t);return String(Math.floor(s/3600)%24).padStart(2,'0')+':'+String(Math.floor(s/60)%60).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}
function rr(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.arcTo(x+w,y,x+w,y+h,r);cx.arcTo(x+w,y+h,x,y+h,r);cx.arcTo(x,y+h,x,y,r);cx.arcTo(x,y,x+w,y,r);cx.closePath();cx.fill()}
function vehicle(e,x){var y=330;cx.fillStyle=e.color;if(e.kind==='car'){rr(x,y,120,38,8);rr(x+28,y-26,60,30,8);cx.fillStyle='#93c5fd';cx.fillRect(x+34,y-20,20,18);cx.fillRect(x+62,y-20,20,18);wheel(x+26,y+40);wheel(x+94,y+40)}
 else if(e.kind==='truck'){rr(x,y-30,150,68,6);cx.fillStyle=e.color;rr(x+152,y-6,58,44,6);cx.fillStyle='#93c5fd';cx.fillRect(x+170,y,28,18);wheel(x+30,y+40);wheel(x+120,y+40);wheel(x+185,y+40)}
 else{cx.fillStyle=e.color;cx.beginPath();cx.arc(x+12,y-12,10,0,6.28);cx.fill();rr(x+3,y,18,34,5);cx.fillRect(x+5,y+34,6,22);cx.fillRect(x+14,y+34,6,22)}}
function wheel(x,y){cx.fillStyle='#111';cx.beginPath();cx.arc(x,y,12,0,6.28);cx.fill();cx.fillStyle='#9ca3af';cx.beginPath();cx.arc(x,y,5,0,6.28);cx.fill()}
function scene(t){var g=cx.createLinearGradient(0,0,0,450);g.addColorStop(0,'#1e293b');g.addColorStop(1,'#334155');cx.fillStyle=g;cx.fillRect(0,0,800,450);
 cx.fillStyle='#475569';[[20,120,110,160],[150,90,90,190],[260,140,140,140],[420,100,120,180],[560,130,100,150],[680,110,110,170]].forEach(function(b){cx.fillRect(b[0],b[1],b[2],b[3])});
 cx.fillStyle='#fde68a';for(var i=0;i<6;i++)for(var j=0;j<3;j++){if((i*7+j*3)%4!==0)cx.fillRect(30+i*130+j*30,140+((i*13)%40),12,14)}
 cx.fillStyle='#6b7280';cx.fillRect(0,280,800,20);cx.fillStyle='#374151';cx.fillRect(0,300,800,150);cx.fillStyle='#e5e7eb';for(var x=0;x<800;x+=80)cx.fillRect(x,372,40,4);
 D.events.forEach(function(e){var L=D.len[e.kind],P=D.pass[e.kind],dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x=e.dir>0?-L+f*(800+2*L):800+L-f*(800+2*L)-L;vehicle(e,x)});
 cx.fillStyle='rgba(0,0,0,.65)';cx.fillRect(10,10,400,30);cx.fillStyle='#fff';cx.font='bold 18px ui-monospace,Menlo,monospace';cx.fillText('CAM-04 FRONT ST   2026-08-14 '+clock(t),18,32);
 if(!playing){cx.fillStyle='rgba(0,0,0,.55)';cx.fillRect(700,10,90,30);cx.fillStyle='#fff';cx.font='bold 15px system-ui';cx.fillText('PAUSED',714,31)}
 for(var yy=0;yy<450;yy+=3){cx.fillStyle='rgba(0,0,0,.08)';cx.fillRect(0,yy,800,1)}}
function timeline(){tx.fillStyle='#1f2937';tx.fillRect(0,0,800,28);tx.fillStyle='#374151';tx.fillRect(0,12,800,4);tx.fillStyle='#f59e0b';D.events.forEach(function(e){var x=e.t/D.dur*800,w=D.pass[e.kind]/D.dur*800;tx.fillRect(x,6,Math.max(3,w),16)});tx.fillStyle='#fff';tx.fillRect(pos/D.dur*800-1,2,2,24);
 tx.fillStyle='#9ca3af';tx.font='10px system-ui';for(var m=0;m<=4;m++){tx.fillText(m+':00',m/4*796-(m==4?22:0),27)}}
function draw(){if(!D)return;scene(pos);timeline();document.getElementById('tm').textContent=fmt(pos)+' / '+fmt(D.dur);document.getElementById('seek').value=pos}
function step(){if(playing){pos=base+rate*(Date.now()-t0)/1000;if(pos>=D.dur){pos=D.dur;base=pos;playing=false;document.getElementById('pp').textContent='Play'}}draw()}
function tick(){step();requestAnimationFrame(tick)}
function seek(t){pos=Math.max(0,Math.min(D.dur,t));base=pos;t0=Date.now();draw()}
fetch('/__data').then(r=>r.json()).then(function(j){D=j;t0=Date.now();setInterval(step,100);requestAnimationFrame(tick)});
document.getElementById('pp').onclick=function(){base=pos;t0=Date.now();playing=!playing;this.textContent=playing?'Pause':'Play'};
document.getElementById('bm10').onclick=function(){seek(pos-10)};document.getElementById('bp10').onclick=function(){seek(pos+10)};document.getElementById('bm1').onclick=function(){seek(pos-1)};document.getElementById('bp1').onclick=function(){seek(pos+1)};
var sk=document.getElementById('seek');sk.oninput=sk.onchange=function(){seek(+this.value)};document.getElementById('spd').onchange=function(){base=pos;t0=Date.now();rate=+this.value};
tl.onclick=function(e){var r=tl.getBoundingClientRect();seek((e.clientX-r.left)/800*D.dur)};
document.addEventListener('keydown',function(e){if(e.target.tagName==='INPUT'&&e.target.type==='text')return;if(e.key===' '){e.preventDefault();document.getElementById('pp').click()}if(e.key==='ArrowLeft')seek(pos-1);if(e.key==='ArrowRight')seek(pos+1)});
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({time:document.getElementById('t').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
})();
</script>"""


def page(): return PAGE.replace("__L2__", " travelling right-to-left" if LEVEL >= 2 else "")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8814)
