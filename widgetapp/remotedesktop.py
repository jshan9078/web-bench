#!/usr/bin/env python3
"""128-remote-desktop: a browser-based remote desktop (Citrix/VNC style): the whole UI is a server-rendered
IMAGE and every interaction is a raw click on it. Task: open Settings, turn ON "Night light" (not "Night light
schedule"), and close the window, changing nothing else. complete = night light on, other toggles untouched,
window closed."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 1024, 640
ICONS = [("Files", (120, 160, 210)), ("Settings", (110, 110, 120)), ("Display", (90, 160, 110)), ("Trash", (150, 150, 150)), ("Mail", (220, 150, 80))]
TOGGLES = ["Bluetooth", "Night light schedule", "Night light", "Do not disturb", "Location"]
S = {"icon_pos": {}, "win": False, "toggles": {}, "log": []}


def reset():
    pos = [(60, 60), (60, 170), (60, 280), (60, 390), (60, 500)]; random.shuffle(pos)
    S["icon_pos"] = {n: p for (n, _), p in zip(ICONS, pos)}; S["win"] = False; S["toggles"] = {t: False for t in TOGGLES}; S["log"] = []
    S["toggles"]["Bluetooth"] = random.random() < 0.5; S["order"] = TOGGLES[:]; random.shuffle(S["order"])


def render():
    img = Image.new("RGB", (W, H), (36, 70, 110)); d = ImageDraw.Draw(img)
    for n, c in ICONS:
        x, y = S["icon_pos"][n]; d.rounded_rectangle([x, y, x + 56, y + 56], 10, fill=c)
        if n == "Settings":
            import math
            for k in range(8): a = math.radians(k * 45); d.line([x + 28 + 14 * math.cos(a), y + 28 + 14 * math.sin(a), x + 28 + 24 * math.cos(a), y + 28 + 24 * math.sin(a)], fill=(230, 230, 235), width=6)
            d.ellipse([x + 14, y + 14, x + 42, y + 42], fill=(230, 230, 235)); d.ellipse([x + 22, y + 22, x + 34, y + 34], fill=c)
        elif n == "Display": d.rectangle([x + 10, y + 12, x + 46, y + 38], fill=(230, 240, 235)); d.rectangle([x + 22, y + 40, x + 34, y + 46], fill=(230, 240, 235))
        d.text((x - 4, y + 62), n, fill=(240, 240, 240), font=base.font(13))
    d.rectangle([0, H - 44, W, H], fill=(20, 24, 32)); d.text((16, H - 30), "Start", fill=(230, 230, 230), font=base.font(14)); d.text((W - 70, H - 30), "14:32", fill=(230, 230, 230), font=base.font(14))
    if S["win"]:
        d.rectangle([300, 90, 860, 520], fill=(245, 245, 247)); d.rectangle([300, 90, 860, 126], fill=(225, 225, 230)); d.text((316, 100), "Settings", fill=(30, 30, 30), font=base.font(15))
        d.rectangle([826, 96, 852, 120], fill=(200, 60, 60)); d.text((833, 98), "x", fill=(255, 255, 255), font=base.font(15))
        d.text((330, 150), "System", fill=(90, 90, 100), font=base.font(13))
        for i, t in enumerate(S["order"]):
            y = 190 + i * 56; on = S["toggles"][t]; d.text((330, y + 4), t, fill=(30, 30, 30), font=base.font(16, False))
            d.rounded_rectangle([760, y, 816, y + 28], 14, fill=(50, 160, 90) if on else (180, 180, 190)); d.ellipse([789 if on else 763, y + 3, 813 if on else 787, y + 25], fill=(255, 255, 255))
    return base.png(img)


def click(x, y):
    S["log"].append((int(x), int(y)))
    if S["win"]:
        if 826 <= x <= 852 and 96 <= y <= 120: S["win"] = False; return {"closed": True}
        for i, t in enumerate(S["order"]):
            yy = 190 + i * 56
            if 700 <= x <= 830 and yy - 6 <= y <= yy + 34: S["toggles"][t] = not S["toggles"][t]; return {"toggled": t, "on": S["toggles"][t]}
        return {"window": True}
    for n, _ in ICONS:
        ix, iy = S["icon_pos"][n]
        if ix <= x <= ix + 56 and iy <= y <= iy + 76:
            if n == "Settings": S["win"] = True; return {"opened": "Settings"}
            return {"opened": n, "note": "app has no window in this demo"}
    return {"ignored": True}


def post(path, data, ctype): return None


def state():
    t = S["toggles"]; init_bt = None
    ok = t["Night light"] and not t["Night light schedule"] and not t["Do not disturb"] and not t["Location"] and not S["win"]
    return {"toggles": t, "window_open": S["win"], "clicks": len(S["log"]), "complete": ok}


def page():
    return base.image_page("Remote desktop: WS-114", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:980px"><p>Remote session to WS-114 (image stream; the desktop responds to clicks on the image, which refreshes after each click).</p>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}})</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8842)
