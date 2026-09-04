#!/usr/bin/env python3
"""307-angle-read: an image with two rays from a common vertex on a plain background (no protractor). Report the
angle between them in degrees within 2 degrees. complete = within tolerance."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Angle"; W, H = 700, 500; QUESTION = "What is the angle between the two rays, in degrees (within 2)?"
S = {"a1": 0, "ang": 0}


def reset(): S["a1"] = random.uniform(0, 360); S["ang"] = random.randint(17, 160)


def draw():
    img = Image.new("RGB", (W, H), (252, 252, 250)); d = ImageDraw.Draw(img); cx, cy = 350, 260
    for a in (S["a1"], S["a1"] + S["ang"]):
        r = math.radians(a); d.line([(cx, cy), (cx + 200 * math.cos(r), cy - 200 * math.sin(r))], fill=(20, 20, 20), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(20, 20, 20)); return img


def check(s):
    try: return abs(float(perception.num(s)) - S["ang"]) <= 2
    except Exception: return False


def answer_state(): return {"angle": S["ang"], "base": round(S["a1"], 1)}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8947)
