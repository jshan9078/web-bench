#!/usr/bin/env python3
"""155-speedometer-needle: a dashboard photo with an analog speedometer (ticks every 10 km/h, labels every 20)
and a needle between ticks; a tachometer beside it is the decoy. Task: the speed within 2 km/h (a fifth of a
tick spacing, the ratio at which the dial task beat every config). complete = within 2."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Dashboard photo"; W, H = 960, 520; QUESTION = "What speed does the SPEEDOMETER needle show, in km/h (within 2)?"
S = {"v": 0, "rpm": 0}


def reset(): S["v"] = random.choice([v for v in range(23, 197) if v % 10 not in (0, 5)]); S["rpm"] = random.randint(12, 48)


def dial(d, cx, cy, r, vmax, step, labstep, v, unit, needle=(220, 38, 38)):
    d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(60, 60, 66)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(18, 18, 22))
    for k in range(0, vmax + 1, step):
        a = math.radians(-225 + 270 * k / vmax); big = k % labstep == 0; l = 20 if big else 10
        d.line([cx + (r - l) * math.cos(a), cy + (r - l) * math.sin(a), cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a)], fill=(230, 230, 230), width=3 if big else 1)
        if big: d.text((cx + (r - 40) * math.cos(a) - 10, cy + (r - 40) * math.sin(a) - 8), str(k), fill=(230, 230, 230), font=base.font(14))
    a = math.radians(-225 + 270 * v / vmax); d.line([cx - 16 * math.cos(a), cy - 16 * math.sin(a), cx + (r - 24) * math.cos(a), cy + (r - 24) * math.sin(a)], fill=needle, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(90, 90, 96)); d.text((cx - 16, cy + r * 0.5), unit, fill=(160, 160, 170), font=base.font(13, False))


def draw():
    img = Image.new("RGB", (W, H), (28, 28, 32)); d = ImageDraw.Draw(img)
    dial(d, 300, 260, 200, 240, 10, 20, S["v"], "km/h"); dial(d, 700, 280, 150, 80, 5, 10, S["rpm"], "rpm x100")
    d.text((20, 12), "Dashboard, instrument cluster", fill=(200, 200, 210), font=base.font(15))
    return img


def check(s):
    try: return abs(perception.num(s) - S["v"]) <= 2
    except Exception: return False


def answer_state(): return {"speed": S["v"], "rpm_x100": S["rpm"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8851)
