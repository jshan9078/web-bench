#!/usr/bin/env python3
"""Shared scaffolding for single-image perception tasks (108-111): an image, a one-field form posting to
/__answer, and a numeric/text check. Each task module sets TITLE, PORT, QUESTION, reset(), draw() -> PIL image,
and check(submission) -> bool; state() exposes the answer for the audit."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base


def make(mod, W, H):
    S = {"submissions": []}
    mod.SUBS = S["submissions"]
    def render(): return base.png(mod.draw())
    def click(x, y): return {"ignored": True}
    def post(path, data, ctype):
        if path == "/__answer":
            S["submissions"].append(str(data.get("answer") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
        return None
    def state():
        st = dict(mod.answer_state()); st["submissions"] = S["submissions"]; st["complete"] = any(mod.check(s) for s in S["submissions"]); return st
    def page():
        return base.image_page(mod.TITLE, W, H, extra_html=f"""
<div style="position:absolute;top:{H + 12}px;left:20px;font:14px system-ui;width:{W - 40}px"><p>{mod.QUESTION}</p><label>Answer <input id=a size=14></label> <button id=go>Submit</button> <span id=msg></span>
<script>document.getElementById('go').onclick=function(){{fetch('/__answer',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{answer:document.getElementById('a').value}})}}).then(r=>r.json()).then(j=>{{document.getElementById('msg').textContent='Submitted ('+j.n+').'}})}}</script></div>""")
    inner = mod.reset
    def reset():
        S["submissions"].clear(); inner()
    mod.render, mod.click, mod.post, mod.state, mod.page, mod.reset = render, click, post, state, page, reset
    return mod


def num(s):
    return float(s.replace("%", "").replace(",", ".").strip().split()[0])
