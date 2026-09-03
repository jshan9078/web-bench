#!/usr/bin/env python3
"""99-seat-map: a theatre seat map rendered as an IMAGE with a legend (available, taken, restricted view,
price by row band) and an aisle. Task: select the two cheapest adjacent available seats that are not
restricted view, then Confirm. In the cheapest band exactly one adjacent pair is clean; other pairs there
include a hatched restricted seat or straddle the aisle (not adjacent). complete = confirmed selection is
that pair."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
ROWS = "ABCDEFGHIJKL"; N = 16; AISLE_AFTER = 8
TIERS = [("A", "D", 120), ("E", "H", 85), ("I", "L", 60)]
X0, Y0, SW, SH, GAP, AISLE_W = 90, 110, 40, 34, 8, 40
S = {"seats": {}, "sel": [], "confirmed": None, "answer": None}


def tier(r): return next(p for a, b, p in TIERS if a <= r <= b)


def pos(r, n):
    x = X0 + (n - 1) * (SW + GAP) + (AISLE_W if n > AISLE_AFTER else 0); y = Y0 + ROWS.index(r) * (SH + GAP); return x, y


def reset():
    S["sel"] = []; S["confirmed"] = None
    while True:
        seats = {}
        for r in ROWS:
            for n in range(1, N + 1):
                seats[(r, n)] = random.choices(["avail", "taken", "restr"], [0.35, 0.55, 0.10])[0]
        # cheapest band: clean adjacent pairs -> exactly one; also plant traps
        cheap = [r for r in ROWS if tier(r) == 60]
        def clean_pairs():
            out = []
            for r in cheap:
                for n in range(1, N):
                    if n == AISLE_AFTER: continue
                    if seats[(r, n)] == "avail" and seats[(r, n + 1)] == "avail": out.append((r, n))
            return out
        cp = clean_pairs()
        if not cp: continue
        keep = random.choice(cp)
        for (r, n) in cp:
            if (r, n) != keep: seats[(r, n + (1 if random.random() < 0.5 else 0))] = "restr" if random.random() < 0.6 else "taken"
        if len(clean_pairs()) != 1: continue
        # traps: restricted-adjacent pairs and an aisle-straddling pair in the cheap band
        r = random.choice(cheap); seats[(r, AISLE_AFTER)] = "avail"; seats[(r, AISLE_AFTER + 1)] = "avail"
        for _ in range(3):
            r = random.choice(cheap); n = random.randint(1, N - 1)
            if n != AISLE_AFTER and (r, n) != keep and (r, n + 1) != keep and (r, n - 1) != keep: seats[(r, n)] = "avail"; seats[(r, n + 1)] = "restr"
        if len(clean_pairs()) != 1: continue
        S["seats"] = seats; S["answer"] = [f"{keep[0]}{keep[1]}", f"{keep[0]}{keep[1] + 1}"]; break


def render():
    W, H = 900, 700; img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    d.rectangle([X0, 40, X0 + N * (SW + GAP) + AISLE_W - GAP, 70], fill=(30, 41, 59)); d.text((W // 2 - 30, 47), "STAGE", fill=(255, 255, 255), font=base.font(16))
    for r in ROWS:
        for n in range(1, N + 1):
            x, y = pos(r, n); st = S["seats"][(r, n)]; sel = f"{r}{n}" in S["sel"]
            col = (34, 197, 94) if st in ("avail", "restr") else (203, 213, 225)
            if sel: col = (37, 99, 235)
            d.rounded_rectangle([x, y, x + SW, y + SH], 6, fill=col, outline=(148, 163, 184))
            if st == "restr" and not sel:
                for k in range(-SH, SW, 8): d.line([x + max(0, k), y + max(0, -k), x + min(SW, k + SH), y + min(SH, SH - k)], fill=(255, 255, 255), width=2)
            d.text((x + 6, y + 10), f"{r}{n}", fill=(15, 23, 42) if st != "taken" else (100, 116, 139), font=base.font(11, False))
    lx, ly = X0, Y0 + 12 * (SH + GAP) + 6; f = base.font(13, False)
    for i, (lab, col, hatch) in enumerate([("Available", (34, 197, 94), False), ("Taken", (203, 213, 225), False), ("Restricted view", (34, 197, 94), True), ("Selected", (37, 99, 235), False)]):
        x = lx + i * 170; d.rounded_rectangle([x, ly, x + 26, ly + 20], 4, fill=col, outline=(148, 163, 184))
        if hatch:
            for k in range(-20, 26, 7): d.line([x + max(0, k), ly + max(0, -k), x + min(26, k + 20), ly + min(20, 20 - k)], fill=(255, 255, 255), width=2)
        d.text((x + 32, ly + 3), lab, fill=(30, 41, 59), font=f)
    d.text((lx, ly + 32), "Prices by row:  A-D $120    E-H $85    I-L $60", fill=(30, 41, 59), font=base.font(14))
    return base.png(img)


def click(x, y):
    for (r, n), st in S["seats"].items():
        sx, sy = pos(r, n)
        if sx <= x <= sx + SW and sy <= y <= sy + SH:
            sid = f"{r}{n}"
            if st == "taken": return {"ignored": "taken"}
            if sid in S["sel"]: S["sel"].remove(sid)
            elif len(S["sel"]) < 2: S["sel"].append(sid)
            return {"sel": S["sel"]}
    return {"ignored": True}


def post(path, data, ctype):
    if path == "/__confirm":
        S["confirmed"] = list(S["sel"]); return (json.dumps({"confirmed": S["confirmed"]}), "application/json")
    return None


def state():
    return {"answer": S["answer"], "selection": S["sel"], "confirmed": S["confirmed"], "complete": S["confirmed"] is not None and sorted(S["confirmed"]) == sorted(S["answer"])}


def page():
    return base.image_page("Select seats, Grand Hall", 900, 700, extra_html="""
<div style="position:absolute;top:710px;left:90px;font:14px system-ui"><p>Click seats to select (up to two), then confirm. Selected: <span id=sel>none</span></p><button id=go>Confirm selection</button> <span id=msg></span></div>
<script>document.getElementById('s').addEventListener('click',function(){setTimeout(function(){document.getElementById('s').src='/__scene.png?'+Date.now()},150)});
document.getElementById('go').onclick=function(){fetch('/__confirm',{method:'POST'}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Confirmed: '+j.confirmed.join(', ')})}</script>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8819)
