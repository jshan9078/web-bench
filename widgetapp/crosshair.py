#!/usr/bin/env python3
"""77-crosshair-align: precision under feedback. A target ring is drawn at a random spot in the image; a
crosshair starts elsewhere. Arrow keys move it 1 px (Shift+arrow: 10 px); Enter locks it. The crosshair
and ring exist only in the server-rendered image, so every adjustment needs a fresh screenshot.
Level 1: 3 px tolerance, two locks allowed. Level 2: 2 px tolerance and ONE lock only (verify before
committing). A dashed decoy ring is present at both levels.
complete = last lock within tolerance and no more locks than allowed."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 900, 600
LEVEL = int(os.environ.get("WIDGET_LEVEL", "2"))
S = {"target": (0, 0), "decoy": None, "cur": (0, 0), "locks": [], "moves": 0}


def reset():
    S["target"] = (random.randint(120, W - 120), random.randint(120, H - 120))
    S["cur"] = (random.randint(60, W - 60), random.randint(60, H - 60))
    S["decoy"] = None
    if LEVEL >= 2:
        while True:
            d = (random.randint(120, W - 120), random.randint(120, H - 120))
            if math.hypot(d[0] - S["target"][0], d[1] - S["target"][1]) > 200: S["decoy"] = d; break
    S["locks"] = []; S["moves"] = 0


def render():
    img = Image.new("RGB", (W, H), (250, 250, 252)); dr = ImageDraw.Draw(img)
    dr.text((14, 10), ("Move the crosshair onto the SOLID ring's centre with the arrow keys (Shift = 10 px), then press Enter." if LEVEL == 1 else "Move the crosshair onto the SOLID ring's centre (arrows; Shift = 10 px). ONE Enter only: verify first."), fill=(90, 96, 105), font=base.font(15))
    tx, ty = S["target"]; col = (30, 100, 200)
    dr.ellipse([tx - 14, ty - 14, tx + 14, ty + 14], outline=col, width=2); dr.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=col)
    if S["decoy"]:
        dx, dy = S["decoy"]
        for a in range(0, 360, 30):
            a0, a1 = math.radians(a), math.radians(a + 15)
            dr.arc([dx - 14, dy - 14, dx + 14, dy + 14], start=a, end=a + 15, fill=col, width=2)
    cx, cy = S["cur"]
    dr.line([cx - 18, cy, cx + 18, cy], fill=col, width=1); dr.line([cx, cy - 18, cx, cy + 18], fill=col, width=1)
    dr.text((14, H - 26), f"crosshair ({cx}, {cy})   moves {S['moves']}   locks {len(S['locks'])}", fill=(120, 120, 120), font=base.font(12))
    return base.png(img)


def page():
    return base.image_page("Crosshair", W, H, extra_html="""
<script>
document.addEventListener('keydown',function(e){var m={ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0]}[e.key];
 if(m){e.preventDefault();var k=e.shiftKey?10:1;fetch('/__move',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({dx:m[0]*k,dy:m[1]*k})}).then(function(){document.getElementById('s').src='/__scene.png?'+Date.now()})}
 else if(e.key==='Enter'){fetch('/__lock',{method:'POST'}).then(function(){document.getElementById('s').src='/__scene.png?'+Date.now()})}});
document.body.tabIndex=0;document.body.focus();
</script>""")


def click(x, y):
    return {"ignored": True}


def post(path, data, ctype):
    if path == "/__move":
        try: dx, dy = int(data.get("dx", 0)), int(data.get("dy", 0))
        except Exception: return ('{"ok":false}', "application/json")
        cx, cy = S["cur"]; S["cur"] = (min(W - 1, max(0, cx + dx)), min(H - 1, max(0, cy + dy))); S["moves"] += 1
        return ('{"ok":true}', "application/json")
    if path == "/__lock":
        S["locks"].append(S["cur"]); return ('{"ok":true}', "application/json")
    return None


def state():
    tx, ty = S["target"]
    dists = [math.hypot(x - tx, y - ty) for x, y in S["locks"]]
    return {"level": LEVEL, "target": S["target"], "cur": S["cur"], "locks": S["locks"], "lock_dists": [round(d, 1) for d in dists],
            "tolerance": (3 if LEVEL == 1 else 2), "max_locks": (2 if LEVEL == 1 else 1),
            "moves": S["moves"], "complete": bool(dists) and dists[-1] <= (3 if LEVEL == 1 else 2) and len(S["locks"]) <= (2 if LEVEL == 1 else 1)}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8799)
