#!/usr/bin/env python3
"""Scaffold for image-only interactive apps (kiosks, trays, panels): the UI is a server-rendered image; clicks are
posted in image coordinates; the page reloads the image after each click. A module provides reset(), draw() -> PIL
image, hit(x, y) (mutates state), state() -> dict with complete, TITLE, W, H, NOTE (text under the image)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base


def make(mod):
    def render(): return base.png(mod.draw())
    def click(x, y): mod.hit(x, y); return {"ok": True}
    def post(path, data, ctype): return None
    def page():
        return base.image_page(mod.TITLE, mod.W, mod.H, extra_html=f"""
<div style="position:absolute;top:{mod.H + 10}px;left:20px;font:14px system-ui;width:{max(400, mod.W - 40)}px"><p>{mod.NOTE}</p>
<script>document.getElementById('s').addEventListener('click',function(){{setTimeout(function(){{document.getElementById('s').src='/__scene.png?'+Date.now()}},150)}})</script></div>""")
    mod.render, mod.click, mod.post, mod.page = render, click, post, page
    return mod


def inside(x, y, box): return box[0] <= x <= box[2] and box[1] <= y <= box[3]
