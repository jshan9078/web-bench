#!/usr/bin/env python3
"""340-tangled-lines: eight coloured-free (all black) curved lines start at labelled points A-H on the left and end
at numbered points 1-8 on the right, crossing each other many times. Which line starts at the named letter and
where does it end? complete = exact number."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Tangled lines"; W, H = 960, 600; QUESTION = ""
S = {"perm": [], "target": 0, "ctrl": []}


def reset():
    global QUESTION
    S["perm"] = random.sample(range(8), 8); S["target"] = random.randrange(8); S["ctrl"] = [[(random.randint(200, 760), random.randint(40, 560)) for _ in range(3)] for _ in range(8)]
    QUESTION = f"The line that starts at letter {'ABCDEFGH'[S['target']]} ends at which number?"; sys.modules[__name__].QUESTION = QUESTION


def bez(pts, n=120):
    out = []
    for i in range(n + 1):
        t = i / n; p = pts[:]
        while len(p) > 1: p = [(p[j][0] * (1 - t) + p[j + 1][0] * t, p[j][1] * (1 - t) + p[j + 1][1] * t) for j in range(len(p) - 1)]
        out.append(p[0])
    return out


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    for i in range(8):
        y0 = 60 + i * 68; y1 = 60 + S["perm"][i] * 68; pts = [(60, y0)] + S["ctrl"][i] + [(900, y1)]
        d.line(bez(pts), fill=(20, 20, 20), width=2)
        d.text((22, y0 - 9), "ABCDEFGH"[i], fill=(20, 20, 20), font=base.font(18)); d.text((915, y1 - 9), str(S["perm"][i] + 1), fill=(20, 20, 20), font=base.font(18))
    return img


def check(s):
    try: return int(perception.num(s)) == S["perm"][S["target"]] + 1
    except Exception: return False


def answer_state(): return {"target": "ABCDEFGH"[S["target"]], "answer": S["perm"][S["target"]] + 1}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8974)
