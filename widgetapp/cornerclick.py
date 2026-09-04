#!/usr/bin/env python3
"""315-corner-click: a rotated square outline; click its TOP-MOST corner within 5 px, then Confirm.
complete = confirmed click within tolerance."""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 800, 560
S = {"c": (0, 0), "r": 0, "rot": 0, "click": None, "confirmed": None}


def corners():
    cx, cy = S["c"]; return [(cx + S["r"] * math.cos(math.radians(S["rot"] + k * 90)), cy - S["r"] * math.sin(math.radians(S["rot"] + k * 90))) for k in range(4)]


def reset(): S["c"] = (random.randint(250, 550), random.randint(200, 360)); S["r"] = random.randint(110, 170); S["rot"] = random.uniform(5, 80); S["click"] = None; S["confirmed"] = None


def render():
    img = Image.new("RGB", (W, H), (248, 247, 244)); d = ImageDraw.Draw(img); pts = corners(); d.polygon(pts, outline=(30, 30, 30)); d.line(pts + [pts[0]], fill=(30, 30, 30), width=2)
    if S["click"]: x, y = S["click"]; d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=(220, 38, 38), width=2)
    return base.png(img)


def click(x, y): S["click"] = (int(x), int(y)); return {"click": S["click"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = S["click"]; return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    top = min(corners(), key=lambda p: p[1]); c = S["confirmed"]; err = math.dist(c, top) if c else None
    return {"top_corner": [round(top[0], 1), round(top[1], 1)], "confirmed": c, "error_px": None if err is None else round(err, 1), "complete": err is not None and err <= 5}


def page():
    return base.image_page("Square", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:760px"><p>The image shows one rotated square outline. Click its TOP-MOST corner (the vertex with the smallest y) within 5 px (a red circle marks your click; re-click to move it; click with click --at X,Y), then confirm.</p><button id=go>Confirm</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+JSON.stringify(j.confirmed)}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8953)
