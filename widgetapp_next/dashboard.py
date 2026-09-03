#!/usr/bin/env python3
"""74-dashboard-triage: a support-desk dashboard with the navigation obstacles real SaaS apps have.
- 180 tickets served in pages of 40 ("Load more"); the list is VIRTUALIZED (only rows near the scroll
  position exist in the DOM), so snapshots/text never show the whole list.
- Filter chips (status, priority), a search box, and a custom sort menu; changing the sort RESETS the
  filters (announced in the UI, as some real apps do).
- Row click opens a detail drawer; "Resolve" needs a non-empty note and a confirm click, then a toast.
- Decoys: a similarly named company, and a more recent High ticket from the target company that is
  Pending (not Open).
complete = exactly the target ticket resolved, with a note that cites the company's other OPEN ticket id.
State/reset are token-gated; /__data and /__resolve are page endpoints (the harness guard fails a run that
calls them directly)."""
import json, random, sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base

COMPANIES = ["Halvorsen Logistics", "Halvorsen Logistic AS", "Brightwater Foods", "Cobalt Systems", "Delaney Press",
             "Emberline Studio", "Fjordview Travel", "Granite Peak Tools", "Hollis & Vane", "Ironwood Dental",
             "Juniper Analytics", "Kestrel Marine", "Lumen Optics", "Marrow Games", "Northgate Realty",
             "Orchard Health", "Pinecrest Bank", "Quill Legal", "Riverbend Textiles", "Sable Motors",
             "Tamsin Bakery", "Umber Ceramics", "Verdant Farms", "Wexley Pharma", "Yarrow Hotels", "Zephyr Air"]
FIRST = ["Ana", "Ben", "Chloe", "Dev", "Elin", "Farid", "Greta", "Hugo", "Isla", "Jonas", "Kai", "Lena", "Mateo", "Nia", "Omar", "Priya", "Quinn", "Rosa", "Sven", "Tara"]
LAST = ["Abbott", "Berg", "Castillo", "Dahl", "Eriksen", "Fischer", "Gomez", "Haugen", "Ito", "Jansen", "Koch", "Lund", "Moreau", "Nakamura", "Olsen", "Petrov", "Quist", "Rask", "Solberg", "Tan"]
SUBJECTS = ["Invoice mismatch", "Login loop after password reset", "Export CSV missing rows", "Webhook retries exhausted",
            "Dashboard chart blank", "SSO group mapping wrong", "API rate limit too low", "Report totals off by one",
            "Mobile app crash on launch", "Duplicate notification emails", "Timezone shown in UTC", "Attachment upload fails"]
LEVEL = int(os.environ.get("WIDGET_LEVEL", "2"))
S = {"tickets": [], "resolved": {}, "target": None, "other_open": None, "log": [], "closed_linked": []}


def reset():
    random.seed()
    base_day = datetime.date(2026, 8, 1)
    tickets = []
    for i in range(180):
        tid = 4100 + i
        tickets.append({"id": tid, "company": random.choice(COMPANIES[2:]), "contact": f"{random.choice(FIRST)} {random.choice(LAST)}",
                        "subject": random.choice(SUBJECTS), "priority": random.choice(["Low", "Medium", "High"]),
                        "status": random.choice(["Open", "Open", "Pending", "Resolved"]),
                        "opened": (base_day + datetime.timedelta(days=random.randint(0, 30), minutes=random.randint(0, 1439))).isoformat()})
    # target company: exactly two OPEN tickets (target: High, most recent open) + decoys
    idx = random.sample(range(180), 6)
    days = random.sample(range(0, 30), 6)
    t_target, t_other, t_pending, t_resolved, t_sim1, t_sim2 = [tickets[i] for i in idx]
    for t in (t_target, t_other, t_pending, t_resolved): t["company"] = "Halvorsen Logistics"
    for t in (t_sim1, t_sim2): t["company"] = "Halvorsen Logistic AS"; t["status"] = "Open"; t["priority"] = "High"
    d = sorted(days)
    t_other.update(status="Open", priority=random.choice(["Low", "Medium"]), opened=f"2026-08-{d[1]+1:02d}T09:{random.randint(10,59)}:00")
    t_target.update(status="Open", priority="High", opened=f"2026-08-{d[3]+1:02d}T14:{random.randint(10,59)}:00")
    t_pending.update(status="Pending", priority="High", opened=f"2026-08-{d[4]+1:02d}T16:{random.randint(10,59)}:00")   # more recent, but not Open
    t_resolved.update(status="Resolved", priority="High", opened=f"2026-08-{d[5]+1:02d}T11:{random.randint(10,59)}:00")
    random.shuffle(tickets)
    S["tickets"] = tickets; S["resolved"] = {}; S["target"] = t_target["id"]; S["other_open"] = t_other["id"]; S["log"] = []; S["closed_linked"] = []


def render():
    return b""


def click(x, y):
    return {"ignored": True}


def get(path):
    if path == "/__data":
        return (json.dumps({"tickets": S["tickets"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__closelinked":
        try: tid = int(data.get("id"))
        except Exception: return (json.dumps({"ok": False}), "application/json")
        S["closed_linked"].append(tid)
        for t in S["tickets"]:
            if t["id"] == tid: t["status"] = "Resolved"
        return (json.dumps({"ok": True}), "application/json")
    if path == "/__resolve":
        try: tid = int(data.get("id")); note = str(data.get("note") or "").strip()
        except Exception: return (json.dumps({"ok": False}), "application/json")
        if not note: return (json.dumps({"ok": False, "error": "note required"}), "application/json")
        S["resolved"][tid] = note
        for t in S["tickets"]:
            if t["id"] == tid: t["status"] = "Resolved"
        S["log"].append({"resolve": tid, "note": note})
        return (json.dumps({"ok": True}), "application/json")
    return None


def state():
    ok = set(S["resolved"]) == {S["target"]} and str(S["other_open"]) in (S["resolved"].get(S["target"]) or "")
    if LEVEL >= 2: ok = ok and not S["closed_linked"]          # the linked ticket must stay Open
    return {"level": LEVEL, "target": S["target"], "other_open": S["other_open"], "resolved": {str(k): v for k, v in S["resolved"].items()},
            "closed_linked": S["closed_linked"], "complete": bool(ok)}


def page():
    return PAGE.replace("__LEVEL__", str(LEVEL))


PAGE = r"""<!doctype html><meta charset=utf-8><title>Helpdesk Console</title>
<style>
body{font:14px system-ui;margin:0;background:#f5f6f8;color:#1f2937}header{background:#111827;color:#fff;padding:12px 20px;font-weight:600}
.bar{display:flex;gap:10px;align-items:center;padding:12px 20px;flex-wrap:wrap}.chip{border:1px solid #cbd5e1;background:#fff;border-radius:999px;padding:4px 10px;cursor:pointer}
.chip[aria-pressed=true]{background:#1f2937;color:#fff;border-color:#1f2937}#search{padding:6px 10px;border:1px solid #cbd5e1;border-radius:6px;width:220px}
.menu{position:relative}.menu ul{position:absolute;top:100%;left:0;background:#fff;border:1px solid #cbd5e1;border-radius:6px;list-style:none;margin:4px 0 0;padding:4px 0;min-width:190px;z-index:5}
.menu li{padding:6px 12px;cursor:pointer}.menu li:hover{background:#eef2ff}.notice{font-size:12px;color:#6b7280}
#list{height:420px;overflow:auto;margin:0 20px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;position:relative}
#spacer{position:relative}.row{position:absolute;left:0;right:0;height:44px;display:grid;grid-template-columns:70px 1.4fr 1fr 1.4fr 90px 90px 150px;align-items:center;padding:0 12px;border-bottom:1px solid #f1f5f9;cursor:pointer}
.row:hover{background:#f8fafc}.hdr{display:grid;grid-template-columns:70px 1.4fr 1fr 1.4fr 90px 90px 150px;padding:8px 32px;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#6b7280}
.pri-High{color:#b91c1c;font-weight:600}.st-Open{color:#047857}.st-Pending{color:#b45309}.st-Resolved{color:#6b7280}
#more{margin:10px 20px;padding:8px 14px}#drawer{position:fixed;top:0;right:-420px;width:400px;height:100%;background:#fff;box-shadow:-8px 0 24px rgba(0,0,0,.15);padding:20px;transition:right .2s;overflow:auto}
#drawer.open{right:0}#drawer h3{margin:0 0 6px}#drawer dl{display:grid;grid-template-columns:110px 1fr;gap:6px 10px}#note{width:100%;height:70px}
#toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#111827;color:#fff;padding:10px 16px;border-radius:8px;display:none}
button{font:inherit;padding:6px 12px;border-radius:6px;border:1px solid #cbd5e1;background:#fff;cursor:pointer}button.primary{background:#1f2937;color:#fff;border-color:#1f2937}
</style>
<header>Helpdesk Console <span style="font-weight:400;opacity:.7">· Tickets</span></header>
<div class=bar>
 <input id=search placeholder="Search tickets" aria-label="Search tickets">
 <span>Status:</span>
 <button class=chip data-f=status data-v=Open aria-pressed=false>Open</button><button class=chip data-f=status data-v=Pending aria-pressed=false>Pending</button><button class=chip data-f=status data-v=Resolved aria-pressed=false>Resolved</button>
 <span>Priority:</span>
 <button class=chip data-f=priority data-v=Low aria-pressed=false>Low</button><button class=chip data-f=priority data-v=Medium aria-pressed=false>Medium</button><button class=chip data-f=priority data-v=High aria-pressed=false>High</button>
 <div class=menu><button id=sortbtn aria-haspopup=true aria-expanded=false>Sort: Newest first</button><ul id=sortmenu hidden role=menu>
  <li role=menuitem data-s=newest>Newest first</li><li role=menuitem data-s=oldest>Oldest first</li><li role=menuitem data-s=company>Company A-Z</li><li role=menuitem data-s=priority>Priority (High first)</li></ul></div>
 <span class=notice>Changing the sort clears active filters.</span>
 <span id=count class=notice></span>
</div>
<div class=hdr><span>ID</span><span>Company</span><span>Contact</span><span>Subject</span><span>Priority</span><span>Status</span><span>Opened</span></div>
<div id=list><div id=spacer></div></div>
<button id=more>Load more</button>
<div id=drawer aria-label="Ticket details"><h3 id=dtitle></h3><dl id=dfields></dl><div id=dactions style="margin-top:14px"></div>
 <div id=resolveform hidden style="margin-top:12px"><label>Resolution note<br><textarea id=note></textarea></label><br><button id=confirmres class=primary>Confirm resolve</button> <button id=cancelres>Cancel</button> <span id=rerr style="color:#b91c1c"></span></div>
 <p style="margin-top:20px"><button id=closed>Close</button></p></div>
<div id=toast role=status></div>
<div id=linkmodal style="position:fixed;inset:0;background:rgba(0,0,0,.45);display:none"><div style="background:#fff;width:420px;margin:14% auto;padding:20px;border-radius:8px">
 <h3 style="margin-top:0">Ticket resolved</h3><p id=linktext></p><button id=linkyes class=primary>Yes, close it too</button> <button id=linkno>No, keep it open</button></div></div>
<script>
var LEVEL=__LEVEL__;
var ALL=[],loaded=0,PAGE=40,filters={status:new Set(),priority:new Set()},sort='newest',q='',view=[],ROW=44,cur=null;
fetch('/__data').then(r=>r.json()).then(j=>{ALL=j.tickets;loaded=Math.min(PAGE,ALL.length);apply()});
function apply(){var v=ALL.slice(0,loaded).filter(t=>(!filters.status.size||filters.status.has(t.status))&&(!filters.priority.size||filters.priority.has(t.priority))&&(!q||(t.company+' '+t.contact+' '+t.subject+' '+t.id).toLowerCase().includes(q)));
 if(sort==='newest')v.sort((a,b)=>b.opened.localeCompare(a.opened));else if(sort==='oldest')v.sort((a,b)=>a.opened.localeCompare(b.opened));else if(sort==='company')v.sort((a,b)=>a.company.localeCompare(b.company)||b.opened.localeCompare(a.opened));else{var o={High:0,Medium:1,Low:2};v.sort((a,b)=>o[a.priority]-o[b.priority]||b.opened.localeCompare(a.opened))}
 view=v;document.getElementById('spacer').style.height=(v.length*ROW)+'px';document.getElementById('count').textContent=v.length+' of '+loaded+' loaded ('+ALL.length+' total)';document.getElementById('more').disabled=loaded>=ALL.length;render()}
function render(){var L=document.getElementById('list'),sp=document.getElementById('spacer');var top=L.scrollTop,first=Math.max(0,Math.floor(top/ROW)-2),last=Math.min(view.length,Math.ceil((top+L.clientHeight)/ROW)+2);
 sp.querySelectorAll('.row').forEach(e=>e.remove());for(var i=first;i<last;i++){var t=view[i],d=document.createElement('div');d.className='row';d.style.top=(i*ROW)+'px';d.setAttribute('role','button');d.setAttribute('aria-label','Ticket '+t.id+' '+t.company);
  d.innerHTML='<span>#'+t.id+'</span><span>'+t.company+'</span><span>'+t.contact+'</span><span>'+t.subject+'</span><span class="pri-'+t.priority+'">'+t.priority+'</span><span class="st-'+t.status+'">'+t.status+'</span><span>'+t.opened.replace('T',' ')+'</span>';
  d.onclick=(function(t){return function(){open(t)}})(t);sp.appendChild(d)}}
document.getElementById('list').addEventListener('scroll',render);
document.querySelectorAll('.chip').forEach(c=>c.onclick=function(){var f=this.dataset.f,v=this.dataset.v;if(filters[f].has(v))filters[f].delete(v);else filters[f].add(v);this.setAttribute('aria-pressed',filters[f].has(v));apply()});
document.getElementById('search').oninput=function(){q=this.value.trim().toLowerCase();apply()};
document.getElementById('sortbtn').onclick=function(){var m=document.getElementById('sortmenu');m.hidden=!m.hidden;this.setAttribute('aria-expanded',!m.hidden)};
document.querySelectorAll('#sortmenu li').forEach(li=>li.onclick=function(){sort=this.dataset.s;document.getElementById('sortbtn').textContent='Sort: '+this.textContent;document.getElementById('sortmenu').hidden=true;
 filters.status.clear();filters.priority.clear();document.querySelectorAll('.chip').forEach(c=>c.setAttribute('aria-pressed','false'));apply()});
document.getElementById('more').onclick=function(){loaded=Math.min(ALL.length,loaded+PAGE);apply()};
function open(t){cur=t;document.getElementById('dtitle').textContent='Ticket #'+t.id+': '+t.subject;document.getElementById('dfields').innerHTML='<dt>Company</dt><dd>'+t.company+'</dd><dt>Contact</dt><dd>'+t.contact+'</dd><dt>Priority</dt><dd>'+t.priority+'</dd><dt>Status</dt><dd>'+t.status+'</dd><dt>Opened</dt><dd>'+t.opened.replace('T',' ')+'</dd>';
 document.getElementById('dactions').innerHTML=t.status==='Resolved'?'<em>Already resolved.</em>':'<button id=resolvebtn class=primary>Resolve</button>';var b=document.getElementById('resolvebtn');if(b)b.onclick=function(){document.getElementById('resolveform').hidden=false};
 document.getElementById('resolveform').hidden=true;document.getElementById('note').value='';document.getElementById('rerr').textContent='';document.getElementById('drawer').classList.add('open')}
document.getElementById('closed').onclick=function(){document.getElementById('drawer').classList.remove('open')};
document.getElementById('cancelres').onclick=function(){document.getElementById('resolveform').hidden=true};
document.getElementById('confirmres').onclick=function(){var n=document.getElementById('note').value.trim();if(!n){document.getElementById('rerr').textContent='A resolution note is required.';return}
 fetch('/__resolve',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:cur.id,note:n})}).then(r=>r.json()).then(j=>{if(!j.ok){document.getElementById('rerr').textContent=j.error||'Failed';return}
  cur.status='Resolved';var T=document.getElementById('toast');T.textContent='Ticket #'+cur.id+' resolved';T.style.display='block';setTimeout(function(){T.style.display='none'},2500);open(cur);apply();
  if(LEVEL>=2){var m=n.match(/#(\d+)/);if(m){var lid=parseInt(m[1]);document.getElementById('linktext').textContent='This note references ticket #'+lid+'. Close #'+lid+' as well?';document.getElementById('linkmodal').style.display='block';
   document.getElementById('linkyes').onclick=function(){fetch('/__closelinked',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:lid})}).then(function(){var t=ALL.find(function(x){return x.id===lid});if(t)t.status='Resolved';document.getElementById('linkmodal').style.display='none';apply()})};
   document.getElementById('linkno').onclick=function(){document.getElementById('linkmodal').style.display='none'}}}})};
</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8796)
