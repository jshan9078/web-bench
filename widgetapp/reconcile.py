#!/usr/bin/env python3
"""83-reconcile-rule: a small parts catalogue whose Inventory list and per-part Detail pages disagree on
stock for some parts. A Data policy page states the precedence rule: the DETAIL page is authoritative when
its "last updated" is newer than the list's snapshot time, otherwise the LIST is. Task: for the named part,
report the authoritative stock count and press "Mark verified" on the authoritative page (each page has its
own button). complete = exactly one verify click, on the correct page for the target part."""
import json, random, sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
PARTS = ["Bearing 6203-2RS", "Hex bolt M8x40", "Relay 12V 30A", "O-ring 25x3", "Capacitor 470uF", "Fuse 10A blade", "Timing belt 120XL", "Thermistor 10k", "LED strip 5m", "Hose clamp 32mm"]
S = {"parts": [], "target": None, "verifies": [], "snapshot": None}


def reset():
    base_t = datetime.datetime(2026, 9, 3, 8, 0)
    S["snapshot"] = base_t + datetime.timedelta(hours=random.randint(1, 5))
    parts = []
    for i, n in enumerate(PARTS):
        list_stock = random.randint(3, 240); detail_stock = list_stock
        upd = S["snapshot"] + datetime.timedelta(minutes=random.choice([-200, -90, -30, 20, 75, 140]))
        if random.random() < 0.6: detail_stock = max(0, list_stock + random.choice([-17, -5, 4, 12, 31]))
        parts.append({"id": 100 + i, "name": n, "list_stock": list_stock, "detail_stock": detail_stock, "updated": upd})
    S["parts"] = parts; S["verifies"] = []
    cands = [p for p in parts if p["list_stock"] != p["detail_stock"]]
    S["target"] = random.choice(cands or parts)


def _auth(p): return "detail" if p["updated"] > S["snapshot"] else "list"
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__catalog":
        return (json.dumps({"snapshot": S["snapshot"].strftime("%Y-%m-%d %H:%M"), "parts": [{"id": p["id"], "name": p["name"], "list_stock": p["list_stock"], "detail_stock": p["detail_stock"], "updated": p["updated"].strftime("%Y-%m-%d %H:%M")} for p in S["parts"]]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__verify":
        S["verifies"].append({"id": data.get("id"), "page": data.get("page")}); return ('{"ok":true}', "application/json")
    return None


def state():
    t = S["target"]; auth = _auth(t)
    v = S["verifies"]
    return {"target": {"name": t["name"], "id": t["id"], "authoritative_page": auth, "stock": t["detail_stock"] if auth == "detail" else t["list_stock"],
                       "list_stock": t["list_stock"], "detail_stock": t["detail_stock"], "updated": t["updated"].strftime("%Y-%m-%d %H:%M"), "snapshot": S["snapshot"].strftime("%Y-%m-%d %H:%M")},
            "verifies": v, "complete": len(v) == 1 and v[0]["id"] == t["id"] and v[0]["page"] == auth}


def page():
    return r"""<!doctype html><meta charset=utf-8><title>Parts Catalogue</title>
<style>body{font:14px system-ui;margin:0;color:#222}nav{background:#1f2937;padding:10px 20px}nav a{color:#fff;margin-right:18px;text-decoration:none}main{max-width:820px;margin:20px auto;padding:0 16px}
table{width:100%;border-collapse:collapse}th,td{padding:8px 10px;border-bottom:1px solid #e5e7eb;text-align:left}a{color:#1d4ed8}button{font:inherit;padding:6px 12px;border:1px solid #888;border-radius:6px;background:#fff;cursor:pointer}.muted{color:#6b7280;font-size:13px}.ok{color:#047857}</style>
<nav><a href="#list">Inventory list</a><a href="#policy">Data policy</a></nav><main id=m></main>
<script>
var C=null;function esc(s){return String(s).replace(/</g,'&lt;')}
function route(){var h=location.hash||'#list';var m=document.getElementById('m');if(!C){m.textContent='Loading...';return}
 if(h==='#policy'){m.innerHTML='<h2>Data policy</h2><p>The inventory list is a periodic snapshot (its time is shown above the table). Part detail pages are updated individually and show their own "last updated" time.</p><p><b>Precedence:</b> when a part\'s detail page was updated AFTER the list snapshot, the detail page is authoritative for that part. Otherwise the inventory list is authoritative, even if the detail page shows a different number.</p><p>Verification must be recorded on the authoritative page for the part.</p>';return}
 if(h.startsWith('#part-')){var id=parseInt(h.slice(6));var p=C.parts.find(x=>x.id===id);if(!p){m.textContent='Not found';return}
  m.innerHTML='<p><a href="#list">← Inventory list</a></p><h2>'+esc(p.name)+'</h2><p>Stock on hand: <b>'+p.detail_stock+'</b></p><p class=muted>Last updated: '+p.updated+'</p><button id=vd>Mark verified (detail page)</button> <span id=vmsg class=ok></span>';
  document.getElementById('vd').onclick=function(){fetch('/__verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:p.id,page:'detail'})}).then(()=>{document.getElementById('vmsg').textContent='Verified on detail page.'})};return}
 var rows=C.parts.map(p=>'<tr><td><a href="#part-'+p.id+'">'+esc(p.name)+'</a></td><td>'+p.list_stock+'</td><td><button data-id="'+p.id+'">Mark verified (list)</button></td></tr>').join('');
 m.innerHTML='<h2>Inventory list</h2><p class=muted>Snapshot taken: '+C.snapshot+'</p><table><thead><tr><th>Part</th><th>Stock</th><th></th></tr></thead><tbody>'+rows+'</tbody></table><p id=vmsg class=ok></p>';
 m.querySelectorAll('button').forEach(b=>b.onclick=function(){fetch('/__verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:parseInt(this.dataset.id),page:'list'})}).then(()=>{document.getElementById('vmsg').textContent='Verified on list for part #'+this.dataset.id+'.'})})}
fetch('/__catalog').then(r=>r.json()).then(j=>{C=j;route()});window.addEventListener('hashchange',route);route();
</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8803)
