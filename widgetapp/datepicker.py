#!/usr/bin/env python3
"""106-datepicker: a hotel booking form whose date fields are read-only and driven by a custom calendar popup
(month navigation, year select, blackout dates). Task: check-in on the last Friday of November 2027, check-out
three nights later, two guests, Confirm. complete = stored booking matches."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"booking": None, "blackout": [], "submissions": []}
TARGET = {"checkin": "2027-11-26", "checkout": "2027-11-29", "guests": 2}


def reset():
    S["booking"] = None; S["submissions"] = []
    S["blackout"] = ["2027-11-27", "2027-11-19", "2027-11-05", "2027-12-24", "2027-12-25"]      # 27 Nov blacked out: checkout can still be the 29th? No: blackout only blocks check-in dates.


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"blackout": S["blackout"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__book":
        b = {"checkin": str(data.get("checkin") or ""), "checkout": str(data.get("checkout") or ""), "guests": int(data.get("guests") or 0)}
        S["submissions"].append(b); S["booking"] = b; return (json.dumps({"ok": True, "ref": "NW-" + str(4000 + len(S["submissions"]))}), "application/json")
    return None


def state(): return {"target": TARGET, "booking": S["booking"], "submissions": S["submissions"], "complete": S["booking"] == TARGET}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Book a stay, Harbor Inn</title>
<style>body{font:15px system-ui;margin:0;background:#f5f5f4;color:#1c1917}main{max-width:560px;margin:30px auto;background:#fff;padding:24px;border-radius:12px;border:1px solid #e7e5e4}label{display:block;margin:12px 0 4px;font-size:13px;color:#57534e}
input[readonly]{font:inherit;padding:8px 10px;width:200px;background:#fafaf9;border:1px solid #d6d3d1;border-radius:6px;cursor:pointer}button{font:inherit;padding:8px 14px;cursor:pointer}
#cal{position:absolute;background:#fff;border:1px solid #d6d3d1;border-radius:10px;padding:10px;box-shadow:0 8px 24px rgba(0,0,0,.12);display:none;width:300px}#cal .hd{display:flex;gap:6px;align-items:center;justify-content:space-between;margin-bottom:8px}
#cal table{border-collapse:collapse;width:100%}#cal td,#cal th{text-align:center;padding:4px 0;font-size:13px}#cal td{cursor:pointer;border-radius:6px}#cal td:hover{background:#f5f5f4}#cal td.dis{color:#d6d3d1;cursor:not-allowed;text-decoration:line-through}#cal td.sel{background:#1c1917;color:#fff}
.step{display:inline-flex;align-items:center;gap:10px}.step button{width:32px}#msg{margin-top:12px;color:#15803d}</style>
<main><h1 style="font-size:20px">Harbor Inn, book a stay</h1>
<label>Check-in</label><input id=ci readonly placeholder="Select date" aria-label="Check-in date"><label>Check-out</label><input id=co readonly placeholder="Select date" aria-label="Check-out date">
<label>Guests</label><div class=step><button id=gm aria-label="Fewer guests">-</button><span id=gv>1</span><button id=gp aria-label="More guests">+</button></div>
<p><button id=book>Confirm booking</button></p><div id=msg></div></main>
<div id=cal role=dialog aria-label="Calendar"><div class=hd><button id=prev aria-label="Previous month">‹</button><select id=mon></select><select id=yr></select><button id=next aria-label="Next month">›</button></div><table><thead><tr><th>Mo<th>Tu<th>We<th>Th<th>Fr<th>Sa<th>Su</tr></thead><tbody id=days></tbody></table><div style="font-size:12px;color:#78716c;margin-top:6px">Struck-through dates are unavailable for check-in.</div></div>
<script>(function(){var BL=[],field=null,vy=2026,vm=8,val={ci:null,co:null},guests=1,M=['January','February','March','April','May','June','July','August','September','October','November','December'];
fetch('/__data').then(r=>r.json()).then(function(j){BL=j.blackout});
var mon=document.getElementById('mon'),yr=document.getElementById('yr');M.forEach(function(m,i){var o=document.createElement('option');o.value=i;o.textContent=m;mon.appendChild(o)});for(var y=2026;y<=2028;y++){var o=document.createElement('option');o.value=y;o.textContent=y;yr.appendChild(o)}
function iso(y,m,d){return y+'-'+String(m+1).padStart(2,'0')+'-'+String(d).padStart(2,'0')}
function draw(){mon.value=vm;yr.value=vy;var first=new Date(vy,vm,1),off=(first.getDay()+6)%7,n=new Date(vy,vm+1,0).getDate(),h='<tr>',c=0;for(var i=0;i<off;i++){h+='<td></td>';c++}
 for(var d=1;d<=n;d++){var s=iso(vy,vm,d),dis=(field==='ci'&&BL.indexOf(s)>=0)||new Date(vy,vm,d)<new Date(2026,8,3)||(field==='co'&&val.ci&&s<=val.ci);h+='<td class="'+(dis?'dis':'')+(val[field]===s?' sel':'')+'" data-d="'+s+'">'+d+'</td>';c++;if(c%7===0)h+='</tr><tr>'}
 document.getElementById('days').innerHTML=h+'</tr>';document.querySelectorAll('#days td[data-d]').forEach(function(td){if(td.classList.contains('dis'))return;td.onclick=function(){val[field]=td.dataset.d;document.getElementById(field).value=td.dataset.d;if(field==='ci'&&val.co&&val.co<=val.ci){val.co=null;document.getElementById('co').value=''}document.getElementById('cal').style.display='none'}})}
function open(f){field=f;var el=document.getElementById(f),r=el.getBoundingClientRect(),cal=document.getElementById('cal');cal.style.left=(r.left+window.scrollX)+'px';cal.style.top=(r.bottom+window.scrollY+4)+'px';cal.style.display='block';draw()}
document.getElementById('ci').onclick=function(){open('ci')};document.getElementById('co').onclick=function(){open('co')};
document.getElementById('prev').onclick=function(){vm--;if(vm<0){vm=11;vy--}draw()};document.getElementById('next').onclick=function(){vm++;if(vm>11){vm=0;vy++}draw()};mon.onchange=function(){vm=+mon.value;draw()};yr.onchange=function(){vy=+yr.value;draw()};
document.getElementById('gm').onclick=function(){guests=Math.max(1,guests-1);document.getElementById('gv').textContent=guests};document.getElementById('gp').onclick=function(){guests=Math.min(6,guests+1);document.getElementById('gv').textContent=guests};
document.addEventListener('click',function(e){var cal=document.getElementById('cal');if(cal.style.display==='block'&&!cal.contains(e.target)&&e.target.id!=='ci'&&e.target.id!=='co')cal.style.display='none'});
document.getElementById('book').onclick=function(){if(!val.ci||!val.co){document.getElementById('msg').textContent='Please select both dates.';return}fetch('/__book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({checkin:val.ci,checkout:val.co,guests:guests})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Booked, reference '+j.ref+': '+val.ci+' to '+val.co+', '+guests+' guest(s).'})};
})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8826)
