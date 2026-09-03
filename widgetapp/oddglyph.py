#!/usr/bin/env python3
"""183-odd-glyph: a print-proof sheet: a 10x6 grid of the same icon, one of which is mirrored. Task: the grid
position (row letter, column number) of the odd one. Visual search among 60 near-identical items; the answer is
exact. complete = correct cell (last submission)."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Print proof sheet"; W, H = 960, 640; QUESTION = "One icon on the sheet is printed mirrored (flipped left-right). Which cell is it? Answer as row letter and column number, e.g. C7."
S = {"odd": (0, 0)}


def reset(): S["odd"] = (random.randrange(6), random.randrange(10))


def glyph(d, x, y, flip):
    s = -1 if flip else 1; c = (40, 60, 120)
    d.polygon([(x + s * -18, y + 16), (x + s * -18, y - 10), (x + s * 2, y - 10), (x + s * 2, y - 20), (x + s * 20, y - 2), (x + s * 2, y + 16)], fill=c)
    d.ellipse([x + s * -12 - 4, y + 2 - 4, x + s * -12 + 4, y + 2 + 4], fill=(255, 255, 255))


def draw():
    img = Image.new("RGB", (W, H), (250, 250, 250)); d = ImageDraw.Draw(img); d.text((20, 12), "Proof sheet 12, arrow icon, 60 up", fill=(60, 60, 60), font=base.font(14))
    for r in range(6):
        d.text((24, 78 + r * 90), "ABCDEF"[r], fill=(120, 120, 120), font=base.font(13))
        for c in range(10):
            x, y = 90 + c * 88, 90 + r * 90
            if r == 0: d.text((x - 4, 44), str(c + 1), fill=(120, 120, 120), font=base.font(13))
            glyph(d, x, y, (r, c) == S["odd"])
    return img


def check(s):
    s = s.strip().upper().replace(" ", "")
    try: return s[0] == "ABCDEF"[S["odd"][0]] and int(s[1:]) == S["odd"][1] + 1
    except Exception: return False


def answer_state(): return {"odd": "ABCDEF"[S["odd"][0]] + str(S["odd"][1] + 1)}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8866)
