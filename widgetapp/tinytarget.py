#!/usr/bin/env python3
"""288-tiny-targets: an image with a field of 40 small grey dots and five 5-pixel blue dots; click each blue dot
(within 4 px) then Confirm. Precision under clutter. complete = all five hit, no more than one stray."""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 900, 560
S = {"blue": [], "grey": [], "clicks": [], "confirmed": None}


def reset():
    pts = []
    while len(pts) < 45:
        p = (random.randint(30, 870), random.randint(30, 530))
        if all(math.dist(p, q) > 26 for q in pts): pts.append(p)
    S["blue"] = pts[:5]; S["grey"] = pts[5:]; S["clicks"] = []; S["confirmed"] = None


def render():
    img = Image.new("RGB", (W, H), (248, 248, 250)); d = ImageDraw.Draw(img)
    for x, y in S["grey"]: d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(150, 150, 158))
    for x, y in S["blue"]: d.ellipse([x - 2, y - 2, x + 3, y + 3], fill=(37, 99, 235))
    for i, (x, y) in enumerate(S["clicks"]): d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(220, 38, 38), width=2)
    return base.png(img)


def click(x, y): S["clicks"].append((int(x), int(y))); return {"n": len(S["clicks"])}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = list(S["clicks"]); return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    if path == "/__undo": S["clicks"] = S["clicks"][:-1]; return (json.dumps({"n": len(S["clicks"])}), "application/json")
    return None


def state():
    c = S["confirmed"] or []; hit = [any(math.dist(k, b) <= 4.5 for k in c) for b in S["blue"]]; stray = sum(1 for k in c if not any(math.dist(k, b) <= 4.5 for b in S["blue"]))
    return {"blue": S["blue"], "confirmed": c, "hits": sum(hit), "stray": stray, "complete": S["confirmed"] is not None and all(hit) and stray <= 1}


def page():
    return base.image_page("Dot field", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:860px"><p>The image contains many grey dots and exactly five small BLUE dots. Click each blue dot precisely (a red ring marks each click; Undo removes the last click), then confirm.</p><button id=undo>Undo last click</button> <button id=go>Confirm</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});document.getElementById('undo').onclick=function(){{fetch('/__undo',{{method:'POST'}}).then(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}})}};document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+j.confirmed.length+' clicks'}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8936)
