#!/usr/bin/env python3
"""114-scatter-threshold: a latency scatter plot IMAGE with a dashed SLA line. Task: how many requests exceeded
the SLA (points strictly above the line). Points cluster near the line and two sit within a few pixels of it.
complete = exact count."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Latency scatter"; W, H = 960, 520; QUESTION = "How many requests exceeded the SLA line (points above the dashed line)? Exact count."
S = {"pts": [], "sla": 0, "answer": 0}


def reset():
    sla = random.choice([300, 400, 500]); pts = []
    for _ in range(random.randint(40, 60)):
        x = random.uniform(0, 60); y = max(20, random.gauss(sla - 60, 120)); pts.append((x, y))
    pts = [(x, y) for x, y in pts if abs(y - sla) > 18]
    pts += [(random.uniform(0, 60), sla + random.uniform(18, 26)) for _ in range(2)] + [(random.uniform(0, 60), sla - random.uniform(18, 26)) for _ in range(2)]
    S["pts"] = pts; S["sla"] = sla; S["answer"] = sum(1 for _, y in pts if y > sla)


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img); L, R, T, B = 70, 30, 40, 50; ph = H - T - B; pw = W - L - R; f = base.font(12, False)
    d.text((L, 10), "Request latency, last hour (ms)", fill=(50, 50, 60), font=base.font(16))
    for g in range(0, 1001, 200):
        y = T + ph * (1 - g / 1000); d.line([(L, y), (W - R, y)], fill=(235, 235, 240)); d.text((L - 40, y - 6), str(g), fill=(100, 100, 110), font=f)
    for m in range(0, 61, 10): d.text((L + pw * m / 60 - 8, H - B + 10), f"{m}m", fill=(100, 100, 110), font=f)
    ys = T + ph * (1 - S["sla"] / 1000)
    for x in range(int(L), int(W - R), 14): d.line([(x, ys), (x + 7, ys)], fill=(220, 40, 40), width=2)
    d.text((W - R - 90, ys - 18), f"SLA {S['sla']} ms", fill=(220, 40, 40), font=base.font(12))
    for x, y in S["pts"]:
        px = L + pw * x / 60; py = T + ph * (1 - min(y, 1000) / 1000); d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(56, 120, 200), outline=(20, 60, 120))
    return img


def check(s):
    try: return int(perception.num(s)) == S["answer"]
    except Exception: return False


def answer_state(): return {"answer": S["answer"], "sla": S["sla"], "n": len(S["pts"])}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8834)
