#!/usr/bin/env python3
"""59-spot-difference: two 440x440 panels side by side; the RIGHT panel differs from the left in NDIFF places
(level 1: four; level 2: five, adding a reshaped shape at the same spot, with a miss budget of two) (a recolored shape, a removed shape, a moved shape, an added shape). The agent clicks each
difference on the RIGHT panel. complete = all four difference regions hit with at most three misses."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base

PW, GAP, H = 440, 20, 480
W = PW * 2 + GAP
PALETTE = [(219, 68, 55), (66, 133, 244), (15, 157, 88), (244, 180, 0), (171, 71, 188), (0, 150, 136), (255, 112, 67)]
import os
LEVEL = int(os.environ.get("WIDGET_LEVEL", "2"))
NDIFF = 4 if LEVEL == 1 else 5
MISS_BUDGET_L3 = 2
NSHAPES = 14
MISS_BUDGET = 3 if LEVEL == 1 else 2
S = {"shapes": [], "diffs": [], "clicks": []}


def _shape(existing):
    while True:
        x = random.randint(40, PW - 40); y = random.randint(60, H - 40); r = random.randint(16, 26)
        if all((x - e["x"]) ** 2 + (y - e["y"]) ** 2 > (r + e["r"] + 14) ** 2 for e in existing):
            return {"x": x, "y": y, "r": r, "kind": random.choice(["circle", "square", "triangle"]),
                    "color": random.choice(PALETTE)}


def reset():
    shapes = []
    for _ in range(NSHAPES):
        shapes.append(_shape(shapes))
    S["shapes"] = shapes; S["clicks"] = []
    idx = random.sample(range(len(shapes)), 4)
    diffs = []
    a = dict(shapes[idx[0]]); a["color"] = random.choice([c for c in PALETTE if c != a["color"]])
    diffs.append({"type": "recolor", "i": idx[0], "shape": a, "x": a["x"], "y": a["y"]})
    b = shapes[idx[1]]
    diffs.append({"type": "remove", "i": idx[1], "shape": None, "x": b["x"], "y": b["y"]})
    c = dict(shapes[idx[2]]); moved = _shape(shapes); c["x"], c["y"] = moved["x"], moved["y"]
    diffs.append({"type": "move", "i": idx[2], "shape": c, "x": c["x"], "y": c["y"], "from": (shapes[idx[2]]["x"], shapes[idx[2]]["y"])})
    extra = _shape(shapes + [c])
    diffs.append({"type": "add", "i": None, "shape": extra, "x": extra["x"], "y": extra["y"]})
    if LEVEL == 2:
        # a fifth, subtler difference: same position and color, different outline (shape kind)
        e = dict(shapes[idx[3]]); e["kind"] = random.choice([k for k in ("circle", "square", "triangle") if k != e["kind"]])
        diffs.append({"type": "reshape", "i": idx[3], "shape": e, "x": e["x"], "y": e["y"]})
    if LEVEL >= 3:
        # design-QA subtleties replace the loud recolor/move: a hue shift, a 6 px nudge, a 15% size change
        diffs.clear()
        a = dict(shapes[idx[0]]); r_, g_, b_ = a["color"]; a["color"] = (min(255, int(r_ * 0.75 + 40)), g_, min(255, int(b_ * 1.15 + 10)))
        diffs.append({"type": "tint", "i": idx[0], "shape": a, "x": a["x"], "y": a["y"]})
        b = shapes[idx[1]]
        diffs.append({"type": "remove", "i": idx[1], "shape": None, "x": b["x"], "y": b["y"]})
        c = dict(shapes[idx[2]]); c["x"] += 6; c["y"] -= 5
        diffs.append({"type": "nudge", "i": idx[2], "shape": c, "x": c["x"], "y": c["y"], "from": (shapes[idx[2]]["x"], shapes[idx[2]]["y"])})
        d = dict(shapes[idx[3]]); d["r"] = max(8, int(d["r"] * 0.85))
        diffs.append({"type": "shrink", "i": idx[3], "shape": d, "x": d["x"], "y": d["y"]})
        extra = _shape(shapes); extra["r"] = 9
        diffs.append({"type": "add", "i": None, "shape": extra, "x": extra["x"], "y": extra["y"]})
    S["diffs"] = diffs


def _draw(dr, s, ox):
    x, y, r = s["x"] + ox, s["y"], s["r"]
    if s["kind"] == "circle":
        dr.ellipse([x - r, y - r, x + r, y + r], fill=s["color"])
    elif s["kind"] == "square":
        dr.rectangle([x - r, y - r, x + r, y + r], fill=s["color"])
    else:
        dr.polygon([(x, y - r), (x - r, y + r), (x + r, y + r)], fill=s["color"])


def render():
    img = Image.new("RGB", (W, H), (247, 248, 250)); dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, PW, H], fill=(255, 255, 255)); dr.rectangle([PW + GAP, 0, W, H], fill=(255, 255, 255))
    dr.text((14, 10), "LEFT: original", fill=(90, 96, 105), font=base.font(16))
    dr.text((PW + GAP + 14, 10), "RIGHT: click the %d differences here" % NDIFF, fill=(90, 96, 105), font=base.font(16))
    for s in S["shapes"]:
        _draw(dr, s, 0)
    right = {d["i"]: d for d in S["diffs"] if d["i"] is not None}
    for i, s in enumerate(S["shapes"]):
        if i in right:
            d = right[i]
            if d["type"] == "remove":
                continue
            _draw(dr, d["shape"], PW + GAP)
        else:
            _draw(dr, s, PW + GAP)
    for d in S["diffs"]:
        if d["type"] == "add": _draw(dr, d["shape"], PW + GAP)
    return base.png(img)


def page():
    return base.image_page("Spot the Difference", W, H)


def click(x, y):
    found = None
    if x >= PW + GAP:
        rx = x - (PW + GAP)
        for k, d in enumerate(S["diffs"]):
            near = (rx - d["x"]) ** 2 + (y - d["y"]) ** 2 <= 34 ** 2
            if not near and d["type"] in ("move", "nudge"):   # the vacated spot is an equally valid "difference"
                fx, fy = d["from"]; near = (rx - fx) ** 2 + (y - fy) ** 2 <= 34 ** 2
            if near:
                found = k; break
    S["clicks"].append({"x": x, "y": y, "found": found})
    return {"found": found}


def state():
    found = sorted({c["found"] for c in S["clicks"] if c["found"] is not None})
    misses = sum(1 for c in S["clicks"] if c["found"] is None)
    return {"level": LEVEL, "n_diffs": NDIFF, "miss_budget": MISS_BUDGET, "clicks": S["clicks"], "found": found, "misses": misses,
            "diff_types": [d["type"] for d in S["diffs"]],
            "complete": len(found) == NDIFF and misses <= (MISS_BUDGET_L3 if LEVEL >= 3 else MISS_BUDGET)}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8793)
