#!/usr/bin/env python3
"""180-radio-tuner: an FM tuner with a linear dial (88-108 MHz, ticks every 0.2, labels every 2) and a needle;
arrow keys move 0.1 MHz (Shift: 1.0). The frequency is never printed. Task: tune to the stated station within
0.1 MHz and press Enter once. Same skill as the dial (needle against fine ticks) in a realistic wrapper."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 900, 300; X0, X1 = 60, 840
S = {"value": 98.0, "target": 101.7, "confirms": [], "moves": 0}


def reset():
    S["target"] = round(random.choice([v for v in range(881, 1079) if v % 5 not in (0,)]) / 10, 1); S["value"] = round(random.uniform(88, 108), 1)
    while abs(S["value"] - S["target"]) < 3: S["value"] = round(random.uniform(88, 108), 1)
    S["confirms"] = []; S["moves"] = 0


def xof(f): return X0 + (X1 - X0) * (f - 88) / 20


def render():
    img = Image.new("RGB", (W, H), (34, 34, 38)); d = ImageDraw.Draw(img); d.text((20, 14), "FM   Arrow keys: 0.1 MHz per press (Shift: 1.0). Enter confirms once.", fill=(180, 180, 190), font=base.font(14))
    d.rectangle([X0 - 30, 90, X1 + 30, 230], fill=(245, 240, 220))
    f = 88.0
    while f <= 108.001:
        x = xof(f); k = round(f * 10); big = k % 20 == 0; mid = k % 10 == 0; L = 34 if big else 22 if mid else 12
        d.line([x, 150, x, 150 + L], fill=(40, 40, 40), width=2 if big else 1)
        if big: d.text((x - 10, 118), f"{f:.0f}", fill=(40, 40, 40), font=base.font(14)); f = round(f + 0.2, 1)
        else: f = round(f + 0.2, 1)
    d.text((X0 - 24, 205), "MHz", fill=(90, 90, 90), font=base.font(12, False))
    x = xof(S["value"]); d.line([x, 100, x, 226], fill=(200, 30, 30), width=3)
    d.text((20, H - 26), f"moves {S['moves']}   confirms {len(S['confirms'])}", fill=(130, 130, 140), font=base.font(12))
    return base.png(img)


def page():
    return base.image_page("FM tuner", W, H, extra_html=f"""
<div style="position:absolute;top:{H + 10}px;left:20px;font:14px system-ui;color:#111;width:860px"><p>Tune to <b>{S['target']:.1f} MHz</b> (within 0.1 MHz), then press Enter once.</p></div>
<script>
document.addEventListener('keydown',function(e){{var d={{ArrowUp:1,ArrowRight:1,ArrowDown:-1,ArrowLeft:-1}}[e.key];
 if(d){{e.preventDefault();fetch('/__turn',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{delta:d*(e.shiftKey?1.0:0.1)}})}}).then(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}})}}
 else if(e.key==='Enter'){{fetch('/__confirm',{{method:'POST'}}).then(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}})}}}});
document.body.tabIndex=0;document.body.focus();
</script>""")


def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__turn":
        try: dd = float(data.get("delta", 0))
        except Exception: return ('{"ok":false}', "application/json")
        S["value"] = round(min(108.0, max(88.0, S["value"] + dd)), 1); S["moves"] += 1; return ('{"ok":true}', "application/json")
    if path == "/__confirm": S["confirms"].append(S["value"]); return ('{"ok":true}', "application/json")
    return None


def state():
    c = S["confirms"]; return {"target": S["target"], "value": S["value"], "confirms": c, "moves": S["moves"], "complete": len(c) == 1 and abs(c[0] - S["target"]) <= 0.1001}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8864)
