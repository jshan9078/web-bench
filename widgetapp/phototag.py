#!/usr/bin/env python3
"""267-gallery-tagging: a photo gallery (24 server-rendered thumbnails with a lightbox) where some photos contain a
red car among other vehicles and objects. Task: open each photo as needed and add the tag "red car" to exactly
the photos that contain one, then Save tags. complete = tag set equals the truth."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
S = {"photos": [], "tags": {}, "saved": None}


def reset():
    S["photos"] = []; S["tags"] = {}; S["saved"] = None
    for i in range(24):
        kind = random.choice(["redcar", "bluecar", "redtruck", "none", "redcar", "bluecar", "none"]); S["photos"].append({"id": i, "kind": kind, "seed": random.randint(1, 10 ** 6)})


def draw(p, w, h):
    rng = random.Random(p["seed"]); img = Image.new("RGB", (w, h), (rng.randint(150, 200), rng.randint(170, 210), rng.randint(180, 230))); d = ImageDraw.Draw(img)
    d.rectangle([0, h * 0.6, w, h], fill=(90, 90, 95)); d.rectangle([w * 0.1, h * 0.25, w * 0.4, h * 0.6], fill=(120, 110, 100)); d.rectangle([w * 0.55, h * 0.3, w * 0.9, h * 0.6], fill=(140, 130, 120))
    k = p["kind"]; x = w * rng.uniform(0.2, 0.6); y = h * 0.66
    if k in ("redcar", "bluecar"):
        c = (200, 40, 40) if k == "redcar" else (40, 80, 200); d.rounded_rectangle([x, y, x + w * 0.28, y + h * 0.12], 6, fill=c); d.rounded_rectangle([x + w * 0.06, y - h * 0.09, x + w * 0.2, y], 6, fill=c); d.ellipse([x + w * 0.03, y + h * 0.09, x + w * 0.09, y + h * 0.17], fill=(20, 20, 20)); d.ellipse([x + w * 0.19, y + h * 0.09, x + w * 0.25, y + h * 0.17], fill=(20, 20, 20))
    elif k == "redtruck":
        d.rectangle([x, y - h * 0.12, x + w * 0.3, y + h * 0.12], fill=(200, 40, 40)); d.rectangle([x + w * 0.3, y - h * 0.02, x + w * 0.42, y + h * 0.12], fill=(200, 40, 40)); d.ellipse([x + w * 0.04, y + h * 0.09, x + w * 0.1, y + h * 0.17], fill=(20, 20, 20)); d.ellipse([x + w * 0.32, y + h * 0.09, x + w * 0.38, y + h * 0.17], fill=(20, 20, 20))
    if rng.random() < 0.5: d.ellipse([w * 0.75, h * 0.08, w * 0.85, h * 0.18], fill=(250, 240, 120))
    return img


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path.startswith("/__photo/"):
        try: i = int(path.split("/")[2].split(".")[0].split("-")[0]); big = "big" in path
        except ValueError: return None
        p = S["photos"][i]; return (base.png(draw(p, 800 if big else 200, 520 if big else 130)), "image/png")
    if path == "/__data": return (json.dumps({"n": len(S["photos"]), "tags": S["tags"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__tag":
        i = str(data.get("id")); tags = [str(t).strip().lower() for t in (data.get("tags") or []) if str(t).strip()]; S["tags"][i] = tags; return (json.dumps({"ok": True}), "application/json")
    if path == "/__savetags": S["saved"] = json.loads(json.dumps(S["tags"])); return (json.dumps({"ok": True}), "application/json")
    return None


def state():
    want = {str(p["id"]) for p in S["photos"] if p["kind"] == "redcar"}; got = {k for k, v in (S["saved"] or {}).items() if "red car" in v}
    return {"want": sorted(want), "got": sorted(got), "saved": S["saved"] is not None, "complete": S["saved"] is not None and want == got}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Photo library</title>
<style>body{font:14px system-ui;margin:0;background:#0f172a;color:#e5e7eb}main{max-width:1000px;margin:0 auto;padding:12px}#g{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}.ph{position:relative;cursor:pointer}.ph img{width:100%;display:block;border-radius:6px}.ph .tg{position:absolute;bottom:4px;left:4px;background:rgba(0,0,0,.7);font-size:11px;padding:1px 5px;border-radius:4px}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;flex-direction:column;gap:10px}#lb.on{display:flex}#lb img{max-width:800px}input,button{font:inherit;padding:6px 9px}</style>
<main><div style="display:flex;gap:10px;align-items:center;margin-bottom:8px"><b>Photo library, 24 photos</b><span style="margin-left:auto"><button id=save>Save tags</button> <span id=msg style="color:#86efac"></span></span></div><div id=g></div><p style="color:#94a3b8;font-size:13px">Click a thumbnail to open it; in the viewer, add or remove tags for that photo, then use the arrows or Close.</p></main>
<div id=lb><img id=big><div><span id=cap></span> &nbsp; Tags: <span id=tl></span> <input id=ti placeholder="new tag" size=12><button id=add>Add tag</button> <button id=prev>◀ Prev</button><button id=next>Next ▶</button><button id=close>Close</button></div></div>
<script>(function(){var N=24,T={},cur=0;function load(){fetch('/__data').then(r=>r.json()).then(function(j){N=j.n;T=j.tags;render()})}
function render(){document.getElementById('g').innerHTML=Array.from({length:N}).map(function(_,i){return '<div class=ph data-i="'+i+'"><img src="/__photo/'+i+'.png"><span class=tg>#'+i+(T[i]&&T[i].length?' · '+T[i].join(', '):'')+'</span></div>'}).join('');document.querySelectorAll('.ph').forEach(function(el){el.onclick=function(){open(+el.dataset.i)}})}
function open(i){cur=i;document.getElementById('big').src='/__photo/'+i+'-big.png';document.getElementById('cap').textContent='Photo #'+i;document.getElementById('tl').innerHTML=(T[i]||[]).map(function(t){return '<button data-rm="'+t+'">'+t+' ✕</button>'}).join(' ')||'none';document.querySelectorAll('[data-rm]').forEach(function(b){b.onclick=function(){setTags(i,(T[i]||[]).filter(function(x){return x!==b.dataset.rm}))}});document.getElementById('lb').classList.add('on')}
function setTags(i,tags){fetch('/__tag',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:i,tags:tags})}).then(function(){T[i]=tags;render();open(i)})}
document.getElementById('add').onclick=function(){var v=document.getElementById('ti').value.trim();if(!v)return;setTags(cur,(T[cur]||[]).concat([v]));document.getElementById('ti').value=''};document.getElementById('prev').onclick=function(){open((cur+N-1)%N)};document.getElementById('next').onclick=function(){open((cur+1)%N)};document.getElementById('close').onclick=function(){document.getElementById('lb').classList.remove('on')};
document.getElementById('save').onclick=function(){fetch('/__savetags',{method:'POST'}).then(function(){document.getElementById('msg').textContent='Tags saved'})};load()})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8924)
