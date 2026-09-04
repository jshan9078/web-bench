#!/usr/bin/env python3
"""308-ellipse-centre: a rotated ellipse outline on a textured background; click its centre within 6 px, then
Confirm. complete = confirmed click within tolerance."""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 800, 560
S = {"c": (0, 0), "ab": (0, 0), "rot": 0, "click": None, "confirmed": None, "noise": []}


def reset():
    S["c"] = (random.randint(220, 580), random.randint(180, 400)); S["ab"] = (random.randint(120, 200), random.randint(50, 90)); S["rot"] = random.uniform(0, 180); S["click"] = None; S["confirmed"] = None
    S["noise"] = [(random.randint(0, W), random.randint(0, H), random.randint(3, 9)) for _ in range(160)]


def render():
    img = Image.new("RGB", (W, H), (245, 243, 238)); d = ImageDraw.Draw(img)
    for x, y, r in S["noise"]: d.ellipse([x - r, y - r, x + r, y + r], fill=(225, 222, 214))
    cx, cy = S["c"]; a, b = S["ab"]; th = math.radians(S["rot"])
    pts = [(cx + a * math.cos(t) * math.cos(th) - b * math.sin(t) * math.sin(th), cy + a * math.cos(t) * math.sin(th) + b * math.sin(t) * math.cos(th)) for t in [i * 2 * math.pi / 180 for i in range(181)]]
    d.line(pts, fill=(30, 30, 30), width=3)
    if S["click"]: x, y = S["click"]; d.line([(x - 8, y), (x + 8, y)], fill=(220, 38, 38), width=2); d.line([(x, y - 8), (x, y + 8)], fill=(220, 38, 38), width=2)
    return base.png(img)


def click(x, y): S["click"] = (int(x), int(y)); return {"click": S["click"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = S["click"]; return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    c = S["confirmed"]; err = math.dist(c, S["c"]) if c else None
    return {"centre": S["c"], "confirmed": c, "error_px": None if err is None else round(err, 1), "complete": err is not None and err <= 6}


def page():
    return base.image_page("Ellipse", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:760px"><p>The image shows one rotated ellipse outline on a speckled background. Click the ellipse's exact centre (within 6 px; a red cross marks your click; re-click to move it; click with click --at X,Y), then confirm.</p><button id=go>Confirm</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+JSON.stringify(j.confirmed)}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8948)
