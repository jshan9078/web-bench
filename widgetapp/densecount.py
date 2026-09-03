#!/usr/bin/env python3
"""178-dense-count: a pallet photo with 110-150 boxes in three colours, tight packing and partial occlusion. Task:
the exact number of BLUE boxes (40-60). Exact counting at this density is at the perception limit; a human counts
row by row. complete = exact (last submission)."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Warehouse pallet photo"; W, H = 1000, 760; QUESTION = "How many BLUE boxes are in this photo (exact count)?"
S = {"boxes": [], "blue": 0}


def reset():
    boxes = []; blue = 0
    for row in range(6):
        y0 = 110 + row * 108; x = 24; n = 0
        while x < W - 40 and n < 26:
            w = random.randint(26, 46); h = random.randint(40, 80); col = random.choices(["blue", "brown", "grey"], [0.4, 0.4, 0.2])[0]
            if random.random() < 0.35 and boxes and boxes[-1]["row"] == row: x -= random.randint(6, 16)
            boxes.append({"row": row, "x": x, "y": y0 + 90 - h, "w": w, "h": h, "col": col}); blue += col == "blue"; x += w + random.randint(2, 8); n += 1
    S["boxes"] = boxes; S["blue"] = blue


def draw():
    img = Image.new("RGB", (W, H), (58, 56, 54)); d = ImageDraw.Draw(img)
    for row in range(6):
        y = 110 + row * 108 + 90; d.rectangle([12, y, W - 12, y + 10], fill=(110, 88, 64))
    for b in S["boxes"]:
        c = {"blue": (52, 101, 190), "brown": (176, 130, 84), "grey": (150, 152, 156)}[b["col"]]; dark = tuple(int(v * 0.7) for v in c)
        d.rectangle([b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]], fill=c, outline=dark, width=1); d.rectangle([b["x"] + 4, b["y"] + 4, b["x"] + min(14, b["w"] - 6), b["y"] + 10], fill=(240, 236, 226))
    d.text((20, 12), "CAM 2  RECEIVING  2026-09-02 06:15", fill=(230, 230, 230), font=base.font(15))
    return img


def check(s):
    try: return int(perception.num(s)) == S["blue"]
    except Exception: return False


def answer_state(): return {"blue": S["blue"], "total": len(S["boxes"])}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8862)
