#!/usr/bin/env python3
"""301-colour-grid-diff: two 7x7 colour grids side by side that are identical except one cell whose colour is
shifted moderately. Report the differing cell. complete = exact cell."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Grid comparison"; W, H = 960, 520; QUESTION = "The two grids are identical except one cell. Which cell differs? Answer as row letter and column number, e.g. D3."
S = {"grid": [], "odd": (0, 0), "shift": (0, 0, 0)}


def reset():
    S["grid"] = [[(random.randint(40, 215), random.randint(40, 215), random.randint(40, 215)) for _ in range(7)] for _ in range(7)]; S["odd"] = (random.randrange(7), random.randrange(7))
    S["shift"] = tuple(random.choice([-34, 34]) for _ in range(3))


def draw():
    img = Image.new("RGB", (W, H), (250, 250, 250)); d = ImageDraw.Draw(img)
    for gi, ox in enumerate((40, 520)):
        d.text((ox + 150, 14), "Left" if gi == 0 else "Right", fill=(80, 80, 80), font=base.font(14))
        for r in range(7):
            d.text((ox - 22, 50 + r * 60 + 20), "ABCDEFG"[r], fill=(120, 120, 120), font=base.font(13))
            for c in range(7):
                if r == 0: d.text((ox + c * 60 + 24, 34), str(c + 1), fill=(120, 120, 120), font=base.font(13))
                col = S["grid"][r][c]
                if gi == 1 and (r, c) == S["odd"]: col = tuple(max(0, min(255, v + s)) for v, s in zip(col, S["shift"]))
                d.rectangle([ox + c * 60, 50 + r * 60, ox + c * 60 + 56, 50 + r * 60 + 56], fill=col)
    return img


def check(s):
    s = s.strip().upper().replace(" ", "")
    try: return s[0] == "ABCDEFG"[S["odd"][0]] and int(s[1:]) == S["odd"][1] + 1
    except Exception: return False


def answer_state(): return {"odd": "ABCDEFG"[S["odd"][0]] + str(S["odd"][1] + 1), "shift": S["shift"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8942)
