#!/usr/bin/env python3
"""137-crop-corners: a document-scanner style crop: a photo of a receipt lying on a desk at an angle; the user
marks the receipt's TOP-LEFT and BOTTOM-RIGHT corners by clicking them (two clicks), then confirms. Precision
placement of two points. complete = both confirmed points within 10 px of the true corners."""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 900, 640
S = {"quad": [], "pts": [], "confirmed": None}


def reset():
    cx, cy = random.randint(380, 520), random.randint(280, 360); w, h = random.randint(220, 300), random.randint(320, 420); a = math.radians(random.uniform(-14, 14))
    def rot(x, y): return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    S["quad"] = [rot(-w / 2, -h / 2), rot(w / 2, -h / 2), rot(w / 2, h / 2), rot(-w / 2, h / 2)]; S["pts"] = []; S["confirmed"] = None


def render():
    img = Image.new("RGB", (W, H), (98, 84, 70)); d = ImageDraw.Draw(img)
    for i in range(0, W, 37): d.line([(i, 0), (i + 20, H)], fill=(92, 79, 66), width=2)
    d.polygon([(x + 8, y + 10) for x, y in S["quad"]], fill=(60, 52, 44)); d.polygon(S["quad"], fill=(246, 244, 236), outline=(200, 196, 186))
    q = S["quad"]; f = base.font(11, False)
    for k in range(9):
        t = 0.12 + k * 0.09; p0 = (q[0][0] + (q[3][0] - q[0][0]) * t, q[0][1] + (q[3][1] - q[0][1]) * t); p1 = (q[1][0] + (q[2][0] - q[1][0]) * t, q[1][1] + (q[2][1] - q[1][1]) * t)
        d.line([p0, (p0[0] + (p1[0] - p0[0]) * 0.7, p0[1] + (p1[1] - p0[1]) * 0.7)], fill=(120, 120, 130), width=2)
    for i, (x, y) in enumerate(S["pts"]): d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=(40, 160, 220), width=3); d.text((x + 10, y - 8), ["TL", "BR"][i], fill=(40, 160, 220), font=base.font(12))
    if len(S["pts"]) == 2: d.rectangle([S["pts"][0], S["pts"][1]], outline=(40, 160, 220), width=2)
    return base.png(img)


def click(x, y):
    if len(S["pts"]) >= 2: S["pts"] = []
    S["pts"].append((int(x), int(y))); return {"pts": S["pts"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = list(S["pts"]); return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    tl, br = S["quad"][0], S["quad"][2]; c = S["confirmed"]; ok = False
    if c and len(c) == 2:
        ok = math.dist(c[0], tl) <= 10 and math.dist(c[1], br) <= 10
    return {"corners": {"tl": [round(v) for v in tl], "br": [round(v) for v in br]}, "points": S["pts"], "confirmed": c, "complete": ok}


def page():
    return base.image_page("Scan receipt: mark corners", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:860px"><p>Mark the receipt's TOP-LEFT corner, then its BOTTOM-RIGHT corner, by clicking exactly on them (a third click starts over). Then confirm.</p><button id=go>Confirm corners</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});
document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+JSON.stringify(j.confirmed)}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8845)
