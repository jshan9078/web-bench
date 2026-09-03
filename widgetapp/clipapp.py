#!/usr/bin/env python3
"""Scaffold for canvas-video counting tasks: a module provides DUR, TITLE, HEADING, QUESTION, reset(), data() (JSON
for the client), SCENE_JS (a JS function scene(t) using D and helpers), and answer()."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base

TEMPLATE = r"""<!doctype html><meta charset=utf-8><title>__TITLE__</title>
<style>body{font:14px system-ui;margin:0;background:#111827;color:#e5e7eb}#wrap{width:800px;margin:0 auto;padding:14px}h1{font-size:17px;margin:0 0 8px}canvas{display:block;background:#000}
#bar{display:flex;gap:8px;align-items:center;margin-top:8px}button,select{font:inherit;background:#374151;color:#e5e7eb;border:0;border-radius:6px;padding:6px 10px;cursor:pointer}input[type=range]{flex:1}
#ans{margin-top:16px;padding:12px;background:#1f2937;border-radius:8px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #4b5563;background:#111827;color:#e5e7eb}</style>
<div id=wrap><h1>__HEADING__</h1><canvas id=v width=800 height=450></canvas>
<div id=bar><button id=pp>Play</button><button id=bm10>-10 s</button><button id=bm1>-1 s</button><button id=bp1>+1 s</button><button id=bp10>+10 s</button><span id=tm>0:00</span><input id=seek type=range min=0 max=__DUR__ step=0.5 value=0 aria-label="Seek"><select id=spd><option value=1>1x</option><option value=2>2x</option><option value=4>4x</option><option value=0.5>0.5x</option></select></div>
<div id=ans><label>__QUESTION__ <input id=c type=text size=6></label> <button id=go>Submit</button> <span id=msg></span></div></div>
<script>(function(){var D=null,pos=0,base=0,t0=Date.now(),playing=false,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d');
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function rr(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.arcTo(x+w,y,x+w,y+h,r);cx.arcTo(x+w,y+h,x,y+h,r);cx.arcTo(x,y+h,x,y,r);cx.arcTo(x,y,x+w,y,r);cx.closePath();cx.fill()}
function person(col,x,y,t){cx.fillStyle=col;cx.beginPath();cx.arc(x+12,y-60,11,0,6.28);cx.fill();rr(x+2,y-48,20,34,6);var sw=Math.sin(t*8)*6;cx.fillRect(x+4,y-14,7,30+sw);cx.fillRect(x+13,y-14,7,30-sw)}
function overlay(t,label){cx.fillStyle='rgba(0,0,0,.65)';cx.fillRect(10,10,330,30);cx.fillStyle='#fff';cx.font='bold 18px ui-monospace,Menlo,monospace';cx.fillText(label+'  '+fmt(t),18,32);if(!playing){cx.fillStyle='rgba(0,0,0,.55)';cx.fillRect(700,10,90,30);cx.fillStyle='#fff';cx.font='bold 15px system-ui';cx.fillText('PAUSED',714,31)}}
__SCENE__
function draw(){if(!D)return;scene(pos);document.getElementById('tm').textContent=fmt(pos)+' / '+fmt(D.dur);document.getElementById('seek').value=pos}
function step(){if(playing){pos=base+rate*(Date.now()-t0)/1000;if(pos>=D.dur){pos=D.dur;base=pos;playing=false;document.getElementById('pp').textContent='Play'}}draw()}
function tick(){step();requestAnimationFrame(tick)}function seek(t){pos=Math.max(0,Math.min(D.dur,t));base=pos;t0=Date.now();draw()}
fetch('/__data').then(r=>r.json()).then(function(j){D=j;t0=Date.now();setInterval(step,100);requestAnimationFrame(tick)});
document.getElementById('pp').onclick=function(){base=pos;t0=Date.now();playing=!playing;this.textContent=playing?'Pause':'Play'};
document.getElementById('bm10').onclick=function(){seek(pos-10)};document.getElementById('bp10').onclick=function(){seek(pos+10)};document.getElementById('bm1').onclick=function(){seek(pos-1)};document.getElementById('bp1').onclick=function(){seek(pos+1)};
var sk=document.getElementById('seek');sk.oninput=sk.onchange=function(){seek(+this.value)};document.getElementById('spd').onchange=function(){base=pos;t0=Date.now();rate=+this.value};
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({count:document.getElementById('c').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
})();</script>"""


def make(mod):
    S = {"submissions": []}
    def render(): return b""
    def click(x, y): return {"ignored": True}
    def get(path):
        if path == "/__data": return (json.dumps(dict(mod.data(), dur=mod.DUR)), "application/json")
        return None
    def post(path, data, ctype):
        if path == "/__answer":
            S["submissions"].append(str(data.get("count") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
        return None
    def state():
        ok = False
        if S["submissions"]:
            try: ok = int(float(S["submissions"][-1])) == mod.answer()
            except ValueError: ok = False
        st = dict(mod.data()); st.update(answer=mod.answer(), submissions=S["submissions"], complete=ok); return st
    def page(): return TEMPLATE.replace("__TITLE__", mod.TITLE).replace("__HEADING__", mod.HEADING).replace("__QUESTION__", mod.QUESTION).replace("__DUR__", str(mod.DUR)).replace("__SCENE__", mod.SCENE_JS)
    inner = mod.reset
    def reset(): S["submissions"].clear(); inner()
    mod.render, mod.click, mod.get, mod.post, mod.state, mod.page, mod.reset = render, click, get, post, state, page, reset
    return mod
