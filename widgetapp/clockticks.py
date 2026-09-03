#!/usr/bin/env python3
"""127-clock-ticks: a single station clock with no numerals, a thin second hand and the 12 mark rotated to the
top by a visible logo only. Task: the time to within 2 minutes. complete = within 2 minutes (12-hour)."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Platform clock"; W, H = 960, 520; QUESTION = "What time does the platform clock show? Answer as HH:MM (12-hour; within 2 minutes)."
S = {"h": 0, "m": 0, "s": 0}


def reset(): S["h"], S["m"], S["s"] = random.randint(1, 12), random.choice([m for m in range(60) if m % 5]), random.randint(3, 57)


def draw():
    img = Image.new("RGB", (W, H), (120, 128, 136)); d = ImageDraw.Draw(img); cx, cy, r = 480, 260, 210
    d.ellipse([cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12], fill=(40, 40, 44)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(248, 248, 246))
    for k in range(60):
        a = math.radians(k * 6 - 90); l = 26 if k % 5 == 0 else 10; w = 6 if k % 5 == 0 else 2
        d.line([cx + (r - l) * math.cos(a), cy + (r - l) * math.sin(a), cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a)], fill=(30, 30, 30), width=w)
    d.text((cx - 36, cy - 90), "NORTHWIND", fill=(90, 90, 90), font=base.font(12))
    h, m, s = S["h"], S["m"], S["s"]; ah = math.radians((h % 12) * 30 + m * 0.5 - 90); am = math.radians(m * 6 + s * 0.1 - 90); asec = math.radians(s * 6 - 90)
    d.line([cx - 20 * math.cos(ah), cy - 20 * math.sin(ah), cx + r * 0.55 * math.cos(ah), cy + r * 0.55 * math.sin(ah)], fill=(20, 20, 20), width=12)
    d.line([cx - 24 * math.cos(am), cy - 24 * math.sin(am), cx + r * 0.86 * math.cos(am), cy + r * 0.86 * math.sin(am)], fill=(20, 20, 20), width=7)
    d.line([cx - 40 * math.cos(asec), cy - 40 * math.sin(asec), cx + r * 0.9 * math.cos(asec), cy + r * 0.9 * math.sin(asec)], fill=(200, 30, 30), width=2)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(200, 30, 30)); d.text((cx - 60, cy + r + 24), "Platform 4", fill=(240, 240, 240), font=base.font(18))
    return img


def check(s):
    try:
        t = s.lower().replace("am", "").replace("pm", "").strip(); hh, mm = [int(x) for x in t.split(":")[:2]]
        target = (S["h"] % 12) * 60 + S["m"]; got = (hh % 12) * 60 + mm; diff = min(abs(target - got), 720 - abs(target - got)); return diff <= 2
    except Exception: return False


def answer_state(): return {"time": "%d:%02d:%02d" % (S["h"], S["m"], S["s"])}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8839)
