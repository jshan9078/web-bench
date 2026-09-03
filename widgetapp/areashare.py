#!/usr/bin/env python3
"""149-area-share: a satellite-style field tile with an irregular flooded (shaded) region. Task: the fraction of
the field that is flooded, as a percentage within 5 points. Area estimation of an irregular shape. complete =
within 5 points (computed from the rendered mask)."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Field survey tile"; W, H = 960, 560; QUESTION = "What percentage of the outlined field is flooded (the dark blue area), within 5 points?"
S = {"poly": [], "pct": 0}


def reset():
    cx, cy = random.randint(380, 480), random.randint(230, 300); pts = []
    n = random.randint(7, 11); rs = [random.uniform(70, 190) for _ in range(n)]
    for i in range(n):
        a = 2 * math.pi * i / n; pts.append((cx + rs[i] * math.cos(a), cy + rs[i] * math.sin(a)))
    S["poly"] = pts
    m = Image.new("1", (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=1); fl = sum(1 for v in m.getdata() if v)
    field = (760 - 60) * (480 - 60); S["pct"] = round(100 * fl / field)


def draw():
    img = Image.new("RGB", (W, H), (120, 132, 90)); d = ImageDraw.Draw(img)
    for i in range(0, W, 7): d.line([(i, 0), (i, H)], fill=(116 + (i * 7) % 9, 128, 86), width=3)
    d.rectangle([60, 60, 760, 480], fill=(150, 160, 90), outline=(255, 235, 80), width=4)
    for y in range(70, 480, 18): d.line([(66, y), (754, y)], fill=(138, 148, 82), width=2)
    d.polygon(S["poly"], fill=(38, 64, 120), outline=(28, 48, 95))
    d.text((60, 496), "Field 14B, outlined in yellow. Flooded area in dark blue. Tile 2026-08-29.", fill=(240, 240, 230), font=base.font(14))
    d.rectangle([790, 60, 940, 200], fill=(30, 41, 59)); d.text((802, 72), "Legend", fill=(226, 232, 240), font=base.font(14)); d.rectangle([802, 100, 826, 118], fill=(38, 64, 120)); d.text((834, 100), "Flooded", fill=(226, 232, 240), font=base.font(13, False)); d.rectangle([802, 130, 826, 148], fill=(150, 160, 90)); d.text((834, 130), "Dry crop", fill=(226, 232, 240), font=base.font(13, False))
    return img


def check(s):
    try: return abs(perception.num(s) - S["pct"]) <= 5
    except Exception: return False


def answer_state(): return {"pct": S["pct"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8848)
