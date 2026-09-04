#!/usr/bin/env python3
"""197-checkout-scans: a self-checkout camera clip: items are scanned one by one; the screen flashes GREEN for an
accepted scan and RED for a rejected one (item must be rescanned). Count DISTINCT accepted scans. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Self-checkout clip"; HEADING = "Self-checkout lane 6 (clip, 2:00)"; QUESTION = "How many scans were ACCEPTED (green) during the clip (exact)?"
S = {"ev": []}


def reset():
    n = random.randint(22, 30); sp = 112 / n; ts = [4 + i * sp + random.uniform(0, sp - 2.5) for i in range(n)]
    S["ev"] = [{"t": round(t, 1), "ok": random.random() < 0.7, "c": random.choice(["#fbbf24", "#f87171", "#60a5fa", "#a3e635", "#f9a8d4"])} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["ok"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#e5e7eb';cx.fillRect(0,0,800,450);cx.fillStyle='#9ca3af';cx.fillRect(0,300,800,150);cx.fillStyle='#1f2937';cx.fillRect(300,60,200,150);cx.fillStyle='#374151';cx.fillRect(560,200,180,100);
 var flash=null;D.ev.forEach(function(e){var dt=t-e.t;if(dt>=0&&dt<2.2){var f=dt/2.2;cx.fillStyle=e.c;cx.fillRect(560+f*40,160+f*40,40,30);if(dt>0.8&&dt<1.8)flash=e.ok}});
 cx.fillStyle=flash===null?'#93c5fd':flash?'#22c55e':'#ef4444';cx.fillRect(310,70,180,130);cx.fillStyle='#fff';cx.font='bold 16px system-ui';cx.fillText(flash===null?'SCAN ITEM':flash?'ACCEPTED':'NOT RECOGNISED',330,140);
 overlay(t,'SCO-6')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8873)
