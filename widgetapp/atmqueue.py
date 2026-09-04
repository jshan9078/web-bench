#!/usr/bin/env python3
"""243-atm-cash: an ATM lobby clip: customers use the machine; some transactions dispense cash (notes appear in
the slot), others end without cash (balance check, or declined with a red screen). Count cash withdrawals.
complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "ATM lobby clip"; HEADING = "ATM lobby camera (clip, 2:00)"; QUESTION = "How many transactions dispensed CASH during the clip (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    t = 3.0; ev = []
    while t < 110:
        ev.append({"t": round(t, 1), "k": random.choice(["cash", "cash", "balance", "declined"]), "c": random.choice(COLORS)}); t += random.uniform(5.5, 8)
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["k"] == "cash")


SCENE_JS = r"""function scene(t){cx.fillStyle='#e2e8f0';cx.fillRect(0,0,800,450);cx.fillStyle='#cbd5e1';cx.fillRect(0,330,800,120);cx.fillStyle='#1e293b';cx.fillRect(330,80,140,250);cx.fillStyle='#93c5fd';cx.fillRect(345,95,110,70);cx.fillStyle='#0f172a';cx.fillRect(345,250,110,14);
 D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P;var x=f<0.3?-30+f/0.3*430:f>0.8?400+(f-0.8)/0.2*430:400;person(e.c,x,410,t);if(f>=0.3&&f<=0.8){var g=(f-0.3)/0.5;if(e.k==='declined'&&g>0.4){cx.fillStyle='#ef4444';cx.fillRect(345,95,110,70);cx.fillStyle='#fff';cx.font='bold 12px system-ui';cx.fillText('DECLINED',360,135)}if(e.k==='cash'&&g>0.6){cx.fillStyle='#86efac';cx.fillRect(360,236,80,14)}if(e.k==='balance'&&g>0.4){cx.fillStyle='#fff';cx.font='bold 11px system-ui';cx.fillText('BALANCE',362,135)}}});
 overlay(t,'ATM-LOBBY')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8906)
