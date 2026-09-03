#!/usr/bin/env python3
"""100-dual-axis-chart: an IMAGE chart with revenue bars on the LEFT axis (k$) and margin % as a line on the
RIGHT axis. Task: the month with the highest margin and the revenue that month. Traps: the tallest bar is a
different month; reading the line against the left axis gives nonsense. complete = correct month and revenue
within 5 k$."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
S = {"rev": [], "margin": [], "answer": None, "submissions": []}


def reset():
    S["submissions"] = []
    while True:
        rev = [random.randint(25, 95) for _ in range(12)]; mg = [random.randint(8, 36) for _ in range(12)]
        i = max(range(12), key=lambda k: mg[k]); j = max(range(12), key=lambda k: rev[k])
        srt = sorted(mg, reverse=True)
        if i != j and srt[0] - srt[1] >= 3 and rev[i] < 80 and abs(rev[i] - rev[j]) >= 12: break
    S["rev"], S["margin"] = rev, mg; S["answer"] = {"month": MONTHS[i], "revenue": rev[i], "margin": mg[i]}


def render():
    W, H = 900, 480; L, R, T, B = 70, 70, 40, 50; img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    d.text((L, 8), "Revenue (bars, k$, left axis) and gross margin (line, %, right axis)", fill=(60, 60, 60), font=base.font(14)); f = base.font(11, False)
    ph = H - T - B
    for g in range(0, 101, 20):
        y = T + ph * (1 - g / 100); d.line([(L, y), (W - R, y)], fill=(230, 230, 230)); d.text((L - 30, y - 6), f"{g}", fill=(37, 99, 235), font=f)
    for g in range(0, 41, 10):
        y = T + ph * (1 - g / 40); d.text((W - R + 8, y - 6), f"{g}%", fill=(220, 38, 38), font=f)
    bw = (W - L - R) / 12
    for i in range(12):
        x = L + i * bw; y = T + ph * (1 - S["rev"][i] / 100); d.rectangle([x + 8, y, x + bw - 8, T + ph], fill=(147, 197, 253)); d.text((x + bw / 2 - 10, H - B + 10), MONTHS[i], fill=(90, 90, 90), font=f)
    pts = [(L + i * bw + bw / 2, T + ph * (1 - S["margin"][i] / 40)) for i in range(12)]
    d.line(pts, fill=(220, 38, 38), width=3)
    for x, y in pts: d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(220, 38, 38))
    return base.png(img)


def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append({"month": str(data.get("month") or "").strip(), "revenue": str(data.get("revenue") or "").strip()}); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    a = S["answer"]; ok = False
    for s in S["submissions"]:
        try: v = float(s["revenue"].replace("k", "").replace("$", "").replace(",", ""))
        except ValueError: continue
        if s["month"].lower()[:3] == a["month"].lower() and abs(v - a["revenue"]) <= 5: ok = True
    return {"answer": a, "revenue": dict(zip(MONTHS, S["rev"])), "margin": dict(zip(MONTHS, S["margin"])), "submissions": S["submissions"], "complete": ok}


def page():
    return base.image_page("Monthly performance", 900, 480, extra_html="""
<div style="position:absolute;top:490px;left:20px;font:14px system-ui;width:860px"><p>Which month had the highest gross margin, and what was revenue (k$) that month?</p>
<label>Month <input id=m size=6></label> &nbsp; <label>Revenue (k$) <input id=v size=8></label> &nbsp; <button id=go>Submit</button> <span id=msg></span>
<script>document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({month:document.getElementById('m').value,revenue:document.getElementById('v').value})}).then(r=>r.json()).then(j=>{document.getElementById('msg').textContent='Submitted ('+j.n+').'})}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8820)
