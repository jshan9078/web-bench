#!/usr/bin/env python3
"""234-hand-hygiene: a ward entrance clip: staff enter through a door; a sanitiser dispenser is beside it and lights
when used. Count staff who entered WITHOUT using the dispenser. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Ward entrance clip"; HEADING = "Ward B entrance camera (clip, 2:00)"; QUESTION = "How many people entered the ward WITHOUT using the sanitiser dispenser (exact)?"
S = {"ev": []}
COLORS = ["#0ea5e9", "#22c55e", "#f8fafc", "#a855f7", "#f97316"]


def reset():
    n = random.randint(18, 26); sp = 110 / n; ts = [3 + i * sp + random.uniform(0, sp - 3) for i in range(n)]
    S["ev"] = [{"t": round(t, 1), "wash": random.random() < 0.6, "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if not e["wash"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#f1f5f9';cx.fillRect(0,0,800,450);cx.fillStyle='#cbd5e1';cx.fillRect(0,330,800,120);cx.fillStyle='#1e293b';cx.fillRect(560,80,120,250);cx.fillStyle='#94a3b8';cx.fillRect(470,170,30,50);cx.fillStyle='#0f172a';cx.font='bold 12px system-ui';cx.fillText('SANITISER',440,160);cx.fillText('WARD B',585,60);
 var lit=false;D.ev.forEach(function(e){var P=e.wash?5:3.5,dt=t-e.t;if(dt<0||dt>P)return;var x;if(e.wash){if(dt<1.5)x=-30+dt/1.5*450;else if(dt<3){x=420;lit=true;cx.fillStyle='#22c55e';cx.fillRect(478,150,14,14)}else x=420+(dt-3)/2*200}else{x=-30+dt/3.5*650}person(e.c,x,400,t)});
 if(!lit){cx.fillStyle='#64748b';cx.fillRect(478,150,14,14)}overlay(t,'WARD-B')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8897)
