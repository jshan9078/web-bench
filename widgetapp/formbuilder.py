#!/usr/bin/env python3
"""260-survey-builder: a drag-free form builder: add questions of different types, set labels, options, required
flags, and reorder with up/down buttons. Task: build a given 4-question survey exactly (types, labels, options,
required, order), then Publish. complete = published schema matches."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
WANT = [{"type": "text", "label": "Full name", "required": True}, {"type": "choice", "label": "Which office?", "options": ["Harbor", "Northport", "Remote"], "required": True},
        {"type": "rating", "label": "Rate the onboarding", "required": False}, {"type": "text", "label": "Anything else?", "required": False}]
S = {"published": None}


def reset(): S["published"] = None
def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__publish": S["published"] = data.get("questions"); return (json.dumps({"ok": True}), "application/json")
    return None


def norm(qs):
    out = []
    for q in qs or []:
        o = {"type": q.get("type"), "label": str(q.get("label") or "").strip(), "required": bool(q.get("required"))}
        if q.get("type") == "choice": o["options"] = [str(x).strip() for x in (q.get("options") or []) if str(x).strip()]
        out.append(o)
    return out


def state(): return {"published": S["published"], "want": WANT, "complete": norm(S["published"]) == WANT}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Form builder</title>
<style>body{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:760px;margin:20px auto;padding:0 16px}.q{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px;margin:8px 0}.q .row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}input,select,button{font:inherit;padding:5px 7px}#add{display:flex;gap:8px;margin:10px 0}.opts input{width:120px}.note{color:#64748b;font-size:12px}</style>
<main><h1 style="font-size:18px">Onboarding survey, builder</h1><div id=add><select id=type><option value=text>Short text</option><option value=choice>Multiple choice</option><option value=rating>Rating 1-5</option></select><button id=addq>Add question</button><span style="margin-left:auto"><button id=pub>Publish</button> <span id=msg style="color:#15803d"></span></span></div><div id=qs></div><p class=note>Each question has a label, a Required box, and Up/Down/Delete controls. Multiple-choice questions have option fields (add more with "+ option").</p></main>
<script>(function(){var Q=[];function render(){document.getElementById('qs').innerHTML=Q.map(function(q,i){return '<div class=q data-i="'+i+'"><div class=row><b>'+(i+1)+'. '+q.type+'</b><input placeholder="Question label" value="'+(q.label||'').replace(/"/g,'&quot;')+'" data-f=label size=30><label><input type=checkbox data-f=required '+(q.required?'checked':'')+'> Required</label><button data-a=up>Up</button><button data-a=down>Down</button><button data-a=del>Delete</button></div>'+(q.type==='choice'?'<div class="row opts">Options: '+(q.options||[]).map(function(o,k){return '<input data-o="'+k+'" value="'+o.replace(/"/g,'&quot;')+'">'}).join('')+'<button data-a=opt>+ option</button></div>':'')+'</div>'}).join('');
 document.querySelectorAll('.q').forEach(function(el){var i=+el.dataset.i,q=Q[i];el.querySelector('[data-f=label]').oninput=function(e){q.label=e.target.value};el.querySelector('[data-f=required]').onchange=function(e){q.required=e.target.checked};el.querySelectorAll('[data-o]').forEach(function(inp){inp.oninput=function(){q.options[+inp.dataset.o]=inp.value}});
  el.querySelectorAll('button[data-a]').forEach(function(b){b.onclick=function(){var a=b.dataset.a;if(a==='up'&&i>0){Q.splice(i-1,0,Q.splice(i,1)[0])}else if(a==='down'&&i<Q.length-1){Q.splice(i+1,0,Q.splice(i,1)[0])}else if(a==='del'){Q.splice(i,1)}else if(a==='opt'){q.options.push('')}render()}})})}
document.getElementById('addq').onclick=function(){var t=document.getElementById('type').value;Q.push({type:t,label:'',required:false,options:t==='choice'?['','']:undefined});render()};
document.getElementById('pub').onclick=function(){fetch('/__publish',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({questions:Q})}).then(function(){document.getElementById('msg').textContent='Published'})};render()})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8920)
