#!/usr/bin/env python3
"""249-inbox-triage: a webmail client with an inbox of eight threads. Task: apply the team's triage rules
(archive newsletters, label invoices "Finance", star messages that ask for a reply by a date, and reply "On it"
to the one message from the manager asking for a status update). One thread has a later reply that cancels the
request. complete = final labels, stars, archive state and replies exactly as the rules require."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
THREADS = [
 {"id": 1, "from": "Northwind Weekly <news@northwind.example>", "subj": "Weekly digest: 12 new features", "msgs": ["Here is what shipped this week..."], "kind": "newsletter"},
 {"id": 2, "from": "Dana Ferreira <dana@northwind.example>", "subj": "Status update for the board pack?", "msgs": ["Hi, can you send me a status update on Harbor by end of day? Thanks, Dana (Manager)"], "kind": "manager"},
 {"id": 3, "from": "Acme Billing <billing@acme.example>", "subj": "Invoice INV-4471 attached", "msgs": ["Please find invoice INV-4471 for August services."], "kind": "invoice"},
 {"id": 4, "from": "Priya Nair <priya@northwind.example>", "subj": "Can you review the spec by Thursday?", "msgs": ["Could you review the attached spec and reply by Thursday?"], "kind": "deadline"},
 {"id": 5, "from": "Tomas Berg <tomas@northwind.example>", "subj": "Need your sign-off by Friday", "msgs": ["Please sign off the vendor list by Friday.", "Update: never mind, Dana already signed it off. No action needed."], "kind": "cancelled"},
 {"id": 6, "from": "Cloud Metrics <noreply@cloudmetrics.example>", "subj": "Your monthly usage report", "msgs": ["Your usage summary for August is ready."], "kind": "newsletter"},
 {"id": 7, "from": "Harbor Supply <ar@harborsupply.example>", "subj": "Statement and invoice HS-2209", "msgs": ["Invoice HS-2209 is due in 30 days."], "kind": "invoice"},
 {"id": 8, "from": "Ines Carvalho <ines@northwind.example>", "subj": "Quick question", "msgs": ["Is the office open on Monday?"], "kind": "plain"},
]
S = {"labels": {}, "star": {}, "archived": {}, "replies": []}


def reset(): S["labels"] = {t["id"]: [] for t in THREADS}; S["star"] = {t["id"]: False for t in THREADS}; S["archived"] = {t["id"]: False for t in THREADS}; S["replies"] = []
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"threads": THREADS, "labels": S["labels"], "star": S["star"], "archived": S["archived"], "replies": S["replies"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__act":
        tid = int(data.get("id")); a = str(data.get("action"))
        if a == "archive": S["archived"][tid] = True
        elif a == "unarchive": S["archived"][tid] = False
        elif a == "star": S["star"][tid] = not S["star"][tid]
        elif a == "label":
            l = str(data.get("label") or "").strip()
            if l and l not in S["labels"][tid]: S["labels"][tid].append(l)
        elif a == "unlabel": S["labels"][tid] = [x for x in S["labels"][tid] if x != str(data.get("label"))]
        elif a == "reply": S["replies"].append({"id": tid, "text": str(data.get("text") or "")})
        return (json.dumps({"labels": S["labels"], "star": S["star"], "archived": S["archived"], "replies": S["replies"]}), "application/json")
    return None


def state():
    want_arch = {1, 6}; want_fin = {3, 7}; want_star = {4}
    ok = (all(S["archived"][i] == (i in want_arch) for i in S["archived"]) and all(("Finance" in S["labels"][i]) == (i in want_fin) for i in S["labels"])
          and all(S["star"][i] == (i in want_star) for i in S["star"]) and len(S["replies"]) == 1 and S["replies"][0]["id"] == 2 and "on it" in S["replies"][0]["text"].lower())
    return {"labels": S["labels"], "star": S["star"], "archived": S["archived"], "replies": S["replies"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Northwind Mail</title>
<style>body{font:14px system-ui;margin:0;background:#fff;color:#111;display:grid;grid-template-columns:200px 380px 1fr;height:100vh}nav{background:#f1f5f9;padding:16px}nav div{padding:8px;border-radius:6px;cursor:pointer}nav div.on{background:#dbeafe}
#list{border-right:1px solid #e2e8f0;overflow:auto}.t{padding:10px 12px;border-bottom:1px solid #f1f5f9;cursor:pointer}.t.on{background:#eff6ff}.t b{display:block}.meta{color:#64748b;font-size:12px}.lab{display:inline-block;background:#fde68a;border-radius:4px;padding:0 6px;font-size:11px;margin-left:4px}
#view{padding:20px}#tools{display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap}button,input{font:inherit;padding:6px 10px}.msg{border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin:8px 0}textarea{width:100%;height:70px;font:inherit}</style>
<nav><div class=on data-f=inbox>Inbox</div><div data-f=starred>Starred</div><div data-f=archived>Archived</div><div data-f=Finance>Label: Finance</div></nav>
<div id=list></div>
<div id=view><p style="color:#64748b">Select a conversation.</p></div>
<script>(function(){var D=null,cur=null,filter='inbox';
function load(){fetch('/__data').then(r=>r.json()).then(function(j){D=j;render()})}
function shown(){return D.threads.filter(function(t){if(filter==='inbox')return !D.archived[t.id];if(filter==='archived')return D.archived[t.id];if(filter==='starred')return D.star[t.id];return (D.labels[t.id]||[]).indexOf(filter)>=0})}
function render(){var l=document.getElementById('list');l.innerHTML=shown().map(function(t){return '<div class="t '+(cur===t.id?'on':'')+'" data-id="'+t.id+'">'+(D.star[t.id]?'★ ':'')+'<b>'+t.subj+'</b><span class=meta>'+t.from+' · '+t.msgs.length+' message'+(t.msgs.length>1?'s':'')+'</span>'+(D.labels[t.id]||[]).map(function(x){return '<span class=lab>'+x+'</span>'}).join('')+'</div>'}).join('');
 l.querySelectorAll('.t').forEach(function(el){el.onclick=function(){cur=+el.dataset.id;render();view()}});document.querySelectorAll('nav div').forEach(function(d){d.classList.toggle('on',d.dataset.f===filter)})}
function act(a,extra){var body=Object.assign({id:cur,action:a},extra||{});fetch('/__act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(r=>r.json()).then(function(j){D.labels=j.labels;D.star=j.star;D.archived=j.archived;D.replies=j.replies;render();view()})}
function view(){var t=D.threads.find(function(x){return x.id===cur});if(!t)return;var v=document.getElementById('view');v.innerHTML='<h2 style="font-size:18px;margin:0 0 4px">'+t.subj+'</h2><div class=meta>'+t.from+'</div><div id=tools><button id=ar>'+(D.archived[t.id]?'Move to inbox':'Archive')+'</button><button id=st>'+(D.star[t.id]?'Unstar':'Star')+'</button><input id=lb placeholder="Label name" size=10><button id=al>Add label</button>'+(D.labels[t.id]||[]).map(function(x){return '<button data-rm="'+x+'">Remove '+x+'</button>'}).join('')+'</div>'+t.msgs.map(function(m,i){return '<div class=msg><div class=meta>Message '+(i+1)+(i>0?' (later reply)':'')+'</div>'+m+'</div>'}).join('')+'<textarea id=rp placeholder="Reply..."></textarea><br><button id=send>Send reply</button><div class=meta>'+D.replies.filter(function(r){return r.id===t.id}).map(function(r){return 'Sent: '+r.text}).join('<br>')+'</div>';
 document.getElementById('ar').onclick=function(){act(D.archived[t.id]?'unarchive':'archive')};document.getElementById('st').onclick=function(){act('star')};document.getElementById('al').onclick=function(){act('label',{label:document.getElementById('lb').value})};v.querySelectorAll('button[data-rm]').forEach(function(b){b.onclick=function(){act('unlabel',{label:b.dataset.rm})}});document.getElementById('send').onclick=function(){act('reply',{text:document.getElementById('rp').value})}}
document.querySelectorAll('nav div').forEach(function(d){d.onclick=function(){filter=d.dataset.f;render()}});load()})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8910)
