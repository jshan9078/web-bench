#!/usr/bin/env python3
"""110-analog-clock: a wall of three office clocks (Lisbon, New York, Tokyo) with hour and minute hands and
only 12/3/6/9 numerals. Task: the time shown on the Tokyo clock to within 2 minutes. Reading analog clocks is a
known vision-model weakness; a human reads it at a glance. complete = within 2 minutes (12-hour, am/pm ignored)."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Office clocks"; W, H = 960, 420; QUESTION = "What time does the TOKYO clock show? Answer as HH:MM (12-hour; within 2 minutes)."
CITIES = ["LISBON", "NEW YORK", "TOKYO"]
S = {"times": []}


def reset():
    S["times"] = [(random.randint(1, 12), random.choice([m for m in range(60) if m % 5 not in (0,)])) for _ in CITIES]


def clock(d, cx, cy, r, h, m):
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=(40, 40, 44)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 248))
    for k in range(60):
        a = math.radians(k * 6 - 90); l = 14 if k % 5 == 0 else 6; w = 3 if k % 5 == 0 else 1
        d.line([cx + (r - l) * math.cos(a), cy + (r - l) * math.sin(a), cx + (r - 3) * math.cos(a), cy + (r - 3) * math.sin(a)], fill=(30, 30, 30), width=w)
    for n, (dx, dy) in zip(["12", "3", "6", "9"], [(0, -1), (1, 0), (0, 1), (-1, 0)]):
        d.text((cx + dx * (r - 34) - 8, cy + dy * (r - 34) - 9), n, fill=(30, 30, 30), font=base.font(18))
    ah = math.radians((h % 12) * 30 + m * 0.5 - 90); am = math.radians(m * 6 - 90)
    d.line([cx, cy, cx + (r * 0.52) * math.cos(ah), cy + (r * 0.52) * math.sin(ah)], fill=(20, 20, 20), width=7)
    d.line([cx, cy, cx + (r * 0.82) * math.cos(am), cy + (r * 0.82) * math.sin(am)], fill=(20, 20, 20), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(180, 30, 30))


def draw():
    img = Image.new("RGB", (W, H), (214, 210, 200)); d = ImageDraw.Draw(img)
    for i, c in enumerate(CITIES):
        cx = 170 + i * 310; clock(d, cx, 190, 120, *S["times"][i]); d.rectangle([cx - 70, 330, cx + 70, 362], fill=(40, 40, 44)); d.text((cx - 8 * len(c) / 2 - 8, 337), c, fill=(240, 240, 240), font=base.font(16))
    return img


def check(s):
    h, m = S["times"][2]
    try:
        t = s.lower().replace("am", "").replace("pm", "").strip(); hh, mm = [int(x) for x in t.split(":")[:2]]
        target = (h % 12) * 60 + m; got = (hh % 12) * 60 + mm; diff = min(abs(target - got), 720 - abs(target - got))
        return diff <= 2
    except Exception: return False


def answer_state(): return {"tokyo": "%d:%02d" % S["times"][2], "all": ["%d:%02d" % t for t in S["times"]]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8830)
