#!/usr/bin/env python3
"""345-rectangle-pile: 18-26 outlined rectangles of random size drawn on top of each other; count them exactly."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Rectangles"; W, H = 900, 600; QUESTION = "How many rectangles are in the image (exact)?"
S = {"rects": []}


def reset(): S["rects"] = [(x := random.randint(30, 700), y := random.randint(30, 450), x + random.randint(60, 180), y + random.randint(40, 130)) for _ in range(random.randint(18, 26))]


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    for r in S["rects"]: d.rectangle(r, outline=(20, 20, 20), width=2)
    return img


def check(s):
    try: return int(perception.num(s)) == len(S["rects"])
    except Exception: return False


def answer_state(): return {"rects": len(S["rects"])}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8979)
