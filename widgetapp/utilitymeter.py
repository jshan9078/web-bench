#!/usr/bin/env python3
"""162-utility-meter: a photo of an electricity meter with four pointer dials that alternate direction (the classic
meter-reading problem); pointers sit between digits. Task: the 4-digit reading (each dial: the digit the pointer
has passed). complete = exact."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Meter reading"; W, H = 960, 480; QUESTION = "What is the meter reading (4 digits, read the dials left to right; each dial shows the digit its pointer has passed, and adjacent dials run in opposite directions as printed)?"
S = {"digits": [], "frac": []}


def reset(): S["digits"] = [random.randint(0, 9) for _ in range(4)]; S["frac"] = [random.uniform(0.25, 0.75) for _ in range(4)]


def draw():
    img = Image.new("RGB", (W, H), (225, 225, 220)); d = ImageDraw.Draw(img); d.rounded_rectangle([40, 40, 920, 440], 16, fill=(245, 245, 240), outline=(120, 120, 120), width=3); d.text((60, 56), "kWh   ELECTRICITY METER   No. 44817-2", fill=(40, 40, 40), font=base.font(15))
    for i in range(4):
        cx, cy, r = 160 + i * 215, 250, 85; cw = (i % 2 == 0)     # dial 1 clockwise, dial 2 counter-clockwise, ...
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=(40, 40, 40), width=2)
        for k in range(10):
            ang = math.radians((k * 36 if cw else -k * 36) - 90); d.line([cx + (r - 10) * math.cos(ang), cy + (r - 10) * math.sin(ang), cx + (r - 2) * math.cos(ang), cy + (r - 2) * math.sin(ang)], fill=(30, 30, 30), width=2)
            d.text((cx + (r - 26) * math.cos(ang) - 5, cy + (r - 26) * math.sin(ang) - 8), str(k), fill=(30, 30, 30), font=base.font(13))
        v = S["digits"][i] + S["frac"][i]; ang = math.radians((v * 36 if cw else -v * 36) - 90)
        d.line([cx - 14 * math.cos(ang), cy - 14 * math.sin(ang), cx + (r - 30) * math.cos(ang), cy + (r - 30) * math.sin(ang)], fill=(200, 30, 30), width=4); d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(30, 30, 30))
        d.text((cx - 22, cy + r + 10), ["1000", "100", "10", "1"][i], fill=(60, 60, 60), font=base.font(12, False)); d.text((cx - 16, cy - r - 26), "CW" if cw else "CCW", fill=(60, 60, 60), font=base.font(12))
    return img


def check(s):
    try: return "".join(ch for ch in s if ch.isdigit()).lstrip("0").rjust(1, "0") == "".join(map(str, S["digits"])).lstrip("0").rjust(1, "0")
    except Exception: return False


def answer_state(): return {"reading": "".join(map(str, S["digits"])), "fractions": [round(f, 2) for f in S["frac"]]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8858)
