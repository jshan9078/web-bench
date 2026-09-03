#!/usr/bin/env python3
"""82-blur-validation: a shipping-address form with the validation behaviour of real checkouts.
- Errors appear only on BLUR (leaving a field), never on submit; submit with errors fails silently apart
  from the inline messages. The postal-code format is stated only in the blur error.
- Choosing country "Canada" reveals a required Province select after a short delay.
- "Ship to billing address" is pre-ticked and, if left ticked, overwrites the shipping fields with the
  stored billing address at submit time (the wrong address for this task).
complete = a recorded submission equals the requested address exactly."""
import json, random, sys, os, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
TARGET = {"name": "Mara Lindqvist", "line1": "48 Rue Sainte-Anne", "city": "Québec", "country": "Canada", "province": "QC", "postal": "G1R 3X3", "phone": "+1 418 555 0147"}
BILLING = {"name": "Mara Lindqvist", "line1": "1200 Bay Street", "city": "Toronto", "country": "Canada", "province": "ON", "postal": "M5R 2A5", "phone": "+1 416 555 0199"}
S = {"submissions": []}


def reset(): S["submissions"] = []
def render(): return b""
def click(x, y): return {"ignored": True}


def _errors(d):
    e = {}
    if not (d.get("name") or "").strip(): e["name"] = "Full name is required."
    if not (d.get("line1") or "").strip(): e["line1"] = "Address line is required."
    if not (d.get("city") or "").strip(): e["city"] = "City is required."
    if d.get("country") == "Canada":
        if not d.get("province"): e["province"] = "Province is required for Canada."
        if not re.fullmatch(r"[A-Z]\d[A-Z] \d[A-Z]\d", (d.get("postal") or "").strip().upper()): e["postal"] = "Use the format A1A 1A1 (letter-digit-letter, space, digit-letter-digit)."
    elif not (d.get("postal") or "").strip(): e["postal"] = "Postal code is required."
    if not re.fullmatch(r"\+\d[\d ]{8,}", (d.get("phone") or "").strip()): e["phone"] = "Phone must start with + and the country code."
    return e


def post(path, data, ctype):
    if path == "/__validate":
        return (json.dumps({"errors": _errors(data)}), "application/json")
    if path == "/__submit":
        d = dict(data)
        if d.get("same_as_billing"):            # the pre-ticked trap: shipping is replaced by billing
            d.update(BILLING)
        errs = _errors(d)
        rec = {"data": {k: (d.get(k) or "").strip() if isinstance(d.get(k), str) else d.get(k) for k in TARGET}, "errors": errs, "same_as_billing": bool(data.get("same_as_billing"))}
        S["submissions"].append(rec)
        if errs: return (json.dumps({"ok": False, "errors": errs}), "application/json")
        return (json.dumps({"ok": True, "ref": "SHP-%05d" % random.randint(0, 99999)}), "application/json")
    return None


def state():
    ok = any(not s["errors"] and {k: s["data"][k].upper() if k == "postal" else s["data"][k] for k in TARGET} == {k: TARGET[k].upper() if k == "postal" else TARGET[k] for k in TARGET} for s in S["submissions"])
    return {"target": TARGET, "submissions": S["submissions"], "complete": bool(ok)}


def page():
    return r"""<!doctype html><meta charset=utf-8><title>Shipping Address</title>
<style>body{font:15px system-ui;margin:0;background:#fafafa;color:#222}main{max-width:540px;margin:36px auto;background:#fff;border:1px solid #e5e5e5;border-radius:10px;padding:24px}
label{display:block;margin:12px 0 4px;font-size:13px;color:#555}input,select{font:inherit;padding:7px 9px;width:100%;box-sizing:border-box;border:1px solid #cbd5e1;border-radius:6px}.err{color:#b91c1c;font-size:12px;min-height:16px}
button{font:inherit;padding:9px 18px;border-radius:6px;border:1px solid #1f2937;background:#1f2937;color:#fff;cursor:pointer;margin-top:16px}#ok{margin-top:14px;color:#047857}.hidden{display:none}</style>
<main><h2>Shipping address</h2>
<label><input type=checkbox id=same checked> Ship to my billing address (1200 Bay Street, Toronto)</label>
<label>Full name</label><input id=name><div class=err id=e_name></div>
<label>Address line</label><input id=line1><div class=err id=e_line1></div>
<label>City</label><input id=city><div class=err id=e_city></div>
<label>Country</label><select id=country><option value="">Choose...</option><option>Canada</option><option>United States</option><option>Sweden</option></select><div class=err id=e_country></div>
<div id=provwrap class=hidden><label>Province</label><select id=province><option value="">Choose...</option><option>AB</option><option>BC</option><option>MB</option><option>NB</option><option>NL</option><option>NS</option><option>ON</option><option>PE</option><option>QC</option><option>SK</option></select><div class=err id=e_province></div></div>
<label>Postal code</label><input id=postal><div class=err id=e_postal></div>
<label>Phone</label><input id=phone><div class=err id=e_phone></div>
<button id=submit>Save address</button><div id=ok></div></main>
<script>
var F=['name','line1','city','country','province','postal','phone'];
function data(){var d={};F.forEach(k=>d[k]=document.getElementById(k).value);d.same_as_billing=document.getElementById('same').checked;return d}
function showErr(k,m){var e=document.getElementById('e_'+k);if(e)e.textContent=m||''}
F.forEach(k=>{var el=document.getElementById(k);el.addEventListener('blur',function(){fetch('/__validate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data())}).then(r=>r.json()).then(j=>{showErr(k,j.errors[k])})})});
document.getElementById('country').addEventListener('change',function(){var w=document.getElementById('provwrap');if(this.value==='Canada'){setTimeout(()=>w.classList.remove('hidden'),900)}else{w.classList.add('hidden');document.getElementById('province').value=''}});
document.getElementById('submit').onclick=function(){fetch('/__submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data())}).then(r=>r.json()).then(j=>{if(!j.ok){Object.keys(j.errors).forEach(k=>showErr(k,j.errors[k]));return}document.getElementById('ok').textContent='Address saved. Reference '+j.ref})};
</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8802)
