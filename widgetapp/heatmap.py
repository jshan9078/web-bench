#!/usr/bin/env python3
"""115-heatmap-max: a weekday-by-hour activity heatmap IMAGE with a colour scale and no numbers. Task: the cell
(day and hour) with the highest activity. The maximum is one step darker than two runners-up elsewhere.
complete = correct day and hour."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Activity heatmap"; W, H = 960, 440; QUESTION = "Which cell has the HIGHEST activity? Answer as 'Day HH' (for example: Tue 14)."
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]; HOURS = list(range(6, 22))
S = {"grid": [], "answer": None}


def reset():
    grid = [[random.randint(5, 70) for _ in HOURS] for _ in DAYS]
    cells = [(d, h) for d in range(7) for h in range(len(HOURS))]; mx, r1, r2 = random.sample(cells, 3)
    grid[mx[0]][mx[1]] = 100; grid[r1[0]][r1[1]] = 88; grid[r2[0]][r2[1]] = 86
    S["grid"] = grid; S["answer"] = (DAYS[mx[0]], HOURS[mx[1]])


def col(v):
    t = v / 100; return (int(255 - 200 * t), int(245 - 190 * t), int(255 - 120 * t))


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img); L, T, cw, ch = 80, 70, 50, 40; f = base.font(12, False)
    d.text((20, 14), "Support chat activity by weekday and hour", fill=(50, 50, 60), font=base.font(16))
    for j, h in enumerate(HOURS): d.text((L + j * cw + 16, T - 22), f"{h:02d}", fill=(90, 90, 100), font=f)
    for i, day in enumerate(DAYS):
        d.text((30, T + i * ch + 12), day, fill=(90, 90, 100), font=f)
        for j in range(len(HOURS)): d.rectangle([L + j * cw, T + i * ch, L + (j + 1) * cw - 2, T + (i + 1) * ch - 2], fill=col(S["grid"][i][j]))
    for k in range(101):
        d.rectangle([L + k * 3, T + 7 * ch + 20, L + k * 3 + 3, T + 7 * ch + 36], fill=col(k))
    d.text((L, T + 7 * ch + 40), "low", fill=(90, 90, 100), font=f); d.text((L + 280, T + 7 * ch + 40), "high", fill=(90, 90, 100), font=f)
    return img


def check(s):
    try:
        parts = s.replace(",", " ").split(); day = parts[0][:3].lower(); hour = int("".join(ch for ch in parts[1] if ch.isdigit())[:2])
        return day == S["answer"][0].lower() and hour == S["answer"][1]
    except Exception: return False


def answer_state(): return {"answer": f"{S['answer'][0]} {S['answer'][1]:02d}"}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8835)
