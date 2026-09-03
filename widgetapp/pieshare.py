#!/usr/bin/env python3
"""113-pie-share: a pie chart IMAGE with a legend and no percentage labels. Task: the share of one named segment
within 4 points. Angle-to-percentage estimation is a documented vision-model weakness; a human judges it against
the quarter marks. complete = within 4 points."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Traffic sources"; W, H = 960, 520
NAMES = ["Organic search", "Paid search", "Social", "Email", "Referral", "Direct"]
COLORS = [(56, 140, 220), (240, 160, 40), (60, 170, 110), (200, 80, 120), (140, 100, 210), (120, 120, 130)]
S = {"shares": [], "target": 0}
QUESTION = ""


def reset():
    global QUESTION
    while True:
        raw = [random.uniform(1, 10) for _ in NAMES]; tot = sum(raw); shares = [round(100 * r / tot) for r in raw]; shares[-1] += 100 - sum(shares)
        t = random.randrange(len(NAMES))
        if 9 <= shares[t] <= 40 and all(s >= 4 for s in shares) and abs(shares[t] - 25) > 5 and abs(shares[t] - 50) > 5: break
    S["shares"] = shares; S["target"] = t
    QUESTION = f"What share of traffic came from '{NAMES[t]}', as a percentage (within 4 points)?"; sys.modules[__name__].QUESTION = QUESTION


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img); d.text((20, 14), "Traffic sources, last 30 days", fill=(50, 50, 60), font=base.font(16))
    cx, cy, r = 330, 280, 200; a0 = -90 + random.Random(sum(S["shares"]) * 7 + S["target"]).randint(0, 359)
    for i, s in enumerate(S["shares"]):
        a1 = a0 + 360 * s / 100; d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=COLORS[i], outline=(255, 255, 255), width=2); a0 = a1
    for i, n in enumerate(NAMES):
        y = 120 + i * 40; d.rectangle([620, y, 646, y + 18], fill=COLORS[i]); d.text((656, y - 1), n, fill=(40, 40, 50), font=base.font(15, False))
    return img


def check(s):
    try: return abs(perception.num(s) - S["shares"][S["target"]]) <= 4
    except Exception: return False


def answer_state(): return {"target": NAMES[S["target"]], "answer": S["shares"][S["target"]], "shares": dict(zip(NAMES, S["shares"]))}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8833)
