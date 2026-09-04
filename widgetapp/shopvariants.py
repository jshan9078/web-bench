#!/usr/bin/env python3
"""259-shop-variants: a product page with three option groups (size, colour, storage) where some combinations are
out of stock or carry surcharges shown only after selection, plus a quantity and a promo code field. Task: add to
the cart the cheapest in-stock configuration meeting given constraints, quantity 2, with the promo code, and check
the cart total. complete = cart line matches the cheapest qualifying configuration with the code applied."""
import json, sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
SIZES = ["S", "M", "L"]; COLORS = ["Black", "Navy", "Red"]; STORAGE = ["64 GB", "128 GB", "256 GB"]
S = {"price": {}, "stock": {}, "cart": [], "promo": "HARBOR10"}


def reset():
    S["cart"] = []; S["price"] = {}; S["stock"] = {}
    for c in itertools.product(SIZES, COLORS, STORAGE):
        base_p = 120 + STORAGE.index(c[2]) * 40 + random.choice([0, 0, 5, 10, -8]) + (12 if c[1] == "Red" else 0)
        S["price"][c] = base_p; S["stock"][c] = random.random() < 0.75
    # ensure at least two in-stock 128GB+ Navy/Black configs at M or L
    q = [c for c in S["price"] if c[0] in ("M", "L") and c[1] != "Red" and c[2] != "64 GB"]
    for c in random.sample(q, 3): S["stock"][c] = True


def qualifying(): return [c for c in S["price"] if S["stock"][c] and c[0] in ("M", "L") and c[1] != "Red" and c[2] != "64 GB"]
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"variants": [{"size": c[0], "color": c[1], "storage": c[2], "price": S["price"][c], "stock": S["stock"][c]} for c in S["price"]]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__cart":
        c = (str(data.get("size")), str(data.get("color")), str(data.get("storage")))
        if c not in S["price"] or not S["stock"][c]: return (json.dumps({"ok": False, "error": "Out of stock"}), "application/json")
        qty = int(data.get("qty") or 1); code = str(data.get("promo") or "").strip().upper(); disc = 0.10 if code == S["promo"] else 0.0
        total = round(S["price"][c] * qty * (1 - disc), 2); S["cart"].append({"variant": list(c), "qty": qty, "promo": code, "total": total}); return (json.dumps({"ok": True, "total": total, "discount": disc}), "application/json")
    return None


def state():
    q = qualifying(); best = min(q, key=lambda c: S["price"][c]); bestp = S["price"][best]; ok = False
    if len(S["cart"]) == 1:
        c = S["cart"][0]; v = tuple(c["variant"]); ok = v in q and S["price"][v] == bestp and c["qty"] == 2 and c["promo"] == S["promo"]
    return {"best": {"variant": best, "price": bestp}, "cart": S["cart"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Harbor Tab 8, buy</title>
<style>body{font:15px system-ui;margin:0;background:#fff;color:#111}main{max-width:900px;margin:20px auto;display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:0 16px}.img{background:#e5e7eb;height:360px;border-radius:12px}h1{font-size:22px;margin:0 0 6px}.opts button{font:inherit;padding:7px 12px;margin:4px 4px 4px 0;border:1px solid #cbd5e1;background:#fff;border-radius:6px;cursor:pointer}.opts button.on{border-color:#2563eb;background:#dbeafe}.opts button.oos{color:#9ca3af;text-decoration:line-through}
#price{font-size:24px;margin:10px 0}#stock{color:#b91c1c}input{font:inherit;padding:6px 8px}#add{font:inherit;padding:10px 16px;background:#111;color:#fff;border:0;border-radius:8px;cursor:pointer}#cart{margin-top:14px;padding:10px;background:#f3f4f6;border-radius:8px}.note{color:#6b7280;font-size:13px}</style>
<main><div><div class=img></div><p class=note>Harbor Tab 8. Prices vary by configuration; some combinations are out of stock (shown struck through once the other options are chosen). Promo codes apply at Add to cart.</p></div>
<div><h1>Harbor Tab 8</h1><div id=price></div><div id=stock></div><div class=opts><div>Size</div><div id=sz></div><div>Colour</div><div id=co></div><div>Storage</div><div id=st></div></div>
<p><label>Quantity <input id=qty type=number value=1 min=1 max=5 style="width:60px"></label> &nbsp; <label>Promo code <input id=promo size=10></label></p><button id=add>Add to cart</button><div id=cart></div></div></main>
<script>(function(){var V=[],sel={size:null,color:null,storage:null};function find(s){return V.find(function(v){return v.size===s.size&&v.color===s.color&&v.storage===s.storage})}
function grp(id,key,vals){var el=document.getElementById(id);el.innerHTML=vals.map(function(v){var probe=Object.assign({},sel);probe[key]=v;var full=probe.size&&probe.color&&probe.storage;var oos=full&&!(find(probe)||{}).stock;return '<button class="'+(sel[key]===v?'on':'')+(oos?' oos':'')+'" data-v="'+v+'">'+v+'</button>'}).join('');el.querySelectorAll('button').forEach(function(b){b.onclick=function(){sel[key]=b.dataset.v;render()}})}
function render(){grp('sz','size',['S','M','L']);grp('co','color',['Black','Navy','Red']);grp('st','storage',['64 GB','128 GB','256 GB']);var v=sel.size&&sel.color&&sel.storage?find(sel):null;document.getElementById('price').textContent=v?'$'+v.price.toFixed(2):'Select options to see the price';document.getElementById('stock').textContent=v&&!v.stock?'Out of stock in this configuration':''}
document.getElementById('add').onclick=function(){fetch('/__cart',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({size:sel.size,color:sel.color,storage:sel.storage,qty:+document.getElementById('qty').value,promo:document.getElementById('promo').value})}).then(r=>r.json()).then(function(j){document.getElementById('cart').textContent=j.ok?'Cart: '+sel.size+' / '+sel.color+' / '+sel.storage+' x'+document.getElementById('qty').value+(j.discount?' with '+(j.discount*100)+'% promo':'')+' = $'+j.total.toFixed(2):j.error})};
fetch('/__data').then(r=>r.json()).then(function(j){V=j.variants;render()})})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8919)
