#!/usr/bin/env python3
"""177-hover-megamenu: a retailer site whose navigation is a hover-only mega menu (submenus render on mouseenter and
vanish on leave; nothing is in the DOM until hovered), with a deep target page reached via a third-level item, where
one product must be added to a wishlist. complete = the right product wishlisted, reached through the menu."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
MENU = {"Home & Garden": {"Kitchen": ["Cookware", "Knives", "Small appliances"], "Outdoor": ["Grills", "Patio furniture", "Lighting"]},
        "Electronics": {"Audio": ["Headphones", "Speakers", "Turntables"], "Cameras": ["Mirrorless", "Lenses", "Tripods"]},
        "Sports": {"Cycling": ["Road bikes", "Helmets", "Lights"], "Running": ["Shoes", "Watches", "Apparel"]}}
PRODUCTS = {"Turntables": ["Orbit Basic", "Orbit Plus", "Debut Carbon"], "Speakers": ["Bookshelf S2", "Orbit Mini"], "Lights": ["Beam 400", "Beam 800"], "Lighting": ["Solar path light", "String lights"]}
S = {"wish": [], "path": [], "visited": []}


def reset(): S["wish"] = []; S["path"] = []; S["visited"] = []
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__menu": return (json.dumps(MENU), "application/json")
    if path.startswith("/c/"):
        cat = path[3:].replace("%20", " "); S["visited"].append(cat); return (catpage(cat), "text/html; charset=utf-8")
    return None


def post(path, data, ctype):
    if path == "/__wish": S["wish"].append(str(data.get("p"))); return (json.dumps({"wish": S["wish"]}), "application/json")
    return None


def state(): return {"wish": S["wish"], "visited": S["visited"], "complete": S["wish"] == ["Orbit Plus"] and "Turntables" in S["visited"]}


HEAD = r"""<!doctype html><meta charset=utf-8><title>Harbor Goods</title>
<style>body{font:15px system-ui;margin:0;background:#fff;color:#111}nav{background:#0f172a;color:#fff;display:flex;gap:0;padding:0 24px;position:relative}nav>div{padding:16px 18px;cursor:default;position:relative}
.sub{display:none;position:absolute;left:0;top:100%;background:#fff;color:#111;min-width:220px;box-shadow:0 10px 30px rgba(0,0,0,.2);z-index:5}nav>div:hover>.sub{display:block}.sub>div{padding:10px 14px;position:relative}.sub>div:hover{background:#f1f5f9}
.sub2{display:none;position:absolute;left:100%;top:0;background:#fff;min-width:200px;box-shadow:0 10px 30px rgba(0,0,0,.2)}.sub>div:hover>.sub2{display:block}.sub2 a{display:block;padding:10px 14px;color:#111;text-decoration:none}.sub2 a:hover{background:#f1f5f9}
main{max-width:900px;margin:24px auto;padding:0 16px}.p{border:1px solid #e2e8f0;border-radius:10px;padding:14px;margin:10px 0;display:flex;justify-content:space-between;align-items:center}button{font:inherit;padding:6px 12px}</style>
<nav id=nav></nav>
<script>(function(){var host=document.getElementById('nav');fetch('/__menu').then(r=>r.json()).then(function(m){Object.keys(m).forEach(function(top){var d=document.createElement('div');d.textContent=top;var s=document.createElement('div');s.className='sub';Object.keys(m[top]).forEach(function(mid){var e=document.createElement('div');e.textContent=mid+' ›';var s2=document.createElement('div');s2.className='sub2';m[top][mid].forEach(function(leaf){var a=document.createElement('a');a.href='/c/'+encodeURIComponent(leaf);a.textContent=leaf;s2.appendChild(a)});e.appendChild(s2);s.appendChild(e)});d.appendChild(s);host.appendChild(d)})})})();</script>"""


def page():
    return HEAD + """<main><h1 style="font-size:22px">Harbor Goods</h1><p>Browse the departments in the menu above. Site search is temporarily unavailable.</p><p style="color:#64748b">Featured: String lights, Beam 400, Bookshelf S2.</p></main>"""


def catpage(cat):
    items = PRODUCTS.get(cat, ["Sample item A", "Sample item B"])
    body = "".join(f'<div class=p><span>{p}</span><button data-p="{p}">Add to wishlist</button></div>' for p in items)
    return HEAD + f"""<main><h1 style="font-size:22px">{cat}</h1>{body}<p id=msg style="color:#15803d"></p></main>
<script>document.querySelectorAll('button[data-p]').forEach(function(b){{b.onclick=function(){{fetch('/__wish',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{p:b.dataset.p}})}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Wishlist: '+j.wish.join(', ')}})}}}})</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8861)
