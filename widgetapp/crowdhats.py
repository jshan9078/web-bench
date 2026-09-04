#!/usr/bin/env python3
"""342-crowd-hats: a dense crowd of ~140 stick figures seen from above the shoulders; count the people wearing a
RED hat (other hats are blue, yellow, green, or none). complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Crowd"; W, H = 960, 640; QUESTION = "How many people in the crowd wear a RED hat (exact)?"
S = {"ppl": []}


def reset():
    ppl = []
    while len(ppl) < 140:
        x, y = random.randint(20, W - 20), random.randint(30, H - 20)
        if all((x - p[0]) ** 2 + (y - p[1]) ** 2 > 26 ** 2 for p in ppl): ppl.append((x, y, random.choice(["red", "blue", "yellow", "green", None, None, "red"]), random.choice([(240, 200, 170), (150, 100, 70), (90, 60, 40), (250, 220, 190)])))
    S["ppl"] = ppl


def draw():
    img = Image.new("RGB", (W, H), (200, 200, 205)); d = ImageDraw.Draw(img); cols = {"red": (220, 30, 30), "blue": (30, 60, 220), "yellow": (240, 200, 20), "green": (30, 160, 60)}
    for x, y, hat, skin in sorted(S["ppl"], key=lambda p: p[1]):
        d.ellipse([x - 12, y - 4, x + 12, y + 14], fill=(random.randint(30, 120),) * 3); d.ellipse([x - 8, y - 14, x + 8, y + 2], fill=skin)
        if hat: d.pieslice([x - 9, y - 15, x + 9, y + 1], 180, 360, fill=cols[hat])
    return img


def check(s):
    try: return int(perception.num(s)) == sum(1 for p in S["ppl"] if p[2] == "red")
    except Exception: return False


def answer_state(): return {"red_hats": sum(1 for p in S["ppl"] if p[2] == "red")}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8976)
