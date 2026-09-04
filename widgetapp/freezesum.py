#!/usr/bin/env python3
"""290-freeze-sum: a live metrics table whose six values change every 3 seconds; a Freeze button locks the table
and records the sum at that moment. Task: press Freeze, then report the sum of the frozen values. The sum is
judged against the values as frozen (chosen by the agent's own press). complete = submitted sum equals the frozen
sum."""
import json, random, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"seed": 0, "t0": 0.0, "frozen": None, "submissions": []}


def reset(): S["seed"] = random.randint(1, 10 ** 9); S["t0"] = time.time(); S["frozen"] = None; S["submissions"] = []
def vals(tick): rng = random.Random(S["seed"] * 31 + tick); return [rng.randint(100, 999) for _ in range(6)]
def tick(): return int((time.time() - S["t0"]) // 3)
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__vals":
        if S["frozen"]: return (json.dumps({"vals": S["frozen"]["vals"], "frozen": True}), "application/json")
        return (json.dumps({"vals": vals(tick()), "frozen": False}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__freeze":
        if not S["frozen"]: S["frozen"] = {"tick": tick(), "vals": vals(tick())}
        return (json.dumps({"vals": S["frozen"]["vals"]}), "application/json")
    if path == "/__answer": S["submissions"].append(str(data.get("sum") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    ok = False
    if S["frozen"] and S["submissions"]:
        try: ok = int(float(S["submissions"][-1].replace(",", ""))) == sum(S["frozen"]["vals"])
        except ValueError: ok = False
    return {"frozen": S["frozen"], "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Live metrics</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:520px;margin:24px auto}table{border-collapse:collapse;width:100%;background:#fff}td,th{border:1px solid #e2e8f0;padding:8px;text-align:right}td:first-child,th:first-child{text-align:left}input,button{font:inherit;padding:6px 9px}</style>
<main><h1 style="font-size:18px">Live metrics (refresh every 3 s)</h1><table><thead><tr><th>Region</th><th>Requests</th></tr></thead><tbody id=tb></tbody></table><p><button id=fz>Freeze</button> <span id=fs></span></p><p><label>Sum of the frozen Requests column: <input id=sum size=8></label> <button id=go>Submit</button> <span id=msg></span></p></main>
<script>(function(){var R=['North','South','East','West','Central','Islands'];function load(){fetch('/__vals').then(r=>r.json()).then(function(j){document.getElementById('tb').innerHTML=j.vals.map(function(v,i){return '<tr><td>'+R[i]+'</td><td>'+v+'</td></tr>'}).join('');document.getElementById('fs').textContent=j.frozen?'Frozen.':'Live'})}
document.getElementById('fz').onclick=function(){fetch('/__freeze',{method:'POST'}).then(load)};document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sum:document.getElementById('sum').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};load();setInterval(load,700)})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8937)
