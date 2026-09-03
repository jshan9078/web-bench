#!/usr/bin/env python3
"""61-grid-toggle: an 8x8 grid rendered as an image. Cells contain a FILLED circle, a hollow RING, a
SQUARE, or nothing. Clicking a cell toggles it (a click on an already-selected cell deselects it; the
selection is shown only via the server-rendered image, which is re-fetched after each click).
complete = the selected set equals exactly the set of filled-circle cells."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base

G, CELL, M = 8, 58, 30
W = H = G * CELL + 2 * M + 30
S = {"cells": {}, "on": set(), "clicks": []}


def reset():
    keys = [(r, c) for r in range(G) for c in range(G)]; random.shuffle(keys)
    S["cells"] = {}
    for k in keys[:10]: S["cells"][k] = "filled"
    for k in keys[10:19]: S["cells"][k] = "ring"
    for k in keys[19:26]: S["cells"][k] = "square"
    S["on"] = set(); S["clicks"] = []


def _rc(x, y):
    c = int((x - M) // CELL); r = int((y - M - 30) // CELL)
    return (r, c) if 0 <= r < G and 0 <= c < G else None


def render():
    img = Image.new("RGB", (W, H), (255, 255, 255)); dr = ImageDraw.Draw(img)
    dr.text((M, 8), "Select every FILLED circle (not rings, not squares). A click toggles a cell.", fill=(90, 96, 105), font=base.font(14))
    col = (52, 73, 94)
    for r in range(G):
        for c in range(G):
            x0, y0 = M + c * CELL, M + 30 + r * CELL
            sel = (r, c) in S["on"]
            dr.rectangle([x0, y0, x0 + CELL, y0 + CELL], fill=(255, 243, 205) if sel else (255, 255, 255), outline=(200, 200, 200))
            if sel:
                dr.rectangle([x0 + 2, y0 + 2, x0 + CELL - 2, y0 + CELL - 2], outline=(230, 160, 0), width=2)
            kind = S["cells"].get((r, c)); cx, cy, rr = x0 + CELL / 2, y0 + CELL / 2, 11
            if kind == "filled":
                dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
            elif kind == "ring":
                dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=col, width=3)
            elif kind == "square":
                dr.rectangle([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    return base.png(img)


def page():
    # after each click the page re-fetches the scene so the selection highlight is visible
    return base.image_page("Grid Toggle", W, H, extra_html="") .replace(
        "body:JSON.stringify({x:Math.round(e.clientX-r.left),y:Math.round(e.clientY-r.top)})});",
        "body:JSON.stringify({x:Math.round(e.clientX-r.left),y:Math.round(e.clientY-r.top)})}).then(function(){var i=document.getElementById('s');i.src='/__scene.png?'+Date.now()});")


def click(x, y):
    k = _rc(x, y)
    if k is not None:
        if k in S["on"]: S["on"].discard(k)
        else: S["on"].add(k)
    S["clicks"].append({"x": x, "y": y, "cell": list(k) if k else None})
    return {"cell": list(k) if k else None, "selected": (k in S["on"]) if k else None}


def state():
    filled = {k for k, v in S["cells"].items() if v == "filled"}
    return {"n_filled": len(filled), "selected": sorted(list(k) for k in S["on"]), "clicks": len(S["clicks"]),
            "wrong_selected": sorted(list(k) for k in S["on"] - filled), "missing": sorted(list(k) for k in filled - S["on"]),
            "complete": S["on"] == filled}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8795)
