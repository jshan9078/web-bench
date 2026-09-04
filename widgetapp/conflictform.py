#!/usr/bin/env python3
"""251-edit-conflict: a record editor where, on Save, the server reports that a colleague changed two other fields
meanwhile and shows a conflict dialog with both versions field by field. Task: change the phone and notes as
instructed, then resolve the conflict keeping the colleague's changes to the other fields and your own changes,
and save. complete = final record merges correctly."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
BASE = {"name": "Harbor Supply Ltd", "phone": "+1 555 201 4400", "address": "14 Harbor St", "tier": "Silver", "notes": "Net 30."}
THEIRS = {"address": "22 Quay Rd, Unit 3", "tier": "Gold"}
S = {"record": {}, "saves": [], "conflicted": False}


def reset(): S["record"] = dict(BASE); S["saves"] = []; S["conflicted"] = False
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"record": S["record"], "version": 7 if not S["conflicted"] else 8}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__save":
        rec = {k: str(data.get(k, "")) for k in BASE}; S["saves"].append(rec)
        if not S["conflicted"]:
            S["conflicted"] = True; theirs = dict(BASE); theirs.update(THEIRS)
            return (json.dumps({"conflict": True, "theirs": theirs, "yours": rec, "base": BASE}), "application/json")
        S["record"] = rec; return (json.dumps({"ok": True, "version": 9}), "application/json")
    return None


def state():
    r = S["record"]; ok = (len(S["saves"]) >= 2 and r["phone"] == "+1 555 201 4499" and r["notes"].strip() == "Net 45. Ask for PO number." and r["address"] == THEIRS["address"] and r["tier"] == THEIRS["tier"] and r["name"] == BASE["name"])
    return {"record": r, "saves": S["saves"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Account editor</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:620px;margin:24px auto;background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0}label{display:block;margin:10px 0}input,textarea,select,button{font:inherit;padding:7px 9px;width:100%;box-sizing:border-box}button{width:auto;cursor:pointer}
.ov{position:fixed;inset:0;background:rgba(15,23,42,.5);display:none;align-items:center;justify-content:center}.ov.on{display:flex}.dlg{background:#fff;padding:20px;border-radius:12px;width:640px;max-height:90vh;overflow:auto}table{width:100%;border-collapse:collapse;font-size:14px}td,th{border-bottom:1px solid #e2e8f0;padding:6px;text-align:left;vertical-align:top}#msg{color:#15803d;margin-top:10px}</style>
<main><h1 style="font-size:19px">Account: Harbor Supply Ltd</h1><form id=f onsubmit="return false"><label>Name <input name=name></label><label>Phone <input name=phone></label><label>Address <input name=address></label><label>Tier <select name=tier><option>Bronze</option><option>Silver</option><option>Gold</option></select></label><label>Notes <textarea name=notes rows=3></textarea></label><button id=save>Save</button><div id=msg></div></form></main>
<div class=ov id=ov><div class=dlg><h2 style="font-size:17px;margin-top:0">Someone else changed this record while you were editing</h2><p>Choose which value to keep for each field, then save again.</p><table><thead><tr><th>Field</th><th>Their version (saved a minute ago)</th><th>Your version</th><th>Keep</th></tr></thead><tbody id=ct></tbody></table><p><button id=apply>Apply choices and save</button> <button id=cancel>Cancel</button></p></div></div>
<script>(function(){var f=document.getElementById('f');function fill(r){['name','phone','address','tier','notes'].forEach(function(k){f.elements[k].value=r[k]})}
function vals(){var o={};['name','phone','address','tier','notes'].forEach(function(k){o[k]=f.elements[k].value});return o}
fetch('/__data').then(r=>r.json()).then(function(j){fill(j.record)});
function save(v){return fetch('/__save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(v)}).then(r=>r.json())}
document.getElementById('save').onclick=function(){var v=vals();save(v).then(function(j){if(j.conflict){var tb=document.getElementById('ct');tb.innerHTML=Object.keys(j.base).map(function(k){var diff=j.theirs[k]!==j.yours[k];return '<tr><td><b>'+k+'</b></td><td>'+j.theirs[k]+(j.theirs[k]!==j.base[k]?' <i>(changed by them)</i>':'')+'</td><td>'+j.yours[k]+(j.yours[k]!==j.base[k]?' <i>(changed by you)</i>':'')+'</td><td>'+(diff?'<select data-k="'+k+'"><option value="theirs">theirs</option><option value="yours">yours</option></select>':'same')+'</td></tr>'}).join('');
  document.getElementById('ov').classList.add('on');document.getElementById('apply').onclick=function(){var out=Object.assign({},j.yours);tb.querySelectorAll('select').forEach(function(s){out[s.dataset.k]=s.value==='theirs'?j.theirs[s.dataset.k]:j.yours[s.dataset.k]});fill(out);document.getElementById('ov').classList.remove('on');save(out).then(function(r){document.getElementById('msg').textContent=r.ok?'Saved (version '+r.version+')':'Not saved'})}}else{document.getElementById('msg').textContent='Saved (version '+j.version+')'}})};
document.getElementById('cancel').onclick=function(){document.getElementById('ov').classList.remove('on')}})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8913)
