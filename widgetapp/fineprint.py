#!/usr/bin/env python3
"""103-fine-print: a product label photo whose serial number is printed in tiny type, with the usual
e-commerce magnifier (click the image to open a 3x lens at that point). Task: report the serial number.
Traps: at native size the glyphs 3/8/6/5, B/8, S/5, Z/2 are ambiguous; a LOT number and a part number use
similar formats. complete = exact serial (case-insensitive, hyphens optional)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import base
W, H = 1000, 700
S = {"serial": "", "lot": "", "pn": "", "submissions": [], "zooms": 0}


def code(fmt):
    L = "BSZQKRXM"; D = "35862"; out = ""
    for ch in fmt: out += random.choice(L) if ch == "X" else random.choice(D) if ch == "N" else ch
    return out


def reset():
    S["submissions"] = []; S["zooms"] = 0; S["serial"] = code("XXN-NNNNN-XX"); S["lot"] = code("XXN-NNNN-XN"); S["pn"] = code("XN-NNNNN-XX")


def label(scale=1):
    """The label drawn at `scale` x. The displayed photo is the 3x master downsampled (tiny type goes mushy, as in
    a real listing photo); the magnifier crops the master."""
    k = scale; img = Image.new("RGB", (W * k, H * k), (236, 233, 226)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([120 * k, 80 * k, 880 * k, 620 * k], 18 * k, fill=(250, 250, 248), outline=(180, 176, 168), width=3 * k)
    d.text((160 * k, 110 * k), "NORTHWIND", fill=(30, 41, 59), font=base.font(54 * k)); d.text((160 * k, 176 * k), "Compact Air Purifier, Model AP-220", fill=(60, 60, 70), font=base.font(24 * k, False))
    for i in range(48): d.rectangle([(160 + i * 9) * k, 250 * k, (160 + i * 9 + random.Random(i * 7).choice([2, 3, 5])) * k, 330 * k], fill=(20, 20, 20))
    d.text((160 * k, 340 * k), "Input 100-240 V ~ 50/60 Hz   0.6 A   Made in Portugal", fill=(70, 70, 80), font=base.font(16 * k, False))
    f7 = base.font(7 * k, False); y = 470 * k
    for ln in [f"LOT {S['lot']}    MFG 2026-06", f"PN {S['pn']}    REV C", f"S/N {S['serial']}", "Certified to EN 60335-1. Do not cover. Indoor use only. Keep away from water.", "Recycle in accordance with local regulations. Contains no user-serviceable parts."]:
        d.text((560 * k, y), ln, fill=(90, 90, 100), font=f7); y += 12 * k
    d.rectangle([160 * k, 460 * k, 520 * k, 560 * k], outline=(180, 176, 168), width=k); d.text((176 * k, 480 * k), "QC PASSED", fill=(37, 99, 235), font=base.font(28 * k)); d.text((176 * k, 520 * k), "Inspector 14", fill=(120, 120, 130), font=base.font(14 * k, False))
    return img


def photo():
    return label(3).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))


def render(): return base.png(photo())
def click(x, y): return {"ignored": True}


def get(path, full):
    if path == "/__zoom.png":
        q = dict(kv.split("=") for kv in full.split("?", 1)[1].split("&") if "=" in kv) if "?" in full else {}
        try: x, y = int(float(q.get("x", W // 2))), int(float(q.get("y", H // 2)))
        except ValueError: x, y = W // 2, H // 2
        S["zooms"] += 1; z = 3; bw, bh = 320 // z, 200 // z
        x0, y0 = max(0, min(W - 2 * bw, x - bw)), max(0, min(H - 2 * bh, y - bh))
        crop = label(3).crop((x0 * 3, y0 * 3, (x0 + 2 * bw) * 3, (y0 + 2 * bh) * 3))
        return (base.png(crop), "image/png")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("serial") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    norm = lambda s: s.upper().replace("-", "").replace(" ", "")
    return {"serial": S["serial"], "lot": S["lot"], "pn": S["pn"], "zooms": S["zooms"], "submissions": S["submissions"], "complete": any(norm(s) == norm(S["serial"]) for s in S["submissions"])}


def page():
    return f"""<!doctype html><meta charset=utf-8><title>AP-220 label photo</title>
<style>body{{font:14px system-ui;margin:0;background:#fff;color:#111}}#wrap{{position:relative;width:1000px;margin:0 auto}}#s{{display:block;cursor:zoom-in}}#lens{{position:absolute;display:none;border:2px solid #111;box-shadow:0 4px 16px rgba(0,0,0,.3);background:#fff}}
#ans{{width:960px;margin:12px auto;padding:12px;background:#f3f4f6;border-radius:8px}}input,button{{font:inherit;padding:6px 8px}}.note{{color:#6b7280;font-size:13px;width:1000px;margin:8px auto}}</style>
<p class=note>Product label, listing photo 3 of 6. Click anywhere on the photo to magnify that area; click the magnified view to close it.</p>
<div id=wrap><img id=s src="/__scene.png" width=1000 height=700 alt="product label"><img id=lens width=640 height=400 alt="magnified"></div>
<div id=ans><label>Serial number (S/N): <input id=sn size=18></label> <button id=go>Submit</button> <span id=msg></span></div>
<script>(function(){{var s=document.getElementById('s'),l=document.getElementById('lens');s.onclick=function(e){{var r=s.getBoundingClientRect(),x=Math.round(e.clientX-r.left),y=Math.round(e.clientY-r.top);l.src='/__zoom.png?x='+x+'&y='+y+'&t='+Date.now();l.style.left=Math.max(0,Math.min(360,x-320))+'px';l.style.top=Math.max(0,Math.min(300,y-200))+'px';l.style.display='block'}};l.onclick=function(){{l.style.display='none'}};
document.getElementById('go').onclick=function(){{fetch('/__answer',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{serial:document.getElementById('sn').value}})}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Submitted ('+j.n+').'}})}}}})();</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8823)
