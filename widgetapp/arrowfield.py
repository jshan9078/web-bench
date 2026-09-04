#!/usr/bin/env python3
"""353-arrow-field: an image of ~120 arrows in eight directions; count the arrows pointing UP-LEFT (exact)."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Arrows"; W, H = 960, 640; QUESTION = "How many arrows point UP-LEFT, i.e. toward the top-left corner (exact)?"
S = {"arrows": []}


def reset():
    arr = []
    while len(arr) < 120:
        x, y = random.randint(30, W - 30), random.randint(30, H - 30)
        if all((x - a[0]) ** 2 + (y - a[1]) ** 2 > 40 ** 2 for a in arr): arr.append((x, y, random.randrange(8)))
    S["arrows"] = arr


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    for x, y, k in S["arrows"]:
        a = math.radians(k * 45); dx, dy = math.cos(a), -math.sin(a); tip = (x + 14 * dx, y + 14 * dy); tail = (x - 14 * dx, y - 14 * dy)
        d.line([tail, tip], fill=(20, 20, 20), width=3); ang = math.atan2(dy, dx)
        d.polygon([tip, (tip[0] - 9 * math.cos(ang - 0.5), tip[1] - 9 * math.sin(ang - 0.5)), (tip[0] - 9 * math.cos(ang + 0.5), tip[1] - 9 * math.sin(ang + 0.5))], fill=(20, 20, 20))
    return img


def check(s):
    try: return int(perception.num(s)) == sum(1 for a in S["arrows"] if a[2] == 3)
    except Exception: return False


def answer_state(): return {"up_left": sum(1 for a in S["arrows"] if a[2] == 3)}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8985)
