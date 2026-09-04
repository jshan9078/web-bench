#!/usr/bin/env python3
"""264-password-reset: a sign-in page with "Forgot password", a separate in-app mail inbox page (/mail) where the
reset code arrives (among other messages, including an older expired code), and a new-password form with rules.
Task: reset the password for the given account to the given value and sign in. complete = signed in with the
new password."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"codes": [], "pw": "Old-Pass-1", "signed_in": False, "log": []}


def reset(): S["codes"] = []; S["pw"] = "Old-Pass-1"; S["signed_in"] = False; S["log"] = []


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/mail": return (MAIL, "text/html; charset=utf-8")
    if path == "/__mail":
        msgs = [{"from": "Northwind Weekly", "subj": "Digest", "body": "What shipped this week.", "t": "08:10"}, {"from": "Harbor Portal", "subj": "Your reset code", "body": "Your password reset code is 118204. It expires in 15 minutes.", "t": "08:31 (yesterday)"}]
        for c in S["codes"]: msgs.append({"from": "Harbor Portal", "subj": "Your reset code", "body": f"Your password reset code is {c}. It expires in 15 minutes.", "t": "just now"})
        msgs.append({"from": "IT Helpdesk", "subj": "Reminder", "body": "Passwords must be at least 12 characters with a digit and a symbol.", "t": "09:02"})
        return (json.dumps({"msgs": msgs}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__request": c = f"{random.randint(100000, 999999)}"; S["codes"].append(c); return (json.dumps({"ok": True}), "application/json")
    if path == "/__setpw":
        code = str(data.get("code") or ""); pw = str(data.get("pw") or ""); S["log"].append({"code": code})
        if not S["codes"] or code != S["codes"][-1]: return (json.dumps({"ok": False, "error": "Invalid or expired code"}), "application/json")
        if len(pw) < 12 or not any(ch.isdigit() for ch in pw) or not any(not ch.isalnum() for ch in pw): return (json.dumps({"ok": False, "error": "Password must be at least 12 characters with a digit and a symbol"}), "application/json")
        S["pw"] = pw; return (json.dumps({"ok": True}), "application/json")
    if path == "/__login":
        ok = str(data.get("user")) == "ana.silva" and str(data.get("pw")) == S["pw"]; S["signed_in"] = S["signed_in"] or ok; return (json.dumps({"ok": ok}), "application/json")
    return None


def state(): return {"pw": S["pw"], "codes": S["codes"], "signed_in": S["signed_in"], "complete": S["signed_in"] and S["pw"] == "Harbor-2026-secure!"}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Harbor Portal, sign in</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:420px;margin:40px auto;background:#fff;padding:24px;border-radius:12px;border:1px solid #e2e8f0}label{display:block;margin:8px 0}input,button{font:inherit;padding:7px 9px;width:100%;box-sizing:border-box}button{width:auto;cursor:pointer}.err{color:#b91c1c}.ok{color:#15803d}a{color:#2563eb}.note{color:#64748b;font-size:13px}</style>
<main id=m></main>
<script>(function(){var m=document.getElementById('m'),view='login';
function render(){if(view==='login'){m.innerHTML='<h1 style="font-size:19px">Sign in</h1><label>Username <input id=u></label><label>Password <input id=p type=password></label><button id=go>Sign in</button> <a href="#" id=fp>Forgot password?</a><div id=msg></div><p class=note>Check your messages at <a href="/mail">/mail</a>.</p>';document.getElementById('fp').onclick=function(e){e.preventDefault();view='forgot';render()};document.getElementById('go').onclick=function(){fetch('/__login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:u.value,pw:p.value})}).then(r=>r.json()).then(function(j){var d=document.getElementById('msg');d.textContent=j.ok?'Signed in. Welcome, Ana.':'Wrong username or password.';d.className=j.ok?'ok':'err'})}}
 else if(view==='forgot'){m.innerHTML='<h1 style="font-size:19px">Reset password</h1><label>Username <input id=u value="ana.silva"></label><button id=send>Send reset code</button><div id=msg></div><p class=note>The code is sent to your inbox at <a href="/mail">/mail</a>. Then enter it below.</p><label>Code <input id=c></label><label>New password <input id=np type=password></label><button id=rs>Set new password</button> <a href="#" id=back>Back to sign in</a>';
  document.getElementById('send').onclick=function(){fetch('/__request',{method:'POST'}).then(function(){document.getElementById('msg').textContent='Code sent.'})};document.getElementById('rs').onclick=function(){fetch('/__setpw',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code:c.value,pw:np.value})}).then(r=>r.json()).then(function(j){var d=document.getElementById('msg');d.textContent=j.ok?'Password updated. Sign in with it.':j.error;d.className=j.ok?'ok':'err'})};document.getElementById('back').onclick=function(e){e.preventDefault();view='login';render()}}}
render()})();</script>"""
MAIL = r"""<!doctype html><meta charset=utf-8><title>Inbox</title><style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}main{max-width:640px;margin:30px auto}.m{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin:8px 0}.t{color:#64748b;font-size:12px}</style>
<main><h1 style="font-size:19px">Inbox</h1><p><a href="/">Back to sign in</a> · <a href="/mail">Refresh</a></p><div id=l></div></main>
<script>fetch('/__mail').then(r=>r.json()).then(function(j){document.getElementById('l').innerHTML=j.msgs.slice().reverse().map(function(x){return '<div class=m><b>'+x.subj+'</b> <span class=t>'+x.from+' · '+x.t+'</span><div>'+x.body+'</div></div>'}).join('')})</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8922)
