#!/usr/bin/env python3
"""284-rotated-odd-one-out: an 8x8 grid of the same asymmetric glyph, all rotated by the same angle except one
rotated 20 degrees further. Report its cell. complete = exact cell (last submission)."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Glyph sheet"; W, H = 900, 640; QUESTION = "One glyph is rotated differently from all the others. Which cell is it? Answer as row letter and column number, e.g. C7."
S = {"odd": (0, 0), "base": 0}


def reset(): S["odd"] = (random.randrange(8), random.randrange(8)); S["base"] = random.randint(0, 359)


def glyph(d, x, y, ang):
    pts = [(-18, 14), (-18, -8), (2, -8), (2, -20), (20, -2), (2, 14), (2, 4), (-8, 4), (-8, 14)]
    a = math.radians(ang); rp = [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]; d.polygon(rp, fill=(40, 60, 120))


def draw():
    img = Image.new("RGB", (W, H), (250, 250, 250)); d = ImageDraw.Draw(img)
    for r in range(8):
        d.text((24, 78 + r * 70), "ABCDEFGH"[r], fill=(120, 120, 120), font=base.font(13))
        for c in range(8):
            x, y = 90 + c * 100, 90 + r * 70
            if r == 0: d.text((x - 4, 44), str(c + 1), fill=(120, 120, 120), font=base.font(13))
            glyph(d, x, y, S["base"] + (20 if (r, c) == S["odd"] else 0))
    return img


def check(s):
    s = s.strip().upper().replace(" ", "")
    try: return s[0] == "ABCDEFGH"[S["odd"][0]] and int(s[1:]) == S["odd"][1] + 1
    except Exception: return False


def answer_state(): return {"odd": "ABCDEFGH"[S["odd"][0]] + str(S["odd"][1] + 1)}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8933)
