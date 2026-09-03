#!/usr/bin/env python3
"""160-parking-meter: an image-only pay-and-display meter. Choose the stated zone, add time to reach exactly the
stated duration (+15 min / +1 h / -15 min buttons), then Pay. complete = paid with the right zone and minutes."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, imgapp
TITLE = "Parking meter"; W, H = 600, 640; NOTE = ""
S = {"zone": None, "mins": 0, "paid": None, "want": ("B", 135)}


def reset():
    global NOTE
    S["zone"] = None; S["mins"] = 0; S["paid"] = None; S["want"] = (random.choice("ABC"), random.choice([75, 105, 135, 165, 195]))
    NOTE = f"Pay-and-display meter (image; responds to clicks; refreshes after each click). Pay for zone {S['want'][0]} for exactly {S['want'][1] // 60} h {S['want'][1] % 60:02d} min."; sys.modules[__name__].NOTE = NOTE


def draw():
    img = Image.new("RGB", (W, H), (70, 74, 80)); d = ImageDraw.Draw(img); d.rounded_rectangle([60, 40, 540, 600], 20, fill=(40, 44, 50)); d.text((90, 60), "CITY PARKING", fill=(230, 230, 230), font=base.font(20))
    d.rectangle([90, 100, 510, 190], fill=(180, 220, 170)); d.text((104, 110), f"Zone: {S['zone'] or '-'}", fill=(20, 40, 20), font=base.font(18)); d.text((104, 142), f"Time: {S['mins'] // 60} h {S['mins'] % 60:02d} min    Cost: ${S['mins'] / 60 * (3.5 if S['zone'] == 'A' else 2.5 if S['zone'] == 'B' else 1.5 if S['zone'] else 0):.2f}", fill=(20, 40, 20), font=base.font(16))
    if S["paid"]: d.text((104, 168), f"PAID  zone {S['paid'][0]}  {S['paid'][1] // 60} h {S['paid'][1] % 60:02d} min", fill=(20, 40, 20), font=base.font(14))
    d.text((90, 210), "Select zone", fill=(180, 180, 190), font=base.font(13, False))
    for i, z in enumerate("ABC"):
        x = 90 + i * 145; d.rounded_rectangle([x, 232, x + 130, 282], 10, fill=(37, 99, 235) if S["zone"] == z else (90, 96, 106)); d.text((x + 52, 246), z, fill=(255, 255, 255), font=base.font(20))
    d.text((90, 306), "Add time", fill=(180, 180, 190), font=base.font(13, False))
    for i, lab in enumerate(["+15 min", "+1 h", "-15 min"]):
        x = 90 + i * 145; d.rounded_rectangle([x, 328, x + 130, 378], 10, fill=(90, 96, 106)); d.text((x + 28, 344), lab, fill=(255, 255, 255), font=base.font(16))
    d.rounded_rectangle([90, 430, 510, 500], 12, fill=(34, 160, 90)); d.text((260, 452), "PAY", fill=(255, 255, 255), font=base.font(22)); d.rounded_rectangle([90, 520, 510, 560], 10, fill=(120, 60, 60)); d.text((270, 530), "Cancel", fill=(255, 255, 255), font=base.font(15))
    return img


def hit(x, y):
    for i, z in enumerate("ABC"):
        if imgapp.inside(x, y, [90 + i * 145, 232, 220 + i * 145, 282]): S["zone"] = z
    for i, dm in enumerate([15, 60, -15]):
        if imgapp.inside(x, y, [90 + i * 145, 328, 220 + i * 145, 378]): S["mins"] = max(0, min(600, S["mins"] + dm))
    if imgapp.inside(x, y, [90, 430, 510, 500]) and S["zone"] and S["mins"] and not S["paid"]: S["paid"] = (S["zone"], S["mins"])
    if imgapp.inside(x, y, [90, 520, 510, 560]): S["zone"] = None; S["mins"] = 0


def state(): return {"want": S["want"], "paid": S["paid"], "complete": S["paid"] == S["want"]}


imgapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8856)
