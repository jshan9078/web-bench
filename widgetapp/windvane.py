#!/usr/bin/env python3
"""141-wind-vane: a weather-station panel with a compass rose (ticks every 10 degrees, labels every 30) and a
wind-direction arrow. Task: the wind direction in degrees within 3 (a third of a tick spacing). complete = within
3 degrees (circular)."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Weather station"; W, H = 960, 520; QUESTION = "What wind direction does the vane show, in degrees (0-359, within 3 degrees)?"
S = {"deg": 0, "speed": 0}


def reset(): S["deg"] = random.choice([d for d in range(360) if d % 10 not in (0, 5)]); S["speed"] = random.randint(4, 38)


def draw():
    img = Image.new("RGB", (W, H), (30, 41, 59)); d = ImageDraw.Draw(img); cx, cy, r = 300, 260, 190
    d.text((20, 14), "Northwind Marina, live weather", fill=(226, 232, 240), font=base.font(16))
    d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(15, 23, 42)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(241, 245, 249))
    for k in range(0, 360, 10):
        a = math.radians(k - 90); big = k % 30 == 0; l = 22 if big else 10
        d.line([cx + (r - l) * math.cos(a), cy + (r - l) * math.sin(a), cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a)], fill=(30, 30, 30), width=3 if big else 1)
        if big: d.text((cx + (r - 44) * math.cos(a) - 12, cy + (r - 44) * math.sin(a) - 8), str(k), fill=(51, 65, 85), font=base.font(13))
    for lab, k in [("N", 0), ("E", 90), ("S", 180), ("W", 270)]:
        a = math.radians(k - 90); d.text((cx + (r - 72) * math.cos(a) - 7, cy + (r - 72) * math.sin(a) - 10), lab, fill=(185, 28, 28) if lab == "N" else (30, 41, 59), font=base.font(20))
    a = math.radians(S["deg"] - 90); tip = (cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a)); tail = (cx - 60 * math.cos(a), cy - 60 * math.sin(a))
    d.line([tail, tip], fill=(220, 38, 38), width=6); d.polygon([tip, (tip[0] - 22 * math.cos(a - 0.4), tip[1] - 22 * math.sin(a - 0.4)), (tip[0] - 22 * math.cos(a + 0.4), tip[1] - 22 * math.sin(a + 0.4))], fill=(220, 38, 38))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(30, 30, 30))
    d.text((580, 120), "Wind speed", fill=(148, 163, 184), font=base.font(14)); d.text((580, 144), f"{S['speed']} kn", fill=(226, 232, 240), font=base.font(40))
    d.text((580, 230), "Gust", fill=(148, 163, 184), font=base.font(14)); d.text((580, 254), f"{S['speed'] + random.Random(S['deg']).randint(3, 9)} kn", fill=(226, 232, 240), font=base.font(40))
    d.text((580, 340), "Direction: see vane (arrow points where the wind blows TO)", fill=(148, 163, 184), font=base.font(13, False))
    return img


def check(s):
    try:
        v = perception.num(s) % 360; diff = min(abs(v - S["deg"]), 360 - abs(v - S["deg"])); return diff <= 3
    except Exception: return False


def answer_state(): return {"deg": S["deg"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8847)
