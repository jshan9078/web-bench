#!/usr/bin/env python3
"""125-custom-slider: an e-commerce price filter built from divs (no <input type=range>): two handles on a
track, values shown live. Task: set the range to given bounds within 5 and Apply. Handles move to the clicked
track position (nearest handle), so pixel clicks with feedback are the only way. complete = applied range within
tolerance."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"lo": 0, "hi": 1000, "target": (0, 0), "applied": None}


def reset(): S["lo"], S["hi"] = 0, 1000; S["applied"] = None; a = random.randrange(60, 700, 5); S["target"] = (a, a + random.randrange(120, 280, 5))
def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__apply":
        try: S["applied"] = (int(data.get("lo")), int(data.get("hi")))
        except Exception: return (json.dumps({"ok": False}), "application/json")
        return (json.dumps({"ok": True, "applied": S["applied"]}), "application/json")
    return None


def state():
    t = S["target"]; a = S["applied"]; ok = a is not None and abs(a[0] - t[0]) <= 5 and abs(a[1] - t[1]) <= 5
    return {"target": t, "applied": a, "complete": ok}


def page():
    lo, hi = S["target"]
    return PAGE.replace("__LO__", str(lo)).replace("__HI__", str(hi))


PAGE = r"""<!doctype html><meta charset=utf-8><title>Shop filters</title>
<style>body{font:15px system-ui;margin:0;background:#fff;color:#111}main{max-width:720px;margin:30px auto}h1{font-size:20px}.f{border:1px solid #e5e7eb;border-radius:10px;padding:18px;margin-top:16px}
#track{position:relative;height:6px;background:#e5e7eb;border-radius:3px;margin:34px 12px 18px}#fill{position:absolute;height:6px;background:#2563eb;border-radius:3px}.h{position:absolute;top:-9px;width:24px;height:24px;margin-left:-12px;border-radius:50%;background:#fff;border:2px solid #2563eb;box-shadow:0 1px 4px rgba(0,0,0,.2)}
.vals{display:flex;justify-content:space-between;font-variant-numeric:tabular-nums;color:#374151}button{font:inherit;padding:8px 14px;margin-top:12px}.note{color:#6b7280;font-size:13px}#msg{margin-left:10px;color:#15803d}</style>
<main><h1>Headphones, 412 results</h1><div class=f><b>Price</b><div class=note>Click on the track to move the nearest handle. Set the range to $__LO__ to $__HI__ and apply.</div>
<div id=track><div id=fill></div><div class=h id=h0 role=slider aria-label="Minimum price"></div><div class=h id=h1 role=slider aria-label="Maximum price"></div></div>
<div class=vals><span>Min: $<span id=v0>0</span></span><span>Max: $<span id=v1>1000</span></span></div><button id=apply>Apply filter</button><span id=msg></span></div></main>
<script>(function(){var lo=0,hi=1000,tr=document.getElementById('track');function pos(v){return (v/1000)*tr.clientWidth}
function render(){document.getElementById('h0').style.left=pos(lo)+'px';document.getElementById('h1').style.left=pos(hi)+'px';var f=document.getElementById('fill');f.style.left=pos(lo)+'px';f.style.width=(pos(hi)-pos(lo))+'px';document.getElementById('v0').textContent=lo;document.getElementById('v1').textContent=hi}
tr.addEventListener('click',function(e){var r=tr.getBoundingClientRect(),v=Math.round(Math.max(0,Math.min(1000,(e.clientX-r.left)/r.width*1000)));if(Math.abs(v-lo)<=Math.abs(v-hi)){lo=Math.min(v,hi-5)}else{hi=Math.max(v,lo+5)}render()});
document.getElementById('apply').onclick=function(){fetch('/__apply',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lo:lo,hi:hi})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Applied: $'+j.applied[0]+' to $'+j.applied[1]})};
render();window.addEventListener('resize',render)})();</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8841)
