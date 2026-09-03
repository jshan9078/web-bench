#!/usr/bin/env python3
"""118-odometer-read: a dashboard photo (insurance mileage check) with a seven-segment odometer at a slight
angle under glare, plus a trip meter in the same style. Task: the odometer reading in km. Seven-segment digits
under glare (0/8/6/9, 1/7) are a known OCR weak spot; the trip meter is the decoy. complete = exact reading."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import base, perception
TITLE = "Dashboard photo"; W, H = 960, 560; QUESTION = "What is the ODOMETER reading (total distance, km)? Enter the number only."
S = {"odo": 0, "trip": 0.0}
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg"}


def reset():
    S["odo"] = random.randint(38000, 189999); S["trip"] = round(random.uniform(10, 999.9), 1)
    if not any(ch in str(S["odo"]) for ch in "0689"): S["odo"] += 6


def seg(d, x, y, w, h, ch, on=(255, 90, 60), off=(70, 34, 30)):
    t = max(3, h // 9); segs = SEG.get(ch, "")
    boxes = {"a": [x + t, y, x + w - t, y + t], "b": [x + w - t, y + t, x + w, y + h // 2 - t // 2], "c": [x + w - t, y + h // 2 + t // 2, x + w, y + h - t],
             "d": [x + t, y + h - t, x + w - t, y + h], "e": [x, y + h // 2 + t // 2, x + t, y + h - t], "f": [x, y + t, x + t, y + h // 2 - t // 2], "g": [x + t, y + h // 2 - t // 2, x + w - t, y + h // 2 + t // 2]}
    for k, b in boxes.items(): d.rectangle(b, fill=on if k in segs else off)


def draw():
    img = Image.new("RGB", (W, H), (28, 28, 32)); d = ImageDraw.Draw(img)
    d.ellipse([60, 60, 460, 460], outline=(90, 90, 100), width=6); d.ellipse([520, 100, 900, 480], outline=(90, 90, 100), width=6)
    for i in range(0, 181, 15):
        import math; a = math.radians(180 + i); d.line([260 + 170 * math.cos(a), 260 + 170 * math.sin(a), 260 + 190 * math.cos(a), 260 + 190 * math.sin(a)], fill=(200, 200, 210), width=3)
    d.text((215, 400), "km/h", fill=(160, 160, 170), font=base.font(16, False)); d.text((690, 420), "rpm x1000", fill=(160, 160, 170), font=base.font(14, False))
    panel = Image.new("RGB", (330, 150), (20, 12, 12)); pd = ImageDraw.Draw(panel)
    pd.text((14, 8), "ODO", fill=(200, 120, 90), font=base.font(13)); s = str(S["odo"]).rjust(6, "0")
    for i, ch in enumerate(s): seg(pd, 14 + i * 40, 28, 28, 52, ch)
    pd.text((14, 92), "TRIP A", fill=(200, 120, 90), font=base.font(13)); ts = f"{S['trip']:06.1f}".replace(".", "")
    for i, ch in enumerate(ts): seg(pd, 130 + i * 30, 96, 20, 40, ch, on=(255, 120, 80))
    pd.rectangle([130 + 4 * 30 - 8, 132, 130 + 4 * 30 - 4, 136], fill=(255, 120, 80))
    panel = panel.rotate(-4, expand=True, resample=Image.BICUBIC, fillcolor=(28, 28, 32))
    img.paste(panel, (315, 300))
    glare = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(glare); gd.ellipse([380, 250, 700, 400], fill=(70, 70, 70)); glare = glare.filter(ImageFilter.GaussianBlur(40))
    from PIL import ImageChops; img = ImageChops.add(img, glare)
    return img.filter(ImageFilter.GaussianBlur(0.7))


def check(s):
    try: return int(perception.num(s.replace(" ", ""))) == S["odo"]
    except Exception: return False


def answer_state(): return {"odometer": S["odo"], "trip": S["trip"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8836)
