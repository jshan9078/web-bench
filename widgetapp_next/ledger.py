#!/usr/bin/env python3
"""84-ledger-audit: a scanned-style expense ledger rendered as an IMAGE (no DOM text): 30 rows x 4 amount
columns (Q1..Q4) plus a row label. Task: find the vendor with the highest Q3 amount, the vendor with the
lowest Q1 amount, and the exact TOTAL of the Q4 column, and submit them in the form below the image.
Near-ties (two Q3 values within 1%), lookalike digits (3/8, 6/9, 1/7 in a slab font), and a 12 px face
make every figure count. complete = all three answers exact (vendor names exact, total exact)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
VENDORS = ["Abelard Supply", "Birchwood Freight", "Calder Print", "Dunmore Cleaning", "Ellery Catering", "Fenwick IT", "Gable Legal", "Harlow Media",
           "Ingram Tools", "Jessop Travel", "Kenway Packaging", "Larkin Security", "Marlowe Design", "Norbury Fuel", "Oakes Insurance", "Pellam Repairs",
           "Quarrie Audio", "Ransome Courier", "Selkirk Telecom", "Thorne Staffing", "Usher Analytics", "Verity Payroll", "Whitlock Signage", "Xander Foods",
           "Yeoman Uniforms", "Zeller Optics", "Ashby Storage", "Bramwell Water", "Corliss Labs", "Denholm Events"]
S = {"rows": [], "answers": {}, "submissions": []}


def reset():
    rows = []
    for v in VENDORS:
        rows.append({"vendor": v, "q": [round(random.uniform(120, 9800), 2) for _ in range(4)]})
    # near-tie at the top of Q3 and at the bottom of Q1; lookalike digits sprinkled in
    i, j = random.sample(range(30), 2); top = round(random.uniform(9000, 9800), 2); rows[i]["q"][2] = top; rows[j]["q"][2] = round(top - random.uniform(5, 60), 2)
    k, l = random.sample(range(30), 2); low = round(random.uniform(130, 300), 2); rows[k]["q"][0] = low; rows[l]["q"][0] = round(low + random.uniform(2, 15), 2)
    for r in random.sample(rows, 8):
        c = random.randint(0, 3); s = f"{r['q'][c]:.2f}".replace("3", "8", 1) if random.random() < 0.5 else f"{r['q'][c]:.2f}".replace("6", "9", 1)
        try: r["q"][c] = float(s)
        except ValueError: pass
    random.shuffle(rows); S["rows"] = rows; S["submissions"] = []
    S["answers"] = {"top_q3": max(rows, key=lambda r: r["q"][2])["vendor"], "low_q1": min(rows, key=lambda r: r["q"][0])["vendor"], "total_q4": round(sum(r["q"][3] for r in rows), 2)}


def render():
    W, H = 900, 30 * 22 + 70
    img = Image.new("RGB", (W, H), (249, 247, 242)); dr = ImageDraw.Draw(img)
    f = base.font(12, False); fb = base.font(12)
    dr.text((20, 12), "Expense ledger FY2026 (scanned)", fill=(60, 60, 60), font=base.font(14))
    dr.text((20, 38), "Vendor", fill=(90, 90, 90), font=fb)
    for c, x in enumerate((330, 470, 610, 750)): dr.text((x, 38), f"Q{c+1}", fill=(90, 90, 90), font=fb)
    dr.line([(20, 56), (880, 56)], fill=(150, 150, 150), width=1)
    for i, r in enumerate(S["rows"]):
        y = 64 + i * 22
        dr.text((20, y), r["vendor"], fill=(40, 40, 40), font=f)
        for c, x in enumerate((330, 470, 610, 750)):
            s = f"{r['q'][c]:,.2f}"; w = dr.textlength(s, font=f); dr.text((x + 90 - w, y), s, fill=(40, 40, 40), font=f)
        if i % 2: dr.line([(20, y + 19), (880, y + 19)], fill=(225, 222, 214), width=1)
    return base.png(img)


def page():
    return base.image_page("Expense Ledger", 900, 730, extra_html="""
<div style="position:absolute;top:740px;left:20px;font:14px system-ui;width:860px">
<p>Enter your findings (vendor names exactly as printed; total with two decimals):</p>
<label>Vendor with the highest Q3 amount <input id=a1 size=28></label><br><br>
<label>Vendor with the lowest Q1 amount <input id=a2 size=28></label><br><br>
<label>Total of the Q4 column <input id=a3 size=16></label><br><br>
<button id=go>Submit findings</button> <span id=msg></span>
<script>
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({top_q3:a1.value,low_q1:a2.value,total_q4:a3.value})}).then(r=>r.json()).then(j=>{document.getElementById('msg').textContent='Submitted ('+j.n+').'})}
</script></div>""")


def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append({k: str(data.get(k) or "").strip() for k in ("top_q3", "low_q1", "total_q4")}); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    a = S["answers"]; ok = False
    for s in S["submissions"]:
        try: tot = float(s["total_q4"].replace(",", ""))
        except ValueError: tot = None
        if s["top_q3"].strip().lower() == a["top_q3"].lower() and s["low_q1"].strip().lower() == a["low_q1"].lower() and tot is not None and abs(tot - a["total_q4"]) < 0.005: ok = True
    return {"answers": a, "submissions": S["submissions"], "complete": ok}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8804)
