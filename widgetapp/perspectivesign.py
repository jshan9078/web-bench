#!/usr/bin/env python3
"""297-perspective-sign: a street photo with a road sign seen at a steep angle (perspective-warped text) listing
three destinations with distances. Report the distance to the named destination. complete = exact number."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Road sign photo"; W, H = 960, 560; QUESTION = ""
NAMES = ["Harbor Point", "Northport", "Millbrook", "Quay End", "Elmridge", "Baywater"]
S = {"rows": [], "target": 0}


def reset():
    global QUESTION
    names = random.sample(NAMES, 3); S["rows"] = [(n, random.randint(3, 48)) for n in names]; S["target"] = random.randrange(3)
    QUESTION = f"According to the sign, how many km is it to {S['rows'][S['target']][0]}?"; sys.modules[__name__].QUESTION = QUESTION


def draw():
    img = Image.new("RGB", (W, H), (150, 185, 220)); d = ImageDraw.Draw(img); d.rectangle([0, 360, W, H], fill=(80, 84, 90)); d.polygon([(380, 560), (580, 560), (520, 360), (440, 360)], fill=(110, 112, 118))
    sign = Image.new("RGB", (520, 260), (20, 90, 60)); sd = ImageDraw.Draw(sign)
    for i, (n, km) in enumerate(S["rows"]): sd.text((24, 24 + i * 76), n, fill=(255, 255, 255), font=base.font(44)); sd.text((400, 24 + i * 76), f"{km}", fill=(255, 255, 255), font=base.font(44))
    # perspective: squash the far side
    w, h = sign.size; coeffs = find_coeffs([(0, 0), (w, 0), (w, h), (0, h)], [(0, 0), (w, 70), (w, h - 70), (0, h)])
    warped = sign.transform((w, h), Image.PERSPECTIVE, coeffs, Image.BICUBIC); small = warped.resize((int(w * 0.62), int(h * 0.62)), Image.BICUBIC)
    img.paste(small, (560, 150)); d.rectangle([560 + small.width // 2 - 6, 150 + small.height, 560 + small.width // 2 + 6, 420], fill=(90, 90, 95))
    return img


def find_coeffs(pa, pb):
    import numpy as np
    A = []
    for (x, y), (u, v) in zip(pa, pb): A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(A, dtype=float); B = np.array([c for p in pb for c in p], dtype=float); res = np.linalg.solve(A, B); return list(res)


def check(s):
    try: return int(perception.num(s.lower().replace("km", ""))) == S["rows"][S["target"]][1]
    except Exception: return False


def answer_state(): return {"rows": S["rows"], "target": S["rows"][S["target"]][0], "answer": S["rows"][S["target"]][1]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8941)
