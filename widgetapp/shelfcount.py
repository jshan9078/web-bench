#!/usr/bin/env python3
"""108-shelf-count: a warehouse shelf photo with several dozen boxes in two colours, some partly hidden behind
others. Task: the exact number of BLUE boxes. Counting many similar objects is a known weak spot of vision
models; a human counts them shelf by shelf. complete = exact count."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Aisle 4 shelf photo"; W, H = 960, 760; QUESTION = "How many BLUE boxes are on the shelves in this photo (exact count)?"
S = {"boxes": [], "blue": 0}


def reset():
    boxes = []; blue = 0
    for shelf in range(4):
        y_base = 180 + shelf * 180; x = 30; n = 0
        while x < W - 60 and n < 24:
            w = random.randint(34, 62); h = random.randint(44, 92); col = random.random() < 0.45
            if random.random() < 0.25 and boxes and boxes[-1]["shelf"] == shelf:      # partial overlap in front of the previous box
                x -= random.randint(10, 22)
            boxes.append({"shelf": shelf, "x": x, "y": y_base - h, "w": w, "h": h, "blue": col}); blue += col; x += w + random.randint(3, 14); n += 1
    S["boxes"] = boxes; S["blue"] = blue


def draw():
    img = Image.new("RGB", (W, H), (60, 58, 55)); d = ImageDraw.Draw(img)
    for shelf in range(4):
        y = 180 + shelf * 180; d.rectangle([20, y, W - 20, y + 14], fill=(120, 96, 70), outline=(70, 55, 40)); d.rectangle([20, y - 170, W - 20, y], fill=(78, 76, 72))
    for b in S["boxes"]:
        c = (52, 101, 190) if b["blue"] else (176, 130, 84); dark = tuple(int(v * 0.7) for v in c)
        d.rectangle([b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]], fill=c, outline=dark, width=2)
        d.line([b["x"] + b["w"] // 2, b["y"], b["x"] + b["w"] // 2, b["y"] + b["h"]], fill=dark, width=1); d.rectangle([b["x"] + 6, b["y"] + 6, b["x"] + min(22, b["w"] - 8), b["y"] + 16], fill=(240, 236, 226))
    d.text((24, 12), "CAM 7  AISLE 4  2026-09-01 07:42", fill=(230, 230, 230), font=base.font(15))
    return img


def check(s):
    try: return int(perception.num(s)) == S["blue"]
    except Exception: return False


def answer_state(): return {"blue": S["blue"], "total": len(S["boxes"])}


perception.make(sys.modules[__name__], W, H)

if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8828)
