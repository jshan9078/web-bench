#!/usr/bin/env python3
"""85-table-diff: two dense 10x8 tables rendered as images, "Monday" and "Tuesday" snapshots of a
price/stock sheet. Exactly five cells changed. Task: list the changed cells (row label + column) and,
for each, the Tuesday value. Each cell is a 12 px figure; lookalike digits and one change in the last
decimal make skimming fail. complete = the submitted set of changed cells equals the true set and the
Tuesday values match."""
import json, random, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base
ROWS = ["Almond", "Basil", "Cumin", "Dill", "Fennel", "Ginger", "Juniper", "Mace", "Nutmeg", "Saffron"]
COLS = ["Bin A", "Bin B", "Bin C", "Bin D", "Price", "Reorder", "Lead d", "Grade"]
S = {"mon": [], "tue": [], "changes": [], "submissions": []}


def reset():
    mon = [[round(random.uniform(1, 99), 1) if c < 4 else (round(random.uniform(2, 40), 2) if c == 4 else (random.randint(5, 60) if c == 5 else (random.randint(2, 21) if c == 6 else random.choice([1, 2, 3])))) for c in range(8)] for _ in range(10)]
    tue = [row[:] for row in mon]
    cells = random.sample([(r, c) for r in range(10) for c in range(8)], 5); changes = []
    for n, (r, c) in enumerate(cells):
        v = mon[r][c]
        if n == 0 and isinstance(v, float): nv = round(v + 0.1, 1 if c < 4 else 2)      # last-decimal change
        elif isinstance(v, float): nv = round(v * random.choice([0.9, 1.1, 1.25]), 1 if c < 4 else 2)
        else: nv = v + random.choice([-2, -1, 1, 3])
        if nv == v: nv = v + (0.2 if isinstance(v, float) else 1)
        tue[r][c] = nv; changes.append({"row": ROWS[r], "col": COLS[c], "tue": nv})
    S["mon"], S["tue"], S["changes"], S["submissions"] = mon, tue, changes, []


def _table(dr, x0, y0, title, data):
    f = base.font(12, False); fb = base.font(12)
    dr.text((x0, y0), title, fill=(60, 60, 60), font=base.font(14)); y0 += 24
    dr.text((x0, y0), "", font=fb)
    for c, col in enumerate(COLS): dr.text((x0 + 70 + c * 46, y0), col, fill=(90, 90, 90), font=fb)
    for r, row in enumerate(data):
        y = y0 + 20 + r * 20
        dr.text((x0, y), ROWS[r], fill=(40, 40, 40), font=f)
        for c, v in enumerate(row):
            s = f"{v:.1f}" if (c < 4) else (f"{v:.2f}" if c == 4 else str(v)); w = dr.textlength(s, font=f); dr.text((x0 + 70 + c * 46 + 40 - w, y), s, fill=(40, 40, 40), font=f)


def render():
    img = Image.new("RGB", (900, 560), (250, 250, 250)); dr = ImageDraw.Draw(img)
    _table(dr, 20, 12, "Monday snapshot", S["mon"]); _table(dr, 20, 292, "Tuesday snapshot", S["tue"])
    return base.png(img)


def page():
    return base.image_page("Stock Sheet Audit", 900, 560, extra_html="""
<div style="position:absolute;top:570px;left:20px;font:14px system-ui;width:860px">
<p>List every cell that changed between Monday and Tuesday, one per line as <code>Row, Column, TuesdayValue</code> (e.g. <code>Basil, Bin C, 47.3</code>):</p>
<textarea id=t rows=7 cols=60></textarea><br><button id=go>Submit audit</button> <span id=msg></span>
<script>
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t.value})}).then(r=>r.json()).then(j=>{document.getElementById('msg').textContent='Submitted ('+j.n+').'})}
</script></div>""")


def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("text") or "")); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def _parse(text):
    """Triples 'Row, Column, Value' anywhere in the text: line breaks are optional, because typing a
    newline into a textarea depends on the agent's tooling and must not decide the verdict."""
    out = set()
    rows = "|".join(re.escape(r) for r in ROWS); cols = "|".join(re.escape(c) for c in COLS)
    for m in re.finditer(rf"({rows})\s*,\s*({cols})\s*,\s*(-?\d+(?:\.\d+)?)", text, re.I):
        out.add((m.group(1).lower(), m.group(2).lower(), round(float(m.group(3)), 2)))
    return out


def state():
    truth = {(c["row"].lower(), c["col"].lower(), round(float(c["tue"]), 2)) for c in S["changes"]}
    ok = any(_parse(s) == truth for s in S["submissions"])
    return {"changes": S["changes"], "submissions": S["submissions"], "complete": ok}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8805)
