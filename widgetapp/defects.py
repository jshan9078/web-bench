#!/usr/bin/env python3
"""161-defect-marking: a QA inspection photo of a painted panel with five small scratches among texture and
decoy dust specks. Click each scratch to mark it (markers render), then Confirm. complete = every scratch has a
marker within 12 px and at most one stray marker."""
import json, random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, imgapp
TITLE = "QA inspection: mark defects"; W, H = 900, 600; NOTE = "Inspection photo (image; click on each scratch to place a marker; click a marker again to remove it; then click the Confirm button at the bottom-right of the image)."
S = {"scr": [], "marks": [], "confirmed": None, "specks": []}


def reset():
    S["marks"] = []; S["confirmed"] = None; scr = []
    while len(scr) < 5:
        x, y = random.randint(80, 820), random.randint(80, 480)
        if all(math.dist((x, y), s[:2]) > 90 for s in scr): scr.append((x, y, random.uniform(0, math.pi), random.randint(14, 26)))
    S["scr"] = scr; S["specks"] = [(random.randint(60, 840), random.randint(60, 500)) for _ in range(14)]


def draw():
    img = Image.new("RGB", (W, H), (140, 150, 165)); d = ImageDraw.Draw(img); rng = random.Random(7)
    for _ in range(2500): x, y = rng.randint(0, W - 1), rng.randint(0, 539); d.point((x, y), fill=(rng.randint(130, 150), rng.randint(140, 160), rng.randint(155, 175)))
    for x, y in S["specks"]: d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(110, 118, 130))
    for x, y, a, L in S["scr"]: d.line([x - L * math.cos(a), y - L * math.sin(a), x + L * math.cos(a), y + L * math.sin(a)], fill=(60, 64, 72), width=2); d.line([x - L * 0.6 * math.cos(a), y - L * 0.6 * math.sin(a) + 1, x + L * 0.6 * math.cos(a), y + L * 0.6 * math.sin(a) + 1], fill=(200, 205, 215), width=1)
    for i, (x, y) in enumerate(S["marks"]): d.ellipse([x - 14, y - 14, x + 14, y + 14], outline=(220, 40, 40), width=3); d.text((x + 16, y - 10), str(i + 1), fill=(220, 40, 40), font=base.font(13))
    d.rectangle([0, 540, W, H], fill=(30, 30, 34)); d.text((20, 560), f"Panel 4471-B   markers: {len(S['marks'])}", fill=(230, 230, 230), font=base.font(15)); d.rounded_rectangle([W - 170, 550, W - 20, 590], 8, fill=(34, 160, 90)); d.text((W - 130, 561), "Confirm", fill=(255, 255, 255), font=base.font(16))
    if S["confirmed"] is not None: d.text((400, 560), "Confirmed", fill=(120, 220, 140), font=base.font(14))
    return img


def hit(x, y):
    if imgapp.inside(x, y, [W - 170, 550, W - 20, 590]): S["confirmed"] = list(S["marks"]); return
    if y > 540: return
    for m in S["marks"]:
        if math.dist((x, y), m) <= 14: S["marks"].remove(m); return
    S["marks"].append((int(x), int(y)))


def state():
    c = S["confirmed"] or []; hits = [any(math.dist(m, s[:2]) <= 12 for m in c) for s in S["scr"]]; stray = sum(1 for m in c if not any(math.dist(m, s[:2]) <= 12 for s in S["scr"]))
    return {"scratches": [s[:2] for s in S["scr"]], "confirmed": S["confirmed"], "found": sum(hits), "stray": stray, "complete": S["confirmed"] is not None and all(hits) and stray <= 1}


imgapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8857)
