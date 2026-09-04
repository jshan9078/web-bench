#!/usr/bin/env python3
"""257-team-calendar-slot: a team calendar week view showing two colleagues' events (overlapping, some all-day,
one spanning lunch), working hours 09:00-17:00. Task: create a 45-minute meeting titled "Harbor sync" with both
colleagues at the EARLIEST time in the week when both are free for 45 minutes within working hours, on a
day without an all-day out-of-office for either. complete = event created at the right start with both invitees."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
S = {"events": [], "created": [], "answer": None}


def gen():
    ev = []
    for d in range(5):
        for who in ("Dana", "Priya"):
            t = 9.0
            while t < 16.5:
                if random.random() < 0.55:
                    dur = random.choice([0.5, 0.75, 1.0, 1.5]); ev.append({"day": d, "who": who, "start": t, "end": min(17.0, t + dur), "title": random.choice(["1:1", "Design review", "Vendor call", "Focus block", "Standup"])}); t += dur
                t += random.choice([0.25, 0.5, 0.75])
    ooo = random.randrange(5); ev.append({"day": ooo, "who": random.choice(["Dana", "Priya"]), "start": 0, "end": 24, "title": "Out of office", "allday": True})
    return ev


def busy(ev, d, who, a, b): return any(e["day"] == d and e["who"] == who and e["start"] < b and e["end"] > a for e in ev)


def solve(ev):
    for d in range(5):
        if any(e["day"] == d and e.get("allday") for e in ev): continue
        t = 9.0
        while t + 0.75 <= 17.0 + 1e-9:
            if not busy(ev, d, "Dana", t, t + 0.75) and not busy(ev, d, "Priya", t, t + 0.75): return (d, t)
            t += 0.25
    return None


def reset():
    while True:
        ev = gen(); ans = solve(ev)
        if ans and not (ans[0] == 0 and ans[1] == 9.0): break
    S["events"] = ev; S["created"] = []; S["answer"] = ans


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"events": S["events"], "created": S["created"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__create":
        S["created"].append({"day": int(data.get("day")), "start": float(data.get("start")), "dur": float(data.get("dur")), "title": str(data.get("title") or ""), "invitees": sorted(str(x) for x in (data.get("invitees") or []))}); return (json.dumps({"ok": True}), "application/json")
    return None


def state():
    a = S["answer"]; ok = False
    if len(S["created"]) == 1:
        c = S["created"][0]; ok = c["day"] == a[0] and abs(c["start"] - a[1]) < 1e-6 and abs(c["dur"] - 0.75) < 1e-6 and c["invitees"] == ["Dana", "Priya"] and c["title"].strip().lower() == "harbor sync"
    return {"answer": {"day": DAYS[a[0]], "start": a[1]}, "created": S["created"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Team calendar</title>
<style>body{font:13px system-ui;margin:0;background:#fff;color:#0f172a}#wrap{max-width:1100px;margin:0 auto;padding:10px}#grid{display:grid;grid-template-columns:50px repeat(5,1fr);border:1px solid #e2e8f0}.hd{padding:6px;text-align:center;font-weight:600;background:#f8fafc;border-bottom:1px solid #e2e8f0}.day{position:relative;height:560px;border-left:1px solid #e2e8f0}.hr{position:absolute;left:0;right:0;border-top:1px solid #f1f5f9;font-size:11px;color:#94a3b8}
.ev{position:absolute;border-radius:4px;padding:2px 4px;font-size:11px;overflow:hidden;color:#fff}.dana{background:#2563eb;left:2%;width:46%}.priya{background:#16a34a;left:52%;width:46%}.all{position:absolute;left:2%;right:2%;top:2px;background:#f59e0b;color:#000;font-size:11px;padding:2px 4px;border-radius:4px}
#form{margin-top:12px;padding:12px;background:#f8fafc;border-radius:8px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}input,select,button{font:inherit;padding:5px 7px}</style>
<div id=wrap><h1 style="font-size:16px">Team calendar, week of 7 Sep (working hours 09:00-17:00)</h1><div style="color:#64748b">Blue: Dana. Green: Priya. Amber bar: all-day out of office.</div><div id=grid></div>
<div id=form><b>New event</b><input id=title placeholder="Title" size=14><select id=day></select><select id=start></select><select id=dur><option value=0.5>30 min</option><option value=0.75>45 min</option><option value=1>60 min</option></select><label><input type=checkbox id=iD> Dana</label><label><input type=checkbox id=iP> Priya</label><button id=go>Create</button><span id=msg style="color:#15803d"></span></div></div>
<script>(function(){var DAYS=['Mon','Tue','Wed','Thu','Fri'];function fmt(h){var H=Math.floor(h),M=Math.round((h-H)*60);return String(H).padStart(2,'0')+':'+String(M).padStart(2,'0')}
fetch('/__data').then(r=>r.json()).then(function(j){var g=document.getElementById('grid');var h='<div class=hd></div>'+DAYS.map(function(d){return '<div class=hd>'+d+'</div>'}).join('');h+='<div class=day>'+[9,10,11,12,13,14,15,16].map(function(x){return '<div class=hr style="top:'+((x-9)*70)+'px">'+x+':00</div>'}).join('')+'</div>';
 for(var d=0;d<5;d++){h+='<div class=day data-d="'+d+'">'+[9,10,11,12,13,14,15,16].map(function(x){return '<div class=hr style="top:'+((x-9)*70)+'px"></div>'}).join('')+j.events.filter(function(e){return e.day===d}).map(function(e){if(e.allday)return '<div class=all>'+e.who+': '+e.title+'</div>';return '<div class="ev '+e.who.toLowerCase()+'" style="top:'+((e.start-9)*70)+'px;height:'+((e.end-e.start)*70-2)+'px" title="'+e.who+' '+fmt(e.start)+'-'+fmt(e.end)+'">'+e.who+' '+fmt(e.start)+'-'+fmt(e.end)+' '+e.title+'</div>'}).join('')+j.created.map(function(c){return '<div class=ev style="left:2%;width:96%;background:#7c3aed;top:'+((c.start-9)*70)+'px;height:'+(c.dur*70-2)+'px">'+c.title+' '+fmt(c.start)+'</div>'}).filter(function(x,i){return j.created[i].day===d}).join('')+'</div>'}
 g.innerHTML=h;var ds=document.getElementById('day');DAYS.forEach(function(x,i){ds.innerHTML+='<option value='+i+'>'+x+'</option>'});var ss=document.getElementById('start');for(var t=9;t<17;t+=0.25)ss.innerHTML+='<option value='+t+'>'+fmt(t)+'</option>'});
document.getElementById('go').onclick=function(){var inv=[];if(document.getElementById('iD').checked)inv.push('Dana');if(document.getElementById('iP').checked)inv.push('Priya');fetch('/__create',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:document.getElementById('title').value,day:+document.getElementById('day').value,start:+document.getElementById('start').value,dur:+document.getElementById('dur').value,invitees:inv})}).then(function(){document.getElementById('msg').textContent='Created';location.reload()})}})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8918)
