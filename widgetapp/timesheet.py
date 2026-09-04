#!/usr/bin/env python3
"""265-timesheet-entry: a weekly timesheet grid (projects x days) with a daily total that must not exceed 8 h and
a submit action. Task: enter the hours from a short work log (given on the page as a notes panel) into the right
cells, then submit. complete = grid equals the log."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
PROJ = ["Harbor API", "Northport site", "Internal", "Support rota"]; DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
LOG = ["Mon: 5h Harbor API, 3h Support rota", "Tue: 2h Internal (team meeting), 6h Harbor API", "Wed: 8h Northport site", "Thu: 4h Northport site, 1h Internal, 3h Support rota", "Fri: 7h Harbor API, 1h Internal"]
WANT = {"Harbor API": [5, 6, 0, 0, 7], "Northport site": [0, 0, 8, 4, 0], "Internal": [0, 2, 0, 1, 1], "Support rota": [3, 0, 0, 3, 0]}
S = {"submitted": None}


def reset(): S["submitted"] = None
def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__submit":
        g = data.get("grid") or {}
        for d in range(5):
            if sum(float((g.get(p) or [0] * 5)[d] or 0) for p in PROJ) > 8.0001: return (json.dumps({"ok": False, "error": f"{DAYS[d]} exceeds 8 hours"}), "application/json")
        S["submitted"] = {p: [float(x or 0) for x in (g.get(p) or [0] * 5)] for p in PROJ}; return (json.dumps({"ok": True}), "application/json")
    return None


def state(): return {"submitted": S["submitted"], "want": WANT, "complete": S["submitted"] == {p: [float(x) for x in WANT[p]] for p in PROJ}}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Timesheet</title>
<style>body{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:900px;margin:20px auto;display:grid;grid-template-columns:1fr 280px;gap:20px;padding:0 16px}table{border-collapse:collapse;background:#fff;width:100%}td,th{border:1px solid #e2e8f0;padding:6px;text-align:center}td:first-child{text-align:left}input{width:48px;font:inherit;padding:4px;text-align:center}
#notes{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:12px}button{font:inherit;padding:7px 12px}.err{color:#b91c1c}.ok{color:#15803d}</style>
<main><div><h1 style="font-size:18px">Timesheet, week of 7 Sep</h1><table id=t></table><p><button id=sub>Submit timesheet</button> <span id=msg></span></p><p style="color:#64748b;font-size:13px">Daily totals may not exceed 8 hours.</p></div>
<div id=notes><b>Work log (notes)</b><ul id=log></ul></div></main>
<script>(function(){var P=__P__,D=__D__,L=__L__;function render(){var h='<tr><th>Project</th>'+D.map(function(d){return '<th>'+d+'</th>'}).join('')+'<th>Total</th></tr>';P.forEach(function(p,i){h+='<tr><td>'+p+'</td>'+D.map(function(d,j){return '<td><input data-p="'+i+'" data-d="'+j+'" value="0"></td>'}).join('')+'<td id="rt'+i+'">0</td></tr>'});h+='<tr><td><b>Daily total</b></td>'+D.map(function(d,j){return '<td id="ct'+j+'">0</td>'}).join('')+'<td></td></tr>';document.getElementById('t').innerHTML=h;document.querySelectorAll('#t input').forEach(function(i){i.oninput=totals})}
function grid(){var g={};P.forEach(function(p,i){g[p]=D.map(function(d,j){return +document.querySelector('input[data-p="'+i+'"][data-d="'+j+'"]').value||0})});return g}
function totals(){var g=grid();P.forEach(function(p,i){document.getElementById('rt'+i).textContent=g[p].reduce(function(a,b){return a+b},0)});D.forEach(function(d,j){document.getElementById('ct'+j).textContent=P.reduce(function(a,p){return a+g[p][j]},0)})}
document.getElementById('log').innerHTML=L.map(function(x){return '<li>'+x+'</li>'}).join('');render();
document.getElementById('sub').onclick=function(){fetch('/__submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({grid:grid()})}).then(r=>r.json()).then(function(j){var m=document.getElementById('msg');m.textContent=j.ok?'Submitted':j.error;m.className=j.ok?'ok':'err'})}})();</script>"""


def page(): return PAGE.replace("__P__", json.dumps(PROJ)).replace("__D__", json.dumps(DAYS)).replace("__L__", json.dumps(LOG))


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8923)
