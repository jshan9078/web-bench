#!/usr/bin/env python3
"""254-map-pan-find: a slippy-map style web map rendered on a canvas (procedural streets and labels) with pan
buttons/arrow keys and zoom levels; place names only render at zoom 3+. Task: find the named place by panning
around from the start view and report the street it sits on and the nearest cross street. complete = both names
right (last submission)."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
STREETS_EW = ["Harbor St", "Maple Ave", "Church St", "King St", "Mill Rd", "Elm St", "Quay Rd", "Bay St"]
STREETS_NS = ["1st Ave", "2nd Ave", "3rd Ave", "4th Ave", "5th Ave", "6th Ave", "7th Ave", "8th Ave"]
PLACES = ["Old Mill Bakery", "Harbor Clinic", "Northwind Library", "Quay Cinema", "Elm Street Gym", "Bay Pharmacy"]
S = {"target": "", "tx": 0, "ty": 0, "places": [], "submissions": []}


def reset():
    S["submissions"] = []; cells = random.sample([(i, j) for i in range(8) for j in range(8)], len(PLACES))
    S["places"] = [{"name": n, "i": c[0], "j": c[1]} for n, c in zip(PLACES, cells)]; t = random.choice(S["places"]); S["target"] = t["name"]; S["tx"], S["ty"] = t["i"], t["j"]


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"ew": STREETS_EW, "ns": STREETS_NS, "places": S["places"], "target": S["target"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append({"street": str(data.get("street") or "").strip(), "cross": str(data.get("cross") or "").strip()}); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    ok = False
    if S["submissions"]:
        s = S["submissions"][-1]; want_ew = STREETS_EW[S["ty"]]; want_ns = STREETS_NS[S["tx"]]
        a, b = s["street"].lower(), s["cross"].lower(); ok = {want_ew.lower(), want_ns.lower()} == {a, b} or (want_ew.lower() in a and want_ns.lower() in b) or (want_ns.lower() in a and want_ew.lower() in b)
    return {"target": S["target"], "on": STREETS_EW[S["ty"]], "cross": STREETS_NS[S["tx"]], "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Harbor City map</title>
<style>body{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a}#wrap{width:900px;margin:0 auto;padding:12px}canvas{display:block;border:1px solid #cbd5e1;background:#e5e7eb}#bar{display:flex;gap:8px;align-items:center;margin-top:8px}button,input{font:inherit;padding:6px 10px}#ans{margin-top:10px;padding:10px;background:#fff;border:1px solid #e2e8f0;border-radius:8px}</style>
<div id=wrap><h1 style="font-size:17px">Harbor City map</h1><canvas id=m width=900 height=520 tabindex=0></canvas>
<div id=bar><button id=l>◀</button><button id=u>▲</button><button id=d>▼</button><button id=r>▶</button><button id=zi>Zoom +</button><button id=zo>Zoom -</button><span id=info></span></div>
<p style="color:#64748b;font-size:13px">Pan with the buttons or arrow keys (click the map first); zoom with + / - or the buttons. Place names appear at zoom 3 and above; street names at zoom 2 and above.</p>
<div id=ans><b>Find <span id=tg></span>.</b> It is on street <input id=s1 size=14 placeholder="e.g. King St"> at the corner of <input id=s2 size=14 placeholder="e.g. 3rd Ave"> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>(function(){var D=null,cv=document.getElementById('m'),cx=cv.getContext('2d'),z=1,cxw=4,cyw=4;var CELL=[60,120,240,480];
function draw(){if(!D)return;var s=CELL[z],ox=450-(cxw*s),oy=260-(cyw*s);cx.fillStyle='#e5e7eb';cx.fillRect(0,0,900,520);
 for(var j=0;j<=8;j++){var y=oy+j*s;cx.fillStyle='#fff';cx.fillRect(0,y-s*0.06,900,s*0.12);if(z>=1&&j<8){cx.fillStyle='#475569';cx.font=Math.max(10,s*0.11)+'px system-ui';cx.fillText(D.ew[j],8,y-s*0.09)}}
 for(var i=0;i<=8;i++){var x=ox+i*s;cx.fillStyle='#fff';cx.fillRect(x-s*0.06,0,s*0.12,520);if(z>=1&&i<8){cx.save();cx.translate(x+s*0.09,14);cx.rotate(Math.PI/2);cx.fillStyle='#475569';cx.font=Math.max(10,s*0.11)+'px system-ui';cx.fillText(D.ns[i],0,0);cx.restore()}}
 D.places.forEach(function(p){var x=ox+p.i*s,y=oy+p.j*s;cx.fillStyle='#dc2626';cx.beginPath();cx.arc(x+s*0.22,y+s*0.22,Math.max(3,s*0.04),0,6.28);cx.fill();if(z>=2){cx.fillStyle='#0f172a';cx.font='bold '+Math.max(10,s*0.07)+'px system-ui';cx.fillText(p.name,x+s*0.28,y+s*0.25)}});
 cx.fillStyle='rgba(15,23,42,.7)';cx.fillRect(10,490,150,24);cx.fillStyle='#fff';cx.font='12px system-ui';cx.fillText('zoom '+(z+1)+'   centre '+cxw.toFixed(1)+','+cyw.toFixed(1),16,507);document.getElementById('info').textContent='Zoom level '+(z+1)}
function pan(dx,dy){cxw=Math.max(0,Math.min(8,cxw+dx));cyw=Math.max(0,Math.min(8,cyw+dy));draw()}
document.getElementById('l').onclick=function(){pan(-0.5,0)};document.getElementById('r').onclick=function(){pan(0.5,0)};document.getElementById('u').onclick=function(){pan(0,-0.5)};document.getElementById('d').onclick=function(){pan(0,0.5)};
document.getElementById('zi').onclick=function(){z=Math.min(3,z+1);draw()};document.getElementById('zo').onclick=function(){z=Math.max(0,z-1);draw()};
cv.addEventListener('keydown',function(e){var m={ArrowLeft:[-0.5,0],ArrowRight:[0.5,0],ArrowUp:[0,-0.5],ArrowDown:[0,0.5]}[e.key];if(m){e.preventDefault();pan(m[0],m[1])}else if(e.key==='+'||e.key==='='){z=Math.min(3,z+1);draw()}else if(e.key==='-'){z=Math.max(0,z-1);draw()}});
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({street:document.getElementById('s1').value,cross:document.getElementById('s2').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
fetch('/__data').then(r=>r.json()).then(function(j){D=j;document.getElementById('tg').textContent=j.target;z=0;draw()})})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8915)
