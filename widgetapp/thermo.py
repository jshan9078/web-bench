#!/usr/bin/env python3
"""156-thermometer-read: a lab photo of an analog alcohol thermometer (ticks every 1 degree, labels every 10,
range -10..50) next to a printed target label. Task: the temperature within 0.5 degrees (half a tick). complete =
within 0.5."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Incubator check"; W, H = 520, 720; QUESTION = "What temperature does the thermometer show, in degrees C (within 0.5)?"
S = {"t": 0.0, "set": 0}


def reset(): S["t"] = round(random.uniform(14, 42) + random.choice([0.2, 0.3, 0.4, 0.6, 0.7, 0.8]), 1); S["set"] = int(S["t"]) + random.choice([-3, -2, 2, 3])


def draw():
    img = Image.new("RGB", (W, H), (214, 218, 222)); d = ImageDraw.Draw(img); x0, ytop, ybot = 200, 60, 640
    d.rounded_rectangle([x0 - 34, ytop - 20, x0 + 70, ybot + 40], 18, fill=(245, 245, 240), outline=(150, 150, 150), width=2)
    d.rounded_rectangle([x0 - 8, ytop, x0 + 8, ybot], 6, fill=(230, 230, 230)); d.ellipse([x0 - 22, ybot - 10, x0 + 22, ybot + 34], fill=(200, 40, 40))
    def y_of(t): return ybot - (t + 10) * (ybot - ytop) / 60
    d.rectangle([x0 - 5, y_of(S["t"]), x0 + 5, ybot], fill=(200, 40, 40))
    for t in range(-10, 51):
        y = y_of(t); big = t % 10 == 0; mid = t % 5 == 0; l = 26 if big else 16 if mid else 8
        d.line([x0 + 12, y, x0 + 12 + l, y], fill=(40, 40, 40), width=2 if big else 1)
        if big: d.text((x0 + 44, y - 8), str(t), fill=(40, 40, 40), font=base.font(14))
    d.text((x0 + 50, ytop - 12), "°C", fill=(40, 40, 40), font=base.font(13, False))
    d.rectangle([30, 300, 150, 380], fill=(255, 250, 200), outline=(180, 170, 120)); d.text((40, 310), "SET POINT", fill=(60, 60, 60), font=base.font(12)); d.text((40, 334), f"{S['set']}.0 °C", fill=(30, 30, 30), font=base.font(22))
    d.text((20, 20), "Incubator 3, daily check photo", fill=(50, 50, 60), font=base.font(15))
    return img


def check(s):
    try: return abs(perception.num(s.replace("°", "").replace("C", "").replace("c", "")) - S["t"]) <= 0.5
    except Exception: return False


def answer_state(): return {"temp": S["t"], "set_point_decoy": S["set"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8852)
