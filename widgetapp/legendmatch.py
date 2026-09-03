#!/usr/bin/env python3
"""109-legend-match: a six-series line chart (regions) whose colours are distinguishable but related shades,
with a legend of swatches. Task: which region was highest in September and its value. The series cross often
and a different region holds the overall peak. complete = correct region and value within 3."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Regional sales"; W, H = 960, 520; QUESTION = "Which region had the HIGHEST sales in September, and what was its value (k units)? Answer as: Region, value"
REGIONS = ["North", "South", "East", "West", "Central", "Islands"]
COLORS = [(31, 119, 180), (23, 190, 207), (44, 160, 44), (148, 103, 189), (255, 127, 14), (214, 39, 40)]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
S = {"data": {}, "answer": None}


def reset():
    while True:
        data = {r: [random.randint(20, 80)] for r in REGIONS}
        for r in REGIONS:
            for _ in range(11): data[r].append(min(95, max(5, data[r][-1] + random.randint(-18, 18))))
        sep = {r: data[r][8] for r in REGIONS}; top = max(sep, key=sep.get); srt = sorted(sep.values(), reverse=True)
        peak_r = max(REGIONS, key=lambda r: max(data[r]))
        if srt[0] - srt[1] >= 5 and peak_r != top and max(data[peak_r]) > sep[top] + 5: break
    S["data"] = data; S["answer"] = {"region": top, "value": sep[top]}


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img); L, R, T, B = 60, 180, 40, 50; ph = H - T - B; f = base.font(12, False)
    d.text((L, 10), "Monthly sales by region (k units)", fill=(60, 60, 60), font=base.font(15))
    for g in range(0, 101, 20):
        y = T + ph * (1 - g / 100); d.line([(L, y), (W - R, y)], fill=(230, 230, 230)); d.text((L - 30, y - 6), str(g), fill=(120, 120, 120), font=f)
    xs = [L + (W - L - R) * i / 11 for i in range(12)]
    for i, m in enumerate(MONTHS): d.text((xs[i] - 10, H - B + 10), m, fill=(90, 90, 90), font=f)
    for k, r in enumerate(REGIONS):
        pts = [(xs[i], T + ph * (1 - S["data"][r][i] / 100)) for i in range(12)]; d.line(pts, fill=COLORS[k], width=3)
        for x, y in pts: d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=COLORS[k])
        ly = T + 10 + k * 26; d.rectangle([W - R + 20, ly, W - R + 44, ly + 12], fill=COLORS[k]); d.text((W - R + 52, ly - 2), r, fill=(40, 40, 40), font=base.font(13, False))
    return img


def check(s):
    a = S["answer"]
    try:
        parts = [p.strip() for p in s.replace(";", ",").split(",")]; reg = parts[0].lower(); val = perception.num(parts[1]) if len(parts) > 1 else None
        return a["region"].lower() in reg and val is not None and abs(val - a["value"]) <= 3
    except Exception: return False


def answer_state(): return {"answer": S["answer"], "september": {r: S["data"][r][8] for r in REGIONS}}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8829)
