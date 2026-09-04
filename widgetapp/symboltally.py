#!/usr/bin/env python3
"""303-symbol-tally: an image of ~180 mixed symbols (stars, circles, squares, triangles, diamonds) in random
colours and rotations. Count exactly how many STARS there are. complete = exact."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Symbol sheet"; W, H = 960, 640; QUESTION = "How many STARS are on the sheet (exact count)?"
S = {"items": [], "stars": 0}


def reset():
    items = []
    while len(items) < 180:
        x, y = random.randint(24, W - 24), random.randint(24, H - 24)
        if all((x - i[0]) ** 2 + (y - i[1]) ** 2 > 30 ** 2 for i in items): items.append((x, y, random.choice(["star", "circle", "square", "tri", "diamond"]), random.randint(0, 359), (random.randint(20, 200), random.randint(20, 200), random.randint(20, 200))))
    S["items"] = items; S["stars"] = sum(1 for i in items if i[2] == "star")


def poly(d, x, y, kind, ang, col):
    a0 = math.radians(ang); r = 11
    if kind == "star": pts = [(x + (r if k % 2 == 0 else r * 0.45) * math.cos(a0 + k * math.pi / 5), y + (r if k % 2 == 0 else r * 0.45) * math.sin(a0 + k * math.pi / 5)) for k in range(10)]
    elif kind == "circle": d.ellipse([x - r, y - r, x + r, y + r], fill=col); return
    elif kind == "square": pts = [(x + r * math.cos(a0 + k * math.pi / 2 + math.pi / 4), y + r * math.sin(a0 + k * math.pi / 2 + math.pi / 4)) for k in range(4)]
    elif kind == "tri": pts = [(x + r * math.cos(a0 + k * 2 * math.pi / 3), y + r * math.sin(a0 + k * 2 * math.pi / 3)) for k in range(3)]
    else: pts = [(x + r * math.cos(a0 + k * math.pi / 2), y + r * math.sin(a0 + k * math.pi / 2)) for k in range(4)]
    d.polygon(pts, fill=col)


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    for x, y, k, a, c in S["items"]: poly(d, x, y, k, a, c)
    return img


def check(s):
    try: return int(perception.num(s)) == S["stars"]
    except Exception: return False


def answer_state(): return {"stars": S["stars"], "total": len(S["items"])}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8943)
