#!/usr/bin/env python3
"""313-clock-grid: six analog clocks without numerals in varied styles; report the time shown by the clock with
the RED rim, HH:MM, within one minute. complete = within tolerance."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Clocks"; W, H = 960, 640; QUESTION = "What time does the clock with the RED rim show? Answer HH:MM (12-hour, e.g. 4:37)."
S = {"times": [], "target": 0}


def reset(): S["times"] = [(random.randint(1, 12), random.randint(0, 59)) for _ in range(6)]; S["target"] = random.randrange(6)


def draw():
    img = Image.new("RGB", (W, H), (240, 238, 232)); d = ImageDraw.Draw(img)
    for i, (h, m) in enumerate(S["times"]):
        cx, cy = 160 + (i % 3) * 320, 160 + (i // 3) * 320; r = 120; rim = (200, 30, 30) if i == S["target"] else random.choice([(40, 40, 40), (90, 70, 40), (30, 60, 110)])
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 252), outline=rim, width=8)
        for k in range(60):
            a = math.radians(k * 6); L = 12 if k % 5 == 0 else 5; d.line([(cx + (r - 14) * math.sin(a), cy - (r - 14) * math.cos(a)), (cx + (r - 14 - L) * math.sin(a), cy - (r - 14 - L) * math.cos(a))], fill=(60, 60, 60), width=2 if k % 5 == 0 else 1)
        ha = math.radians((h % 12 + m / 60) * 30); ma = math.radians(m * 6)
        d.line([(cx, cy), (cx + 60 * math.sin(ha), cy - 60 * math.cos(ha))], fill=(20, 20, 20), width=7)
        d.line([(cx, cy), (cx + 95 * math.sin(ma), cy - 95 * math.cos(ma))], fill=(20, 20, 20), width=4)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(20, 20, 20))
    return img


def check(s):
    try:
        hh, mm = s.strip().lower().replace("am", "").replace("pm", "").split(":"); h, m = S["times"][S["target"]]; got = (int(hh) % 12) * 60 + int(mm); want = (h % 12) * 60 + m
        return min(abs(got - want), 720 - abs(got - want)) <= 1
    except Exception: return False


def answer_state(): return {"target_time": "%d:%02d" % S["times"][S["target"]], "all": S["times"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8951)
