#!/usr/bin/env python3
"""287-sequence-recall: a 3x3 tile board plays a sequence of 6 tiles (each lit for 1.5 s with a 0.5 s gap) after
Play is pressed; then the tiles must be clicked in the same order. Replay is allowed (resets input). State over
time with generous timing. complete = the sequence entered correctly."""
import json, random, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"seq": [], "t0": None, "input": [], "done": False, "plays": 0}


def reset(): S["seq"] = [random.randrange(9) for _ in range(6)]; S["t0"] = None; S["input"] = []; S["done"] = False; S["plays"] = 0
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__lit":
        if S["t0"] is None: return (json.dumps({"lit": None}), "application/json")
        dt = time.time() - S["t0"]; k = int(dt // 2.0)
        return (json.dumps({"lit": S["seq"][k] if k < 6 and (dt - k * 2.0) < 1.5 else None, "playing": dt < 12}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__play": S["t0"] = time.time(); S["input"] = []; S["plays"] += 1; return (json.dumps({"ok": True}), "application/json")
    if path == "/__tile":
        if S["done"]: return (json.dumps({"ok": True}), "application/json")
        S["input"].append(int(data.get("i")))
        if S["input"] == S["seq"]: S["done"] = True
        elif S["input"] != S["seq"][:len(S["input"])]: S["input"] = []
        return (json.dumps({"n": len(S["input"]), "done": S["done"]}), "application/json")
    return None


def state(): return {"seq": S["seq"], "input": S["input"], "plays": S["plays"], "complete": S["done"]}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Sequence recall</title>
<style>body{font:15px system-ui;margin:0;background:#0f172a;color:#e5e7eb}main{max-width:420px;margin:24px auto;text-align:center}#b{display:grid;grid-template-columns:repeat(3,110px);gap:10px;justify-content:center;margin:14px 0}button.t{height:100px;font:inherit;border:0;border-radius:10px;background:#334155;cursor:pointer;color:#e5e7eb}button.t.lit{background:#fbbf24;color:#000}button{font:inherit;padding:8px 14px}</style>
<main><h1 style="font-size:18px">Sequence recall</h1><p>Press Play: six tiles light up one after another (each for 1.5 s). Then click the tiles in the same order. A wrong tile clears your input; Play again to re-watch.</p><button id=play>Play sequence</button><div id=b></div><p id=st>Entered: 0 of 6</p></main>
<script>(function(){var lit=null;function render(){document.getElementById('b').innerHTML=Array.from({length:9}).map(function(_,i){return '<button class="t '+(lit===i?'lit':'')+'" data-i="'+i+'" aria-label="tile '+(i+1)+'">'+(i+1)+'</button>'}).join('');document.querySelectorAll('button.t').forEach(function(b){b.onclick=function(){fetch('/__tile',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({i:+b.dataset.i})}).then(r=>r.json()).then(function(j){document.getElementById('st').textContent=j.done?'Sequence complete!':'Entered: '+j.n+' of 6'})}})}
function poll(){fetch('/__lit').then(r=>r.json()).then(function(j){if(j.lit!==lit){lit=j.lit;render()}})}
document.getElementById('play').onclick=function(){fetch('/__play',{method:'POST'}).then(function(){document.getElementById('st').textContent='Watch...'})};render();setInterval(poll,150)})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8935)
