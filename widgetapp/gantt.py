#!/usr/bin/env python3
"""112-gantt-read: a project Gantt chart as an IMAGE (bars against a day axis, no dates printed on bars).
Task: which tasks are in progress on a given day. Bars that end the day before or start the day after are
the traps. complete = the exact set of task names."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Project timeline"; W, H = 960, 520
NAMES = ["Discovery", "Wireframes", "Design review", "API build", "Frontend build", "Content", "QA pass", "Security review", "Launch prep", "Training"]
S = {"bars": [], "day": 0, "answer": []}
QUESTION = ""


def reset():
    global QUESTION
    while True:
        bars = []
        for n in NAMES:
            s = random.randint(1, 22); e = s + random.randint(2, 9); bars.append((n, s, min(e, 30)))
        day = random.randint(8, 24)
        active = [n for n, s, e in bars if s <= day <= e]
        near = [n for n, s, e in bars if e == day - 1 or s == day + 1]
        if 3 <= len(active) <= 5 and len(near) >= 2: break
    S["bars"] = bars; S["day"] = day; S["answer"] = sorted(active)
    QUESTION = f"Which tasks are in progress on September {day} (their bar covers that day)? List all of them, comma-separated."
    sys.modules[__name__].QUESTION = QUESTION


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img); L, T = 170, 60; dw = (W - L - 30) / 30; rh = 40; f = base.font(12, False)
    d.text((20, 14), "September 2026 delivery plan", fill=(50, 50, 60), font=base.font(16))
    for day in range(1, 31):
        x = L + (day - 1) * dw; d.line([(x, T - 6), (x, T + 10 * rh)], fill=(238, 238, 242) if day % 7 else (200, 200, 210))
        if day % 2 == 1: d.text((x + dw / 2 - 6, T - 24), str(day), fill=(90, 90, 100), font=f)
    for i, (n, s, e) in enumerate(S["bars"]):
        y = T + i * rh + 8; d.text((20, y + 2), n, fill=(40, 40, 50), font=base.font(13, False))
        d.rounded_rectangle([L + (s - 1) * dw + 1, y, L + e * dw - 1, y + 22], 5, fill=[(56, 140, 220), (34, 160, 110), (230, 140, 40), (150, 100, 200)][i % 4])
    return img


def check(s):
    got = sorted(p.strip().lower() for p in s.replace(";", ",").split(",") if p.strip())
    return got == [a.lower() for a in S["answer"]]


def answer_state(): return {"day": S["day"], "answer": S["answer"], "bars": S["bars"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8832)
