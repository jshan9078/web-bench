#!/usr/bin/env python3
"""237-barrier-reversals: a car-park entry clip: vehicles drive up to a ticket barrier; it usually rises, but for
some it stays down and the vehicle reverses out. Count vehicles that REVERSED. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Car park entry clip"; HEADING = "Car park entry camera (clip, 2:00)"; QUESTION = "How many vehicles REVERSED away from the barrier without entering (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280"]


def reset():
    t = 2.0; ev = []
    while t < 108:
        r = random.random() < 0.35; ev.append({"t": round(t, 1), "rev": r, "c": random.choice(COLORS)}); t += 7 + random.uniform(0, 3)
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["rev"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#4b5563';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(0,260,800,90);cx.fillStyle='#d1d5db';cx.fillRect(430,140,60,120);cx.fillStyle='#111827';cx.font='bold 12px system-ui';cx.fillText('TICKET',436,130);
 var up=false;D.ev.forEach(function(e){var P=7,dt=t-e.t;if(dt<0||dt>P)return;var x;if(dt<2.5)x=-60+dt/2.5*440;else if(dt<4){x=380;if(!e.rev)up=true}else{if(e.rev)x=380-(dt-4)/3*460;else{up=dt<5.5;x=380+(dt-4)/3*520}}cx.fillStyle=e.c;cx.fillRect(x-40,285,80,34);cx.fillStyle='#111827';cx.beginPath();cx.arc(x-26,322,9,0,6.28);cx.arc(x+26,322,9,0,6.28);cx.fill()});
 cx.fillStyle='#fbbf24';if(up){cx.fillRect(496,180,8,100)}else{cx.fillRect(496,272,150,8)}cx.fillStyle='#0f172a';cx.fillText(up?'BARRIER UP':'BARRIER DOWN',500,120);
 overlay(t,'CP-ENTRY')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8900)
