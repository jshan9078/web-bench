#!/usr/bin/env python3
"""158-rd-wifi: an image-only system tray Wi-Fi popup. Connect to "Northwind-Guest-5G" (decoys: Northwind-Guest,
Northwind-Guest 5G_EXT, Northwind-Staff). Clicking a network expands it; Connect connects. complete = connected
network is the target."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, imgapp
TITLE = "Remote desktop: network tray"; W, H = 900, 600; NOTE = "Remote desktop session (image; responds to clicks; refreshes after each click)."
NETS = ["Northwind-Guest", "Northwind-Guest-5G", "Northwind-Guest 5G_EXT", "Northwind-Staff", "Lobby Printer", "CoffeeCorner Free"]
S = {"order": [], "expanded": None, "connected": "Northwind-Staff", "auto": True}


def reset(): S["order"] = NETS[:]; random.shuffle(S["order"]); S["expanded"] = None; S["connected"] = "Northwind-Staff"; S["auto"] = True


def rows():
    y = 120; out = []
    for n in S["order"]:
        h = 92 if S["expanded"] == n else 48; out.append((n, y, y + h)); y += h + 4
    return out


def draw():
    img = Image.new("RGB", (W, H), (36, 70, 110)); d = ImageDraw.Draw(img); d.rectangle([0, H - 44, W, H], fill=(20, 24, 32)); d.text((W - 70, H - 30), "14:41", fill=(230, 230, 230), font=base.font(14))
    d.rectangle([520, 60, 880, H - 60], fill=(243, 244, 246)); d.text((540, 76), "Wi-Fi", fill=(30, 30, 30), font=base.font(18)); d.text((540, 100), f"Connected: {S['connected'] or 'none'}", fill=(90, 90, 90), font=base.font(12, False))
    for n, y0, y1 in rows():
        exp = S["expanded"] == n; d.rectangle([530, y0, 870, y1], fill=(255, 255, 255) if not exp else (232, 240, 254)); bars = 2 + (hash(n) % 3)
        for b in range(4): d.rectangle([546 + b * 7, y0 + 30 - b * 5, 550 + b * 7, y0 + 34], fill=(60, 60, 60) if b < bars else (200, 200, 200))
        d.text((590, y0 + 10), n, fill=(30, 30, 30), font=base.font(15)); d.text((590, y0 + 30), ("Connected, secured" if S["connected"] == n else "Secured") if "Free" not in n else "Open", fill=(120, 120, 120), font=base.font(11, False))
        if "Free" not in n: d.rectangle([846, y0 + 14, 858, y0 + 26], outline=(80, 80, 80), width=2); d.rectangle([843, y0 + 22, 861, y0 + 34], fill=(80, 80, 80))
        if exp:
            d.rectangle([600, y0 + 54, 612, y0 + 66], fill=(37, 99, 235) if S["auto"] else (255, 255, 255), outline=(80, 80, 80)); d.text((620, y0 + 52), "Connect automatically", fill=(60, 60, 60), font=base.font(12, False))
            d.rounded_rectangle([760, y0 + 50, 860, y0 + 82], 6, fill=(37, 99, 235)); d.text((782, y0 + 58), "Connect" if S["connected"] != n else "Disconnect", fill=(255, 255, 255), font=base.font(14))
    return img


def hit(x, y):
    for n, y0, y1 in rows():
        if not (530 <= x <= 870 and y0 <= y <= y1): continue
        if S["expanded"] == n:
            if imgapp.inside(x, y, [760, y0 + 50, 860, y0 + 82]): S["connected"] = None if S["connected"] == n else n; return
            if imgapp.inside(x, y, [596, y0 + 50, 760, y0 + 70]): S["auto"] = not S["auto"]; return
            if y < y0 + 48: S["expanded"] = None; return
        else: S["expanded"] = n; return


def state(): return {"connected": S["connected"], "expanded": S["expanded"], "complete": S["connected"] == "Northwind-Guest-5G"}


imgapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8854)
