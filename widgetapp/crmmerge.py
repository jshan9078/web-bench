#!/usr/bin/env python3
"""250-crm-merge: a contacts CRM with 30 contacts, two of which are the same person entered twice (same email, one
with a newer phone). Task: find the duplicates (search, sort) and merge them keeping the newer phone and the
earlier created date, into a single record. complete = one record left with the right fields, nothing else lost."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
FIRST = ["Aisha", "Ben", "Carla", "Deepak", "Elena", "Farid", "Grace", "Hugo", "Iris", "Jonas", "Kaya", "Liam", "Mira", "Noah", "Olga", "Pavel", "Quinn", "Rosa", "Sven", "Tara", "Umar", "Vera", "Wen", "Ximena", "Yara", "Zane", "Ana", "Bo", "Cy", "Dee"]
S = {"contacts": [], "dup": None, "merged": []}


def reset():
    cs = []
    for i, n in enumerate(FIRST):
        cs.append({"id": 100 + i, "name": f"{n} {random.choice(['Silva','Okafor','Larsen','Meyer','Tanaka'])}", "email": f"{n.lower()}{random.randint(1,99)}@example.com", "phone": f"+1 555 {random.randint(200,999)} {random.randint(1000,9999)}", "created": f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}", "company": random.choice(["Acme", "Harbor Supply", "Northwind", "Cloud Metrics"])})
    d = random.choice(cs); dup = dict(d); dup["id"] = 200; dup["name"] = d["name"].replace(" ", "  ").strip() if random.random() < 0.3 else d["name"]; dup["phone"] = f"+1 555 {random.randint(200,999)} {random.randint(1000,9999)}"; dup["created"] = "2026-03-14"; dup["company"] = d["company"]
    older = d if d["created"] < dup["created"] else dup; newer = dup if older is d else d
    cs.append(dup); random.shuffle(cs); S["contacts"] = cs; S["merged"] = []
    S["dup"] = {"ids": [d["id"], dup["id"]], "email": d["email"], "want_phone": newer["phone"], "want_created": older["created"], "name": d["name"]}


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"contacts": S["contacts"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__merge":
        a, b = int(data.get("keep")), int(data.get("remove")); fields = data.get("fields") or {}
        ka = next((c for c in S["contacts"] if c["id"] == a), None); kb = next((c for c in S["contacts"] if c["id"] == b), None)
        if not ka or not kb: return (json.dumps({"ok": False}), "application/json")
        for k in ("name", "email", "phone", "created", "company"):
            if k in fields: ka[k] = str(fields[k])
        S["contacts"] = [c for c in S["contacts"] if c["id"] != b]; S["merged"].append({"keep": a, "remove": b, "fields": fields}); return (json.dumps({"ok": True}), "application/json")
    if path == "/__edit":
        cid = int(data.get("id")); c = next((x for x in S["contacts"] if x["id"] == cid), None)
        if c:
            for k in ("name", "email", "phone", "created", "company"):
                if k in data: c[k] = str(data[k])
        return (json.dumps({"ok": True}), "application/json")
    return None


def state():
    d = S["dup"]; recs = [c for c in S["contacts"] if c["email"] == d["email"]]
    ok = len(S["contacts"]) == 30 and len(recs) == 1 and recs[0]["phone"] == d["want_phone"] and recs[0]["created"] == d["want_created"] and recs[0]["id"] in d["ids"]
    return {"dup": d, "remaining_with_email": recs, "n_contacts": len(S["contacts"]), "merges": S["merged"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Contacts, Harbor CRM</title>
<style>body{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a}header{padding:10px 16px;background:#0f172a;color:#fff}main{max-width:1000px;margin:0 auto;padding:16px}#ctl{display:flex;gap:10px;margin-bottom:10px;align-items:center}input,button,select{font:inherit;padding:6px 8px}
table{width:100%;border-collapse:collapse;background:#fff}th,td{padding:7px 10px;border-bottom:1px solid #e2e8f0;text-align:left}th{cursor:pointer;background:#f1f5f9}tr.sel{background:#eff6ff}
#merge{margin-top:14px;padding:12px;background:#fff;border:1px solid #e2e8f0;border-radius:8px}#merge label{display:block;margin:6px 0}</style>
<header><b>Harbor CRM</b> &nbsp; Contacts</header><main>
<div id=ctl><input id=q placeholder="Search name, email, phone, company" size=36><span id=cnt></span><span style="margin-left:auto">Select two rows (click) to merge</span></div>
<table><thead><tr><th data-k=name>Name</th><th data-k=email>Email</th><th data-k=phone>Phone</th><th data-k=company>Company</th><th data-k=created>Created</th></tr></thead><tbody id=tb></tbody></table>
<div id=merge><b>Merge selected</b><div id=mbody style="color:#64748b">Select exactly two contacts.</div></div></main>
<script>(function(){var C=[],key='name',dir=1,sel=[];
function load(){fetch('/__data').then(r=>r.json()).then(function(j){C=j.contacts;render()})}
function render(){var q=document.getElementById('q').value.toLowerCase();var rows=C.filter(function(c){return !q||[c.name,c.email,c.phone,c.company].join(' ').toLowerCase().indexOf(q)>=0}).sort(function(a,b){return (String(a[key])<String(b[key])?-1:String(a[key])>String(b[key])?1:0)*dir});
 document.getElementById('tb').innerHTML=rows.map(function(c){return '<tr class="'+(sel.indexOf(c.id)>=0?'sel':'')+'" data-id="'+c.id+'"><td>'+c.name+'</td><td>'+c.email+'</td><td>'+c.phone+'</td><td>'+c.company+'</td><td>'+c.created+'</td></tr>'}).join('');document.getElementById('cnt').textContent=rows.length+' of '+C.length;
 document.querySelectorAll('#tb tr').forEach(function(tr){tr.onclick=function(){var id=+tr.dataset.id;var i=sel.indexOf(id);if(i>=0)sel.splice(i,1);else{sel.push(id);if(sel.length>2)sel.shift()}render();mergeUI()}})}
function mergeUI(){var m=document.getElementById('mbody');if(sel.length!==2){m.textContent='Select exactly two contacts.';return}var a=C.find(function(c){return c.id===sel[0]}),b=C.find(function(c){return c.id===sel[1]});
 m.innerHTML=['name','email','phone','company','created'].map(function(k){return '<label>'+k+': <select data-k="'+k+'"><option value="'+a[k]+'">'+a[k]+' (from #'+a.id+')</option><option value="'+b[k]+'">'+b[k]+' (from #'+b.id+')</option></select></label>'}).join('')+'<label>Keep record: <select id=keep><option value="'+a.id+'">#'+a.id+'</option><option value="'+b.id+'">#'+b.id+'</option></select></label><button id=go>Merge into one contact</button><span id=msg></span>';
 document.getElementById('go').onclick=function(){var keep=+document.getElementById('keep').value,remove=keep===a.id?b.id:a.id,fields={};m.querySelectorAll('select[data-k]').forEach(function(s){fields[s.dataset.k]=s.value});fetch('/__merge',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({keep:keep,remove:remove,fields:fields})}).then(r=>r.json()).then(function(){sel=[];load();document.getElementById('mbody').textContent='Merged.'})}}
document.getElementById('q').oninput=render;document.querySelectorAll('th').forEach(function(th){th.onclick=function(){if(key===th.dataset.k)dir=-dir;else{key=th.dataset.k;dir=1}render()}});load()})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8911)
