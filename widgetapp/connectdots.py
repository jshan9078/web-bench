#!/usr/bin/env python3
"""304-connect-the-numbers: fifteen numbered points scattered among lettered decoys; click 1, 2, ... 15 in order
(a line is drawn as you go; a wrong click resets), then Confirm. Search plus ordered precise clicks.
complete = confirmed sequence is 1..15."""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 900, 600
S = {"pts": [], "seq": [], "confirmed": None}


def reset():
    pts = []
    while len(pts) < 30:
        p = (random.randint(30, 870), random.randint(30, 570))
        if all(math.dist(p, q) > 48 for q in pts): pts.append(p)
    labels = [str(i) for i in range(1, 16)] + list("ABCDEFGHJKLMNPQ"); random.shuffle(labels)
    S["pts"] = [(p[0], p[1], l) for p, l in zip(pts, labels)]; S["seq"] = []; S["confirmed"] = None


def render():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    path = [next((x, y) for x, y, l in S["pts"] if l == str(k)) for k in range(1, len(S["seq"]) + 1)]
    if len(path) > 1: d.line(path, fill=(220, 38, 38), width=3)
    for x, y, l in S["pts"]:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(30, 41, 59)); d.text((x + 7, y - 9), l, fill=(30, 41, 59), font=base.font(13))
    return base.png(img)


def click(x, y):
    hit = min(S["pts"], key=lambda p: math.dist((x, y), (p[0], p[1])))
    if math.dist((x, y), (hit[0], hit[1])) > 14: return {"miss": True}
    want = str(len(S["seq"]) + 1)
    if hit[2] == want: S["seq"].append(hit[2])
    else: S["seq"] = []
    return {"seq": S["seq"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = list(S["seq"]); return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state(): return {"confirmed": S["confirmed"], "progress": len(S["seq"]), "complete": S["confirmed"] == [str(i) for i in range(1, 16)]}


def page():
    return base.image_page("Connect the numbers", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:860px"><p>The image shows thirty labelled points: the numbers 1 to 15 and fifteen letters as decoys. Click the numbered points in order from 1 to 15 (click within a few pixels of the dot; a red line traces your progress; a wrong click resets to the start), then confirm.</p><button id=go>Confirm</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+j.confirmed.length+' points'}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8944)
