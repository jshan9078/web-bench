#!/usr/bin/env python3
"""81-memory-flow: a five-step device-pairing flow with no way back. Step 1 shows a pairing code; steps 2-4
are unrelated (room choice, two toggles, a notice); step 5 asks for the code from step 1 and the room
chosen in step 2. Reloading or revisiting step 1 issues a NEW code and restarts the flow. A decoy "device
serial" on step 3 looks like a code. complete = the final submission carries the code that was current
for that flow instance and the room actually chosen in it."""
import json, random, sys, os, string
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
ROOMS = ["Kitchen", "Living room", "Office", "Bedroom", "Garage", "Hallway"]
S = {"instance": 0, "code": None, "room_wanted": None, "serial": None, "chosen": {}, "submissions": []}


def _code(): return "".join(random.choice("ACDEFGHJKLMNPQRTUVWXY2346789") for _ in range(6))


def reset():
    S["instance"] = 0; S["code"] = None; S["room_wanted"] = random.choice(ROOMS); S["serial"] = None; S["chosen"] = {}; S["submissions"] = []


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__start":           # a fresh flow instance: new code, everything else cleared
        S["instance"] += 1; S["code"] = _code(); S["serial"] = "SN-" + "".join(random.choice(string.digits) for _ in range(8)); S["chosen"] = {}
        return (json.dumps({"instance": S["instance"], "code": S["code"], "serial": S["serial"], "room_wanted": S["room_wanted"]}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__choose":
        S["chosen"][str(data.get("field"))] = data.get("value"); return ('{"ok":true}', "application/json")
    if path == "/__finish":
        rec = {"instance": data.get("instance"), "code": str(data.get("code") or "").strip().upper(), "room": data.get("room"),
               "code_valid": S["code"], "room_chosen": S["chosen"].get("room")}
        S["submissions"].append(rec); return (json.dumps({"ok": True, "ref": "PAIR-%04d" % random.randint(0, 9999)}), "application/json")
    return None


def state():
    ok = False
    last = S["submissions"][-1] if S["submissions"] else None
    if last and last["instance"] == S["instance"] and last["code"] == S["code"] and last["room"] == S["chosen"].get("room") and last["room"] == S["room_wanted"]:
        ok = True
    return {"instance": S["instance"], "code": S["code"], "room_wanted": S["room_wanted"], "chosen": S["chosen"], "submissions": S["submissions"], "complete": ok}


def page():
    return r"""<!doctype html><meta charset=utf-8><title>Device Pairing</title>
<style>body{font:15px system-ui;margin:0;background:#fafafa;color:#222}main{max-width:560px;margin:40px auto;background:#fff;border:1px solid #e5e5e5;border-radius:10px;padding:26px}
.code{font:600 30px ui-monospace,Menlo,monospace;letter-spacing:.2em;background:#f1f5f9;padding:12px;border-radius:8px;text-align:center;margin:12px 0}.muted{color:#777;font-size:13px}
button{font:inherit;padding:8px 16px;border-radius:6px;border:1px solid #888;background:#fff;cursor:pointer}.primary{background:#1f2937;color:#fff;border-color:#1f2937}label{display:block;margin:10px 0}select,input{font:inherit;padding:6px 8px}.err{color:#b91c1c}
.steps{display:flex;gap:6px;margin-bottom:14px}.steps span{flex:1;height:5px;background:#e5e7eb;border-radius:3px}.steps span.on{background:#1f2937}</style>
<main><div class=steps><span id=p1></span><span id=p2></span><span id=p3></span><span id=p4></span><span id=p5></span></div>
<section id=s1><h2>Step 1 · Pairing code</h2><p>Your device shows this code. You will need it at the end of setup. There is no way back to this step; leaving it generates a new code.</p><div class=code id=code></div><button id=n1 class=primary>Continue</button></section>
<section id=s2 hidden><h2>Step 2 · Location</h2><label>Which room is the device in? <select id=room><option value="">Choose...</option></select></label><button id=n2 class=primary>Continue</button> <span id=e2 class=err></span></section>
<section id=s3 hidden><h2>Step 3 · Options</h2><label><input type=checkbox id=opt1> Enable automatic updates</label><label><input type=checkbox id=opt2> Share diagnostics</label><p class=muted>Device serial: <b id=serial></b></p><button id=n3 class=primary>Continue</button></section>
<section id=s4 hidden><h2>Step 4 · Notice</h2><p>Pairing links this device to your account. You can unpair it at any time from Settings.</p><label><input type=checkbox id=ack> I understand</label><button id=n4 class=primary>Continue</button> <span id=e4 class=err></span></section>
<section id=s5 hidden><h2>Step 5 · Confirm</h2><label>Pairing code from step 1 <input id=fcode autocomplete=off maxlength=6></label><label>Room you chose <select id=froom><option value="">Choose...</option></select></label><button id=fin class=primary>Finish pairing</button> <span id=e5 class=err></span><p id=done></p></section></main>
<script>
var INST=null,ROOMS=["Kitchen","Living room","Office","Bedroom","Garage","Hallway"];
function show(n){for(var i=1;i<=5;i++){document.getElementById('s'+i).hidden=i!==n;document.getElementById('p'+i).className=i<=n?'on':''}}
fetch('/__start').then(r=>r.json()).then(j=>{INST=j.instance;document.getElementById('code').textContent=j.code;document.getElementById('serial').textContent=j.serial;
 var want=j.room_wanted;document.getElementById('s2').querySelector('label').firstChild.textContent='The device is installed in the '+want.toLowerCase()+'. Which room is it in? ';
 ROOMS.forEach(r=>{['room','froom'].forEach(id=>{var o=document.createElement('option');o.textContent=r;o.value=r;document.getElementById(id).appendChild(o)})});show(1)});
n1.onclick=function(){document.getElementById('code').textContent='••••••';show(2)};
n2.onclick=function(){var v=document.getElementById('room').value;if(!v){e2.textContent='Choose a room.';return}fetch('/__choose',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({field:'room',value:v})});show(3)};
n3.onclick=function(){show(4)};
n4.onclick=function(){if(!ack.checked){e4.textContent='Please acknowledge.';return}show(5)};
fin.onclick=function(){var c=fcode.value.trim(),r=froom.value;if(!c||!r){e5.textContent='Both fields are required.';return}
 fetch('/__finish',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({instance:INST,code:c,room:r})}).then(x=>x.json()).then(j=>{done.textContent='Paired. Reference '+j.ref;fin.disabled=true})};
</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8801)
