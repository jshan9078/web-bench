#!/usr/bin/env python3
"""172-nested-modal-terms: a checkout confirmation where Accept is disabled until the terms box (a scrollable
container INSIDE a modal that opened from another modal) has been scrolled to the bottom; then a second
confirmation dialog with a checkbox that must be ticked. Real browser control: scrolling a nested element,
stacked modals. complete = order confirmed with terms scrolled, checkbox ticked."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"events": [], "confirmed": None}


def reset(): S["events"] = []; S["confirmed"] = None
def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__event": S["events"].append(dict(data)); return (json.dumps({"ok": True}), "application/json")
    if path == "/__confirm":
        S["confirmed"] = {"scrolled": bool(data.get("scrolled")), "ticked": bool(data.get("ticked"))}; return (json.dumps({"ref": "NW-77120"}), "application/json")
    return None


def state(): c = S["confirmed"]; return {"confirmed": c, "events": S["events"][-8:], "complete": c is not None and c["scrolled"] and c["ticked"]}


TERMS = "".join(f"<p>{i + 1}. Clause {i + 1}: The customer agrees that deliveries are made to the address on file, that returns are accepted within 30 days in original packaging, and that disputes are handled by the Harbor County arbitration service. Nothing in this clause limits statutory rights.</p>" for i in range(28))
PAGE = r"""<!doctype html><meta charset=utf-8><title>Checkout, Harbor Supply</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:680px;margin:30px auto;background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0}button{font:inherit;padding:8px 14px;cursor:pointer}button:disabled{opacity:.45;cursor:not-allowed}
.ov{position:fixed;inset:0;background:rgba(15,23,42,.45);display:none;align-items:center;justify-content:center}.ov.on{display:flex}.dlg{background:#fff;border-radius:12px;padding:20px;width:520px;box-shadow:0 20px 60px rgba(0,0,0,.3)}
#terms{height:220px;overflow:auto;border:1px solid #cbd5e1;padding:10px;font-size:13px;color:#334155;margin:10px 0}#msg{color:#15803d;margin-top:10px}label{display:flex;gap:8px;align-items:center;margin:12px 0}</style>
<main><h1 style="font-size:20px">Order summary</h1><p>3 items, total $184.20, delivery to 14 Harbor St.</p><button id=place>Place order</button><div id=msg></div></main>
<div class=ov id=m1><div class=dlg><h2 style="font-size:17px;margin-top:0">Confirm order</h2><p>Before we place your order you need to accept the updated terms of sale.</p><button id=open>Review terms</button> <button id=c1>Cancel</button></div></div>
<div class=ov id=m2><div class=dlg><h2 style="font-size:17px;margin-top:0">Terms of sale</h2><div id=terms aria-label="Terms of sale (scroll to the end to enable Accept)">__TERMS__</div><p style="font-size:12px;color:#64748b">Accept becomes available once you have scrolled to the end of the terms.</p><button id=accept disabled>Accept</button> <button id=c2>Back</button></div></div>
<div class=ov id=m3><div class=dlg><h2 style="font-size:17px;margin-top:0">One more thing</h2><label><input type=checkbox id=ack> I confirm the delivery address is correct</label><button id=confirm disabled>Confirm and place order</button> <button id=c3>Cancel</button></div></div>
<script>(function(){var scrolled=false;function ev(n){fetch('/__event',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({e:n})})}
function show(id,on){document.getElementById(id).classList.toggle('on',on)}
document.getElementById('place').onclick=function(){show('m1',true);ev('open-m1')};document.getElementById('c1').onclick=function(){show('m1',false)};
document.getElementById('open').onclick=function(){show('m2',true);ev('open-m2')};document.getElementById('c2').onclick=function(){show('m2',false)};
var t=document.getElementById('terms');t.addEventListener('scroll',function(){if(t.scrollTop+t.clientHeight>=t.scrollHeight-4){scrolled=true;document.getElementById('accept').disabled=false;ev('scrolled-to-end')}});
document.getElementById('accept').onclick=function(){show('m2',false);show('m1',false);show('m3',true);ev('accepted')};
document.getElementById('ack').onchange=function(){document.getElementById('confirm').disabled=!this.checked};document.getElementById('c3').onclick=function(){show('m3',false)};
document.getElementById('confirm').onclick=function(){fetch('/__confirm',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scrolled:scrolled,ticked:document.getElementById('ack').checked})}).then(r=>r.json()).then(function(j){show('m3',false);document.getElementById('msg').textContent='Order placed, reference '+j.ref})};
})();</script>"""


def page(): return PAGE.replace("__TERMS__", TERMS)


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8860)
