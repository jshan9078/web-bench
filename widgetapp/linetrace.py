#!/usr/bin/env python3
"""272-line-trace: six tangled curves connect numbered starts on the left to lettered ends on the right. Task:
which letter does line 3 reach? Classic visual tracing. complete = exact letter (last submission)."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Cable tracing"; W, H = 960, 560; QUESTION = "Following the cables, which letter on the right does cable 3 connect to?"
S = {"perm": [], "ctrl": []}


def reset():
    S["perm"] = list(range(6)); random.shuffle(S["perm"]); S["ctrl"] = [[(random.randint(200, 760), random.randint(40, 520)) for _ in range(3)] for _ in range(6)]


def bez(p, n=200):
    out = []
    for i in range(n + 1):
        t = i / n; pts = p[:]
        while len(pts) > 1: pts = [(pts[k][0] * (1 - t) + pts[k + 1][0] * t, pts[k][1] * (1 - t) + pts[k + 1][1] * t) for k in range(len(pts) - 1)]
        out.append(pts[0])
    return out


def draw():
    img = Image.new("RGB", (W, H), (250, 250, 252)); d = ImageDraw.Draw(img)
    for i in range(6):
        y0 = 60 + i * 88; y1 = 60 + S["perm"][i] * 88; pts = bez([(80, y0)] + S["ctrl"][i] + [(880, y1)]); d.line(pts, fill=(30, 41, 59), width=3)
        d.text((36, y0 - 10), str(i + 1), fill=(220, 38, 38), font=base.font(20)); d.text((900, y1 - 10), "ABCDEF"[S["perm"][i]], fill=(37, 99, 235), font=base.font(20))
    return img


def check(s): return s.strip().upper()[:1] == "ABCDEF"[S["perm"][2]]
def answer_state(): return {"answer": "ABCDEF"[S["perm"][2]], "perm": S["perm"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8925)
