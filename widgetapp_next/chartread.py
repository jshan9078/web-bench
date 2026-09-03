#!/usr/bin/env python3
"""86-chart-read: a monthly revenue line chart rendered as an IMAGE with gridlines and axis ticks but no
data labels and no tooltips (the way many embedded dashboards ship). Task: report the month with the
LARGEST month-over-month DROP and the approximate value that month (within 5% of full scale). Two drops
are close but distinguishable against the gridlines. complete = correct month and value within tolerance."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
S = {"vals": [], "answer": None, "submissions": []}
YMAX = 100


def reset():
    while True:
        vals = [random.randint(20, 95)]
        for _ in range(11): vals.append(min(95, max(10, vals[-1] + random.randint(-30, 30))))
        drops = [(vals[i - 1] - vals[i], i) for i in range(1, 12) if vals[i] < vals[i - 1]]
        if len(drops) >= 3:
            drops.sort(reverse=True)
            if drops[0][0] - drops[1][0] >= 4 and drops[0][0] >= 15: break
    S["vals"] = vals; S["submissions"] = []
    S["answer"] = {"month": MONTHS[drops[0][1]], "value": vals[drops[0][1]]}


def render():
    W, H = 900, 480; L, R, T, B = 70, 30, 30, 50
    img = Image.new("RGB", (W, H), (255, 255, 255)); dr = ImageDraw.Draw(img)
    dr.text((L, 6), "Monthly revenue (k$)", fill=(60, 60, 60), font=base.font(14))
    f = base.font(11, False)
    for g in range(0, YMAX + 1, 10):
        y = T + (H - T - B) * (1 - g / YMAX); dr.line([(L, y), (W - R, y)], fill=(225, 225, 225), width=1); dr.text((L - 34, y - 6), f"{g}", fill=(120, 120, 120), font=f)
    xs = [L + (W - L - R) * i / 11 for i in range(12)]
    pts = [(xs[i], T + (H - T - B) * (1 - S["vals"][i] / YMAX)) for i in range(12)]
    dr.line(pts, fill=(37, 99, 235), width=2)
    for i, (x, y) in enumerate(pts):
        dr.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(37, 99, 235)); dr.text((x - 10, H - B + 12), MONTHS[i], fill=(90, 90, 90), font=f)
    return base.png(img)


def page():
    return base.image_page("Revenue Chart", 900, 480, extra_html="""
<div style="position:absolute;top:490px;left:20px;font:14px system-ui;width:860px">
<p>Which month shows the largest drop from the previous month, and what is that month's value (k$)?</p>
<label>Month <input id=m size=6></label> &nbsp; <label>Value (k$) <input id=v size=8></label> &nbsp; <button id=go>Submit</button> <span id=msg></span>
<script>
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({month:m.value,value:v.value})}).then(r=>r.json()).then(j=>{document.getElementById('msg').textContent='Submitted ('+j.n+').'})}
</script></div>""")


def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append({"month": str(data.get("month") or "").strip(), "value": str(data.get("value") or "").strip()}); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    a = S["answer"]; ok = False
    for s in S["submissions"]:
        try: v = float(s["value"].replace("k", "").replace("$", ""))
        except ValueError: continue
        if s["month"].lower()[:3] == a["month"].lower() and abs(v - a["value"]) <= 5: ok = True
    return {"values": dict(zip(MONTHS, S["vals"])), "answer": a, "submissions": S["submissions"], "complete": ok}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8806)
