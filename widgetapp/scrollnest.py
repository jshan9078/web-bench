#!/usr/bin/env python3
"""274-nested-scroll-code: a page with a scrollable panel inside a scrollable panel inside a tall page; a
confirmation code is on a line far down the innermost panel (the DOM contains many decoy codes labelled for other
accounts). Task: report the code for account HB-4471 and enter it. complete = exact code (last submission)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"code": "", "lines": [], "submissions": []}


def reset():
    S["submissions"] = []; S["code"] = "".join(random.choice("ACDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(8)); lines = []
    for i in range(400):
        acct = f"HB-{random.randint(1000, 9999)}"; code = "".join(random.choice("ACDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(8)); lines.append(f"Account {acct}: confirmation {code}")
    lines[random.randint(300, 380)] = f"Account HB-4471: confirmation {S['code']}"
    S["lines"] = lines


def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer": S["submissions"].append(str(data.get("code") or "").strip().upper()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state(): return {"code": S["code"], "submissions": S["submissions"], "complete": bool(S["submissions"]) and S["submissions"][-1] == S["code"]}


def page():
    body = "".join(f"<div class=l>{l}</div>" for l in S["lines"])
    return f"""<!doctype html><meta charset=utf-8><title>Confirmation ledger</title>
<style>body{{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a}}main{{max-width:800px;margin:0 auto;padding:16px}}.spacer{{height:1400px;background:linear-gradient(#f8fafc,#e2e8f0)}}#outer{{height:300px;overflow:auto;border:1px solid #cbd5e1;background:#fff;padding:10px}}#inner{{height:180px;overflow:auto;border:1px solid #e2e8f0;padding:8px;margin-top:900px;font:13px ui-monospace,Menlo,monospace}}.l{{line-height:1.7}}#ans{{margin:16px 0;padding:12px;background:#fff;border:1px solid #e2e8f0;border-radius:8px}}input,button{{font:inherit;padding:6px 8px}}</style>
<main><h1 style="font-size:18px">Confirmation ledger</h1><div id=ans><label>Confirmation code for account HB-4471: <input id=c size=12></label> <button id=go>Submit</button> <span id=msg></span></div><p style="color:#64748b">The ledger panel is further down this page; the account lines are inside the inner panel of that panel.</p><div class=spacer></div>
<div id=outer><p>Ledger panel. Scroll down inside this panel to reach the account list.</p><div id=inner>{body}</div><p style="margin-top:600px">End of panel.</p></div><div class=spacer></div></main>
<script>document.getElementById('go').onclick=function(){{fetch('/__answer',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{code:document.getElementById('c').value}})}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Submitted ('+j.n+').'}})}}</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8932)
