#!/usr/bin/env python3
"""76-settings-maze: an account-settings app with the DOM hazards agents meet on real products.
- Top-level tabs (Profile / Notifications / Billing / Security), a nested tab strip inside Notifications,
  and an accordion inside Security.
- The "Two-step verification" toggle lives inside a custom element with a SHADOW ROOT inside an IFRAME.
- Every change marks the page dirty; navigating between top-level tabs with unsaved changes opens an
  "Unsaved changes" modal (Discard / Keep editing); Save is only in the sticky footer and is disabled
  until something changed; a success toast confirms; autosave is OFF (a fake "autosaved" hint exists).
- Decoys: "Email digest" (weekly) vs "Email alerts", and a Billing email that must NOT be changed.
Task: set Notifications > Email > digest frequency to Monthly, turn Security > Two-step verification ON,
change the display name to "J. Halvorsen", save. complete = saved state has exactly those three
changes and nothing else changed. /__save is the page endpoint; state/reset token-gated."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base

DEFAULTS = {"display_name": "Jon Halvorsen", "digest": "Weekly", "alerts": True, "push": False, "billing_email": "billing@halvorsen.example",
            "twostep": False, "sessions_timeout": "30 min", "marketing": False}
TARGET = {"display_name": "J. Halvorsen", "digest": "Monthly", "twostep": True}
LEVEL = int(os.environ.get("WIDGET_LEVEL", "2"))
S = {"saved": dict(DEFAULTS), "saves": []}


def reset():
    S["saved"] = dict(DEFAULTS); S["saves"] = []


def render():
    return b""


def click(x, y):
    return {"ignored": True}


def get(path):
    if path == "/__settings":
        return (json.dumps(S["saved"]), "application/json")
    if path == "/__frame":
        return (FRAME, "text/html; charset=utf-8")
    return None


def post(path, data, ctype):
    if path == "/__save":
        new = dict(S["saved"])
        for k in DEFAULTS:
            if k in data: new[k] = data[k]
        S["saved"] = new; S["saves"].append(new)
        return (json.dumps({"ok": True}), "application/json")
    return None


def state():
    want = dict(DEFAULTS); want.update(TARGET)
    return {"level": LEVEL, "saved": S["saved"], "expected": want, "n_saves": len(S["saves"]), "complete": S["saved"] == want}


FRAME = """<!doctype html><meta charset=utf-8><style>body{font:14px system-ui;margin:12px}</style>
<p><b>Two-step verification</b> adds a code from your authenticator app at sign-in.</p>
<x-toggle id=twostep label="Two-step verification"></x-toggle>
<script>
class XToggle extends HTMLElement{constructor(){super();var r=this.attachShadow({mode:'open'});r.innerHTML='<style>button{font:14px system-ui;padding:6px 12px;border-radius:999px;border:1px solid #888;background:#eee;cursor:pointer}button[aria-checked=true]{background:#1f7a3a;color:#fff;border-color:#1f7a3a}</style><button role=switch aria-checked=false aria-label="'+(this.getAttribute('label')||'toggle')+'">Off</button>';
 var b=r.querySelector('button');b.onclick=()=>{var on=b.getAttribute('aria-checked')!=='true';b.setAttribute('aria-checked',on);b.textContent=on?'On':'Off';parent.postMessage({type:'twostep',value:on},'*')}}
 set value(v){var b=this.shadowRoot.querySelector('button');b.setAttribute('aria-checked',!!v);b.textContent=v?'On':'Off'}}
customElements.define('x-toggle',XToggle);
window.addEventListener('message',e=>{if(e.data&&e.data.type==='init'){document.getElementById('twostep').value=e.data.twostep}});
parent.postMessage({type:'ready'},'*');
</script>"""


def page():
    return PAGE.replace("__LEVEL__", str(LEVEL))


PAGE = r"""<!doctype html><meta charset=utf-8><title>Account Settings</title>
<style>body{font:14px system-ui;margin:0;background:#f7f7f8;color:#222}header{padding:14px 22px;background:#fff;border-bottom:1px solid #e5e5e5;font-weight:600}
.tabs{display:flex;gap:4px;padding:10px 22px 0}.tabs button{font:inherit;padding:8px 14px;border:1px solid transparent;border-bottom:0;background:transparent;cursor:pointer;border-radius:8px 8px 0 0}
.tabs button[aria-selected=true]{background:#fff;border-color:#e5e5e5}.panel{background:#fff;margin:0 22px;padding:18px;border:1px solid #e5e5e5;border-top:0;min-height:320px}
.sub{display:flex;gap:14px;border-bottom:1px solid #eee;margin-bottom:12px}.sub button{font:inherit;background:none;border:0;padding:6px 2px;cursor:pointer;border-bottom:2px solid transparent}.sub button[aria-selected=true]{border-bottom-color:#222;font-weight:600}
label{display:block;margin:10px 0}input,select{font:inherit;padding:6px 8px}.acc h4{margin:0;padding:10px;border:1px solid #e5e5e5;cursor:pointer;background:#fafafa}.acc .body{display:none;padding:12px;border:1px solid #e5e5e5;border-top:0}.acc.open .body{display:block}
footer{position:sticky;bottom:0;background:#fff;border-top:1px solid #e5e5e5;padding:12px 22px;display:flex;gap:12px;align-items:center}footer button{font:inherit;padding:8px 16px;border-radius:6px;border:1px solid #888;background:#fff;cursor:pointer}
footer .primary{background:#1f2937;color:#fff;border-color:#1f2937}footer button:disabled{opacity:.45}.hint{color:#777;font-size:12px}
#modal{position:fixed;inset:0;background:rgba(0,0,0,.4);display:none}#modal .box{background:#fff;width:380px;margin:14% auto;padding:20px;border-radius:8px}#toast{position:fixed;bottom:70px;left:50%;transform:translateX(-50%);background:#1f2937;color:#fff;padding:10px 16px;border-radius:8px;display:none}
iframe{width:100%;height:120px;border:1px solid #e5e5e5;border-radius:6px}</style>
<header>Account settings</header>
<div class=tabs role=tablist><button role=tab data-t=profile aria-selected=true>Profile</button><button role=tab data-t=notifications aria-selected=false>Notifications</button><button role=tab data-t=billing aria-selected=false>Billing</button><button role=tab data-t=security aria-selected=false>Security</button></div>
<div class=panel>
 <section id=profile><h3>Profile</h3><label>Display name <input id=display_name></label><label>Marketing emails <input type=checkbox id=marketing></label></section>
 <section id=notifications hidden><h3>Notifications</h3><div class=sub role=tablist><button role=tab data-s=email aria-selected=true>Email</button><button role=tab data-s=push aria-selected=false>Push</button></div>
  <div id=sub-email><label>Email alerts (immediate) <input type=checkbox id=alerts></label><label>Email digest frequency <select id=digest><option>Daily</option><option>Weekly</option><option>Monthly</option><option>Never</option></select></label></div>
  <div id=sub-push hidden><label>Push notifications <input type=checkbox id=push></label></div></section>
 <section id=billing hidden><h3>Billing</h3><label>Billing email <input id=billing_email></label><p class=hint>Changes to the billing email trigger a verification email.</p></section>
 <section id=security hidden><h3>Security</h3>
  <div class=acc id=acc1><h4>Session timeout</h4><div class=body><label>Sign out after <select id=sessions_timeout><option>15 min</option><option>30 min</option><option>1 hour</option></select></label></div></div>
  <div class=acc id=acc2><h4>Two-step verification</h4><div class=body><iframe id=tsf src="/__frame" title="Two-step verification"></iframe></div></div></section>
</div>
<footer><button id=save class=primary disabled>Save changes</button><button id=discard disabled>Discard</button><span class=hint id=status>All changes saved</span><span class=hint style="margin-left:auto">Autosave is off</span></footer>
<div id=modal><div class=box><h3>Unsaved changes</h3><p>You have unsaved changes on this tab. Leaving will discard them.</p><button id=keep>Keep editing</button> <button id=leave>Discard and leave</button></div></div>
<div id=toast role=status></div>
<div id=review style="position:fixed;inset:0;background:rgba(0,0,0,.4);display:none"><div style="background:#fff;width:420px;margin:12% auto;padding:20px;border-radius:8px">
 <h3 style="margin-top:0">Review changes</h3><ul id=reviewlist></ul><label><input type=checkbox id=applybilling checked> Also use the new display name for billing contact (updates billing email)</label><p><button id=reviewok class=primary>Confirm and save</button> <button id=reviewcancel>Back</button></p></div></div>
<script>
var LEVEL=__LEVEL__;
var saved={},cur={},dirty=false,pendingTab=null,frameReady=false;
fetch('/__settings').then(r=>r.json()).then(j=>{saved=j;cur=Object.assign({},j);paint()});
function paint(){display_name.value=cur.display_name;marketing.checked=cur.marketing;alerts.checked=cur.alerts;digest.value=cur.digest;push.checked=cur.push;billing_email.value=cur.billing_email;sessions_timeout.value=cur.sessions_timeout;if(frameReady)document.getElementById('tsf').contentWindow.postMessage({type:'init',twostep:cur.twostep},'*');setDirty(JSON.stringify(cur)!==JSON.stringify(saved))}
function setDirty(d){dirty=d;save.disabled=!d;discard.disabled=!d;status.textContent=d?'Unsaved changes':'All changes saved'}
function bind(id,key,prop){document.getElementById(id).addEventListener('change',function(){cur[key]=this[prop];setDirty(true)})}
bind('display_name','display_name','value');bind('marketing','marketing','checked');bind('alerts','alerts','checked');bind('digest','digest','value');bind('push','push','checked');bind('billing_email','billing_email','value');bind('sessions_timeout','sessions_timeout','value');
window.addEventListener('message',e=>{if(!e.data)return;if(e.data.type==='ready'){frameReady=true;document.getElementById('tsf').contentWindow.postMessage({type:'init',twostep:cur.twostep},'*')}else if(e.data.type==='twostep'){cur.twostep=e.data.value;setDirty(true)}});
function showTab(t){document.querySelectorAll('.tabs [role=tab]').forEach(b=>b.setAttribute('aria-selected',b.dataset.t===t));['profile','notifications','billing','security'].forEach(s=>document.getElementById(s).hidden=s!==t)}
document.querySelectorAll('.tabs [role=tab]').forEach(b=>b.onclick=function(){if(dirty){pendingTab=this.dataset.t;modal.style.display='block';return}showTab(this.dataset.t)});
keep.onclick=function(){modal.style.display='none';pendingTab=null};
leave.onclick=function(){modal.style.display='none';cur=Object.assign({},saved);paint();showTab(pendingTab);pendingTab=null};
document.querySelectorAll('.sub [role=tab]').forEach(b=>b.onclick=function(){document.querySelectorAll('.sub [role=tab]').forEach(x=>x.setAttribute('aria-selected',x===this));document.getElementById('sub-email').hidden=this.dataset.s!=='email';document.getElementById('sub-push').hidden=this.dataset.s!=='push'});
document.querySelectorAll('.acc h4').forEach(h=>h.onclick=function(){this.parentElement.classList.toggle('open')});
discard.onclick=function(){cur=Object.assign({},saved);paint()};
function doSave(){fetch('/__save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(cur)}).then(r=>r.json()).then(()=>{saved=Object.assign({},cur);setDirty(false);toast.textContent='Settings saved';toast.style.display='block';setTimeout(()=>toast.style.display='none',2500)})}
save.onclick=function(){if(LEVEL<2){doSave();return}var ul=document.getElementById('reviewlist');ul.innerHTML='';Object.keys(cur).forEach(k=>{if(JSON.stringify(cur[k])!==JSON.stringify(saved[k])){var li=document.createElement('li');li.textContent=k+': '+saved[k]+' → '+cur[k];ul.appendChild(li)}});document.getElementById('applybilling').checked=true;document.getElementById('review').style.display='block'};
reviewcancel.onclick=function(){document.getElementById('review').style.display='none'};
reviewok.onclick=function(){if(document.getElementById('applybilling').checked){cur.billing_email=cur.display_name.toLowerCase().replace(/[^a-z]+/g,'.').replace(/^\.|\.$/g,'')+'@halvorsen.example'}document.getElementById('review').style.display='none';doSave()};
</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8798)
