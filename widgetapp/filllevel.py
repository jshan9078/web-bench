#!/usr/bin/env python3
"""111-fill-level: five storage tanks of different heights drawn as gauges with liquid levels and only 0/50/100
marks. Task: tank C's fill percentage within 5 points. Fill must be judged relative to each tank's own height.
complete = within 5 points."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Tank farm overview"; W, H = 960, 480; QUESTION = "What is the fill level of tank C, as a percentage of its capacity (within 5 points)?"
TANKS = "ABCDE"
S = {"fill": [], "height": []}


def reset():
    S["fill"] = [random.choice([v for v in range(8, 93) if abs(v - 50) > 6 and v % 10 not in (0,)]) for _ in TANKS]
    S["height"] = [random.randint(180, 330) for _ in TANKS]


def draw():
    img = Image.new("RGB", (W, H), (245, 245, 247)); d = ImageDraw.Draw(img); d.text((20, 12), "Tank farm, live levels", fill=(50, 50, 60), font=base.font(16))
    for i, t in enumerate(TANKS):
        x = 80 + i * 180; h = S["height"][i]; y0 = 400 - h; w = 90
        d.rounded_rectangle([x, y0, x + w, 400], 12, fill=(255, 255, 255), outline=(90, 90, 100), width=3)
        lvl = 400 - int(h * S["fill"][i] / 100); d.rounded_rectangle([x + 3, lvl, x + w - 3, 397], 9, fill=(56, 140, 220))
        for frac, lab in [(0, "0"), (0.5, "50"), (1, "100")]:
            yy = 400 - int(h * frac); d.line([x + w, yy, x + w + 10, yy], fill=(90, 90, 100), width=2); d.text((x + w + 14, yy - 7), lab, fill=(90, 90, 100), font=base.font(12, False))
        d.text((x + w / 2 - 8, 412), t, fill=(50, 50, 60), font=base.font(20))
    return img


def check(s):
    try: return abs(perception.num(s) - S["fill"][2]) <= 5
    except Exception: return False


def answer_state(): return {"tank_c": S["fill"][2], "fills": dict(zip(TANKS, S["fill"]))}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8831)
