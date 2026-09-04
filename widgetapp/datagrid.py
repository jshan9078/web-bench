#!/usr/bin/env python3
"""252-keyboard-datagrid: an admin data grid (120 orders) with per-column filter boxes, keyboard row selection
(arrow keys move focus, Space toggles selection, Shift+Down extends) and a bulk action bar. Task: select every
order from a given customer with status Pending and mark them Shipped, without touching other orders.
complete = exactly those orders are Shipped."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
CUST = ["Acme Ltd", "Acme Ltd (EU)", "Birch & Co", "Cobalt Systems", "Delta Freight", "Evergreen Foods"]
S = {"orders": [], "target": ""}


def reset():
    S["orders"] = [{"id": 5000 + i, "customer": random.choice(CUST), "status": random.choice(["Pending", "Pending", "Shipped", "Cancelled"]), "total": round(random.uniform(20, 900), 2), "date": f"2026-08-{random.randint(1, 28):02d}"} for i in range(120)]
    S["target"] = "Acme Ltd"
    if sum(1 for o in S["orders"] if o["customer"] == "Acme Ltd" and o["status"] == "Pending") < 4:
        for o in random.sample([o for o in S["orders"] if o["customer"] == "Acme Ltd"], 4): o["status"] = "Pending"
    S["initial"] = json.loads(json.dumps(S["orders"]))


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"orders": S["orders"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__bulk":
        ids = set(int(x) for x in (data.get("ids") or [])); st = str(data.get("status"))
        for o in S["orders"]:
            if o["id"] in ids: o["status"] = st
        return (json.dumps({"ok": True, "n": len(ids)}), "application/json")
    return None


def state():
    want = {o["id"] for o in S["initial"] if o["customer"] == S["target"] and o["status"] == "Pending"}
    now = {o["id"]: o["status"] for o in S["orders"]}; init = {o["id"]: o["status"] for o in S["initial"]}
    ok = all(now[i] == "Shipped" for i in want) and all(now[i] == init[i] for i in now if i not in want)
    return {"target": S["target"], "want": sorted(want), "changed": sorted(i for i in now if now[i] != init[i]), "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Orders grid</title>
<style>body{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a}header{padding:10px 16px;background:#0f172a;color:#fff}main{max-width:1000px;margin:0 auto;padding:12px}#bar{display:flex;gap:10px;align-items:center;margin:8px 0}button,select,input{font:inherit;padding:5px 8px}
table{width:100%;border-collapse:collapse;background:#fff}th,td{padding:6px 10px;border-bottom:1px solid #e2e8f0;text-align:left}th input{width:95%;box-sizing:border-box}tr.row{cursor:default}tr.row:focus{outline:2px solid #2563eb;outline-offset:-2px}tr.sel{background:#dbeafe}.note{color:#64748b;font-size:13px}</style>
<header><b>Ledger Admin</b> &nbsp; Orders</header><main>
<p class=note>Filter with the boxes under each header. Keyboard: click a row or press Tab to focus the grid, ArrowUp/ArrowDown move, Space toggles selection, Shift+ArrowDown extends the selection, Escape clears. Bulk actions apply to selected rows.</p>
<div id=bar><span id=cnt></span><span id=selcnt style="margin-left:auto"></span><select id=st><option>Shipped</option><option>Cancelled</option><option>Pending</option></select><button id=apply>Apply status to selected</button><span id=msg style="color:#15803d"></span></div>
<table><thead><tr><th>Order<br><input data-k=id></th><th>Customer<br><input data-k=customer></th><th>Status<br><input data-k=status></th><th>Total<br><input data-k=total></th><th>Date<br><input data-k=date></th></tr></thead><tbody id=tb></tbody></table></main>
<script>(function(){var O=[],sel=new Set(),focus=-1,filt={};
function rows(){return O.filter(function(o){return Object.keys(filt).every(function(k){var f=filt[k].toLowerCase();return !f||String(o[k]).toLowerCase().indexOf(f)>=0})})}
function render(){var r=rows();document.getElementById('tb').innerHTML=r.map(function(o,i){return '<tr class="row '+(sel.has(o.id)?'sel':'')+'" tabindex=0 data-id="'+o.id+'" data-i="'+i+'"><td>'+o.id+'</td><td>'+o.customer+'</td><td>'+o.status+'</td><td>'+o.total.toFixed(2)+'</td><td>'+o.date+'</td></tr>'}).join('');document.getElementById('cnt').textContent=r.length+' of '+O.length+' orders';document.getElementById('selcnt').textContent=sel.size+' selected';
 document.querySelectorAll('tr.row').forEach(function(tr){tr.onclick=function(){focus=+tr.dataset.i;tr.focus()};tr.onkeydown=function(e){var r=rows(),i=+tr.dataset.i,id=+tr.dataset.id;if(e.key===' '){e.preventDefault();if(sel.has(id))sel.delete(id);else sel.add(id);render();refocus(i)}else if(e.key==='ArrowDown'){e.preventDefault();if(e.shiftKey){sel.add(id);if(r[i+1])sel.add(r[i+1].id)}if(r[i+1]){render();refocus(i+1)}}else if(e.key==='ArrowUp'){e.preventDefault();if(e.shiftKey){sel.add(id);if(r[i-1])sel.add(r[i-1].id)}if(r[i-1]){render();refocus(i-1)}}else if(e.key==='Escape'){sel.clear();render();refocus(i)}}});if(focus>=0)refocus(focus)}
function refocus(i){focus=i;var el=document.querySelector('tr.row[data-i="'+i+'"]');if(el)el.focus()}
document.querySelectorAll('th input').forEach(function(inp){inp.oninput=function(){filt[inp.dataset.k]=inp.value;focus=-1;render()}});
document.getElementById('apply').onclick=function(){fetch('/__bulk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ids:Array.from(sel),status:document.getElementById('st').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Updated '+j.n+' order(s)';sel.clear();fetch('/__data').then(r=>r.json()).then(function(d){O=d.orders;render()})})};
fetch('/__data').then(r=>r.json()).then(function(d){O=d.orders;render()})})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8914)
