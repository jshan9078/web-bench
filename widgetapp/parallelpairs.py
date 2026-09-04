#!/usr/bin/env python3
"""317-parallel-pairs: six pairs of lines labelled A-F; five pairs are parallel, one pair diverges by 3 degrees.
Report the non-parallel pair. complete = exact letter."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Line pairs"; W, H = 960, 640; QUESTION = "Five of the six labelled pairs are parallel; which pair is NOT parallel? Answer with its letter."
S = {"angles": [], "odd": 0}


def reset(): S["angles"] = [random.uniform(0, 180) for _ in range(6)]; S["odd"] = random.randrange(6)


def draw():
    img = Image.new("RGB", (W, H), (252, 252, 250)); d = ImageDraw.Draw(img)
    for i, a in enumerate(S["angles"]):
        cx, cy = 160 + (i % 3) * 320, 170 + (i // 3) * 300; d.text((cx - 130, cy - 130), "ABCDEF"[i], fill=(60, 60, 60), font=base.font(18))
        for j, off in enumerate((-28, 28)):
            ang = a + (3 if (i == S["odd"] and j == 1) else 0); r = math.radians(ang); nx, ny = -math.sin(r) * off, math.cos(r) * off
            d.line([(cx + nx - 110 * math.cos(r), cy + ny - 110 * math.sin(r)), (cx + nx + 110 * math.cos(r), cy + ny + 110 * math.sin(r))], fill=(20, 20, 20), width=2)
    return img


def check(s): return s.strip().upper()[:1] == "ABCDEF"[S["odd"]]
def answer_state(): return {"odd": "ABCDEF"[S["odd"]]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8955)
