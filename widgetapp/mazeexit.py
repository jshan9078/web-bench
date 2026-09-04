#!/usr/bin/env python3
"""273-maze-exit: a maze image with a start marker and three openings on the border; only one opening is
reachable from the start. Click that opening, then Confirm. Visual path finding plus a precise click.
complete = confirmed click within the reachable opening's cell."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
N = 15; CELL = 34; OFF = 30; W = H = OFF * 2 + N * CELL
S = {"walls": None, "start": (0, 0), "exits": [], "good": None, "click": None, "confirmed": None}


def gen():
    # walls[r][c] = set of open directions; carve a perfect maze with DFS
    op = [[set() for _ in range(N)] for _ in range(N)]; seen = [[False] * N for _ in range(N)]; st = [(0, 0)]; seen[0][0] = True
    while st:
        r, c = st[-1]; nb = [(dr, dc) for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)) if 0 <= r + dr < N and 0 <= c + dc < N and not seen[r + dr][c + dc]]
        if not nb: st.pop(); continue
        dr, dc = random.choice(nb); op[r][c].add((dr, dc)); op[r + dr][c + dc].add((-dr, -dc)); seen[r + dr][c + dc] = True; st.append((r + dr, c + dc))
    return op


def reset():
    op = gen(); S["walls"] = op; S["start"] = (N // 2, N // 2)
    # cut the maze into two regions by re-adding a wall on the path... simpler: pick three border cells; make two of them unreachable by sealing them off
    border = [(r, c) for r in range(N) for c in range(N) if r in (0, N - 1) or c in (0, N - 1)]
    ex = random.sample(border, 3); S["exits"] = ex; S["good"] = ex[0]
    for r, c in ex[1:]:   # seal the decoy exits: remove all openings of that cell so it is isolated except the outside opening
        for dr, dc in list(op[r][c]): op[r][c].discard((dr, dc)); op[r + dr][c + dc].discard((-dr, -dc))
    S["click"] = None; S["confirmed"] = None


def cellxy(r, c): return OFF + c * CELL, OFF + r * CELL


def render():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img); op = S["walls"]
    for r in range(N):
        for c in range(N):
            x, y = cellxy(r, c)
            if (0, -1) not in op[r][c]: d.line([x, y, x, y + CELL], fill=(20, 20, 20), width=3)
            if (-1, 0) not in op[r][c]: d.line([x, y, x + CELL, y], fill=(20, 20, 20), width=3)
            if (0, 1) not in op[r][c]: d.line([x + CELL, y, x + CELL, y + CELL], fill=(20, 20, 20), width=3)
            if (1, 0) not in op[r][c]: d.line([x, y + CELL, x + CELL, y + CELL], fill=(20, 20, 20), width=3)
    for r, c in S["exits"]:   # draw the border opening
        x, y = cellxy(r, c); side = (0, -1) if c == 0 else (0, 1) if c == N - 1 else (-1, 0) if r == 0 else (1, 0)
        if side == (0, -1): d.line([x, y + 4, x, y + CELL - 4], fill=(255, 255, 255), width=5); d.text((x - 26, y + 8), "E", fill=(37, 99, 235), font=base.font(16))
        if side == (0, 1): d.line([x + CELL, y + 4, x + CELL, y + CELL - 4], fill=(255, 255, 255), width=5); d.text((x + CELL + 8, y + 8), "E", fill=(37, 99, 235), font=base.font(16))
        if side == (-1, 0): d.line([x + 4, y, x + CELL - 4, y], fill=(255, 255, 255), width=5); d.text((x + 10, y - 26), "E", fill=(37, 99, 235), font=base.font(16))
        if side == (1, 0): d.line([x + 4, y + CELL, x + CELL - 4, y + CELL], fill=(255, 255, 255), width=5); d.text((x + 10, y + CELL + 6), "E", fill=(37, 99, 235), font=base.font(16))
    sx, sy = cellxy(*S["start"]); d.ellipse([sx + 8, sy + 8, sx + CELL - 8, sy + CELL - 8], fill=(220, 38, 38))
    if S["click"]: cx, cy = S["click"]; d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=(37, 99, 235), width=3)
    return base.png(img)


def click(x, y): S["click"] = (int(x), int(y)); return {"click": S["click"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = S["click"]; return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    c = S["confirmed"]; ok = False
    if c:
        r, col = S["good"]; x, y = cellxy(r, col); ok = x - 6 <= c[0] <= x + CELL + 6 and y - 6 <= c[1] <= y + CELL + 6
    return {"good_exit_cell": S["good"], "exits": S["exits"], "confirmed": c, "complete": ok}


def page():
    return base.image_page("Maze", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:{W - 20}px"><p>The red dot is the start. Three openings on the border are marked E, but only one can be reached from the start without crossing walls. Click inside the cell of that reachable opening, then confirm.</p><button id=go>Confirm</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+JSON.stringify(j.confirmed)}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8927)
