#!/usr/bin/env python3
"""270-shadow-iframe-form: a form whose fields live three levels deep: inside an open shadow root, inside a
same-origin iframe, inside another shadow root, with labels provided via slots. Task: fill four fields with given
values and submit the innermost form. complete = submitted values match."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"submitted": None}
WANT = {"ref": "HB-7731", "qty": "14", "contact": "ana.silva@example.com", "note": "leave at reception"}


def reset(): S["submitted"] = None
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/inner": return (INNER, "text/html; charset=utf-8")
    return None


def post(path, data, ctype):
    if path == "/__submit": S["submitted"] = {k: str(data.get(k) or "").strip() for k in WANT}; return (json.dumps({"ok": True}), "application/json")
    return None


def state(): return {"submitted": S["submitted"], "want": WANT, "complete": S["submitted"] == WANT}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Delivery request</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:720px;margin:24px auto}</style>
<main><h1 style="font-size:18px">Delivery request</h1><p>Complete the request form below.</p><x-panel id=p></x-panel></main>
<script>(function(){var host=document.getElementById('p');var root=host.attachShadow({mode:'open'});root.innerHTML='<style>.card{border:1px solid #e2e8f0;border-radius:10px;padding:14px;background:#fff}</style><div class=card><b>Request details</b><iframe src="/inner" style="width:100%;height:360px;border:0;margin-top:10px" title="request form"></iframe></div>'})();</script>"""
INNER = r"""<!doctype html><meta charset=utf-8><style>body{font:14px system-ui;margin:0;color:#0f172a}</style><x-form id=f></x-form>
<script>(function(){var host=document.getElementById('f');var root=host.attachShadow({mode:'open'});root.innerHTML='<style>label{display:block;margin:8px 0}input,button{font:inherit;padding:6px 8px}</style><label><slot name=l1>Reference</slot> <input id=ref></label><label><slot name=l2>Quantity</slot> <input id=qty></label><label><slot name=l3>Contact email</slot> <input id=contact></label><label><slot name=l4>Delivery note</slot> <input id=note size=30></label><button id=go>Submit request</button> <span id=msg></span>';
 root.getElementById('go').onclick=function(){var b={};['ref','qty','contact','note'].forEach(function(k){b[k]=root.getElementById(k).value});fetch('/__submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}).then(function(){root.getElementById('msg').textContent='Submitted'})}})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8931)
