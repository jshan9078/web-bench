#!/usr/bin/env python3
"""318-week-free-time: a week-view calendar (DOM) with timed events, some overlapping, plus all-day items of
which only those marked 'busy' block time. Report the free hours on the named day between 09:00 and 17:00.
complete = exact (in 0.5 h steps)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
S = {"events": [], "allday": [], "day": "", "subs": []}


def reset():
    ev = []
    for d in DAYS:
        for _ in range(random.randint(2, 4)):
            s = random.choice([8, 8.5, 9, 9.5, 10, 11, 12, 13, 13.5, 14, 15, 16, 16.5]); e = s + random.choice([0.5, 1, 1.5, 2]); ev.append({"day": d, "start": s, "end": e, "title": random.choice(["Standup", "1:1", "Design review", "Interview", "Planning", "Vendor call", "Lunch", "Retro"])})
    S["events"] = ev; S["allday"] = [{"day": random.choice(DAYS), "title": t, "busy": b} for t, b in [("Team offsite", True), ("Birthday", False), ("Release day", False), ("Training (busy)", True)]]
    busy = {a["day"] for a in S["allday"] if a["busy"]}; free_ad = [a["day"] for a in S["allday"] if not a["busy"] and a["day"] not in busy]
    S["day"] = random.choice(free_ad or [d for d in DAYS if d not in busy] or DAYS); S["subs"] = []


def free_hours(day):
    if any(a["day"] == day and a["busy"] for a in S["allday"]): return 0.0
    busy = [(max(9, e["start"]), min(17, e["end"])) for e in S["events"] if e["day"] == day and e["end"] > 9 and e["start"] < 17]
    busy.sort(); tot = 0; cur = None
    for s, e in busy:
        if cur is None or s > cur[1]:
            if cur: tot += cur[1] - cur[0]
            cur = [s, e]
        else: cur[1] = max(cur[1], e)
    if cur: tot += cur[1] - cur[0]
    return 8 - tot


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__cal": return (json.dumps({"events": S["events"], "allday": S["allday"], "day": S["day"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__answer": S["subs"].append(str(data.get("v") or "").strip()); return (json.dumps({"n": len(S["subs"])}), "application/json")
    return None


def state():
    ok = False
    if S["subs"]:
        try: ok = abs(float(S["subs"][-1].lower().replace("h", "").replace("hours", "").strip()) - free_hours(S["day"])) < 0.01
        except ValueError: ok = False
    return {"day": S["day"], "answer": free_hours(S["day"]), "submissions": S["subs"], "complete": ok}


def page():
    full = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}[S["day"]]
    return """<!doctype html><meta charset=utf-8><title>Week view</title><style>body{font:13px system-ui;margin:16px;color:#1f2937;background:#fff}#g{display:grid;grid-template-columns:50px repeat(5,1fr);gap:2px}.hd{font-weight:600;text-align:center;padding:4px}.ad{min-height:22px;background:#f3f4f6;font-size:12px;padding:2px 4px}.ad.busy{background:#fecaca}.col{position:relative;height:660px;background:linear-gradient(#e5e7eb 1px,transparent 1px) 0 0/100% 60px;border:1px solid #e5e7eb}.ev{position:absolute;left:2px;right:2px;background:#bfdbfe;border-left:3px solid #2563eb;font-size:11px;padding:2px 4px;overflow:hidden;border-radius:3px}.hr{height:60px;font-size:11px;color:#6b7280;text-align:right;padding-right:4px}#q{margin:14px 0;padding:10px;background:#f9fafb;border:1px solid #e5e7eb}</style>
<h1 style="font-size:16px">Week of 21 Sep 2026</h1><div id=q>How many hours are FREE on <b>""" + full + """</b> between 09:00 and 17:00? All-day items only block the day when they are marked busy (red); overlapping meetings do not double count. <input id=v size=6> <button id=go>Submit</button> <span id=msg></span></div><div id=g></div>
<script>(function(){var D=["Mon","Tue","Wed","Thu","Fri"];fetch('/__cal').then(r=>r.json()).then(function(j){var g=document.getElementById('g'),h='<div></div>';D.forEach(function(d){h+='<div class=hd>'+d+'</div>'});h+='<div></div>';D.forEach(function(d){var a=j.allday.filter(function(x){return x.day===d});h+='<div class="ad '+(a.some(function(x){return x.busy})?'busy':'')+'">'+a.map(function(x){return x.title+(x.busy?' (busy)':'')}).join(', ')+'</div>'});
h+='<div>';for(var t=7;t<18;t++)h+='<div class=hr>'+t+':00</div>';h+='</div>';D.forEach(function(d){h+='<div class=col>';j.events.filter(function(e){return e.day===d}).forEach(function(e){h+='<div class=ev style="top:'+((e.start-7)*60)+'px;height:'+((e.end-e.start)*60-2)+'px">'+e.title+'<br>'+fmt(e.start)+'-'+fmt(e.end)+'</div>'});h+='</div>'});g.innerHTML=h});
function fmt(x){return String(Math.floor(x)).padStart(2,'0')+':'+(x%1?'30':'00')}
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({v:document.getElementById('v').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})}})();</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8956)
