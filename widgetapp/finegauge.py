#!/usr/bin/env python3
"""314-fine-gauge: a pressure gauge with labelled ticks every 10 units and no minor ticks; the needle sits at an
arbitrary value. Report it within 1 unit (a tenth of the tick spacing). complete = within tolerance."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Gauge"; W, H = 640, 520; QUESTION = "What value does the needle indicate (within 1 unit)?"
S = {"v": 0.0}


def reset(): S["v"] = round(random.uniform(3, 97), 1)


def ang(v): return math.radians(225 - v * 2.7)


def draw():
    img = Image.new("RGB", (W, H), (250, 250, 250)); d = ImageDraw.Draw(img); cx, cy, r = 320, 280, 200
    d.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], fill=(255, 255, 255), outline=(50, 50, 50), width=5)
    for k in range(0, 101, 10):
        a = ang(k); d.line([(cx + (r - 25) * math.cos(a), cy - (r - 25) * math.sin(a)), (cx + r * math.cos(a), cy - r * math.sin(a))], fill=(30, 30, 30), width=3)
        d.text((cx + (r - 48) * math.cos(a) - 8, cy - (r - 48) * math.sin(a) - 7), str(k), fill=(30, 30, 30), font=base.font(15))
    a = ang(S["v"]); d.line([(cx - 20 * math.cos(a), cy + 20 * math.sin(a)), (cx + (r - 8) * math.cos(a), cy - (r - 8) * math.sin(a))], fill=(200, 30, 30), width=3); d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(40, 40, 40))
    return img


def check(s):
    try: return abs(float(perception.num(s)) - S["v"]) <= 1.0
    except Exception: return False


def answer_state(): return {"value": S["v"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8952)
