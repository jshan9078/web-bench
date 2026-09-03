#!/usr/bin/env python3
"""154-tower-clock: a town-square webcam still where the tower clock is small in frame; the page offers the
same click-to-magnify lens as a photo viewer. Task: the time on the tower clock within 2 minutes. Combines
finding the clock, using the zoom, and reading hands. complete = within 2 minutes."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 1000, 700
S = {"h": 0, "m": 0, "submissions": []}


def reset(): S["h"], S["m"] = random.randint(1, 12), random.choice([m for m in range(60) if m % 5]); S["submissions"] = []


def scene(k=1):
    img = Image.new("RGB", (W * k, H * k), (170, 190, 215)); d = ImageDraw.Draw(img)
    d.rectangle([0, 420 * k, W * k, H * k], fill=(120, 110, 100))
    for x, w, h, c in [(40, 160, 300, (190, 170, 150)), (230, 120, 260, (170, 160, 150)), (620, 170, 280, (185, 175, 160)), (820, 150, 320, (175, 165, 150))]:
        d.rectangle([x * k, (420 - h) * k, (x + w) * k, 420 * k], fill=c)
        for wy in range((420 - h + 20), 400, 34):
            for wx in range(x + 14, x + w - 14, 30): d.rectangle([wx * k, wy * k, (wx + 14) * k, (wy + 20) * k], fill=(90, 100, 120))
    d.rectangle([400 * k, 120 * k, 560 * k, 420 * k], fill=(160, 150, 140)); d.polygon([(400 * k, 120 * k), (480 * k, 60 * k), (560 * k, 120 * k)], fill=(120, 80, 70))
    cx, cy, r = 480 * k, 180 * k, 34 * k; d.ellipse([cx - r - 3 * k, cy - r - 3 * k, cx + r + 3 * k, cy + r + 3 * k], fill=(60, 60, 60)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 243, 235))
    for t in range(12):
        a = math.radians(t * 30 - 90); d.line([cx + (r - 6 * k) * math.cos(a), cy + (r - 6 * k) * math.sin(a), cx + (r - 2 * k) * math.cos(a), cy + (r - 2 * k) * math.sin(a)], fill=(30, 30, 30), width=max(1, int(1.5 * k)))
    ah = math.radians((S["h"] % 12) * 30 + S["m"] * 0.5 - 90); am = math.radians(S["m"] * 6 - 90)
    d.line([cx, cy, cx + r * 0.5 * math.cos(ah), cy + r * 0.5 * math.sin(ah)], fill=(20, 20, 20), width=max(2, int(3 * k))); d.line([cx, cy, cx + r * 0.85 * math.cos(am), cy + r * 0.85 * math.sin(am)], fill=(20, 20, 20), width=max(1, int(2 * k)))
    for i in range(14): d.ellipse([(60 + i * 70) * k, 470 * k, (76 + i * 70) * k, 486 * k], fill=(90, 80, 70))
    d.text((20 * k, 660 * k), "Market Square webcam, still image", fill=(250, 250, 250), font=base.font(16 * k))
    return img


def render(): return base.png(scene(1))
def click(x, y): return {"ignored": True}


def get(path, full):
    if path == "/__zoom.png":
        q = dict(kv.split("=") for kv in full.split("?", 1)[1].split("&") if "=" in kv) if "?" in full else {}
        try: x, y = int(float(q.get("x", 480))), int(float(q.get("y", 180)))
        except ValueError: x, y = 480, 180
        z = 4; bw, bh = 80, 50; x0, y0 = max(0, min(W - 2 * bw, x - bw)), max(0, min(H - 2 * bh, y - bh))
        return (base.png(scene(z).crop((x0 * z, y0 * z, (x0 + 2 * bw) * z, (y0 + 2 * bh) * z))), "image/png")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("time") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


import json
def state():
    ok = False
    if S["submissions"]:
        try:
            t = S["submissions"][-1].lower().replace("am", "").replace("pm", "").strip(); hh, mm = [int(v) for v in t.split(":")[:2]]
            target = (S["h"] % 12) * 60 + S["m"]; got = (hh % 12) * 60 + mm; ok = min(abs(target - got), 720 - abs(target - got)) <= 2
        except Exception: ok = False
    return {"time": "%d:%02d" % (S["h"], S["m"]), "submissions": S["submissions"], "complete": ok}


def page():
    return f"""<!doctype html><meta charset=utf-8><title>Market Square webcam</title>
<style>body{{font:14px system-ui;margin:0;background:#fff;color:#111}}#wrap{{position:relative;width:1000px;margin:0 auto}}#s{{display:block;cursor:zoom-in}}#lens{{position:absolute;display:none;border:2px solid #111;box-shadow:0 4px 16px rgba(0,0,0,.3);background:#fff}}
#ans{{width:960px;margin:12px auto;padding:12px;background:#f3f4f6;border-radius:8px}}input,button{{font:inherit;padding:6px 8px}}.note{{color:#6b7280;font-size:13px;width:1000px;margin:8px auto}}</style>
<p class=note>Market Square webcam, latest still. Click anywhere on the photo to magnify that area; click the magnified view to close it.</p>
<div id=wrap><img id=s src="/__scene.png" width=1000 height=700 alt="webcam still"><img id=lens width=640 height=400 alt="magnified"></div>
<div id=ans><label>Time on the tower clock (HH:MM, 12-hour): <input id=t size=8></label> <button id=go>Submit</button> <span id=msg></span></div>
<script>(function(){{var s=document.getElementById('s'),l=document.getElementById('lens');s.onclick=function(e){{var r=s.getBoundingClientRect(),x=Math.round(e.clientX-r.left),y=Math.round(e.clientY-r.top);l.src='/__zoom.png?x='+x+'&y='+y+'&t='+Date.now();l.style.left=Math.max(0,Math.min(360,x-320))+'px';l.style.top=Math.max(0,Math.min(300,y-200))+'px';l.style.display='block'}};l.onclick=function(){{l.style.display='none'}};
document.getElementById('go').onclick=function(){{fetch('/__answer',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{time:document.getElementById('t').value}})}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Submitted ('+j.n+').'}})}}}})();</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8850)
