#!/usr/bin/env python3
"""271-moving-target: a page with twelve identical-looking buttons whose positions and DOM order reshuffle every
5 seconds; exactly one is the real "Proceed" button (identified only by a tiny inner glyph that also changes
position). Task: click Proceed five times in a row; a click on a decoy resets the streak. complete = streak of 5."""
import json, random, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"seed": 0, "streak": 0, "best": 0, "clicks": 0}


def reset(): S["seed"] = random.randint(1, 10 ** 9); S["streak"] = 0; S["best"] = 0; S["clicks"] = 0
def epoch(): return int(time.time() // 5)
def layout(e):
    rng = random.Random(S["seed"] * 7919 + e); order = list(range(12)); rng.shuffle(order); return {"order": order, "real": rng.randrange(12), "epoch": e}
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__layout": return (json.dumps(layout(epoch())), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__press":
        e = int(data.get("epoch", -1)); slot = int(data.get("slot", -1)); now = epoch(); S["clicks"] += 1
        if e not in (now, now - 1): S["streak"] = 0; return (json.dumps({"streak": 0, "note": "stale"}), "application/json")
        lay = layout(e)
        if slot == lay["real"]: S["streak"] += 1; S["best"] = max(S["best"], S["streak"])
        else: S["streak"] = 0
        return (json.dumps({"streak": S["streak"]}), "application/json")
    return None


def state(): return {"best_streak": S["best"], "clicks": S["clicks"], "complete": S["best"] >= 5}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Proceed</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:700px;margin:24px auto}#grid{display:grid;grid-template-columns:repeat(4,150px);gap:14px;margin:16px 0}button.b{height:64px;font:inherit;border:1px solid #cbd5e1;border-radius:10px;background:#fff;cursor:pointer;position:relative}button.b i{position:absolute;width:6px;height:6px;border-radius:50%;background:#2563eb}#st{font-weight:600}</style>
<main><h1 style="font-size:18px">Find the real Proceed button</h1><p>All twelve buttons say Proceed. Only the one with a small blue dot inside it is real. The buttons reshuffle every 5 seconds. Click the real one five times in a row (a wrong click resets the streak).</p><div id=grid></div><p>Streak: <span id=st>0</span> of 5</p></main>
<script>(function(){var L=null;function load(){fetch('/__layout').then(r=>r.json()).then(function(j){if(!L||L.epoch!==j.epoch){L=j;render()}})}
function render(){var g=document.getElementById('grid');g.innerHTML='';L.order.forEach(function(slot,k){var b=document.createElement('button');b.className='b';b.textContent='Proceed';b.setAttribute('data-k',k);if(slot===L.real){var i=document.createElement('i');var rng=(L.epoch*31+slot)%4;i.style.left=[8,120,8,120][rng]+'px';i.style.top=[8,8,48,48][rng]+'px';b.appendChild(i)}
 b.onclick=function(){fetch('/__press',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({epoch:L.epoch,slot:slot})}).then(r=>r.json()).then(function(j){document.getElementById('st').textContent=j.streak})};g.appendChild(b)})}
load();setInterval(load,500)})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8930)
