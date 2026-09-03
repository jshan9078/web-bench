#!/usr/bin/env python3
"""97-locale-ledger: a French-locale invoicing page (lang=fr): dates dd/mm/yyyy, amounts "1 234,56 EUR".
Task: total of all invoices dated in March 2026. Trap: many dates have day <= 12, so a US (mm/dd) reading
selects a different set of rows; decimal commas and space thousands separators must be parsed as such.
complete = a submitted total within 0.01 of the true sum (comma or dot decimals accepted)."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
CLIENTS = ["Atelier Morin", "Boulangerie Dupuis", "Cabinet Leroy", "Distribution Nord", "Éditions Marceau", "Fromagerie Blanc", "Garage Petit", "Hôtel des Arts", "Imprimerie Roux", "Jardins Lefèvre"]
S = {"rows": [], "answer": 0.0, "submissions": []}


def fr(v): return f"{v:,.2f}".replace(",", " ").replace(".", ",") + " €"


def reset():
    S["submissions"] = []; rows = []
    # March rows with day <= 12 (US reading moves them to other months) and non-March rows whose day is 3 (US reading makes them March)
    dates = [(d, 3) for d in random.sample(range(1, 13), 6)] + [(d, 3) for d in random.sample(range(13, 31), 2)]
    dates += [(3, m) for m in (2, 4, 5)] + [(d, m) for d, m in [(random.randint(13, 28), 2), (random.randint(13, 28), 4), (random.randint(1, 12), 2), (random.randint(1, 12), 4), (random.randint(14, 28), 5)]]
    random.shuffle(dates)
    for i, (d, m) in enumerate(dates):
        rows.append({"num": f"F-2026-{101 + i:03d}", "client": random.choice(CLIENTS), "d": d, "m": m, "amount": round(random.uniform(120, 4800), 2), "status": random.choice(["Payée", "En attente", "Payée", "En retard"])})
    rows.sort(key=lambda r: r["num"]); S["rows"] = rows
    S["answer"] = round(sum(r["amount"] for r in rows if r["m"] == 3), 2)


def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("total") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def parse(s):
    s = s.replace("€", "").replace("EUR", "").replace(" ", "").replace(" ", "").strip()
    if "," in s and "." in s: s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s: s = s.replace(",", ".")
    return float(s)


def state():
    ok = False
    for s in S["submissions"]:
        try: ok = ok or abs(parse(s) - S["answer"]) < 0.01
        except ValueError: pass
    us_wrong = round(sum(r["amount"] for r in S["rows"] if r["d"] == 3), 2)
    return {"answer": S["answer"], "us_reading_total": us_wrong, "march_rows": [r["num"] for r in S["rows"] if r["m"] == 3], "submissions": S["submissions"], "complete": ok}


def page():
    tr = "".join(f"<tr><td>{r['num']}</td><td>{r['client']}</td><td>{r['d']:02d}/{r['m']:02d}/2026</td><td class=n>{fr(r['amount'])}</td><td>{r['status']}</td></tr>" for r in S["rows"])
    return f"""<!doctype html><html lang=fr><meta charset=utf-8><title>Factures, Northwind SARL</title>
<style>body{{font:15px system-ui;margin:0;background:#fafaf9;color:#1c1917}}header{{background:#1c1917;color:#fff;padding:12px 24px;display:flex;gap:24px;align-items:center}}main{{max-width:960px;margin:0 auto;padding:20px}}
table{{border-collapse:collapse;width:100%}}th,td{{padding:8px 12px;border-bottom:1px solid #e7e5e4;text-align:left}}td.n{{text-align:right;font-variant-numeric:tabular-nums}}th{{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#78716c}}
#ans{{margin-top:20px;padding:14px;background:#f5f5f4;border-radius:8px}}input,button{{font:inherit;padding:6px 8px}}.note{{color:#78716c;font-size:13px}}</style>
<header><b>Northwind SARL</b><span>Comptabilité</span><span>Factures</span><span style="margin-left:auto">Paris (UTC+1)</span></header>
<main><h1 style="font-size:20px">Factures émises, T1 et T2 2026</h1><p class=note>Montants TTC en euros. Dates au format jour/mois/année.</p>
<table><thead><tr><th>N°</th><th>Client</th><th>Date</th><th>Montant</th><th>Statut</th></tr></thead><tbody>{tr}</tbody></table>
<div id=ans><label>Total des factures de mars 2026 : <input id=tot size=14 placeholder="0,00"></label> <button id=go>Valider</button> <span id=msg></span></div></main>
<script>document.getElementById('go').onclick=function(){{fetch('/__answer',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{total:document.getElementById('tot').value}})}}).then(r=>r.json()).then(function(j){{document.getElementById('msg').textContent='Envoyé ('+j.n+').'}})}}</script></html>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8817)
