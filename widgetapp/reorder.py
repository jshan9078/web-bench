#!/usr/bin/env python3
"""107-reorder-list: an ordered runbook whose steps can be reordered by drag, by keyboard (grab with Space,
move with arrows, drop with Enter) or via each row's menu (Move up / Move down). Task: move one step to
directly after another named step; two steps have near-identical names. complete = saved order matches."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
STEPS = ["Acknowledge the alert", "Notify on-call lead", "Check dashboards", "Rotate API keys", "Notify on-call", "Scale the API tier", "Verify error rate", "Post status update", "Write the incident summary"]
S = {"order": [], "saved": None, "target": []}


def reset():
    order = STEPS[:]; random.shuffle(order)
    # ensure "Rotate API keys" is NOT already right after "Notify on-call"
    while order.index("Rotate API keys") == order.index("Notify on-call") + 1: random.shuffle(order)
    S["order"] = order; S["saved"] = None
    t = [x for x in order if x != "Rotate API keys"]; t.insert(t.index("Notify on-call") + 1, "Rotate API keys"); S["target"] = t


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"order": S["order"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__save":
        S["saved"] = list(data.get("order") or []); return (json.dumps({"ok": True}), "application/json")
    return None


def state(): return {"initial": S["order"], "target": S["target"], "saved": S["saved"], "complete": S["saved"] == S["target"]}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Runbook editor</title>
<style>body{font:15px system-ui;margin:0;background:#fafafa;color:#18181b}main{max-width:640px;margin:24px auto}h1{font-size:20px}ol{list-style:none;padding:0;margin:0}li{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #e4e4e7;border-radius:8px;padding:10px 12px;margin:6px 0}
li:focus{outline:2px solid #2563eb}li.grab{background:#eff6ff}.h{color:#a1a1aa;cursor:grab}.n{color:#71717a;width:22px}.sp{flex:1}.menu{position:relative}.menu button{font:inherit;background:none;border:0;cursor:pointer;padding:4px 8px}.dd{position:absolute;right:0;top:28px;background:#fff;border:1px solid #e4e4e7;border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.1);display:none;min-width:140px;z-index:2}.dd div{padding:8px 12px;cursor:pointer}.dd div:hover{background:#f4f4f5}
.help{font-size:13px;color:#71717a}#save{font:inherit;padding:8px 14px;margin-top:12px}#msg{color:#15803d;margin-left:10px}</style>
<main><h1>Runbook: API latency incident</h1><p class=help>Drag steps to reorder, or focus a step and press Space to grab it, arrow keys to move, Enter to drop. Each step's ⋮ menu also offers Move up / Move down.</p>
<ol id=list></ol><button id=save>Save order</button><span id=msg></span></main>
<script>(function(){var order=[],grab=-1;
function render(){var ol=document.getElementById('list');ol.innerHTML='';order.forEach(function(s,i){var li=document.createElement('li');li.tabIndex=0;li.draggable=true;li.dataset.i=i;li.className=grab===i?'grab':'';li.innerHTML='<span class=h>⠿</span><span class=n>'+(i+1)+'.</span><span class=sp>'+s+'</span><span class=menu><button aria-label="More actions for '+s+'">⋮</button><div class=dd><div data-a=up>Move up</div><div data-a=down>Move down</div></div></span>';
 li.addEventListener('keydown',function(e){if(e.key===' '){e.preventDefault();grab=grab===i?-1:i;render();focus(grab>=0?grab:i)}else if(grab===i&&(e.key==='ArrowUp'||e.key==='ArrowDown')){e.preventDefault();var j=e.key==='ArrowUp'?i-1:i+1;if(j<0||j>=order.length)return;move(i,j);grab=j;render();focus(j)}else if(e.key==='Enter'&&grab===i){grab=-1;render();focus(i)}});
 li.addEventListener('dragstart',function(e){e.dataTransfer.setData('text/plain',i)});li.addEventListener('dragover',function(e){e.preventDefault()});li.addEventListener('drop',function(e){e.preventDefault();var from=+e.dataTransfer.getData('text/plain');move(from,i);render()});
 var mb=li.querySelector('.menu button'),dd=li.querySelector('.dd');mb.onclick=function(e){e.stopPropagation();document.querySelectorAll('.dd').forEach(function(d){d.style.display='none'});dd.style.display='block'};
 dd.querySelectorAll('div').forEach(function(it){it.onclick=function(e){e.stopPropagation();var j=it.dataset.a==='up'?i-1:i+1;if(j>=0&&j<order.length)move(i,j);render()}});ol.appendChild(li)})}
function focus(i){var el=document.querySelector('li[data-i="'+i+'"]');if(el)el.focus()}
function move(a,b){var x=order.splice(a,1)[0];order.splice(b,0,x)}
document.addEventListener('click',function(){document.querySelectorAll('.dd').forEach(function(d){d.style.display='none'})});
fetch('/__data').then(r=>r.json()).then(function(j){order=j.order;render()});
document.getElementById('save').onclick=function(){fetch('/__save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({order:order})}).then(function(){document.getElementById('msg').textContent='Saved.'})};
})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8827)
