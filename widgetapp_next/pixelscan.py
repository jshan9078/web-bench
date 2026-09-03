#!/usr/bin/env python3
"""58-pixel-scan: a TALL scene (900x1500, taller than any viewport) with ten small numbered circles and
six numbered square decoys. The agent must scroll, screenshot, translate viewport pixels to clicks, and
click the circles 1..10 in ascending order without ever hitting a square.
complete = circles hit in click order are exactly 1..10 and no decoy was hit."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base

import os
LEVEL = int(os.environ.get("WIDGET_LEVEL", "2"))
# level 1 (pilot round 1): 10 circles r=20, 6 decoys with random numbers, 900x1500
# level 2: same 10 circles and scene, r=16, 8 decoy squares that all reuse a real circle's number and sit near it
W, H, R, N, ND = (900, 1500, 20, 10, 6) if LEVEL == 1 else (900, 1500, 16, 10, 8)
COLORS = [(219, 68, 55), (66, 133, 244), (15, 157, 88), (244, 180, 0), (171, 71, 188), (0, 150, 136)]
S = {"targets": [], "decoys": [], "clicks": []}


def _place(k, existing):
    pts = []
    while len(pts) < k:
        x = random.randint(R + 30, W - R - 30); y = random.randint(70, H - R - 30)
        if all((x - px) ** 2 + (y - py) ** 2 > (3.2 * R) ** 2 for px, py in existing + pts):
            pts.append((x, y))
    return pts


def reset():
    c = _place(N, [])
    nums = list(range(1, N + 1)); random.shuffle(nums)
    S["targets"] = [{"n": nums[i], "x": c[i][0], "y": c[i][1]} for i in range(N)]
    if LEVEL == 1:
        d = _place(ND, c); dn = random.sample(range(1, 21), ND)
        S["decoys"] = [{"n": dn[i], "x": d[i][0], "y": d[i][1]} for i in range(ND)]
    else:
        # each decoy copies a real circle's number and is placed within ~120 px of that circle, so the
        # trap is discrimination (shape) at the moment of clicking, not more searching
        S["decoys"] = []
        twins = random.sample(S["targets"], ND)
        for t in twins:
            for _ in range(200):
                ang = random.uniform(0, 6.283); dist = random.uniform(3.0 * R, 7.5 * R)
                x = int(t["x"] + dist * __import__("math").cos(ang)); y = int(t["y"] + dist * __import__("math").sin(ang))
                if R + 30 <= x <= W - R - 30 and 70 <= y <= H - R - 30 and \
                   all((x - o["x"]) ** 2 + (y - o["y"]) ** 2 > (2.6 * R) ** 2 for o in S["targets"] + S["decoys"]):
                    S["decoys"].append({"n": t["n"], "x": x, "y": y}); break
    S["clicks"] = []


def render():
    img = Image.new("RGB", (W, H), (247, 248, 250)); dr = ImageDraw.Draw(img)
    dr.text((16, 12), "Click the numbered CIRCLES in ascending order (1..%d). Squares are decoys. The page scrolls." % N,
            fill=(90, 96, 105), font=base.font(17))
    f = base.font(20 if LEVEL == 1 else 16)
    for t in S["targets"]:
        c = COLORS[(t["n"] - 1) % len(COLORS)]
        dr.ellipse([t["x"] - R, t["y"] - R, t["x"] + R, t["y"] + R], fill=c)
        s = str(t["n"]); bb = dr.textbbox((0, 0), s, font=f)
        dr.text((t["x"] - (bb[2] - bb[0]) / 2, t["y"] - (bb[3] - bb[1]) / 2 - bb[1]), s, fill=(255, 255, 255), font=f)
    for t in S["decoys"]:
        c = COLORS[(t["n"] - 1) % len(COLORS)]
        dr.rectangle([t["x"] - R, t["y"] - R, t["x"] + R, t["y"] + R], fill=c)
        s = str(t["n"]); bb = dr.textbbox((0, 0), s, font=f)
        dr.text((t["x"] - (bb[2] - bb[0]) / 2, t["y"] - (bb[3] - bb[1]) / 2 - bb[1]), s, fill=(255, 255, 255), font=f)
    return base.png(img)


def page():
    return base.image_page("Pixel Scan", W, H)


def click(x, y):
    hit = next((t["n"] for t in S["targets"] if (x - t["x"]) ** 2 + (y - t["y"]) ** 2 <= R ** 2), None)
    decoy = next((t["n"] for t in S["decoys"] if abs(x - t["x"]) <= R and abs(y - t["y"]) <= R), None)
    S["clicks"].append({"x": x, "y": y, "hit": hit, "decoy": decoy})
    return {"hit": hit, "decoy": decoy}


def state():
    order = []
    for c in S["clicks"]:
        if c["hit"] is not None and c["hit"] not in order:
            order.append(c["hit"])
    decoy_hits = sum(1 for c in S["clicks"] if c["decoy"] is not None)
    return {"level": LEVEL, "n_targets": N, "clicks": S["clicks"], "hit_order": order, "decoy_hits": decoy_hits,
            "complete": order == list(range(1, N + 1)) and decoy_hits == 0}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8792)
