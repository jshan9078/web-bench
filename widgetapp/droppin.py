#!/usr/bin/env python3
"""122-drop-pin: a street-map IMAGE (named streets, blocks, a park) and a task to drop a pin exactly on a named
intersection, then Confirm. Clicking places the pin (server side) and re-renders; Confirm records it. Precision
click on an image with feedback. complete = confirmed pin within 8 px of the intersection."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 900, 620
EW = ["Harbor St", "Maple Ave", "Church St", "King St", "Mill Rd", "Elm St"]; NS = ["1st Ave", "2nd Ave", "3rd Ave", "4th Ave", "5th Ave", "6th Ave", "7th Ave"]
S = {"xs": [], "ys": [], "target": (0, 0), "pin": None, "confirmed": None}


def reset():
    xs = sorted(random.sample(range(70, 850, 40), 7)); ys = sorted(random.sample(range(70, 570, 40), 6))
    S["xs"], S["ys"] = xs, ys; S["target"] = (random.randrange(7), random.randrange(6)); S["pin"] = None; S["confirmed"] = None


def tpos(): return S["xs"][S["target"][0]], S["ys"][S["target"][1]]


def render():
    img = Image.new("RGB", (W, H), (232, 236, 226)); d = ImageDraw.Draw(img)
    d.rectangle([S["xs"][1] + 6, S["ys"][3] + 6, S["xs"][3] - 6, S["ys"][5] - 6], fill=(190, 222, 180)); d.text((S["xs"][1] + 14, S["ys"][3] + 12), "Riverside Park", fill=(70, 110, 60), font=base.font(12, False))
    for i, y in enumerate(S["ys"]):
        d.line([(20, y), (W - 20, y)], fill=(255, 255, 255), width=10); d.line([(20, y), (W - 20, y)], fill=(200, 200, 205), width=1); d.text((24, y - 18), EW[i], fill=(60, 60, 70), font=base.font(11, False))
    for j, x in enumerate(S["xs"]):
        d.line([(x, 20), (x, H - 20)], fill=(255, 255, 255), width=10); d.line([(x, 20), (x, H - 20)], fill=(200, 200, 205), width=1)
        t = Image.new("RGBA", (70, 14), (0, 0, 0, 0)); ImageDraw.Draw(t).text((0, 0), NS[j], fill=(60, 60, 70), font=base.font(11, False)); img.paste(t.rotate(90, expand=True), (x + 6, 26), t.rotate(90, expand=True))
    if S["pin"]:
        px, py = S["pin"]; d.polygon([(px, py), (px - 9, py - 18), (px + 9, py - 18)], fill=(220, 40, 40)); d.ellipse([px - 11, py - 30, px + 11, py - 8], fill=(220, 40, 40)); d.ellipse([px - 4, py - 23, px + 4, py - 15], fill=(255, 255, 255))
    return base.png(img)


def click(x, y): S["pin"] = (int(x), int(y)); return {"pin": S["pin"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = S["pin"]; return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    tx, ty = tpos(); c = S["confirmed"]; ok = c is not None and ((c[0] - tx) ** 2 + (c[1] - ty) ** 2) ** 0.5 <= 8
    return {"target": {"streets": f"{NS[S['target'][0]]} & {EW[S['target'][1]]}", "xy": [tx, ty]}, "pin": S["pin"], "confirmed": c, "complete": ok}


def page():
    t = f"{NS[S['target'][0]]} and {EW[S['target'][1]]}"
    return base.image_page("Report an issue: drop a pin", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:860px"><p>Drop the pin exactly on the intersection of <b>{t}</b> (click the map; the pin's tip marks the spot; you can re-click to move it), then confirm.</p><button id=go>Confirm pin</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});
document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent=j.confirmed?'Pin confirmed at '+j.confirmed.join(','):'No pin placed yet.'}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8840)
