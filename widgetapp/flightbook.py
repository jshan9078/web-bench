#!/usr/bin/env python3
"""248-flight-booking: a four-step booking wizard (search with date and passenger count, fare selection with
rules, passenger details with validation, seat map and confirmation). Task: book the cheapest fare that allows a
free checked bag for 2 adults on the stated date, choose two adjacent window+middle seats in the same row, enter
the given passenger names, and confirm. complete = booking matches all constraints."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"booking": None, "date": "", "taken": []}
FLIGHTS = [{"id": "HB101", "dep": "07:15", "arr": "09:40", "fares": {"Basic": 89, "Standard": 129, "Flex": 189}},
           {"id": "HB205", "dep": "12:30", "arr": "14:55", "fares": {"Basic": 79, "Standard": 119, "Flex": 179}},
           {"id": "HB309", "dep": "18:05", "arr": "20:30", "fares": {"Basic": 99, "Standard": 139, "Flex": 199}}]
RULES = {"Basic": "Cabin bag only. Checked bag $35 each way.", "Standard": "1 checked bag included. Seat selection included.", "Flex": "1 checked bag included. Free changes."}
ROWS = 12; COLS = "ABCDEF"


def reset():
    S["booking"] = None; S["date"] = "2026-10-21"
    S["taken"] = sorted(random.sample([f"{r}{c}" for r in range(1, ROWS + 1) for c in COLS], 40))


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"date": S["date"], "flights": FLIGHTS, "rules": RULES, "taken": S["taken"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__book": S["booking"] = dict(data); return (json.dumps({"ref": "HB-" + str(random.randint(100000, 999999))}), "application/json")
    return None


def state():
    b = S["booking"] or {}; ok = False
    if b:
        seats = b.get("seats") or []
        def adj(s1, s2):
            r1, c1, r2, c2 = s1[:-1], s1[-1], s2[:-1], s2[-1]
            return r1 == r2 and {c1, c2} in ({"A", "B"}, {"E", "F"})
        ok = (b.get("flight") == "HB205" and b.get("fare") == "Standard" and b.get("date") == S["date"] and int(b.get("adults", 0)) == 2
              and len(seats) == 2 and adj(seats[0], seats[1]) and not any(s in S["taken"] for s in seats)
              and sorted(p.get("name", "").strip().lower() for p in (b.get("pax") or [])) == ["ana silva", "tomas berg"])
    return {"booking": b, "date": S["date"], "taken": S["taken"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Harbor Air, book</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:820px;margin:20px auto;background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0}.steps{display:flex;gap:16px;color:#94a3b8;margin-bottom:16px}.steps b{color:#0f172a}
label{display:block;margin:8px 0}input,select,button{font:inherit;padding:7px 10px}button{cursor:pointer}.f{border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin:8px 0;display:flex;justify-content:space-between;align-items:center}.fare{display:inline-block;margin-left:8px;padding:6px 10px;border:1px solid #cbd5e1;border-radius:6px;cursor:pointer}.fare.on{background:#dbeafe;border-color:#2563eb}
#seats{display:grid;grid-template-columns:repeat(7,36px);gap:6px;margin:12px 0}.st{width:34px;height:30px;border:1px solid #94a3b8;border-radius:5px;font-size:11px;display:grid;place-items:center;cursor:pointer;background:#fff}.st.taken{background:#cbd5e1;color:#64748b;cursor:not-allowed}.st.on{background:#2563eb;color:#fff}.aisle{width:20px}
.err{color:#b91c1c;font-size:13px}.note{color:#64748b;font-size:13px}</style>
<main><div class=steps id=steps></div><div id=body></div></main>
<script>(function(){var D=null,step=1,B={date:'',adults:1,flight:null,fare:null,pax:[],seats:[]};
function steps(){document.getElementById('steps').innerHTML=['Search','Fare','Passengers','Seats and confirm'].map(function(s,i){return (i+1===step?'<b>':'<span>')+(i+1)+'. '+s+(i+1===step?'</b>':'</span>')}).join('')}
function render(){steps();var b=document.getElementById('body');
 if(step===1){b.innerHTML='<h2 style="font-size:19px">Search flights</h2><label>From <input value="Harbor City" readonly></label><label>To <input value="Northport" readonly></label><label>Date <input type=date id=date value="'+(B.date||'')+'"></label><label>Adults <select id=ad>'+[1,2,3,4].map(function(n){return '<option '+(n===B.adults?'selected':'')+'>'+n+'</option>'}).join('')+'</select></label><button id=n1>Search</button><div class=err id=e1></div>';
  document.getElementById('n1').onclick=function(){B.date=document.getElementById('date').value;B.adults=+document.getElementById('ad').value;if(!B.date){document.getElementById('e1').textContent='Choose a date.';return}step=2;render()}}
 else if(step===2){b.innerHTML='<h2 style="font-size:19px">Choose a flight and fare ('+B.date+', '+B.adults+' adult'+(B.adults>1?'s':'')+')</h2>'+D.flights.map(function(f){return '<div class=f><div><b>'+f.id+'</b> '+f.dep+' to '+f.arr+'</div><div>'+Object.keys(f.fares).map(function(k){return '<span class="fare '+(B.flight===f.id&&B.fare===k?'on':'')+'" data-f="'+f.id+'" data-k="'+k+'" title="'+D.rules[k]+'">'+k+' $'+f.fares[k]+'</span>'}).join('')+'</div></div>'}).join('')+'<p class=note>Hover a fare for its rules. Fare rules: '+Object.keys(D.rules).map(function(k){return '<b>'+k+'</b>: '+D.rules[k]}).join(' ')+'</p><button id=p2>Back</button> <button id=n2>Continue</button><div class=err id=e2></div>';
  b.querySelectorAll('.fare').forEach(function(s){s.onclick=function(){B.flight=s.dataset.f;B.fare=s.dataset.k;render()}});document.getElementById('p2').onclick=function(){step=1;render()};document.getElementById('n2').onclick=function(){if(!B.fare){document.getElementById('e2').textContent='Select a fare.';return}step=3;render()}}
 else if(step===3){b.innerHTML='<h2 style="font-size:19px">Passenger details</h2>'+Array.from({length:B.adults}).map(function(_,i){return '<label>Adult '+(i+1)+' full name <input data-i="'+i+'" value="'+((B.pax[i]||{}).name||'')+'"></label>'}).join('')+'<button id=p3>Back</button> <button id=n3>Continue</button><div class=err id=e3></div>';
  document.getElementById('p3').onclick=function(){step=2;render()};document.getElementById('n3').onclick=function(){var pax=[];var bad=false;b.querySelectorAll('input[data-i]').forEach(function(inp){var v=inp.value.trim();if(v.split(' ').length<2)bad=true;pax.push({name:v})});if(bad){document.getElementById('e3').textContent='Enter first and last name for every passenger.';return}B.pax=pax;step=4;render()}}
 else{var rows='';for(var r=1;r<=12;r++){'ABCDEF'.split('').forEach(function(c,ci){var id=r+c,t=D.taken.indexOf(id)>=0;rows+='<div class="st '+(t?'taken':'')+(B.seats.indexOf(id)>=0?' on':'')+'" data-s="'+id+'">'+id+'</div>';if(ci===2)rows+='<div class=aisle></div>'})}
  b.innerHTML='<h2 style="font-size:19px">Seats (A and F are windows, C and D are aisle)</h2><div id=seats>'+rows+'</div><p class=note>Select '+B.adults+' seat(s). Selected: <span id=ss>'+B.seats.join(', ')+'</span></p><p><b>Summary:</b> '+B.flight+' '+B.fare+' on '+B.date+', '+B.pax.map(function(p){return p.name}).join(' and ')+'</p><button id=p4>Back</button> <button id=go>Confirm booking</button><div class=err id=e4></div><div id=msg></div>';
  b.querySelectorAll('.st:not(.taken)').forEach(function(s){s.onclick=function(){var id=s.dataset.s,i=B.seats.indexOf(id);if(i>=0)B.seats.splice(i,1);else{B.seats.push(id);if(B.seats.length>B.adults)B.seats.shift()}render()}});document.getElementById('p4').onclick=function(){step=3;render()};
  document.getElementById('go').onclick=function(){if(B.seats.length!==B.adults){document.getElementById('e4').textContent='Select one seat per passenger.';return}fetch('/__book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(B)}).then(r=>r.json()).then(function(j){document.getElementById('msg').innerHTML='<b>Booked, reference '+j.ref+'</b>'})}}}
fetch('/__data').then(r=>r.json()).then(function(j){D=j;render()})})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8912)
