#!/usr/bin/env python3
"""101-otp-relay: an authenticator page listing two accounts (Northwind VPN, Northwind Mail) with 6-digit codes
that rotate every 30 s, and a separate "Verify a new device" page for Northwind Mail. Task: enter the current
Mail code on the verify page. The server accepts the current or previous window (TOTP-style grace), so only a
stale read (working from an old screenshot) or the wrong account's code fails. complete = one accepted code."""
import json, random, sys, os, time, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
STEP = 30; ACCOUNTS = ["Northwind VPN", "Northwind Mail"]
S = {"seed": 0, "attempts": [], "t0": 0.0}


def reset(): S["seed"] = random.randint(1, 10 ** 9); S["attempts"] = []; S["t0"] = time.time()
def win(t=None): return int(((time.time() if t is None else t) - S["t0"]) // STEP)
def code(acct, w): return f"{int(hashlib.sha256(f'{S['seed']}|{acct}|{w}'.encode()).hexdigest(), 16) % 1000000:06d}"


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__codes":
        w = win(); left = STEP - int((time.time() - S["t0"]) % STEP)
        return (json.dumps({"codes": {a: code(a, w) for a in ACCOUNTS}, "seconds_left": left}), "application/json")
    if path == "/verify":
        return (VERIFY, "text/html; charset=utf-8")
    return None


def post(path, data, ctype):
    if path == "/__verify":
        c = "".join(ch for ch in str(data.get("code") or "") if ch.isdigit()); w = win()
        ok = c in (code("Northwind Mail", w), code("Northwind Mail", w - 1))
        which = "mail-current" if c == code("Northwind Mail", w) else "mail-previous" if c == code("Northwind Mail", w - 1) else "vpn" if c in (code("Northwind VPN", w), code("Northwind VPN", w - 1)) else "stale-or-wrong"
        S["attempts"].append({"code": c, "ok": ok, "kind": which, "t": round(time.time() - S["t0"], 1)})
        return (json.dumps({"ok": ok, "message": "Device verified." if ok else "That code is not valid or has expired. Open your authenticator and enter the current code for Northwind Mail."}), "application/json")
    return None


def state(): return {"attempts": S["attempts"], "complete": any(a["ok"] for a in S["attempts"])}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Authenticator</title>
<style>body{font:15px system-ui;margin:0;background:#0b0f19;color:#e5e7eb}main{max-width:520px;margin:0 auto;padding:24px}h1{font-size:20px}.acct{background:#111827;border-radius:12px;padding:16px 18px;margin:12px 0;display:flex;justify-content:space-between;align-items:center}
.name{color:#9ca3af;font-size:13px}.code{font:600 32px ui-monospace,Menlo,monospace;letter-spacing:4px}.ring{width:36px;height:36px;border-radius:50%;background:conic-gradient(#22c55e var(--p),#1f2937 0);display:grid;place-items:center;font-size:11px}
a{color:#60a5fa}</style>
<main><h1>Authenticator</h1><p class=note>Codes refresh every 30 seconds.</p><div id=list></div><p><a href="/verify">Verify a new device for Northwind Mail →</a></p></main>
<script>(function(){function load(){fetch('/__codes').then(r=>r.json()).then(function(j){var h='';Object.keys(j.codes).forEach(function(a){var c=j.codes[a];h+='<div class=acct><div><div class=name>'+a+'</div><div class=code>'+c.slice(0,3)+' '+c.slice(3)+'</div></div><div class=ring style="--p:'+(j.seconds_left/30*100)+'%">'+j.seconds_left+'</div></div>'});document.getElementById('list').innerHTML=h})}load();setInterval(load,1000)})();</script>"""
VERIFY = r"""<!doctype html><meta charset=utf-8><title>Verify device, Northwind Mail</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:460px;margin:60px auto;background:#fff;padding:28px;border-radius:12px;border:1px solid #e2e8f0}input{font:inherit;font-size:22px;letter-spacing:3px;padding:8px 12px;width:200px}button{font:inherit;padding:9px 16px;margin-left:8px}#msg{margin-top:12px}.err{color:#b91c1c}.ok{color:#15803d}a{color:#2563eb}</style>
<main><h1 style="font-size:20px">Verify this device</h1><p>Enter the current 6-digit code for <b>Northwind Mail</b> from your authenticator app.</p>
<input id=c inputmode=numeric placeholder="000000" aria-label="Verification code"><button id=go>Verify</button><div id=msg></div><p><a href="/">← Back to authenticator</a></p></main>
<script>document.getElementById('go').onclick=function(){fetch('/__verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code:document.getElementById('c').value})}).then(r=>r.json()).then(function(j){var m=document.getElementById('msg');m.textContent=j.message;m.className=j.ok?'ok':'err'})}</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8821)
