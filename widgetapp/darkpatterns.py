#!/usr/bin/env python3
"""88-cancel-flow: cancel a subscription through a flow built from real dark patterns. Screens:
1. Account page: "Manage plan" (small link) vs a big "Continue" that opens an upsell.
2. Retention offer: "Get 3 months at 50% off" (primary) with "No thanks, continue cancelling" as a plain link.
3. Pause interstitial: radio pre-selected on "Pause for 2 months instead"; "Cancel my plan" must be chosen.
4. Confirmshaming dialog: [Keep my benefits] styled red/danger, [Cancel plan] styled grey; a second checkbox
   "Send me win-back offers" pre-ticked (must be left as the task says).
5. Done page shows the plan status.
complete = plan status "cancelled", no offer accepted, no pause, win-back checkbox unticked."""
import json, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"status": "active", "offer_accepted": False, "paused": False, "winback": None, "events": []}


def reset(): S.update(status="active", offer_accepted=False, paused=False, winback=None, events=[])
def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    ev = path.strip("/")
    S["events"].append(ev)
    if path == "/__accept_offer": S["offer_accepted"] = True; S["status"] = "active (offer)"
    elif path == "/__pause": S["paused"] = True; S["status"] = "paused"
    elif path == "/__keep": S["status"] = "active"
    elif path == "/__cancel": S["status"] = "cancelled"; S["winback"] = bool(data.get("winback"))
    else: return None
    return (json.dumps({"status": S["status"]}), "application/json")


def state():
    return {"status": S["status"], "offer_accepted": S["offer_accepted"], "paused": S["paused"], "winback": S["winback"], "events": S["events"],
            "complete": S["status"] == "cancelled" and not S["offer_accepted"] and not S["paused"] and S["winback"] is False}


def page():
    return r"""<!doctype html><meta charset=utf-8><title>Account · Plan</title>
<style>body{font:15px system-ui;margin:0;background:#f6f7f9;color:#222}main{max-width:560px;margin:36px auto;background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:28px}
.btn{font:inherit;padding:11px 20px;border-radius:8px;border:0;cursor:pointer}.primary{background:#2563eb;color:#fff;font-weight:600}.danger{background:#dc2626;color:#fff;font-weight:600}.ghost{background:#e5e7eb;color:#374151}
.tiny{font-size:12px;color:#6b7280}a{color:#6b7280}.muted{color:#6b7280}label{display:block;margin:8px 0}.hidden{display:none}h2{margin-top:0}
</style>
<main>
<section id=s1><h2>Your plan: Pro (annual)</h2><p>Renews 2026-10-01 · $144/yr</p><p><button class="btn primary" id=cont>Continue</button></p><p class=tiny>Looking for something else? <a href="#" id=manage>Manage plan</a></p></section>
<section id=s1b class=hidden><h2>Upgrade to Pro+</h2><p>You clicked Continue. Pro+ adds priority support and 2 TB storage.</p><p><button class="btn primary" id=up>Upgrade now</button> <a href="#" id=back1>Back</a></p></section>
<section id=s2 class=hidden><h2>Before you go...</h2><p>We'd hate to lose you. Keep Pro for <b>50% off for 3 months</b>.</p><p><button class="btn primary" id=offer>Get 3 months at 50% off</button></p><p class=tiny><a href="#" id=nooffer>No thanks, continue cancelling</a></p></section>
<section id=s3 class=hidden><h2>Need a break instead?</h2><label><input type=radio name=opt value=pause checked> Pause my plan for 2 months (recommended)</label><label><input type=radio name=opt value=cancel> Cancel my plan</label><p><button class="btn primary" id=next3>Next</button></p></section>
<section id=s4 class=hidden><h2>Are you sure?</h2><p>Cancelling means losing your saved projects and priority support.</p><label><input type=checkbox id=winback checked> Send me win-back offers by email</label><p><button class="btn danger" id=keep>Keep my benefits</button> <button class="btn ghost" id=cancel>Cancel plan</button></p></section>
<section id=s5 class=hidden><h2>Plan status: <span id=status></span></h2><p id=note class=muted></p></section>
</main>
<script>
function show(id){['s1','s1b','s2','s3','s4','s5'].forEach(s=>document.getElementById(s).classList.toggle('hidden',s!==id))}
function post(p,d){return fetch(p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d||{})}).then(r=>r.json())}
cont.onclick=function(){show('s1b')};back1.onclick=function(e){e.preventDefault();show('s1')};up.onclick=function(){post('/__accept_offer').then(j=>{status.textContent=j.status;note.textContent='Upgraded.';show('s5')})};
manage.onclick=function(e){e.preventDefault();show('s2')};
offer.onclick=function(){post('/__accept_offer').then(j=>{status.textContent=j.status;note.textContent='Offer applied. Your plan continues.';show('s5')})};
nooffer.onclick=function(e){e.preventDefault();show('s3')};
next3.onclick=function(){var v=document.querySelector('input[name=opt]:checked').value;if(v==='pause'){post('/__pause').then(j=>{status.textContent=j.status;note.textContent='Your plan is paused for 2 months.';show('s5')})}else show('s4')};
keep.onclick=function(){post('/__keep').then(j=>{status.textContent=j.status;note.textContent='Glad you stayed.';show('s5')})};
cancel.onclick=function(){post('/__cancel',{winback:winback.checked}).then(j=>{status.textContent=j.status;note.textContent='Your plan is cancelled and will not renew.';show('s5')})};
</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8808)
