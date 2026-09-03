#!/usr/bin/env python3
"""182-map-measure: a trail map IMAGE with a scale bar and a marked route of 4-6 straight segments. Task: the
route's length in metres within 6 percent. Multi-segment measurement against a scale bar. complete = within 6%."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Trail map"; W, H = 960, 640; QUESTION = "How long is the marked route (from the start marker S to the finish marker F, following the red line) in metres, within 6 percent? Use the scale bar."
S = {"pts": [], "m_per_px": 0.0, "answer": 0}


def reset():
    pts = [(random.randint(80, 200), random.randint(120, 520))]
    for _ in range(random.randint(4, 6)):
        x, y = pts[-1]; nx, ny = x + random.randint(90, 200), max(90, min(540, y + random.randint(-180, 180))); pts.append((nx, ny))
    S["pts"] = pts; S["m_per_px"] = random.choice([1.5, 2.0, 2.5, 3.0])
    px = sum(math.dist(a, b) for a, b in zip(pts, pts[1:])); S["answer"] = round(px * S["m_per_px"])


def draw():
    img = Image.new("RGB", (W, H), (222, 232, 205)); d = ImageDraw.Draw(img); rng = random.Random(S["answer"])
    for _ in range(9): x, y = rng.randint(0, W), rng.randint(0, 560); r = rng.randint(30, 90); d.ellipse([x - r, y - r, x + r, y + r], fill=(205, 220, 185))
    for k in range(60, 560, 40): d.line([(0, k), (W, k + rng.randint(-20, 20))], fill=(212, 224, 195))
    d.line([(0, 300), (300, 260), (600, 330), (W, 290)], fill=(120, 170, 220), width=6)
    d.line(S["pts"], fill=(210, 40, 40), width=4)
    for x, y in S["pts"][1:-1]: d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(210, 40, 40))
    sx, sy = S["pts"][0]; fx, fy = S["pts"][-1]; d.ellipse([sx - 12, sy - 12, sx + 12, sy + 12], fill=(30, 120, 60)); d.text((sx - 5, sy - 8), "S", fill=(255, 255, 255), font=base.font(13)); d.ellipse([fx - 12, fy - 12, fx + 12, fy + 12], fill=(30, 30, 120)); d.text((fx - 5, fy - 8), "F", fill=(255, 255, 255), font=base.font(13))
    bar = int(200 / S["m_per_px"] * (1 if S["m_per_px"] <= 2 else 0.5)) if False else 200; metres = int(bar * S["m_per_px"])
    d.rectangle([40, 590, 40 + bar, 600], fill=(30, 30, 30)); d.rectangle([40, 590, 40 + bar // 2, 600], fill=(255, 255, 255), outline=(30, 30, 30)); d.text((40, 604), "0", fill=(30, 30, 30), font=base.font(12)); d.text((40 + bar - 16, 604), f"{metres} m", fill=(30, 30, 30), font=base.font(12))
    d.text((600, 596), "Harbor Ridge trails, north loop", fill=(60, 60, 60), font=base.font(13))
    return img


def check(s):
    try: v = perception.num(s.lower().replace("m", "").replace("etres", "")); return abs(v - S["answer"]) <= 0.06 * S["answer"]
    except Exception: return False


def answer_state(): return {"answer_m": S["answer"], "m_per_px": S["m_per_px"], "points": S["pts"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8865)
