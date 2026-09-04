#!/usr/bin/env python3
"""281-count-intersections: eight random straight segments; count the points where two segments cross. Exact.
complete = exact count."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Segment crossings"; W, H = 900, 560; QUESTION = "How many points are there where two line segments cross (exact count)?"
S = {"segs": [], "n": 0}


def cross(a, b, c, d):
    def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (o(a, b, c) * o(a, b, d) < 0) and (o(c, d, a) * o(c, d, b) < 0)


def reset():
    while True:
        segs = [((random.randint(40, 860), random.randint(40, 520)), (random.randint(40, 860), random.randint(40, 520))) for _ in range(8)]
        if any(((s[0][0] - s[1][0]) ** 2 + (s[0][1] - s[1][1]) ** 2) < 200 ** 2 for s in segs): continue
        n = sum(1 for i in range(8) for j in range(i + 1, 8) if cross(segs[i][0], segs[i][1], segs[j][0], segs[j][1]))
        if 6 <= n <= 14: break
    S["segs"] = segs; S["n"] = n


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    for i, s in enumerate(S["segs"]): d.line([s[0], s[1]], fill=[(220, 38, 38), (37, 99, 235), (22, 163, 74), (217, 119, 6), (124, 58, 237), (14, 116, 144), (190, 24, 93), (31, 41, 55)][i], width=3)
    return img


def check(s):
    try: return int(perception.num(s)) == S["n"]
    except Exception: return False


def answer_state(): return {"answer": S["n"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8926)
