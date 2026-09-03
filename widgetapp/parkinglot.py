#!/usr/bin/env python3
"""95-lot-occupancy: top-down parking-camera playback (canvas, burned-in clock, timeline motion marks, seek,
1 s steps, speed). Cars arrive and leave over four minutes. Task: report the camera clock at the moment the lot
FIRST holds exactly four parked cars. Occupancy is state accumulated over time: no single frame answers it, and
a departure before the fourth arrival means "the fourth arrival" is the wrong moment. Arrivals and departures
look identical on the timeline, so every mark must be inspected (or the recording watched at speed).
complete = a submitted HH:MM:SS within [park-1 s, park+4 s] of the target car coming to rest."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base

DUR = 240; W = 800
BAY_X = [120 + i * 110 for i in range(6)]; BAY_Y = 130; AISLE_Y = 300; ENTRY_X = -70
ARRIVE = 7.0; DEPART = 7.0
COLORS = ["#dc2626", "#2563eb", "#f59e0b", "#10b981", "#e5e7eb", "#8b5cf6", "#f472b6", "#64748b"]
PATTERN = ["A", "A", "A", "D", "A", "A", "D", "A"]     # occupancy 1 2 3 2 3 4(target) 3 4
S = {"clock0": 0, "events": [], "target": None, "submissions": []}


def reset():
    S["submissions"] = []; S["clock0"] = random.randint(0, 86400 - 600)
    while True:
        ts = sorted(random.uniform(12, 222) for _ in PATTERN)
        if all(b - a >= 16 for a, b in zip(ts, ts[1:])): break
    cols = random.sample(COLORS, len(COLORS)); bays = list(range(6)); parked = []; ev = []; occ = 0; target = None
    for t, kind in zip(ts, PATTERN):
        if kind == "A":
            bay = random.choice([b for b in bays if b not in [p["bay"] for p in parked]])
            car = {"id": len(ev), "color": cols.pop(), "bay": bay}; parked.append(car); occ += 1
            ev.append({"t": round(t, 1), "kind": "arrive", "bay": bay, "color": car["color"], "id": car["id"]})
            if occ == 4 and target is None: target = {"t": round(t, 1), "parked_at": round(t + ARRIVE, 1), "bay": bay}
        else:
            car = parked.pop(random.randrange(len(parked))); occ -= 1
            ev.append({"t": round(t, 1), "kind": "depart", "bay": car["bay"], "color": car["color"], "id": car["id"]})
    S["events"] = ev; S["target"] = target


def clock(t):
    s = int(S["clock0"] + t); return f"{s // 3600 % 24:02d}:{s // 60 % 60:02d}:{s % 60:02d}"


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"dur": DUR, "clock0": S["clock0"], "events": S["events"], "arrive": ARRIVE, "depart": DEPART, "bay_x": BAY_X}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("time") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    tg = S["target"]; lo, hi = S["clock0"] + tg["parked_at"] - 1, S["clock0"] + tg["parked_at"] + 4; ok = False
    for s in S["submissions"]:
        try:
            h, m, sec = [int(x) for x in s.split(":")[:3]]; v = h * 3600 + m * 60 + sec
        except Exception: continue
        if lo <= v <= hi or lo <= v + 86400 <= hi: ok = True
    occ = 0; timeline = []
    for e in S["events"]:
        occ += 1 if e["kind"] == "arrive" else -1; timeline.append({**e, "clock": clock(e["t"]), "occupancy_after": occ})
    return {"target": tg, "clock_window": [clock(tg["parked_at"] - 1), clock(tg["parked_at"] + 4)], "events": timeline, "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>NVR Playback: LOT-02</title>
<style>body{font:14px system-ui;margin:0;background:#111827;color:#e5e7eb}#wrap{width:800px;margin:0 auto;padding:14px}h1{font-size:17px;margin:0 0 8px}
canvas{display:block}#v{background:#000}#tl{background:#1f2937;margin-top:6px;cursor:pointer}#bar{display:flex;gap:8px;align-items:center;margin-top:8px}
button,select{font:inherit;background:#374151;color:#e5e7eb;border:0;border-radius:6px;padding:6px 10px;cursor:pointer}input[type=range]{flex:1}
#ans{margin-top:16px;padding:12px;background:#1f2937;border-radius:8px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #4b5563;background:#111827;color:#e5e7eb}.note{color:#9ca3af;font-size:12px}</style>
<div id=wrap><h1>NVR Playback, LOT-02 Staff Parking (recording, 4:00)</h1>
<canvas id=v width=800 height=450 aria-label="camera playback"></canvas>
<canvas id=tl width=800 height=28 aria-label="timeline with motion markers"></canvas><div class=note>Orange marks on the timeline are motion events. Click the timeline to jump.</div>
<div id=bar><button id=pp>Play</button><button id=bm10>-10 s</button><button id=bm1>-1 s</button><button id=bp1>+1 s</button><button id=bp10>+10 s</button><span id=tm>0:00 / 4:00</span>
<input id=seek type=range min=0 max=240 step=0.5 value=0 aria-label="Seek"><select id=spd><option value=1>1x</option><option value=2>2x</option><option value=4>4x</option><option value=8>8x</option></select></div>
<div id=ans><label>Camera clock when the lot first holds exactly four parked cars (HH:MM:SS): <input id=t type=text size=10 placeholder="00:00:00"></label> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>
(function(){var D=null,pos=0,base=0,t0=Date.now(),playing=false,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d'),tl=document.getElementById('tl'),tx=tl.getContext('2d');
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function clock(t){var s=Math.floor(D.clock0+t);return String(Math.floor(s/3600)%24).padStart(2,'0')+':'+String(Math.floor(s/60)%60).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}
function rr(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.arcTo(x+w,y,x+w,y+h,r);cx.arcTo(x+w,y+h,x,y+h,r);cx.arcTo(x,y+h,x,y,r);cx.arcTo(x,y,x+w,y,r);cx.closePath();cx.fill()}
function car(x,y,col,vert){cx.fillStyle=col;if(vert){rr(x-24,y-48,48,96,10);cx.fillStyle='rgba(30,41,59,.85)';rr(x-18,y-30,36,22,5);rr(x-18,y+12,36,18,5)}else{rr(x-48,y-24,96,48,10);cx.fillStyle='rgba(30,41,59,.85)';rr(x-30,y-18,22,36,5);rr(x+12,y-18,18,36,5)}}
function posOf(e,t){var dt=t-e.t,bx=D.bay_x[e.bay];if(e.kind==='arrive'){if(dt<0)return null;if(dt>=D.arrive)return {x:bx,y:130,v:true,still:true};if(dt<4){return {x:-70+(bx+70)*(dt/4),y:300,v:false}}return {x:bx,y:300-(170)*((dt-4)/3),v:true}}
 else{if(dt<0)return {x:bx,y:130,v:true,still:true};if(dt>=D.depart)return null;if(dt<3)return {x:bx,y:130+170*(dt/3),v:true};return {x:bx-(bx+70)*((dt-3)/4),y:300,v:false}}}
function scene(t){cx.fillStyle='#3f3f46';cx.fillRect(0,0,800,450);cx.fillStyle='#52525b';cx.fillRect(0,0,800,230);cx.strokeStyle='#e5e7eb';cx.lineWidth=3;for(var i=0;i<=6;i++){var x=65+i*110;cx.beginPath();cx.moveTo(x,50);cx.lineTo(x,215);cx.stroke()}
 cx.fillStyle='#fde68a';cx.font='bold 16px system-ui';for(var i=0;i<6;i++)cx.fillText(String(i+1),D.bay_x[i]-5,40);cx.fillStyle='#fbbf24';for(var x=0;x<800;x+=60)cx.fillRect(x,298,30,4);
 cx.fillStyle='#166534';cx.fillRect(0,380,800,70);cx.fillStyle='#e5e7eb';cx.font='13px system-ui';cx.fillText('ENTRANCE / EXIT',8,292);
 var arr={},dep={};D.events.forEach(function(e){(e.kind==='arrive'?arr:dep)[e.id]=e});
 Object.keys(arr).forEach(function(id){var a=arr[id],d=dep[id],p=null;if(t<a.t)return;if(t<a.t+D.arrive)p=posOf(a,t);else if(!d||t<d.t)p={x:D.bay_x[a.bay],y:130,v:true};else if(t<d.t+D.depart)p=posOf(d,t);if(p)car(p.x,p.y,a.color,p.v)});
 cx.fillStyle='rgba(0,0,0,.65)';cx.fillRect(10,10,400,30);cx.fillStyle='#fff';cx.font='bold 18px ui-monospace,Menlo,monospace';cx.fillText('LOT-02 STAFF     2026-08-14 '+clock(t),18,32);
 if(!playing){cx.fillStyle='rgba(0,0,0,.55)';cx.fillRect(700,10,90,30);cx.fillStyle='#fff';cx.font='bold 15px system-ui';cx.fillText('PAUSED',714,31)}
 for(var yy=0;yy<450;yy+=3){cx.fillStyle='rgba(0,0,0,.08)';cx.fillRect(0,yy,800,1)}}
function timeline(){tx.fillStyle='#1f2937';tx.fillRect(0,0,800,28);tx.fillStyle='#374151';tx.fillRect(0,12,800,4);tx.fillStyle='#f59e0b';D.events.forEach(function(e){var x=e.t/D.dur*800,w=7/D.dur*800;tx.fillRect(x,6,Math.max(3,w),16)});tx.fillStyle='#fff';tx.fillRect(pos/D.dur*800-1,2,2,24);
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


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8815)
