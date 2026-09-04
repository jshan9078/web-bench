#!/usr/bin/env python3
"""263-multi-page-checkout: a four-page checkout (cart with quantities, address with postcode validation, shipping
method rules, payment form with card validation) ending in an order confirmation. Task: adjust the cart to the
stated quantities, ship to the given address with the cheapest method that arrives by a date, pay with the given
test card, and confirm. complete = order matches."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
ITEMS = [{"sku": "HB-MUG", "name": "Harbor mug", "price": 12.0}, {"sku": "HB-TEE", "name": "Harbor tee", "price": 24.0}, {"sku": "HB-CAP", "name": "Harbor cap", "price": 18.0}]
SHIP = [{"id": "std", "name": "Standard (5-7 days)", "price": 4.99, "days": 7}, {"id": "exp", "name": "Express (2-3 days)", "price": 9.99, "days": 3}, {"id": "nxt", "name": "Next day", "price": 19.99, "days": 1}]
S = {"order": None}


def reset(): S["order"] = None
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"items": ITEMS, "ship": SHIP}), "application/json")
    return None


def luhn(n):
    d = [int(c) for c in n if c.isdigit()]; s = 0
    for i, x in enumerate(reversed(d)):
        if i % 2 == 1: x = x * 2 - 9 if x * 2 > 9 else x * 2
        s += x
    return len(d) >= 13 and s % 10 == 0


def post(path, data, ctype):
    if path == "/__order":
        card = str(data.get("card") or "")
        if not luhn(card): return (json.dumps({"ok": False, "error": "Card number is not valid"}), "application/json")
        if not str(data.get("postcode") or "").strip(): return (json.dumps({"ok": False, "error": "Postcode required"}), "application/json")
        S["order"] = dict(data); return (json.dumps({"ok": True, "ref": "ORD-77812"}), "application/json")
    return None


def state():
    o = S["order"] or {}; q = o.get("qty") or {}
    ok = bool(o) and q.get("HB-MUG") == 3 and q.get("HB-TEE") == 1 and q.get("HB-CAP") == 0 and o.get("ship") == "exp" and o.get("postcode", "").replace(" ", "").upper() == "M5S2C6" and "quay" in o.get("address", "").lower() and o.get("card", "").replace(" ", "") == "4242424242424242" and o.get("name", "").strip().lower() == "ana silva"
    return {"order": o, "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Harbor Store checkout</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:700px;margin:20px auto;background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0}.steps{display:flex;gap:14px;color:#94a3b8;margin-bottom:14px}.steps b{color:#0f172a}label{display:block;margin:8px 0}input,select,button{font:inherit;padding:7px 9px}.line{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #f1f5f9}.err{color:#b91c1c}.note{color:#64748b;font-size:13px}</style>
<main><div class=steps id=st></div><div id=b></div></main>
<script>(function(){var D=null,step=1,O={qty:{'HB-MUG':1,'HB-TEE':1,'HB-CAP':1},name:'',address:'',postcode:'',ship:null,card:'',exp:'',cvc:''};
function steps(){document.getElementById('st').innerHTML=['Cart','Address','Shipping','Payment'].map(function(s,i){return (i+1===step?'<b>':'<span>')+(i+1)+'. '+s+(i+1===step?'</b>':'</span>')}).join('')}
function sub(){return D.items.reduce(function(a,it){return a+it.price*(O.qty[it.sku]||0)},0)}
function render(){steps();var b=document.getElementById('b');
 if(step===1){b.innerHTML='<h2 style="font-size:19px">Your cart</h2>'+D.items.map(function(it){return '<div class=line><span>'+it.name+' ($'+it.price.toFixed(2)+')</span><span>Qty <input type=number min=0 max=9 value="'+O.qty[it.sku]+'" data-s="'+it.sku+'" style="width:60px"></span></div>'}).join('')+'<p><b>Subtotal $'+sub().toFixed(2)+'</b></p><button id=n>Continue to address</button>';
  b.querySelectorAll('input[data-s]').forEach(function(i){i.onchange=function(){O.qty[i.dataset.s]=+i.value;render()}});document.getElementById('n').onclick=function(){step=2;render()}}
 else if(step===2){b.innerHTML='<h2 style="font-size:19px">Delivery address</h2><label>Full name <input id=nm value="'+O.name+'"></label><label>Address <input id=ad size=40 value="'+O.address+'"></label><label>Postcode <input id=pc value="'+O.postcode+'"></label><button id=p>Back</button> <button id=n>Continue to shipping</button><div class=err id=e></div>';
  document.getElementById('p').onclick=function(){step=1;render()};document.getElementById('n').onclick=function(){O.name=nm.value;O.address=ad.value;O.postcode=pc.value;if(!/^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$/.test(O.postcode.trim())){document.getElementById('e').textContent='Enter a valid Canadian postcode (e.g. M5S 2C6).';return}if(!O.name.trim()||!O.address.trim()){document.getElementById('e').textContent='Name and address are required.';return}step=3;render()}}
 else if(step===3){b.innerHTML='<h2 style="font-size:19px">Shipping method</h2><p class=note>Today is Tue 8 Sep 2026. Delivery estimates count business days.</p>'+D.ship.map(function(s){return '<label><input type=radio name=sh value="'+s.id+'" '+(O.ship===s.id?'checked':'')+'> '+s.name+' $'+s.price.toFixed(2)+'</label>'}).join('')+'<button id=p>Back</button> <button id=n>Continue to payment</button><div class=err id=e></div>';
  document.getElementById('p').onclick=function(){step=2;render()};document.getElementById('n').onclick=function(){var r=b.querySelector('input[name=sh]:checked');if(!r){document.getElementById('e').textContent='Choose a shipping method.';return}O.ship=r.value;step=4;render()}}
 else{var s=D.ship.find(function(x){return x.id===O.ship});b.innerHTML='<h2 style="font-size:19px">Payment</h2><p>Items $'+sub().toFixed(2)+' + shipping $'+s.price.toFixed(2)+' = <b>$'+(sub()+s.price).toFixed(2)+'</b></p><label>Card number <input id=cn value="'+O.card+'"></label><label>Expiry (MM/YY) <input id=ex value="'+O.exp+'" size=6></label><label>CVC <input id=cv value="'+O.cvc+'" size=4></label><button id=p>Back</button> <button id=n>Place order</button><div class=err id=e></div><div id=ok style="color:#15803d"></div>';
  document.getElementById('p').onclick=function(){step=3;render()};document.getElementById('n').onclick=function(){O.card=cn.value;O.exp=ex.value;O.cvc=cv.value;if(!/^\d\d\/\d\d$/.test(O.exp)||O.cvc.length<3){document.getElementById('e').textContent='Enter expiry as MM/YY and a 3-digit CVC.';return}fetch('/__order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(O)}).then(r=>r.json()).then(function(j){if(!j.ok){document.getElementById('e').textContent=j.error;return}document.getElementById('ok').innerHTML='<b>Order placed: '+j.ref+'</b>'})}}}
fetch('/__data').then(r=>r.json()).then(function(j){D=j;render()})})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8921)
