#!/usr/bin/env python3
"""282-hue-order: nine colour swatches of the same saturation and lightness but different hues, shuffled. Task:
click them in order from the reddest going through orange, yellow, green, cyan, blue to violet (hue ascending),
then Confirm. complete = confirmed sequence equals the hue order."""
import json, random, sys, os, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 900, 300
S = {"hues": [], "order": [], "clicks": [], "confirmed": None}


def reset():
    while True:
        hues = sorted(random.sample(range(0, 300, 6), 9))
        if all(b - a >= 18 for a, b in zip(hues, hues[1:])): break
    S["order"] = list(range(9)); random.shuffle(S["order"]); S["hues"] = hues; S["clicks"] = []; S["confirmed"] = None


def pos(i): return 30 + i * 96, 90


def render():
    img = Image.new("RGB", (W, H), (245, 245, 245)); d = ImageDraw.Draw(img)
    for i, k in enumerate(S["order"]):
        x, y = pos(i); r, g, b = colorsys.hls_to_rgb(S["hues"][k] / 360, 0.5, 0.75); d.rectangle([x, y, x + 80, y + 120], fill=(int(r * 255), int(g * 255), int(b * 255)), outline=(60, 60, 60))
        if i in S["clicks"]: d.text((x + 30, y + 130), str(S["clicks"].index(i) + 1), fill=(30, 30, 30), font=base.font(18))
    d.text((30, 20), "Click the swatches in hue order (red first, violet last), then Confirm.", fill=(40, 40, 40), font=base.font(15))
    return base.png(img)


def click(x, y):
    for i in range(9):
        px, py = pos(i)
        if px <= x <= px + 80 and py <= y <= py + 120:
            if i in S["clicks"]: S["clicks"].remove(i)
            else: S["clicks"].append(i)
    return {"clicks": S["clicks"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = list(S["clicks"]); return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    want = sorted(range(9), key=lambda i: S["hues"][S["order"][i]]); return {"want_positions": want, "confirmed": S["confirmed"], "complete": S["confirmed"] == want}


def page():
    return base.image_page("Colour sort", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui"><p>Click the nine swatches (image above; use click --at X,Y) in hue order from red through orange, yellow, green, cyan and blue to violet; a number appears on each clicked swatch (click again to unselect). Then confirm.</p><button id=go>Confirm order</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+JSON.stringify(j.confirmed)}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8928)
