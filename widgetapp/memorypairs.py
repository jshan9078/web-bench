#!/usr/bin/env python3
"""275-memory-pairs: a 4x4 grid of face-down cards (DOM buttons); clicking reveals a symbol for 4 seconds, then it
hides again; at most two cards can be face up at once. Task: find and match all four pairs of a given symbol set
(each match locks both cards). State across time with a generous reveal window. complete = all 8 pairs matched."""
import json, random, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
SYM = ["anchor", "bell", "crown", "drum", "eagle", "flame", "gear", "harp"]
S = {"cards": [], "matched": set(), "up": [], "flips": 0}


def reset(): cs = SYM * 2; random.shuffle(cs); S["cards"] = cs; S["matched"] = set(); S["up"] = []; S["flips"] = 0
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__board": return (json.dumps({"n": 16, "matched": sorted(S["matched"]), "up": [{"i": i, "sym": S["cards"][i]} for i, t in S["up"] if time.time() - t < 4]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__flip":
        i = int(data.get("i")); now = time.time(); S["up"] = [(k, t) for k, t in S["up"] if now - t < 4]
        if i in S["matched"] or any(k == i for k, _ in S["up"]): return (json.dumps({"ok": False}), "application/json")
        if len(S["up"]) >= 2: S["up"] = S["up"][1:]
        S["up"].append((i, now)); S["flips"] += 1
        if len(S["up"]) == 2 and S["cards"][S["up"][0][0]] == S["cards"][S["up"][1][0]]:
            S["matched"].update({S["up"][0][0], S["up"][1][0]}); S["up"] = []
        return (json.dumps({"sym": S["cards"][i], "matched": sorted(S["matched"])}), "application/json")
    return None


def state(): return {"matched": sorted(S["matched"]), "flips": S["flips"], "complete": len(S["matched"]) == 16}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Memory pairs</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:520px;margin:24px auto;text-align:center}#g{display:grid;grid-template-columns:repeat(4,110px);gap:10px;justify-content:center}button.c{height:90px;font:inherit;border:1px solid #cbd5e1;border-radius:10px;background:#1e293b;color:#fff;cursor:pointer}button.c.up{background:#fff;color:#0f172a}button.c.done{background:#bbf7d0;color:#14532d}</style>
<main><h1 style="font-size:18px">Memory pairs</h1><p>Click a card to reveal its symbol for 4 seconds. Two revealed cards with the same symbol lock in place. Match all eight pairs.</p><div id=g></div><p id=st></p></main>
<script>(function(){var B=null;function load(){fetch('/__board').then(r=>r.json()).then(function(j){B=j;render()})}
function render(){var up={};B.up.forEach(function(u){up[u.i]=u.sym});document.getElementById('g').innerHTML=Array.from({length:B.n}).map(function(_,i){var m=B.matched.indexOf(i)>=0;return '<button class="c '+(m?'done':up[i]!==undefined?'up':'')+'" data-i="'+i+'" aria-label="card '+(i+1)+'">'+(m?'✓':up[i]!==undefined?up[i]:'?')+'</button>'}).join('');document.getElementById('st').textContent=B.matched.length/2+' of 8 pairs matched';
 document.querySelectorAll('button.c').forEach(function(b){b.onclick=function(){fetch('/__flip',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({i:+b.dataset.i})}).then(load)}})}
load();setInterval(load,700)})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8929)
