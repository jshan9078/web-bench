#!/usr/bin/env python3
"""157-kiosk-order: a self-service food kiosk rendered as an image. Order exactly 2 Veggie Wrap and 1 Lemonade,
decline the upsell, place the order. Decoys: Veggie Bowl, Limeade. complete = placed order matches exactly and
the upsell was declined."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, imgapp
TITLE = "Order kiosk"; W, H = 900, 640; NOTE = "Self-service kiosk (image; it responds to clicks and refreshes after each click)."
ITEMS = [("Veggie Wrap", 8.5), ("Veggie Bowl", 9.0), ("Chicken Wrap", 9.5), ("Lemonade", 3.0), ("Limeade", 3.0), ("Iced Tea", 2.5)]
S = {"cart": {}, "screen": "menu", "upsell": None, "placed": None, "order": []}


def reset(): S["cart"] = {n: 0 for n, _ in ITEMS}; S["screen"] = "menu"; S["upsell"] = None; S["placed"] = None; S["order"] = ITEMS[:]; random.shuffle(S["order"])


def cell(i): r, c = divmod(i, 3); return 30 + c * 280, 90 + r * 200


def draw():
    img = Image.new("RGB", (W, H), (250, 247, 240)); d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 60], fill=(180, 40, 40)); d.text((24, 18), "Harbor Deli, order here", fill=(255, 255, 255), font=base.font(22))
    if S["screen"] == "menu":
        for i, (n, p) in enumerate(S["order"]):
            x, y = cell(i); d.rounded_rectangle([x, y, x + 250, y + 170], 12, fill=(255, 255, 255), outline=(220, 215, 205)); d.rectangle([x + 16, y + 14, x + 234, y + 80], fill=[(200, 230, 180), (230, 200, 150), (240, 220, 180), (250, 240, 150), (200, 240, 160), (220, 200, 170)][ITEMS.index((n, p))])
            d.text((x + 16, y + 92), n, fill=(30, 30, 30), font=base.font(17)); d.text((x + 16, y + 116), f"${p:.2f}", fill=(90, 90, 90), font=base.font(14, False))
            d.rounded_rectangle([x + 150, y + 118, x + 180, y + 148], 6, fill=(235, 235, 235)); d.text((x + 160, y + 124), "-", fill=(30, 30, 30), font=base.font(18))
            d.text((x + 190, y + 124), str(S["cart"][n]), fill=(30, 30, 30), font=base.font(18)); d.rounded_rectangle([x + 208, y + 118, x + 238, y + 148], 6, fill=(180, 40, 40)); d.text((x + 217, y + 123), "+", fill=(255, 255, 255), font=base.font(18))
        tot = sum(S["cart"][n] * p for n, p in ITEMS); d.rectangle([0, H - 60, W, H], fill=(40, 40, 44)); d.text((24, H - 40), f"Items: {sum(S['cart'].values())}   Total: ${tot:.2f}", fill=(255, 255, 255), font=base.font(16)); d.rounded_rectangle([W - 200, H - 50, W - 24, H - 10], 8, fill=(34, 160, 90)); d.text((W - 160, H - 40), "Checkout", fill=(255, 255, 255), font=base.font(17))
    elif S["screen"] == "upsell":
        d.rounded_rectangle([150, 150, 750, 470], 16, fill=(255, 255, 255), outline=(220, 215, 205)); d.text((190, 190), "Add a chocolate cookie for $1.00?", fill=(30, 30, 30), font=base.font(24)); d.text((190, 240), "Most customers add one.", fill=(120, 120, 120), font=base.font(14, False))
        d.rounded_rectangle([190, 330, 430, 400], 10, fill=(180, 40, 40)); d.text((250, 352), "Yes, add cookie", fill=(255, 255, 255), font=base.font(18)); d.rounded_rectangle([470, 330, 710, 400], 10, fill=(235, 235, 235)); d.text((550, 352), "No thanks", fill=(30, 30, 30), font=base.font(18))
    elif S["screen"] == "review":
        d.text((40, 90), "Review your order", fill=(30, 30, 30), font=base.font(22)); y = 140
        for n, p in ITEMS:
            if S["cart"][n]: d.text((40, y), f"{S['cart'][n]} x {n}", fill=(30, 30, 30), font=base.font(17, False)); d.text((500, y), f"${S['cart'][n] * p:.2f}", fill=(30, 30, 30), font=base.font(17, False)); y += 32
        if S["upsell"]: d.text((40, y), "1 x Chocolate cookie", fill=(30, 30, 30), font=base.font(17, False)); d.text((500, y), "$1.00", fill=(30, 30, 30), font=base.font(17, False)); y += 32
        d.rounded_rectangle([40, 520, 300, 580], 10, fill=(235, 235, 235)); d.text((110, 540), "Back to menu", fill=(30, 30, 30), font=base.font(17)); d.rounded_rectangle([600, 520, 860, 580], 10, fill=(34, 160, 90)); d.text((680, 540), "Place order", fill=(255, 255, 255), font=base.font(17))
    else:
        d.text((40, 200), f"Order #{S['placed']['num']} placed. Thank you!", fill=(30, 30, 30), font=base.font(26))
    return img


def hit(x, y):
    if S["screen"] == "menu":
        for i, (n, p) in enumerate(S["order"]):
            cx, cy = cell(i)
            if imgapp.inside(x, y, [cx + 150, cy + 118, cx + 180, cy + 148]): S["cart"][n] = max(0, S["cart"][n] - 1)
            if imgapp.inside(x, y, [cx + 208, cy + 118, cx + 238, cy + 148]): S["cart"][n] += 1
        if imgapp.inside(x, y, [W - 200, H - 50, W - 24, H - 10]) and sum(S["cart"].values()): S["screen"] = "upsell"
    elif S["screen"] == "upsell":
        if imgapp.inside(x, y, [190, 330, 430, 400]): S["upsell"] = True; S["screen"] = "review"
        if imgapp.inside(x, y, [470, 330, 710, 400]): S["upsell"] = False; S["screen"] = "review"
    elif S["screen"] == "review":
        if imgapp.inside(x, y, [40, 520, 300, 580]): S["screen"] = "menu"
        if imgapp.inside(x, y, [600, 520, 860, 580]): S["placed"] = {"num": random.randint(100, 999), "cart": dict(S["cart"]), "upsell": S["upsell"]}; S["screen"] = "done"


def state():
    want = {n: 0 for n, _ in ITEMS}; want["Veggie Wrap"] = 2; want["Lemonade"] = 1; p = S["placed"]
    return {"cart": S["cart"], "screen": S["screen"], "placed": p, "complete": p is not None and p["cart"] == want and p["upsell"] is False}


imgapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8853)
