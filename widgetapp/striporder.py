#!/usr/bin/env python3
"""292-strip-order: a picture (a simple landscape with a road and a river) is cut into six vertical strips and
shuffled. Click the strips in the order that reconstructs the picture from left to right, then Confirm. Visual
continuity reasoning. complete = confirmed order is correct."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 900, 360; SW = 140
S = {"order": [], "clicks": [], "confirmed": None, "seed": 0}


def reset(): S["order"] = list(range(6)); random.shuffle(S["order"]); S["clicks"] = []; S["confirmed"] = None; S["seed"] = random.randint(1, 10 ** 6)


def picture():
    rng = random.Random(S["seed"]); img = Image.new("RGB", (6 * SW, 300), (135, 190, 235)); d = ImageDraw.Draw(img)
    d.rectangle([0, 170, 840, 300], fill=(90, 160, 80)); pts = [(0, 150)]
    for i in range(1, 9): pts.append((i * 105, rng.randint(60, 150)))
    d.polygon(pts + [(840, 300), (0, 300)], fill=(110, 120, 130))
    ry = rng.randint(200, 250); d.line([(0, ry), (200, ry + rng.randint(-30, 30)), (450, ry + rng.randint(-30, 30)), (840, ry + rng.randint(-30, 30))], fill=(60, 120, 200), width=18)
    d.line([(0, 285), (840, 190 + rng.randint(-20, 20))], fill=(80, 80, 80), width=14)
    for _ in range(5): x, y = rng.randint(20, 820), rng.randint(180, 260); d.ellipse([x - 12, y - 24, x + 12, y], fill=(40, 110, 50))
    return img


def render():
    img = Image.new("RGB", (W, H), (240, 240, 240)); pic = picture(); d = ImageDraw.Draw(img)
    for i, k in enumerate(S["order"]):
        strip = pic.crop((k * SW, 0, (k + 1) * SW, 300)); img.paste(strip, (5 + i * 148, 30))
        if i in S["clicks"]: d.rectangle([5 + i * 148, 30, 5 + i * 148 + SW, 330], outline=(220, 38, 38), width=4); d.text((60 + i * 148, 335), str(S["clicks"].index(i) + 1), fill=(220, 38, 38), font=base.font(16))
    return base.png(img)


def click(x, y):
    for i in range(6):
        if 5 + i * 148 <= x <= 5 + i * 148 + SW and 30 <= y <= 330:
            if i in S["clicks"]: S["clicks"].remove(i)
            else: S["clicks"].append(i)
    return {"clicks": S["clicks"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = list(S["clicks"]); return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    want = sorted(range(6), key=lambda i: S["order"][i]); return {"want_positions": want, "confirmed": S["confirmed"], "complete": S["confirmed"] == want}


def page():
    return base.image_page("Strip puzzle", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:860px"><p>The picture was cut into six vertical strips and shuffled (image above; click with click --at X,Y). Click the strips in the order that rebuilds the original picture from LEFT to RIGHT (the road and river must join up); a number appears on each clicked strip (click again to unselect). Then confirm.</p><button id=go>Confirm order</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+JSON.stringify(j.confirmed)}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8938)
