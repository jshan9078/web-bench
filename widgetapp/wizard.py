#!/usr/bin/env python3
"""60-form-wizard: a four-step DOM checkout wizard with the traps real sites have.
Step 1: name + email fields (values given in the prompt; exact match required).
Step 2: shipping options exist only as a rendered IMAGE (price + delivery day); pick, via radio buttons
        labelled A-D, the cheapest option that arrives by the deadline stated in the prompt.
Step 3: 'Continue' stays disabled behind a spinner for ~8 s; clicking early does nothing.
Step 4: a confirmation modal with a checkbox that must be ticked before 'Place order' works.
complete = submitted payload has the right name, email, option, and confirmed=true."""
import random, sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
EXPECT = {"name": "Priya Raman", "email": "priya.raman@example.org"}
S = {"options": [], "answer": None, "submissions": [], "started": 0.0, "deadline": "Thursday"}


def reset():
    while True:
        opts = []
        for L in "ABCD":
            opts.append({"id": L, "price": round(random.choice([4.99, 6.49, 7.99, 9.49, 11.99, 12.49, 14.99, 18.99]), 2),
                         "day": random.choice(DAYS)})
        by = {"Thursday": 3}
        ok = [o for o in opts if DAYS.index(o["day"]) <= by["Thursday"]]
        prices = [o["price"] for o in opts]
        if ok and len(set(prices)) == 4 and min(o["price"] for o in ok) != min(prices):
            break   # the cheapest overall must NOT be the right answer (arrives too late)
    S["options"] = opts; S["answer"] = min(ok, key=lambda o: o["price"])["id"]
    S["submissions"] = []; S["started"] = 0.0


def render():
    img = Image.new("RGB", (620, 230), (255, 255, 255)); dr = ImageDraw.Draw(img)
    dr.text((16, 12), "Shipping options", fill=(40, 40, 40), font=base.font(22))
    dr.text((16, 44), "Option    Price      Arrives", fill=(110, 110, 110), font=base.font(15, False))
    y = 72
    for o in S["options"]:
        dr.text((16, y), o["id"], fill=(40, 40, 40), font=base.font(19))
        dr.text((110, y), "$%.2f" % o["price"], fill=(40, 40, 40), font=base.font(19, False))
        dr.text((230, y), o["day"], fill=(40, 40, 40), font=base.font(19, False))
        y += 36
    return base.png(img)


def page():
    return """<!doctype html><meta charset=utf-8><title>Checkout Wizard</title>
<style>body{font:15px system-ui;margin:24px;max-width:680px}fieldset{margin:0 0 16px;padding:14px}
button{padding:8px 16px}button:disabled{opacity:.5}.hidden{display:none}
#modal{position:fixed;inset:0;background:rgba(0,0,0,.45)}#modal .box{background:#fff;margin:12% auto;padding:22px;width:380px;border-radius:8px}
.spin{display:inline-block;width:14px;height:14px;border:2px solid #999;border-top-color:transparent;border-radius:50%;animation:r 1s linear infinite;vertical-align:middle}@keyframes r{to{transform:rotate(360deg)}}</style>
<h2>Checkout</h2>
<fieldset id=s1><legend>Step 1 of 4: Contact</legend>
<label>Full name <input id=fullname autocomplete=off></label><br><br>
<label>Email <input id=mail autocomplete=off></label><br><br>
<button id=next1>Next</button> <span id=err1 style="color:#b00"></span></fieldset>
<fieldset id=s2 class=hidden><legend>Step 2 of 4: Shipping</legend>
<img src="/__scene.png" width=620 height=230 alt="shipping options table"><br>
<label><input type=radio name=opt value=A> Option A</label>
<label><input type=radio name=opt value=B> Option B</label>
<label><input type=radio name=opt value=C> Option C</label>
<label><input type=radio name=opt value=D> Option D</label><br><br>
<button id=next2>Next</button> <span id=err2 style="color:#b00"></span></fieldset>
<fieldset id=s3 class=hidden><legend>Step 3 of 4: Review</legend>
<p id=review></p><p id=wait><span class=spin></span> Preparing your order, please wait...</p>
<button id=next3 disabled>Continue</button></fieldset>
<fieldset id=s4 class=hidden><legend>Step 4 of 4: Done</legend><p id=done></p></fieldset>
<div id=modal class=hidden><div class=box><h3>Confirm your order</h3>
<label><input type=checkbox id=agree> I confirm the details above are correct</label><br><br>
<button id=place>Place order</button> <button id=cancel>Cancel</button> <span id=err4 style="color:#b00"></span></div></div>
<script>
var P={};
function show(id){['s1','s2','s3','s4'].forEach(function(s){document.getElementById(s).classList.toggle('hidden',s!==id)})}
next1.onclick=function(){P.name=document.getElementById('fullname').value.trim();P.email=document.getElementById('mail').value.trim();
 if(!P.name||!P.email){err1.textContent='Both fields are required.';return} err1.textContent='';show('s2')};
next2.onclick=function(){var o=document.querySelector('input[name=opt]:checked');if(!o){err2.textContent='Choose a shipping option.';return}
 P.option=o.value;err2.textContent='';review.textContent='Name: '+P.name+' | Email: '+P.email+' | Shipping: option '+P.option;show('s3');
 fetch('/__step3',{method:'POST'});setTimeout(function(){wait.classList.add('hidden');next3.disabled=false},8000)};
next3.onclick=function(){modal.classList.remove('hidden')};
cancel.onclick=function(){modal.classList.add('hidden')};
place.onclick=function(){if(!agree.checked){err4.textContent='Tick the confirmation box first.';return}
 P.confirmed=true;fetch('/__submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(P)})
 .then(function(r){return r.json()}).then(function(j){modal.classList.add('hidden');done.textContent='Order received: reference '+j.ref;show('s4')})};
</script>"""


def click(x, y):
    return {"ignored": True}


def post(path, data, ctype):
    if path == "/__step3":
        S["started"] = time.time(); return (json.dumps({"ok": True}), "application/json")
    if path == "/__submit":
        rec = {"name": data.get("name"), "email": data.get("email"), "option": data.get("option"),
               "confirmed": bool(data.get("confirmed")), "t_since_step3": round(time.time() - S["started"], 1) if S["started"] else None}
        S["submissions"].append(rec)
        return (json.dumps({"ref": "WB-%04d" % random.randint(0, 9999)}), "application/json")
    return None


def state():
    ok = False
    for s in S["submissions"]:
        if (s["name"] == EXPECT["name"] and (s["email"] or "").lower() == EXPECT["email"] and s["option"] == S["answer"]
                and s["confirmed"] and (s["t_since_step3"] is None or s["t_since_step3"] >= 7.5)):
            ok = True
    return {"options": S["options"], "answer": S["answer"], "expect": EXPECT, "submissions": S["submissions"], "complete": ok}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8794)
