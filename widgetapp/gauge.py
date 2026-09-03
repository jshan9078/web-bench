#!/usr/bin/env python3
"""120-gauge-needle: a boiler-room panel photo with two analog pressure gauges (0-10 bar, major ticks every bar,
minor every 0.2). Task: gauge 2's reading to within 0.15 bar. Needle-angle interpolation between minor ticks is
the same skill the dial task showed every config failing. complete = within 0.15."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Boiler room panel"; W, H = 960, 480; QUESTION = "What pressure does GAUGE 2 show, in bar (within 0.15)?"
S = {"vals": []}


def reset(): S["vals"] = [round(random.uniform(1.3, 8.7), 1) for _ in range(2)]


def gauge(d, cx, cy, r, v, label):
    d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(60, 60, 64)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 245, 240))
    for k in range(51):
        a = math.radians(-225 + k * 270 / 50); big = k % 5 == 0; l = 18 if big else 8
        d.line([cx + (r - l) * math.cos(a), cy + (r - l) * math.sin(a), cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a)], fill=(30, 30, 30), width=3 if big else 1)
        if big: d.text((cx + (r - 38) * math.cos(a) - 7, cy + (r - 38) * math.sin(a) - 8), str(k // 5), fill=(30, 30, 30), font=base.font(15))
    a = math.radians(-225 + v * 27); d.line([cx - 18 * math.cos(a), cy - 18 * math.sin(a), cx + (r - 26) * math.cos(a), cy + (r - 26) * math.sin(a)], fill=(200, 30, 30), width=4)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(40, 40, 40)); d.text((cx - 12, cy + r * 0.45), "bar", fill=(80, 80, 80), font=base.font(12, False)); d.text((cx - 34, cy + r + 14), label, fill=(230, 230, 230), font=base.font(15))


def draw():
    img = Image.new("RGB", (W, H), (70, 74, 80)); d = ImageDraw.Draw(img); d.text((20, 12), "Boiler room, panel B", fill=(220, 220, 220), font=base.font(16))
    gauge(d, 260, 220, 150, S["vals"][0], "GAUGE 1"); gauge(d, 680, 220, 150, S["vals"][1], "GAUGE 2")
    return img


def check(s):
    try: return abs(perception.num(s) - S["vals"][1]) <= 0.15
    except Exception: return False


def answer_state(): return {"gauge2": S["vals"][1], "gauge1": S["vals"][0]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8838)
