#!/usr/bin/env python3
"""102-admin-table: a customers table (240 rows, paginated, sortable, rows-per-page selector). The Balance
column's sort is a STRING sort (a common bug), so sorting descending puts "998.10" above "8431.20"; two
customers share a name. Task: the customer with the highest outstanding balance (name and id). Honest paths:
notice the sort is wrong and scan, or show all rows and check. complete = submitted id is the true maximum."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
FIRST = ["Acme Ltd", "Birch & Co", "Cobalt Systems", "Delta Freight", "Evergreen Foods", "Fulcrum Labs", "Granite Works", "Harbor Supply", "Ionic Media", "Juniper Health", "Kestrel Air", "Lumen Retail", "Meridian Bank", "Nimbus Cloud", "Orchid Studio", "Pioneer Tools", "Quartz Mining", "Ridge Outdoor", "Summit Legal", "Tidal Energy"]
S = {"rows": [], "answer": None, "submissions": []}


def reset():
    S["submissions"] = []; rows = []
    for i in range(240):
        rows.append({"id": f"C-{1001 + i}", "name": random.choice(FIRST) + random.choice(["", "", " (EU)", " Holdings", " Group"]), "city": random.choice(["Leeds", "Lyon", "Porto", "Gdansk", "Malmo", "Cork"]), "balance": round(random.uniform(5, 999), 2)})
    mx = random.randrange(240); rows[mx]["balance"] = round(random.uniform(8000, 8999), 2); rows[mx]["name"] = "Acme Ltd"
    dup = random.choice([k for k in range(240) if k != mx]); rows[dup]["name"] = "Acme Ltd"; rows[dup]["balance"] = round(random.uniform(990, 999), 2)
    for k in random.sample([k for k in range(240) if k not in (mx, dup)], 3): rows[k]["balance"] = round(random.uniform(990, 999.99), 2)
    S["rows"] = rows; S["answer"] = rows[mx]


def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("id") or "").strip().upper()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    a = S["answer"]; digits = lambda s: "".join(ch for ch in s if ch.isdigit())
    return {"answer": a, "string_sort_top": max(S["rows"], key=lambda r: f"{r['balance']:.2f}")["id"], "submissions": S["submissions"], "complete": any(digits(s) == digits(a["id"]) for s in S["submissions"])}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Customers, Ledger Admin</title>
<style>body{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a}header{padding:12px 24px;background:#0f172a;color:#fff}main{max-width:960px;margin:0 auto;padding:16px}
table{width:100%;border-collapse:collapse;background:#fff}th,td{padding:7px 10px;border-bottom:1px solid #e2e8f0;text-align:left}th{cursor:pointer;user-select:none;background:#f1f5f9}td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
#ctl{display:flex;gap:12px;align-items:center;margin:10px 0}select,button,input{font:inherit;padding:5px 8px}#ans{margin-top:16px;padding:12px;background:#fff;border:1px solid #e2e8f0;border-radius:8px}</style>
<header><b>Ledger Admin</b> &nbsp; Customers</header><main>
<div id=ctl><span id=info></span><span style="margin-left:auto">Rows per page <select id=pp><option>25</option><option>50</option><option>100</option><option value=240>All</option></select></span><button id=prev>Prev</button><span id=pg></span><button id=next>Next</button></div>
<table><thead><tr><th data-k=id>Customer id</th><th data-k=name>Name</th><th data-k=city>City</th><th data-k=balance class=n>Outstanding balance</th></tr></thead><tbody id=tb></tbody></table>
<div id=ans><b>Highest outstanding balance:</b> <label>Customer id <input id=cid size=10></label> <button id=go>Submit</button> <span id=msg></span></div></main>
<script>(function(){var ROWS=__ROWS__,key='id',dir=1,page=0,per=25;
function sorted(){var r=ROWS.slice();r.sort(function(a,b){var x=String(a[key]),y=String(b[key]);return (x<y?-1:x>y?1:0)*dir});return r}   // string compare on every column (bug: balance)
function render(){var r=sorted(),n=Math.ceil(r.length/per);page=Math.min(page,n-1);var s=r.slice(page*per,(page+1)*per);
 document.getElementById('tb').innerHTML=s.map(function(c){return '<tr><td>'+c.id+'</td><td>'+c.name+'</td><td>'+c.city+'</td><td class=n>'+c.balance.toFixed(2)+'</td></tr>'}).join('');
 document.getElementById('pg').textContent='Page '+(page+1)+' of '+n;document.getElementById('info').textContent=ROWS.length+' customers, sorted by '+key+(dir>0?' ascending':' descending')}
document.querySelectorAll('th').forEach(function(th){th.onclick=function(){var k=th.dataset.k;if(k===key)dir=-dir;else{key=k;dir=1}render()}});
document.getElementById('pp').onchange=function(){per=+this.value;page=0;render()};document.getElementById('prev').onclick=function(){page=Math.max(0,page-1);render()};document.getElementById('next').onclick=function(){page++;render()};
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:document.getElementById('cid').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
render()})();</script>"""


def page(): return PAGE.replace("__ROWS__", json.dumps(S["rows"]))


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8822)
