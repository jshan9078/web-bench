#!/usr/bin/env python3
"""105-ruler-measure: a product photo of two parts beside a ruler (cm labels, mm ticks). Task: the length of
part A in millimetres. Neither part starts at zero; the second part is a distractor. complete = within 2 mm."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
PX_PER_MM = 5; X0 = 80
S = {"a": (0, 0), "b": (0, 0), "answer": 0, "submissions": []}


def reset():
    S["submissions"] = []
    la = random.randint(43, 118); sa = random.randint(4, 140 - la); lb = random.randint(30, 90); sb = random.randint(4, 140 - lb)
    S["a"] = (sa, la); S["b"] = (sb, lb); S["answer"] = la


def render():
    W, H = 900, 420; img = Image.new("RGB", (W, H), (226, 224, 218)); d = ImageDraw.Draw(img)
    # ruler
    d.rectangle([X0 - 30, 300, X0 + 150 * PX_PER_MM + 30, 380], fill=(250, 240, 200), outline=(120, 110, 80))
    for mm in range(0, 151):
        x = X0 + mm * PX_PER_MM; h = 28 if mm % 10 == 0 else 18 if mm % 5 == 0 else 10
        d.line([x, 300, x, 300 + h], fill=(40, 40, 40), width=2 if mm % 10 == 0 else 1)
        if mm % 10 == 0: d.text((x - 6, 340), str(mm // 10), fill=(40, 40, 40), font=base.font(16, False))
    d.text((X0 + 150 * PX_PER_MM - 40, 358), "cm", fill=(40, 40, 40), font=base.font(12, False))
    # part A (red bar with rounded ends) and part B (grey hex-ish)
    sa, la = S["a"]; d.rounded_rectangle([X0 + sa * PX_PER_MM, 150, X0 + (sa + la) * PX_PER_MM, 200], 10, fill=(200, 50, 50), outline=(120, 20, 20)); d.text((X0 + sa * PX_PER_MM, 120), "A", fill=(120, 20, 20), font=base.font(20))
    sb, lb = S["b"]; d.rectangle([X0 + sb * PX_PER_MM, 230, X0 + (sb + lb) * PX_PER_MM, 270], fill=(120, 125, 135), outline=(60, 60, 70)); d.text((X0 + sb * PX_PER_MM, 205), "B", fill=(60, 60, 70), font=base.font(20))
    d.text((20, 20), "Replacement parts, listing photo. Ruler for scale.", fill=(60, 60, 60), font=base.font(15, False))
    return base.png(img)


def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("mm") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    ok = False
    for s in S["submissions"]:
        try:
            v = float(s.lower().replace("mm", "").strip()); ok = ok or abs(v - S["answer"]) <= 2
        except ValueError: pass
    return {"answer_mm": S["answer"], "part_a": S["a"], "part_b": S["b"], "submissions": S["submissions"], "complete": ok}


def page():
    return base.image_page("Replacement parts", 900, 420, extra_html="""
<div style="position:absolute;top:430px;left:20px;font:14px system-ui"><label>Length of part A (mm): <input id=a size=8></label> <button id=go>Submit</button> <span id=msg></span>
<script>document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mm:document.getElementById('a').value})}).then(r=>r.json()).then(j=>{document.getElementById('msg').textContent='Submitted ('+j.n+').'})}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8825)
