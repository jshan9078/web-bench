#!/usr/bin/env python3
"""343-dot-cluster: an irregular cluster of 55-85 same-colour dots, some nearly touching; count them exactly."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Dots"; W, H = 800, 600; QUESTION = "How many dots are in the image (exact)?"
S = {"dots": []}


def reset():
    dots = []; n = random.randint(55, 85)
    while len(dots) < n:
        a = random.uniform(0, 6.28); r = random.gauss(0, 120); x, y = 400 + r * math.cos(a), 300 + r * math.sin(a) * 0.8
        if 20 < x < W - 20 and 20 < y < H - 20 and all((x - d[0]) ** 2 + (y - d[1]) ** 2 > 15 ** 2 for d in dots): dots.append((x, y))
    S["dots"] = dots


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    for x, y in S["dots"]: d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(30, 30, 200))
    return img


def check(s):
    try: return int(perception.num(s)) == len(S["dots"])
    except Exception: return False


def answer_state(): return {"dots": len(S["dots"])}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8977)
