#!/usr/bin/env python3
"""366-stamp-collage: an image of ~55 overlapping postage stamps; each carries one motif (triangle, circle, star,
square). Count the stamps whose motif is a TRIANGLE, including partly covered ones. complete = exact."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Stamps"; W, H = 960, 640; QUESTION = "How many stamps carry a TRIANGLE motif, counting partly covered stamps (exact)?"
S = {"stamps": []}


def reset():
    st = []
    for _ in range(55):
        st.append((random.randint(30, W - 90), random.randint(30, H - 90), random.choice(["tri", "circle", "star", "square"]), random.uniform(-20, 20), (random.randint(120, 240), random.randint(120, 240), random.randint(120, 240))))
    S["stamps"] = st


def draw():
    img = Image.new("RGB", (W, H), (245, 240, 230))
    for x, y, motif, ang, col in S["stamps"]:
        tile = Image.new("RGBA", (80, 80), (0, 0, 0, 0)); d = ImageDraw.Draw(tile); d.rectangle([6, 6, 73, 73], fill=col + (255,), outline=(255, 255, 255, 255), width=3)
        cx, cy = 40, 40; m = (30, 30, 30, 255)
        if motif == "tri": d.polygon([(cx, cy - 14), (cx - 13, cy + 10), (cx + 13, cy + 10)], fill=m)
        elif motif == "circle": d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=m)
        elif motif == "square": d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], fill=m)
        else: d.polygon([(cx + (14 if k % 2 == 0 else 6) * math.cos(-math.pi / 2 + k * math.pi / 5), cy + (14 if k % 2 == 0 else 6) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)], fill=m)
        tile = tile.rotate(ang, resample=Image.BICUBIC, expand=True); img.paste(tile, (x, y), tile)
    return img


def visible_tris():
    # a stamp's motif is visible unless a later stamp covers its centre
    n = 0
    for i, (x, y, motif, ang, col) in enumerate(S["stamps"]):
        if motif != "tri": continue
        cx, cy = x + 40, y + 40; covered = any(abs(cx - (x2 + 40)) < 30 and abs(cy - (y2 + 40)) < 30 for x2, y2, *_ in S["stamps"][i + 1:])
        if not covered: n += 1
    return n


def check(s):
    try: return int(perception.num(s)) == visible_tris()
    except Exception: return False


def answer_state(): return {"triangles_visible": visible_tris(), "triangles_total": sum(1 for s in S["stamps"] if s[2] == "tri")}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8993)
