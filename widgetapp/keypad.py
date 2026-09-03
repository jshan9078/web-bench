#!/usr/bin/env python3
"""138-virtual-keypad: a banking-style login where the 6-digit access code must be entered on an IMAGE keypad
whose key layout is shuffled on every load (an anti-keylogger pattern). The code to enter is shown on the
page as text. Task: enter the code and press the keypad's Enter key. complete = the entered digits equal the
code (server-side)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 360, 480
S = {"layout": [], "code": "", "typed": "", "entered": None}


def reset():
    keys = list("0123456789"); random.shuffle(keys); S["layout"] = keys; S["code"] = "".join(random.choice("0123456789") for _ in range(6)); S["typed"] = ""; S["entered"] = None


def kpos(i):
    r, c = divmod(i, 3); return 30 + c * 100, 120 + r * 80


def render():
    img = Image.new("RGB", (W, H), (245, 246, 250)); d = ImageDraw.Draw(img)
    d.text((30, 24), "Secure keypad", fill=(40, 40, 50), font=base.font(18)); d.rectangle([30, 60, 330, 100], fill=(255, 255, 255), outline=(180, 180, 190))
    d.text((44, 70), "•" * len(S["typed"]), fill=(30, 30, 30), font=base.font(22))
    for i, k in enumerate(S["layout"]):
        x, y = kpos(i); d.rounded_rectangle([x, y, x + 80, y + 60], 8, fill=(255, 255, 255), outline=(170, 170, 180)); d.text((x + 30, y + 16), k, fill=(30, 30, 30), font=base.font(24))
    x, y = kpos(10); d.rounded_rectangle([x, y, x + 80, y + 60], 8, fill=(255, 235, 235), outline=(170, 170, 180)); d.text((x + 14, y + 20), "Clear", fill=(150, 40, 40), font=base.font(16))
    x, y = kpos(11); d.rounded_rectangle([x, y, x + 80, y + 60], 8, fill=(220, 240, 225), outline=(170, 170, 180)); d.text((x + 14, y + 20), "Enter", fill=(30, 110, 60), font=base.font(16))
    return base.png(img)


def click(x, y):
    for i in range(12):
        kx, ky = kpos(i)
        if kx <= x <= kx + 80 and ky <= y <= ky + 60:
            if i < 10:
                if len(S["typed"]) < 6: S["typed"] += S["layout"][i]
            elif i == 10: S["typed"] = ""
            else: S["entered"] = S["typed"]; S["typed"] = ""
            return {"typed_len": len(S["typed"]), "entered": S["entered"]}
    return {"ignored": True}


def post(path, data, ctype): return None


def state(): return {"code": S["code"], "typed": S["typed"], "entered": S["entered"], "complete": S["entered"] == S["code"]}


def page():
    return base.image_page("Harbor Bank, sign in", W, H, extra_html=f"""
<div style="position:absolute;top:0;left:400px;width:520px;font:15px system-ui;color:#111"><h1 style="font-size:20px">Harbor Bank online banking</h1>
<p>For your security, enter your one-time access code on the image keypad to the left. Its key layout changes on every visit. Then press <b>Enter</b> on the keypad.</p>
<p style="font-size:14px;color:#374151">Your access code for this session: <b style="font-size:20px;letter-spacing:3px">{S['code']}</b></p>
<p style="font-size:13px;color:#6b7280">Dots appear in the box above the keypad as you type. Use Clear to start over.</p><p id=msg></p>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}})</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8844)
