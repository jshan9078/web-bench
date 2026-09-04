#!/usr/bin/env python3
"""256-helpdesk-escalate: a support ticket queue (40 tickets, list with filters and a detail pane with a
conversation). Task: find the oldest OPEN ticket from a Gold-tier customer that mentions a refund and has no
agent reply yet, set its priority to High, assign it to Dana, add an internal note "Escalated per refund
policy", and change its status to Escalated. complete = exactly that ticket changed as required."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
CUST = [("Acme Ltd", "Gold"), ("Birch & Co", "Silver"), ("Cobalt Systems", "Gold"), ("Delta Freight", "Bronze"), ("Evergreen Foods", "Gold"), ("Harbor Supply", "Silver")]
SUBJ = ["Login loop on mobile", "Refund for duplicate charge", "Invoice mismatch", "Feature request: exports", "Refund request, order 4471", "Slow dashboard", "Password reset failing", "Refund not received"]
S = {"tickets": [], "target": None, "log": []}


def reset():
    ts = []; base_day = 1
    for i in range(40):
        c = random.choice(CUST); subj = random.choice(SUBJ); msgs = [{"who": "customer", "text": f"{subj}. Please advise."}]
        if random.random() < 0.5: msgs.append({"who": "agent", "text": "Thanks, looking into it."})
        ts.append({"id": 7000 + i, "customer": c[0], "tier": c[1], "subject": subj, "status": random.choice(["Open", "Open", "Pending", "Closed"]), "priority": "Normal", "assignee": "", "created": f"2026-08-{random.randint(1, 28):02d} {random.randint(8, 18):02d}:{random.randint(0, 59):02d}", "msgs": msgs, "notes": []})
    cands = [t for t in ts if t["tier"] == "Gold" and t["status"] == "Open" and "refund" in t["subject"].lower() and len(t["msgs"]) == 1]
    if len(cands) < 2:
        for t in random.sample(ts, 3): t.update(tier="Gold", status="Open", subject="Refund request, order 5510", msgs=[{"who": "customer", "text": "Refund request, order 5510. Please advise."}])
        cands = [t for t in ts if t["tier"] == "Gold" and t["status"] == "Open" and "refund" in t["subject"].lower() and len(t["msgs"]) == 1]
    S["tickets"] = ts; S["target"] = min(cands, key=lambda t: t["created"])["id"]; S["log"] = []; S["initial"] = json.loads(json.dumps(ts))


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"tickets": S["tickets"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__act":
        tid = int(data.get("id")); t = next(x for x in S["tickets"] if x["id"] == tid); S["log"].append(dict(data))
        for k in ("status", "priority", "assignee"):
            if k in data: t[k] = str(data[k])
        if data.get("note"): t["notes"].append(str(data["note"]))
        return (json.dumps({"ok": True}), "application/json")
    return None


def state():
    tg = next(x for x in S["tickets"] if x["id"] == S["target"]); others_ok = all(json.dumps({k: v for k, v in a.items() if k != "notes"}) == json.dumps({k: v for k, v in b.items() if k != "notes"}) and a["notes"] == b["notes"] for a, b in zip(S["initial"], S["tickets"]) if a["id"] != S["target"])
    ok = others_ok and tg["priority"] == "High" and tg["assignee"] == "Dana" and tg["status"] == "Escalated" and any("escalated per refund policy" in n.lower() for n in tg["notes"])
    return {"target": S["target"], "ticket": tg, "others_untouched": others_ok, "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Helpdesk</title>
<style>body{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a;display:grid;grid-template-columns:460px 1fr;height:100vh}#l{border-right:1px solid #e2e8f0;overflow:auto}#f{padding:10px;display:flex;gap:6px;flex-wrap:wrap;background:#fff;border-bottom:1px solid #e2e8f0}input,select,button,textarea{font:inherit;padding:5px 7px}
table{width:100%;border-collapse:collapse}td,th{padding:6px 8px;border-bottom:1px solid #f1f5f9;text-align:left;font-size:13px}th{cursor:pointer;background:#f1f5f9}tr.t{cursor:pointer}tr.on{background:#eff6ff}#d{padding:16px;overflow:auto}.m{border:1px solid #e2e8f0;border-radius:8px;padding:8px;margin:6px 0}.m.agent{background:#f1f5f9}label{display:block;margin:6px 0}</style>
<div id=l><div id=f><input id=q placeholder="Search subject/customer" size=22><select id=fs><option value="">Any status</option><option>Open</option><option>Pending</option><option>Closed</option><option>Escalated</option></select><select id=ft><option value="">Any tier</option><option>Gold</option><option>Silver</option><option>Bronze</option></select></div>
<table><thead><tr><th data-k=id>#</th><th data-k=customer>Customer</th><th data-k=tier>Tier</th><th data-k=subject>Subject</th><th data-k=status>Status</th><th data-k=created>Created</th></tr></thead><tbody id=tb></tbody></table></div>
<div id=d><p style="color:#64748b">Select a ticket.</p></div>
<script>(function(){var T=[],cur=null,key='created',dir=1;
function load(){fetch('/__data').then(r=>r.json()).then(function(j){T=j.tickets;render();if(cur)detail()})}
function rows(){var q=document.getElementById('q').value.toLowerCase(),fs=document.getElementById('fs').value,ft=document.getElementById('ft').value;return T.filter(function(t){return (!q||(t.subject+' '+t.customer).toLowerCase().indexOf(q)>=0)&&(!fs||t.status===fs)&&(!ft||t.tier===ft)}).sort(function(a,b){return (String(a[key])<String(b[key])?-1:String(a[key])>String(b[key])?1:0)*dir})}
function render(){document.getElementById('tb').innerHTML=rows().map(function(t){return '<tr class="t '+(cur===t.id?'on':'')+'" data-id="'+t.id+'"><td>'+t.id+'</td><td>'+t.customer+'</td><td>'+t.tier+'</td><td>'+t.subject+'</td><td>'+t.status+'</td><td>'+t.created+'</td></tr>'}).join('');document.querySelectorAll('tr.t').forEach(function(tr){tr.onclick=function(){cur=+tr.dataset.id;render();detail()}})}
function detail(){var t=T.find(function(x){return x.id===cur});var d=document.getElementById('d');d.innerHTML='<h2 style="font-size:17px;margin:0">#'+t.id+' '+t.subject+'</h2><div style="color:#64748b">'+t.customer+' ('+t.tier+') · created '+t.created+'</div>'+t.msgs.map(function(m){return '<div class="m '+m.who+'"><b>'+m.who+':</b> '+m.text+'</div>'}).join('')+'<h3 style="font-size:14px">Properties</h3><label>Status <select id=ps>'+['Open','Pending','Escalated','Closed'].map(function(s){return '<option '+(t.status===s?'selected':'')+'>'+s+'</option>'}).join('')+'</select></label><label>Priority <select id=pp>'+['Low','Normal','High','Urgent'].map(function(s){return '<option '+(t.priority===s?'selected':'')+'>'+s+'</option>'}).join('')+'</select></label><label>Assignee <select id=pa>'+['','Dana','Priya','Tomas','Ines'].map(function(s){return '<option '+(t.assignee===s?'selected':'')+'>'+(s||'Unassigned')+'</option>'}).join('')+'</select></label><label>Internal note <textarea id=pn rows=2></textarea></label><button id=upd>Update ticket</button> <span id=msg style="color:#15803d"></span><div style="color:#64748b;font-size:12px;margin-top:8px">Notes: '+(t.notes.join(' | ')||'none')+'</div>';
 document.getElementById('upd').onclick=function(){fetch('/__act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:t.id,status:document.getElementById('ps').value,priority:document.getElementById('pp').value,assignee:document.getElementById('pa').value,note:document.getElementById('pn').value})}).then(function(){load()})}}
['q','fs','ft'].forEach(function(i){document.getElementById(i).oninput=render;document.getElementById(i).onchange=render});document.querySelectorAll('th').forEach(function(th){th.onclick=function(){if(key===th.dataset.k)dir=-dir;else{key=th.dataset.k;dir=1}render()}});load()})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8917)
