#!/usr/bin/env python3
"""362-letter-grid: an image of a 16x12 grid of the letters R, P, B and K in mixed fonts and slight rotations; count
the letter R exactly."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Letters"; W, H = 960, 640; QUESTION = "How many times does the letter R appear (exact)?"
S = {"grid": []}


def reset(): S["grid"] = [[(random.choice("RPBKRB"), random.uniform(-25, 25), random.choice([22, 26, 30])) for _ in range(16)] for _ in range(12)]


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    for r, row in enumerate(S["grid"]):
        for c, (ch, ang, sz) in enumerate(row):
            tile = Image.new("RGBA", (60, 60), (0, 0, 0, 0)); ImageDraw.Draw(tile).text((18, 12), ch, fill=(20, 20, 20, 255), font=base.font(sz, bold=random.random() < 0.5)); tile = tile.rotate(ang, resample=Image.BICUBIC)
            img.paste(tile, (c * 60, r * 53), tile)
    return img


def check(s):
    try: return int(perception.num(s)) == sum(1 for row in S["grid"] for ch, _, _ in row if ch == "R")
    except Exception: return False


def answer_state(): return {"R": sum(1 for row in S["grid"] for ch, _, _ in row if ch == "R")}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8991)
