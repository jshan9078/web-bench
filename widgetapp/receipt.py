#!/usr/bin/env python3
"""104-receipt-total: a photographed restaurant receipt (rotated, noisy) with a printed pre-tip total, a printed
"suggested tip" line, and a HANDWRITTEN tip and total. Task: the amount actually charged including tip.
complete = submitted amount within 0.01 of the handwritten total."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import base
ITEMS = [("Margherita pizza", 16.5), ("Caesar salad", 12.0), ("Grilled salmon", 27.0), ("Ribeye 12oz", 38.0), ("Fries", 6.5), ("Sparkling water", 4.0), ("Lemonade", 4.5), ("Tiramisu", 9.0), ("Espresso", 3.5), ("House red (glass)", 11.0)]
S = {"items": [], "subtotal": 0, "tax": 0, "total": 0, "tip": 0, "grand": 0, "submissions": []}


def reset():
    S["submissions"] = []; items = random.sample(ITEMS, random.randint(4, 6)); S["items"] = [(n, p, random.choice([1, 1, 1, 2])) for n, p in items]
    sub = round(sum(p * q for _, p, q in S["items"]), 2); tax = round(sub * 0.08875, 2); tot = round(sub + tax, 2)
    tip = round(random.choice([0.15, 0.18, 0.2, 0.22]) * sub + random.choice([-0.4, 0.0, 0.35, 1.0]), 2); tip = round(tip, 0) if random.random() < 0.5 else tip
    S.update(subtotal=sub, tax=tax, total=tot, tip=tip, grand=round(tot + tip, 2))


def hand_font(size):
    for p in ("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf", "/System/Library/Fonts/Supplemental/Noteworthy.ttc", "/System/Library/Fonts/Supplemental/Comic Sans MS.ttf", "/System/Library/Fonts/Supplemental/Chalkboard.ttc"):
        try:
            from PIL import ImageFont; return ImageFont.truetype(p, size)
        except Exception: continue
    return base.font(size)


def mono(size):
    from PIL import ImageFont
    for p in ("/System/Library/Fonts/Supplemental/Courier New.ttf", "/System/Library/Fonts/Menlo.ttc"):
        try: return ImageFont.truetype(p, size)
        except Exception: continue
    return base.font(size, False)


def render():
    rw, rh = 400, 760; r = Image.new("RGB", (rw, rh), (247, 246, 240)); d = ImageDraw.Draw(r); f = mono(15); fb = mono(17); y = 24
    for ln in ["      TRATTORIA MARCO", "    412 Harbor St, Brooklyn", "    Tel (718) 555-0142", "", "  Table 7      Server: Dana", "  Guests 2     09/01/26 20:14", "  --------------------------------"]:
        d.text((16, y), ln, fill=(40, 40, 40), font=f); y += 20
    for n, p, q in S["items"]:
        d.text((16, y), f"  {q} x {n[:20]:<20}{p * q:>8.2f}", fill=(40, 40, 40), font=f); y += 20
    y += 6
    for lab, v in [("Subtotal", S["subtotal"]), ("Tax 8.875%", S["tax"])]:
        d.text((16, y), f"  {lab:<24}{v:>8.2f}", fill=(40, 40, 40), font=f); y += 20
    d.text((16, y), f"  {'TOTAL':<24}{S['total']:>8.2f}", fill=(20, 20, 20), font=fb); y += 30
    d.text((16, y), "  --------------------------------", fill=(40, 40, 40), font=f); y += 20
    d.text((16, y), f"  Suggested tip 18%: {S['subtotal'] * 0.18:>7.2f}", fill=(80, 80, 80), font=f); y += 20
    d.text((16, y), f"  Suggested tip 20%: {S['subtotal'] * 0.20:>7.2f}", fill=(80, 80, 80), font=f); y += 34
    d.text((16, y), "  TIP:   ______________", fill=(40, 40, 40), font=fb); hf = hand_font(30)
    d.text((150, y - 14), f"{S['tip']:.2f}" if S["tip"] != int(S["tip"]) else f"{int(S['tip'])}.00", fill=(20, 40, 140), font=hf); y += 40
    d.text((16, y), "  TOTAL: ______________", fill=(40, 40, 40), font=fb); d.text((150, y - 14), f"{S['grand']:.2f}", fill=(20, 40, 140), font=hf); y += 44
    d.text((16, y), "  X ", fill=(40, 40, 40), font=fb); d.text((60, y - 16), "D. Ferreira", fill=(20, 40, 140), font=hand_font(28)); y += 40
    d.text((16, y), "  Thank you! Come again.", fill=(40, 40, 40), font=f)
    # photo effects: rotation, noise, blur, vignette-ish background
    r = r.rotate(random.Random(S["subtotal"]).uniform(-8, -4), expand=True, fillcolor=(110, 105, 98), resample=Image.BICUBIC)
    bg = Image.new("RGB", (900, 900), (110, 105, 98)); bg.paste(r, ((900 - r.width) // 2, (900 - r.height) // 2))
    px = bg.load(); rng = random.Random(1)
    for _ in range(30000):
        x, y = rng.randrange(900), rng.randrange(900); c = px[x, y]; k = rng.randint(-14, 14); px[x, y] = (max(0, min(255, c[0] + k)), max(0, min(255, c[1] + k)), max(0, min(255, c[2] + k)))
    return base.png(bg.filter(ImageFilter.GaussianBlur(0.5)))


def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("amount") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    ok = False
    for s in S["submissions"]:
        try: ok = ok or abs(float(s.replace("$", "").replace(",", "")) - S["grand"]) < 0.01
        except ValueError: pass
    return {"printed_total": S["total"], "tip": S["tip"], "answer": S["grand"], "submissions": S["submissions"], "complete": ok}


def page():
    return base.image_page("Expense receipt", 900, 900, extra_html="""
<div style="position:absolute;top:910px;left:20px;font:14px system-ui"><label>Amount charged including tip ($): <input id=a size=10></label> <button id=go>Submit</button> <span id=msg></span>
<script>document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({amount:document.getElementById('a').value})}).then(r=>r.json()).then(j=>{document.getElementById('msg').textContent='Submitted ('+j.n+').'})}</script></div>""")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8824)
