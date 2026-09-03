#!/usr/bin/env python3
"""90-dial-set: a rendered control dial (like a thermostat or audio gain knob) with a needle and a tick
scale from 0 to 100 with labels every 10. Arrow keys turn it 0.5 units (Shift: 5). The current value is
never printed: it must be read from the needle against the scale. Task: set it to the target value given
in the prompt within 1 unit (one tick) and press Enter once. complete = single confirm within tolerance."""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
W, H = 700, 520
S = {"value": 0.0, "target": 0.0, "confirms": [], "moves": 0}


def reset():
    S["target"] = float(random.randint(8, 92))            # a whole-number target; ticks every unit
    S["value"] = round(random.uniform(0, 100) * 2) / 2
    while abs(S["value"] - S["target"]) < 15: S["value"] = round(random.uniform(0, 100) * 2) / 2
    S["confirms"] = []; S["moves"] = 0


def _angle(v): return math.radians(-225 + 270 * v / 100)   # 0 at 7:30 o'clock, 100 at 4:30


def render():
    img = Image.new("RGB", (W, H), (248, 248, 250)); dr = ImageDraw.Draw(img)
    cx, cy, R = W / 2, 290, 190
    dr.text((20, 12), "Gain control. Arrow keys: 0.5 per press (Shift: 5). Enter confirms once.", fill=(80, 80, 80), font=base.font(14))
    dr.ellipse([cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14], fill=(235, 235, 240), outline=(200, 200, 205), width=2)
    for v in range(0, 101):
        a = _angle(v); major = v % 10 == 0; L = 18 if major else (11 if v % 5 == 0 else 6)
        x0, y0 = cx + (R - L) * math.cos(a), cy + (R - L) * math.sin(a); x1, y1 = cx + R * math.cos(a), cy + R * math.sin(a)
        dr.line([(x0, y0), (x1, y1)], fill=(60, 60, 70), width=2 if major else 1)
        if major:
            tx, ty = cx + (R - 36) * math.cos(a), cy + (R - 36) * math.sin(a); s = str(v); w = dr.textlength(s, font=base.font(13))
            dr.text((tx - w / 2, ty - 7), s, fill=(60, 60, 70), font=base.font(13))
    a = _angle(S["value"]); nx, ny = cx + (R - 26) * math.cos(a), cy + (R - 26) * math.sin(a)
    dr.line([(cx, cy), (nx, ny)], fill=(200, 40, 40), width=3); dr.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(60, 60, 70))
    dr.text((20, H - 26), f"moves {S['moves']}   confirms {len(S['confirms'])}", fill=(130, 130, 130), font=base.font(12))
    return base.png(img)


def page():
    return base.image_page("Gain Control", W, H, extra_html="""
<script>
document.addEventListener('keydown',function(e){var d={ArrowUp:1,ArrowRight:1,ArrowDown:-1,ArrowLeft:-1}[e.key];
 if(d){e.preventDefault();fetch('/__turn',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({delta:d*(e.shiftKey?5:0.5)})}).then(function(){document.getElementById('s').src='/__scene.png?'+Date.now()})}
 else if(e.key==='Enter'){fetch('/__confirm',{method:'POST'}).then(function(){document.getElementById('s').src='/__scene.png?'+Date.now()})}});
document.body.tabIndex=0;document.body.focus();
</script>""")


def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__turn":
        try: d = float(data.get("delta", 0))
        except Exception: return ('{"ok":false}', "application/json")
        S["value"] = min(100.0, max(0.0, round((S["value"] + d) * 2) / 2)); S["moves"] += 1; return ('{"ok":true}', "application/json")
    if path == "/__confirm":
        S["confirms"].append(S["value"]); return ('{"ok":true}', "application/json")
    return None


def state():
    c = S["confirms"]
    return {"target": S["target"], "value": S["value"], "confirms": c, "moves": S["moves"],
            "complete": len(c) == 1 and abs(c[0] - S["target"]) <= 1.0}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8810)
