#!/usr/bin/env python3
"""311-keyboard-only: an invoice list operated only by keys (j/k move the cursor, x toggles a mark, Enter submits
the marked set); no buttons, clicks are ignored. Mark exactly the overdue invoices above 500 and submit.
complete = submitted set equals the target set."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"rows": [], "submitted": None}
NAMES = ["Acme", "Birch", "Cobalt", "Delta", "Ember", "Fjord", "Granite", "Helix", "Iris", "Juniper", "Kestrel", "Lumen", "Maple", "Nimbus", "Orchid", "Pike"]


def reset():
    S["rows"] = [{"id": f"INV-{1040 + i}", "name": n, "amount": random.choice([120, 340, 480, 505, 620, 790, 1250, 2100]), "status": random.choice(["Paid", "Open", "Overdue", "Overdue"])} for i, n in enumerate(NAMES)]; S["submitted"] = None


def target(): return sorted(r["id"] for r in S["rows"] if r["status"] == "Overdue" and r["amount"] > 500)


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__rows": return (json.dumps(S["rows"]), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__submit": S["submitted"] = sorted(data.get("ids") or []); return (json.dumps({"ok": True, "n": len(S["submitted"])}), "application/json")
    return None


def state(): return {"target": target(), "submitted": S["submitted"], "complete": S["submitted"] is not None and S["submitted"] == target()}


def page():
    return """<!doctype html><meta charset=utf-8><title>Invoices (keyboard)</title><style>body{font:14px system-ui;margin:24px;background:#0f172a;color:#e2e8f0}table{border-collapse:collapse}td,th{padding:6px 14px;text-align:left}tr.cur td{outline:2px solid #38bdf8}tr.mk td:first-child::before{content:'\\2713 ';color:#4ade80}.Overdue{color:#f87171}#hint{color:#94a3b8;margin:10px 0}</style>
<h1 style="font-size:18px">Invoices</h1><div id=hint>Keyboard only: <b>j</b>/<b>k</b> move, <b>x</b> mark/unmark, <b>Enter</b> submit marked. Mouse clicks are ignored.</div><table id=t><thead><tr><th>Invoice</th><th>Customer</th><th>Amount</th><th>Status</th></tr></thead><tbody></tbody></table><div id=msg></div>
<script>(function(){var rows=[],cur=0,mk={};function draw(){var tb=document.querySelector('tbody');tb.innerHTML='';rows.forEach(function(r,i){var tr=document.createElement('tr');tr.className=(i===cur?'cur ':'')+(mk[r.id]?'mk':'');tr.innerHTML='<td>'+r.id+'</td><td>'+r.name+'</td><td>$'+r.amount.toFixed(2)+'</td><td class='+r.status+'>'+r.status+'</td>';tb.appendChild(tr)})}
fetch('/__rows').then(r=>r.json()).then(function(j){rows=j;draw()});
document.addEventListener('keydown',function(e){if(e.key==='j')cur=Math.min(rows.length-1,cur+1);else if(e.key==='k')cur=Math.max(0,cur-1);else if(e.key==='x')mk[rows[cur].id]=!mk[rows[cur].id];else if(e.key==='Enter'){var ids=Object.keys(mk).filter(function(k){return mk[k]});fetch('/__submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ids:ids})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted '+j.n+' invoice(s).'});return}else return;e.preventDefault();draw()});
document.addEventListener('click',function(e){e.preventDefault()},true);})();</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8949)
