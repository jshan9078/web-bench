#!/usr/bin/env python3
"""341-coin-pile: an image of 30-45 coins of two sizes scattered with partial overlaps; count the coins exactly."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Coins"; W, H = 900, 600; QUESTION = "How many coins are in the image (exact)?"
S = {"coins": []}


def reset():
    coins = []
    while len(coins) < random.randint(30, 45):
        r = random.choice([22, 30]); x, y = random.randint(40, W - 40), random.randint(40, H - 40)
        if all(((x - c[0]) ** 2 + (y - c[1]) ** 2) ** 0.5 > (r + c[2]) * 0.55 for c in coins): coins.append((x, y, r, random.choice([(212, 175, 55), (192, 192, 192), (184, 115, 51)])))
    S["coins"] = coins


def draw():
    img = Image.new("RGB", (W, H), (60, 80, 60)); d = ImageDraw.Draw(img)
    for x, y, r, col in S["coins"]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=tuple(max(0, c - 70) for c in col), width=2); d.ellipse([x - r + 6, y - r + 6, x + r - 6, y + r - 6], outline=tuple(max(0, c - 40) for c in col), width=1)
    return img


def check(s):
    try: return int(perception.num(s)) == len(S["coins"])
    except Exception: return False


def answer_state(): return {"coins": len(S["coins"])}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8975)
