#!/usr/bin/env python3
"""285-occluded-circles: 14-22 filled circles of a few colours, many partly hidden behind others. Count the circles
of one named colour exactly, counting partly hidden ones. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Overlapping discs"; W, H = 900, 560; QUESTION = ""
COLS = {"red": (220, 38, 38), "blue": (37, 99, 235), "green": (22, 163, 74), "amber": (217, 119, 6)}
S = {"discs": [], "target": "", "n": 0}


def reset():
    global QUESTION
    discs = [(random.randint(60, 840), random.randint(60, 500), random.randint(28, 60), random.choice(list(COLS))) for _ in range(random.randint(16, 24))]
    S["discs"] = discs; S["target"] = random.choice(list(COLS)); S["n"] = sum(1 for d in discs if d[3] == S["target"])
    QUESTION = f"How many {S['target']} discs are there, counting ones that are partly hidden behind others (exact)?"; sys.modules[__name__].QUESTION = QUESTION


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    for x, y, r, c in S["discs"]: d.ellipse([x - r, y - r, x + r, y + r], fill=COLS[c], outline=(255, 255, 255), width=2)
    return img


def check(s):
    try: return int(perception.num(s)) == S["n"]
    except Exception: return False


def answer_state(): return {"target": S["target"], "answer": S["n"], "total": len(S["discs"])}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8934)
