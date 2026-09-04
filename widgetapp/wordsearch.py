#!/usr/bin/env python3
"""293-word-search: a 12x12 letter grid image with one hidden word placed horizontally, vertically or diagonally
(possibly backwards). Click the word's FIRST letter, then Confirm. Visual search plus a precise click.
complete = confirmed click on the first letter's cell."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
N = 12; CELL = 44; OFF = 40; W = H = OFF * 2 + N * CELL
WORDS = ["HARBOR", "ANCHOR", "LANTERN", "COMPASS", "MARINA", "PELICAN"]
S = {"grid": [], "word": "", "start": (0, 0), "click": None, "confirmed": None}


def reset():
    while True:
        g = [[random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(N)] for _ in range(N)]; w = random.choice(WORDS)
        dr, dc = random.choice([(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1)]); r, c = random.randrange(N), random.randrange(N)
        if not (0 <= r + dr * (len(w) - 1) < N and 0 <= c + dc * (len(w) - 1) < N): continue
        for i, ch in enumerate(w): g[r + dr * i][c + dc * i] = ch
        S["grid"] = g; S["word"] = w; S["start"] = (r, c); S["click"] = None; S["confirmed"] = None; break


def render():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img); f = base.font(22)
    for r in range(N):
        for c in range(N):
            x, y = OFF + c * CELL, OFF + r * CELL; d.rectangle([x, y, x + CELL, y + CELL], outline=(225, 225, 225)); d.text((x + 13, y + 9), S["grid"][r][c], fill=(30, 30, 30), font=f)
    if S["click"]: cx, cy = S["click"]; d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=(220, 38, 38), width=3)
    return base.png(img)


def click(x, y): S["click"] = (int(x), int(y)); return {"click": S["click"]}


def post(path, data, ctype):
    if path == "/__confirm": S["confirmed"] = S["click"]; return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    c = S["confirmed"]; r, col = S["start"]; x, y = OFF + col * CELL, OFF + r * CELL
    ok = bool(c) and x <= c[0] <= x + CELL and y <= c[1] <= y + CELL
    return {"word": S["word"], "start_cell": S["start"], "confirmed": c, "complete": ok}


def page():
    return base.image_page("Word search", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;width:{W - 20}px"><p>The grid (image above; click with click --at X,Y) hides the word <b>{S['word']}</b> once, written horizontally, vertically or diagonally, forwards or backwards. Click the cell of the word's FIRST letter (a red circle marks your click; re-click to move it), then confirm.</p><button id=go>Confirm</button> <span id=msg></span>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}});document.getElementById('go').onclick=function(){{fetch('/__confirm',{{method:'POST'}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Confirmed '+JSON.stringify(j.confirmed)}})}}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8939)
