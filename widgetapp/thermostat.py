#!/usr/bin/env python3
"""159-thermostat: an image-only smart-thermostat panel. Set the target to a stated temperature (0.5 steps via the
+/- buttons), mode Heat, leave fan as is, then Save. complete = saved setpoint and mode match, fan unchanged."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, imgapp
TITLE = "Thermostat panel"; W, H = 700, 520
S = {"set": 19.0, "mode": "Cool", "fan": "Auto", "saved": None, "target": 21.5}
NOTE = ""


def reset():
    global NOTE
    S["set"] = random.choice([17.0, 18.5, 19.0, 24.0]); S["mode"] = random.choice(["Cool", "Off", "Auto"]); S["fan"] = random.choice(["Auto", "On"]); S["saved"] = None; S["target"] = random.choice([20.5, 21.5, 22.5, 23.5])
    NOTE = f"Wall thermostat (image; responds to clicks; refreshes after each click). Set the target temperature to {S['target']:.1f} C in Heat mode, leave the fan setting unchanged, then Save."; sys.modules[__name__].NOTE = NOTE


MODES = ["Off", "Heat", "Cool", "Auto"]


def draw():
    img = Image.new("RGB", (W, H), (30, 30, 34)); d = ImageDraw.Draw(img); d.text((30, 24), "Living room", fill=(200, 200, 210), font=base.font(18)); d.text((30, 50), "Current 20.1 C", fill=(140, 140, 150), font=base.font(14, False))
    d.ellipse([230, 90, 470, 330], fill=(45, 45, 52)); d.text((286, 170), f"{S['set']:.1f}", fill=(255, 255, 255), font=base.font(56)); d.text((320, 240), "target", fill=(140, 140, 150), font=base.font(13, False))
    d.ellipse([120, 170, 200, 250], fill=(70, 70, 80)); d.text((150, 190), "-", fill=(255, 255, 255), font=base.font(34)); d.ellipse([500, 170, 580, 250], fill=(70, 70, 80)); d.text((526, 190), "+", fill=(255, 255, 255), font=base.font(34))
    for i, m in enumerate(MODES):
        x = 60 + i * 150; on = S["mode"] == m; d.rounded_rectangle([x, 370, x + 130, 410], 8, fill=(220, 90, 40) if on and m == "Heat" else (60, 130, 220) if on and m == "Cool" else (90, 90, 100) if on else (50, 50, 58)); d.text((x + 45, 381), m, fill=(255, 255, 255), font=base.font(15))
    d.text((60, 432), "Fan:", fill=(140, 140, 150), font=base.font(14, False)); d.rounded_rectangle([110, 426, 200, 456], 8, fill=(90, 90, 100)); d.text((135, 434), S["fan"], fill=(255, 255, 255), font=base.font(14))
    d.rounded_rectangle([520, 424, 660, 462], 8, fill=(34, 160, 90)); d.text((570, 434), "Save", fill=(255, 255, 255), font=base.font(16))
    if S["saved"]: d.text((360, 470), "Saved", fill=(120, 220, 140), font=base.font(13))
    return img


def hit(x, y):
    if imgapp.inside(x, y, [120, 170, 200, 250]): S["set"] = round(max(10, S["set"] - 0.5), 1); S["saved"] = None
    elif imgapp.inside(x, y, [500, 170, 580, 250]): S["set"] = round(min(30, S["set"] + 0.5), 1); S["saved"] = None
    elif imgapp.inside(x, y, [110, 426, 200, 456]): S["fan"] = "On" if S["fan"] == "Auto" else "Auto"; S["saved"] = None
    elif imgapp.inside(x, y, [520, 424, 660, 462]): S["saved"] = {"set": S["set"], "mode": S["mode"], "fan": S["fan"]}
    else:
        for i, m in enumerate(MODES):
            if imgapp.inside(x, y, [60 + i * 150, 370, 190 + i * 150, 410]): S["mode"] = m; S["saved"] = None


def state():
    sv = S["saved"]; return {"target": S["target"], "initial_fan": S.get("fan0"), "saved": sv, "complete": sv is not None and sv["set"] == S["target"] and sv["mode"] == "Heat" and sv["fan"] == S["fan0"]}


_r = reset
def reset():
    _r(); S["fan0"] = S["fan"]
imgapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8855)
