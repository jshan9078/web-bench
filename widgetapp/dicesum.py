#!/usr/bin/env python3
"""356-dice-sum: an image of 36 dice showing random faces at random rotations; report the total of all pips."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Dice"; W, H = 960, 640; QUESTION = "What is the total number of pips showing on all the dice (exact)?"
S = {"dice": []}
PIPS = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)], 5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}


def reset():
    dice = []
    while len(dice) < 36:
        x, y = random.randint(40, W - 40), random.randint(40, H - 40)
        if all((x - d[0]) ** 2 + (y - d[1]) ** 2 > 62 ** 2 for d in dice): dice.append((x, y, random.randint(1, 6), random.uniform(0, 90), random.choice([(255, 255, 255), (220, 30, 30), (30, 60, 200)])))
    S["dice"] = dice


def draw():
    img = Image.new("RGB", (W, H), (34, 100, 60)); d = ImageDraw.Draw(img)
    for x, y, n, ang, col in S["dice"]:
        a = math.radians(ang); s = 22; pts = [(x + s * math.cos(a + k * math.pi / 2 + math.pi / 4) * 1.414, y + s * math.sin(a + k * math.pi / 2 + math.pi / 4) * 1.414) for k in range(4)]
        d.polygon(pts, fill=col, outline=(20, 20, 20)); pc = (20, 20, 20) if col == (255, 255, 255) else (255, 255, 255)
        for px, py in PIPS[n]:
            rx, ry = px * 12, py * 12; qx = x + rx * math.cos(a) - ry * math.sin(a); qy = y + rx * math.sin(a) + ry * math.cos(a); d.ellipse([qx - 3.5, qy - 3.5, qx + 3.5, qy + 3.5], fill=pc)
    return img


def check(s):
    try: return int(perception.num(s)) == sum(dd[2] for dd in S["dice"])
    except Exception: return False


def answer_state(): return {"total": sum(dd[2] for dd in S["dice"]), "faces": [dd[2] for dd in S["dice"]]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8987)
