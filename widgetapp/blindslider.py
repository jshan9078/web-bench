#!/usr/bin/env python3
"""151-blind-slider: a media player's volume control is a plain div bar with a handle and NO numeric readout;
the target volume is stated. Clicking the bar sets the level (server-side, re-rendered as an image so nothing
in the DOM carries the value). Task: set the volume to a given percentage within 3 points and press Save.
complete = saved level within tolerance."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 700, 200; X0, X1 = 60, 640
S = {"target": 0, "level": 50, "saved": None}


def reset(): S["target"] = random.choice([v for v in range(12, 92) if v % 5 not in (0,)]); S["level"] = random.choice([20, 35, 50, 65]); S["saved"] = None


def render():
    img = Image.new("RGB", (W, H), (24, 24, 27)); d = ImageDraw.Draw(img); d.text((60, 30), "Output volume", fill=(212, 212, 216), font=base.font(16))
    d.rounded_rectangle([X0, 96, X1, 108], 6, fill=(63, 63, 70)); x = X0 + (X1 - X0) * S["level"] / 100; d.rounded_rectangle([X0, 96, x, 108], 6, fill=(96, 165, 250)); d.ellipse([x - 12, 90, x + 12, 114], fill=(250, 250, 250))
    d.text((X0 - 4, 124), "0", fill=(113, 113, 122), font=base.font(12, False)); d.text((X1 - 18, 124), "100", fill=(113, 113, 122), font=base.font(12, False))
    return base.png(img)


def click(x, y):
    if 80 <= y <= 124 and X0 - 14 <= x <= X1 + 14: S["level"] = int(round(max(0, min(100, (x - X0) / (X1 - X0) * 100)))); return {"ok": True}
    return {"ignored": True}


def post(path, data, ctype):
    if path == "/__save": S["saved"] = S["level"]; return (json.dumps({"saved": True}), "application/json")
    return None


def state(): return {"target": S["target"], "level": S["level"], "saved": S["saved"], "complete": S["saved"] is not None and abs(S["saved"] - S["target"]) <= 3}


def page():
    return base.image_page("Sound settings", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:660px"><p>Set the output volume to <b>{S['target']}%</b> (within 3 points) by clicking on the bar, then save. The bar shows the level only visually.</p><button id=go>Save</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});
document.getElementById('go').onclick=function(){{fetch('/__save',{{method:'POST'}}).then(r=>r.json()).then(function(){{document.getElementById('msg').textContent='Saved.'}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8849)
