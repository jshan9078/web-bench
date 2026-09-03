#!/usr/bin/env python3
"""171-spreadsheet-grid: a keyboard-driven spreadsheet grid (click a cell or use arrow keys; type to edit; Enter
commits; formulas =SUM(range) and =A1*B1 supported). Task: fix a mistyped label, enter a formula in the total
cell, and set a unit price, then Save. complete = saved cells match (formula result and text)."""
import json, random, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"cells": {}, "saved": None, "target": {}}
COLS = "ABCD"; ROWS = 8


def reset():
    items = [("Widgets", 12, 3.5), ("Gadgets", 5, 12.0), ("Cables", 40, 1.25), ("Adapters", 7, 9.0), ("Batteres", 24, 0.8)]
    cells = {"A1": "Item", "B1": "Qty", "C1": "Unit price", "D1": "Line total"}
    for i, (n, q, p) in enumerate(items, start=2): cells[f"A{i}"] = n; cells[f"B{i}"] = str(q); cells[f"C{i}"] = f"{p:.2f}"; cells[f"D{i}"] = f"=B{i}*C{i}"
    cells["A7"] = "Total"; S["cells"] = cells; S["saved"] = None
    S["target"] = {"A6": "Batteries", "C4": "1.40", "D7": "=SUM(D2:D6)"}


def value(ref, depth=0):
    v = S["cells"].get(ref, "")
    if not v.startswith("=") or depth > 5: return v
    expr = v[1:].upper()
    m = re.match(r"SUM\(([A-D])(\d+):([A-D])(\d+)\)$", expr)
    try:
        if m:
            c1, r1, c2, r2 = m.groups(); tot = 0.0
            for c in COLS[COLS.index(c1):COLS.index(c2) + 1]:
                for r in range(int(r1), int(r2) + 1): tot += float(value(f"{c}{r}", depth + 1) or 0)
            return f"{tot:.2f}"
        expr2 = re.sub(r"[A-D]\d+", lambda mm: str(float(value(mm.group(0), depth + 1) or 0)), expr)
        if re.fullmatch(r"[0-9.+\-*/() ]+", expr2): return f"{eval(expr2):.2f}"
    except Exception: pass
    return "#ERR"


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"cells": S["cells"], "values": {k: value(k) for k in S["cells"]}}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__set":
        ref = str(data.get("ref") or "").upper(); val = str(data.get("value") or "")
        if re.fullmatch(r"[A-D][1-8]", ref):
            if val == "": S["cells"].pop(ref, None)
            else: S["cells"][ref] = val
        return (json.dumps({"values": {k: value(k) for k in S["cells"]}}), "application/json")
    if path == "/__save": S["saved"] = dict(S["cells"]); return (json.dumps({"ok": True}), "application/json")
    return None


def state():
    sv = S["saved"] or {}; ok = False
    if S["saved"]:
        cur = S["cells"]; S["cells"] = sv
        try:
            total = value("D7"); expect = sum(float(value(f"B{i}")) * float(value(f"C{i}")) for i in range(2, 7))
            ok = sv.get("A6") == "Batteries" and value("C4") == "1.40" and sv.get("D7", "").upper().replace(" ", "") == "=SUM(D2:D6)" and abs(float(total) - expect) < 0.01 and all(sv.get(k) == S["cells"].get(k) for k in [])
        except Exception: ok = False
        S["cells"] = cur
    return {"target": S["target"], "saved": S["saved"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Sheet: September order</title>
<style>body{font:14px system-ui;margin:0;background:#fff;color:#111}header{padding:10px 16px;border-bottom:1px solid #e5e7eb;display:flex;gap:14px;align-items:center}#fx{font:13px ui-monospace,Menlo,monospace;padding:6px 8px;border:1px solid #d1d5db;border-radius:4px;width:420px}
table{border-collapse:collapse;margin:16px}td,th{border:1px solid #d1d5db;min-width:110px;height:26px;padding:0 6px;text-align:left;font-size:13px}th{background:#f3f4f6;font-weight:600;text-align:center;width:36px}td.sel{outline:2px solid #2563eb;outline-offset:-2px}td.num{text-align:right}
td input{width:100%;box-sizing:border-box;font:inherit;border:0;outline:0;background:#fff}button{font:inherit;padding:6px 12px}.note{color:#6b7280;font-size:12px;margin:0 16px}</style>
<header><b>September order</b><span id=ref>A1</span><input id=fx aria-label="Formula bar" readonly><button id=save>Save</button><span id=msg style="color:#15803d"></span></header>
<p class=note>Click a cell or move with the arrow keys; start typing to edit (Enter commits, Escape cancels). Formulas: =B2*C2, =SUM(D2:D6).</p>
<table id=grid></table>
<script>(function(){var cells={},vals={},sel='A1',editing=null;var COLS='ABCD',ROWS=8;
function load(){fetch('/__data').then(r=>r.json()).then(function(j){cells=j.cells;vals=j.values;render()})}
function render(){var t=document.getElementById('grid'),h='<tr><th></th>';COLS.split('').forEach(function(c){h+='<th>'+c+'</th>'});h+='</tr>';
 for(var r=1;r<=ROWS;r++){h+='<tr><th>'+r+'</th>';COLS.split('').forEach(function(c){var ref=c+r,v=vals[ref]!==undefined?vals[ref]:'';h+='<td tabindex=0 data-ref="'+ref+'" class="'+(ref===sel?'sel ':'')+(/^-?\d+(\.\d+)?$/.test(v)?'num':'')+'">'+(editing===ref?'<input id=ed value="'+(cells[ref]||'').replace(/"/g,'&quot;')+'">':v)+'</td>'});h+='</tr>'}
 t.innerHTML=h;document.getElementById('ref').textContent=sel;document.getElementById('fx').value=cells[sel]||'';
 t.querySelectorAll('td').forEach(function(td){td.onclick=function(){if(editing&&editing!==td.dataset.ref)commit();sel=td.dataset.ref;render();focusSel()};td.ondblclick=function(){editing=td.dataset.ref;render();var e=document.getElementById('ed');e.focus()}});
 var ed=document.getElementById('ed');if(ed){ed.focus();ed.onkeydown=function(e){if(e.key==='Enter'){e.preventDefault();commit();move(0,1)}else if(e.key==='Escape'){editing=null;render();focusSel()}else if(e.key==='Tab'){e.preventDefault();commit();move(1,0)}}}}
function focusSel(){var el=document.querySelector('td[data-ref="'+sel+'"]');if(el)el.focus()}
function commit(){var e=document.getElementById('ed');if(!e){editing=null;return}var ref=editing,val=e.value;editing=null;fetch('/__set',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ref:ref,value:val})}).then(r=>r.json()).then(function(j){if(val==='')delete cells[ref];else cells[ref]=val;vals=j.values;render();focusSel()})}
function move(dc,dr){var c=COLS.indexOf(sel[0])+dc,r=parseInt(sel.slice(1))+dr;if(c<0||c>=COLS.length||r<1||r>ROWS)return;sel=COLS[c]+r;render();focusSel()}
document.addEventListener('keydown',function(e){if(editing)return;if(e.target.id==='fx')return;if(e.key==='ArrowLeft'){e.preventDefault();move(-1,0)}else if(e.key==='ArrowRight'){e.preventDefault();move(1,0)}else if(e.key==='ArrowUp'){e.preventDefault();move(0,-1)}else if(e.key==='ArrowDown'){e.preventDefault();move(0,1)}else if(e.key==='Enter'||e.key==='F2'){e.preventDefault();editing=sel;render()}else if(e.key==='Delete'||e.key==='Backspace'){e.preventDefault();editing=sel;render();document.getElementById('ed').value=''}else if(e.key.length===1&&!e.ctrlKey&&!e.metaKey){editing=sel;render();var ed=document.getElementById('ed');ed.value='';}});
document.getElementById('save').onclick=function(){if(editing)commit();fetch('/__save',{method:'POST'}).then(function(){document.getElementById('msg').textContent='Saved'})};
load()})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8859)
