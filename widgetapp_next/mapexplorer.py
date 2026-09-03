#!/usr/bin/env python3
"""75-map-explorer: a synthetic map app with no search box, the way an agent meets an unfamiliar map UI.
A 3000x3000 world (roads, a river, districts) is rendered server-side into a 900x600 viewport at the
current pan/zoom. POI labels appear only at zoom >= 2. Pan with the on-screen arrow buttons (or the
arrow keys), zoom with + / -. Clicking a POI marker opens a popup with its name, category, and the
distance to City Hall; the popup has a "Route to City Hall" button.
Task: find the named POI (a hint gives its district), open its popup, report distance + category, click
Route. complete = popup opened for the target AND route clicked for the target, and no route clicked
for another POI. All page actions go through /__act (pan/zoom/click); state/reset are token-gated."""
import json, math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base

W, H = 900, 600
WORLD = 3000
NAMES = ["Aurora Bakery", "Birch Street Clinic", "Cinder Records", "Dockside Grill", "Elm Court Library", "Fable Bookshop",
         "Glasswing Cafe", "Harbor Pharmacy", "Ivy Lane Florist", "Juniper Gym", "Kettle & Crumb", "Lantern Theater",
         "Meridian Bank", "Nook Cinema", "Oakridge Dental", "Pier Nine Market", "Quarry Climbing", "Rook Hardware",
         "Saffron Kitchen", "Tidewater Hotel", "Umbra Gallery", "Violet Vinyl", "Willow Pet Care", "Yonder Hostel"]
CATS = ["Bakery", "Clinic", "Music store", "Restaurant", "Library", "Bookshop", "Cafe", "Pharmacy", "Florist", "Gym",
        "Bakery", "Theater", "Bank", "Cinema", "Dentist", "Market", "Climbing gym", "Hardware store", "Restaurant", "Hotel",
        "Gallery", "Music store", "Pet care", "Hostel"]
DISTRICTS = {"Northwest": (0, 0), "Northeast": (1, 0), "Southwest": (0, 1), "Southeast": (1, 1)}
S = {"pois": [], "view": {"cx": WORLD / 2, "cy": WORLD / 2, "zoom": 1.0}, "hall": (WORLD / 2, WORLD / 2), "target": None,
     "opened": [], "routed": [], "roads": [], "river": []}


def reset():
    random.seed()
    S["roads"] = [(random.randint(0, WORLD), 0, random.randint(0, WORLD), WORLD) for _ in range(5)] + \
                 [(0, random.randint(0, WORLD), WORLD, random.randint(0, WORLD)) for _ in range(5)]
    S["river"] = [(0, 900)] + [(x, 900 + 400 * math.sin(x / 600) + random.randint(-40, 40)) for x in range(200, WORLD, 200)] + [(WORLD, 1200)]
    pois = []
    idx = list(range(len(NAMES))); random.shuffle(idx)
    for i in idx:
        for _ in range(100):
            x, y = random.randint(120, WORLD - 120), random.randint(120, WORLD - 120)
            if all((x - p["x"]) ** 2 + (y - p["y"]) ** 2 > 220 ** 2 for p in pois) and (x - S["hall"][0]) ** 2 + (y - S["hall"][1]) ** 2 > 300 ** 2:
                pois.append({"id": i, "name": NAMES[i], "cat": CATS[i], "x": x, "y": y}); break
    S["pois"] = pois
    S["target"] = random.choice([p for p in pois if p["name"] != "Meridian Bank"])
    S["view"] = {"cx": WORLD / 2, "cy": WORLD / 2, "zoom": 1.0}
    S["opened"] = []; S["routed"] = []


def _dist(p):
    return int(math.hypot(p["x"] - S["hall"][0], p["y"] - S["hall"][1]) * 0.6)   # world units -> metres


def district_of(p):
    return ("North" if p["y"] < WORLD / 2 else "South") + ("west" if p["x"] < WORLD / 2 else "east")


def _w2s(x, y):
    v = S["view"]; z = v["zoom"]
    return (W / 2 + (x - v["cx"]) * z * (W / WORLD) * 1.0 * (WORLD / W) / (WORLD / W), H / 2 + (y - v["cy"]) * z * (H / WORLD) * (WORLD / H) / (WORLD / H))


def w2s(x, y):
    v = S["view"]; z = v["zoom"]; scale = z * (W / WORLD)
    return (W / 2 + (x - v["cx"]) * scale, H / 2 + (y - v["cy"]) * scale)


def render():
    v = S["view"]; z = v["zoom"]; scale = z * (W / WORLD)
    img = Image.new("RGB", (W, H), (236, 240, 233)); dr = ImageDraw.Draw(img)
    # districts shading
    for name, (qx, qy) in DISTRICTS.items():
        x0, y0 = w2s(qx * WORLD / 2, qy * WORLD / 2); x1, y1 = w2s((qx + 1) * WORLD / 2, (qy + 1) * WORLD / 2)
        dr.rectangle([x0, y0, x1, y1], fill=(236, 240, 233) if (qx + qy) % 2 == 0 else (229, 235, 226))
        if z <= 1.6: dr.text((x0 + 8, y0 + 6), name, fill=(150, 160, 150), font=base.font(13))
    # river
    pts = [w2s(x, y) for x, y in S["river"]]
    dr.line(pts, fill=(140, 180, 220), width=max(6, int(14 * scale * 3)))
    # roads
    for x0, y0, x1, y1 in S["roads"]:
        dr.line([w2s(x0, y0), w2s(x1, y1)], fill=(255, 255, 255), width=max(3, int(8 * scale * 3)))
        dr.line([w2s(x0, y0), w2s(x1, y1)], fill=(200, 200, 200), width=1)
    # city hall
    hx, hy = w2s(*S["hall"]); dr.rectangle([hx - 9, hy - 9, hx + 9, hy + 9], fill=(90, 60, 140)); dr.text((hx + 12, hy - 8), "City Hall", fill=(60, 40, 100), font=base.font(13))
    # POIs
    for p in S["pois"]:
        sx, sy = w2s(p["x"], p["y"])
        if -20 <= sx <= W + 20 and -20 <= sy <= H + 20:
            r = 6 if z < 2 else 8
            dr.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 70, 60), outline=(120, 30, 30))
            if z >= 2: dr.text((sx + 10, sy - 8), p["name"], fill=(40, 40, 40), font=base.font(13))
    dr.rectangle([0, H - 26, 210, H], fill=(255, 255, 255)); dr.text((8, H - 22), f"zoom {z:.1f}x   center ({int(v['cx'])}, {int(v['cy'])})", fill=(90, 90, 90), font=base.font(12))
    return base.png(img)


def page():
    return """<!doctype html><meta charset=utf-8><title>Metro Explorer</title>
<style>body{margin:0;font:14px system-ui;background:#fff}#wrap{position:relative;width:900px}#s{display:block}
#ctl{position:absolute;right:12px;top:12px;display:grid;grid-template-columns:repeat(3,36px);gap:4px}#ctl button,#zoom button{font:16px system-ui;width:36px;height:36px;border:1px solid #999;background:#fff;border-radius:6px;cursor:pointer}
#zoom{position:absolute;left:12px;top:12px;display:grid;gap:4px}#pop{position:absolute;background:#fff;border:1px solid #888;border-radius:8px;padding:10px 12px;box-shadow:0 6px 18px rgba(0,0,0,.2);display:none;min-width:200px}
#pop h4{margin:0 0 4px}#pop button{margin-top:8px;font:inherit;padding:5px 10px}#hint{padding:8px 12px;color:#555}</style>
<div id=hint>Metro Explorer. No search: pan with the arrow buttons or arrow keys, zoom with + / -. Labels appear when zoomed in. Click a marker for details.</div>
<div id=wrap><img id=s src="/__scene.png" width=900 height=600 alt="map">
<div id=zoom><button id=zin aria-label="Zoom in">+</button><button id=zout aria-label="Zoom out">−</button></div>
<div id=ctl><span></span><button data-d=up aria-label="Pan up">↑</button><span></span><button data-d=left aria-label="Pan left">←</button><span></span><button data-d=right aria-label="Pan right">→</button><span></span><button data-d=down aria-label="Pan down">↓</button><span></span></div>
<div id=pop role=dialog><h4 id=pname></h4><div id=pcat></div><div id=pdist></div><button id=route>Route to City Hall</button> <button id=pclose>Close</button></div></div>
<script>
function act(a){return fetch('/__act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(a)}).then(r=>r.json()).then(j=>{document.getElementById('s').src='/__scene.png?'+Date.now();return j})}
document.querySelectorAll('#ctl button').forEach(b=>b.onclick=function(){hide();act({op:'pan',dir:this.dataset.d})});
document.getElementById('zin').onclick=function(){hide();act({op:'zoom',dir:'in'})};document.getElementById('zout').onclick=function(){hide();act({op:'zoom',dir:'out'})};
document.addEventListener('keydown',function(e){var m={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right'};if(m[e.key]){e.preventDefault();hide();act({op:'pan',dir:m[e.key]})}else if(e.key==='+'||e.key==='='){act({op:'zoom',dir:'in'})}else if(e.key==='-'){act({op:'zoom',dir:'out'})}});
function hide(){document.getElementById('pop').style.display='none'}
document.getElementById('s').addEventListener('click',function(e){var r=this.getBoundingClientRect();act({op:'click',x:Math.round(e.clientX-r.left),y:Math.round(e.clientY-r.top)}).then(j=>{if(j.poi){var p=document.getElementById('pop');document.getElementById('pname').textContent=j.poi.name;document.getElementById('pcat').textContent='Category: '+j.poi.cat;document.getElementById('pdist').textContent='Distance to City Hall: '+j.poi.dist+' m';p.style.left=Math.min(680,j.sx+12)+'px';p.style.top=Math.max(8,j.sy-20)+'px';p.style.display='block';p.dataset.id=j.poi.id}else hide()})});
document.getElementById('pclose').onclick=hide;
document.getElementById('route').onclick=function(){act({op:'route',id:parseInt(document.getElementById('pop').dataset.id)}).then(j=>{document.getElementById('pdist').textContent='Route requested: '+j.dist+' m to City Hall'})};
</script>"""


def click(x, y):
    return {"ignored": True}


def post(path, data, ctype):
    if path != "/__act": return None
    v = S["view"]; op = data.get("op")
    if op == "pan":
        step = 600 / v["zoom"]; d = data.get("dir")
        if d == "up": v["cy"] -= step
        elif d == "down": v["cy"] += step
        elif d == "left": v["cx"] -= step
        elif d == "right": v["cx"] += step
        v["cx"] = min(WORLD, max(0, v["cx"])); v["cy"] = min(WORLD, max(0, v["cy"]))
        return (json.dumps({"ok": True, "view": v}), "application/json")
    if op == "zoom":
        v["zoom"] = min(4.0, v["zoom"] * 1.5) if data.get("dir") == "in" else max(1.0, v["zoom"] / 1.5)
        v["zoom"] = round(v["zoom"], 3)
        return (json.dumps({"ok": True, "view": v}), "application/json")
    if op == "click":
        x, y = float(data.get("x", -1)), float(data.get("y", -1)); hit = None
        for p in S["pois"]:
            sx, sy = w2s(p["x"], p["y"])
            if (x - sx) ** 2 + (y - sy) ** 2 <= 12 ** 2: hit = p; break
        if hit:
            S["opened"].append(hit["id"]); sx, sy = w2s(hit["x"], hit["y"])
            return (json.dumps({"poi": {"id": hit["id"], "name": hit["name"], "cat": hit["cat"], "dist": _dist(hit)}, "sx": sx, "sy": sy}), "application/json")
        return (json.dumps({"poi": None}), "application/json")
    if op == "route":
        pid = data.get("id"); p = next((p for p in S["pois"] if p["id"] == pid), None)
        if p: S["routed"].append(pid); return (json.dumps({"ok": True, "dist": _dist(p)}), "application/json")
        return (json.dumps({"ok": False}), "application/json")
    return (json.dumps({"ok": False}), "application/json")


def state():
    t = S["target"]
    return {"target": {"name": t["name"], "cat": t["cat"], "dist_m": _dist(t), "district": district_of(t)},
            "opened": S["opened"], "routed": S["routed"], "view": S["view"],
            "complete": t["id"] in S["opened"] and S["routed"] == [t["id"]]}


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8797)
