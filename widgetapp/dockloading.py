#!/usr/bin/env python3
"""239-loading-bay: a loading bay clip: workers carry boxes from the truck to the store room; some boxes are
dropped and put in the reject bin instead. Count boxes that reached the STORE ROOM. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Loading bay clip"; HEADING = "Loading bay camera (clip, 2:00)"; QUESTION = "How many boxes were carried into the STORE ROOM (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981"]


def reset():
    n = random.randint(20, 28); ts = sorted(random.uniform(2, 112) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "ok": random.random() < 0.7, "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["ok"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#d6d3d1';cx.fillRect(0,0,800,450);cx.fillStyle='#78716c';cx.fillRect(0,330,800,120);cx.fillStyle='#f59e0b';cx.fillRect(0,120,180,210);cx.fillStyle='#1c1917';cx.fillRect(620,100,180,230);cx.fillStyle='#b91c1c';cx.fillRect(380,250,90,60);cx.fillStyle='#fff';cx.font='bold 13px system-ui';cx.fillText('TRUCK',60,100);cx.fillText('STORE ROOM',650,80);cx.fillText('REJECT',395,240);
 D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x,y;if(e.ok){x=180+f*440;y=400}else{x=180+Math.min(f*2,1)*250;y=400-(f>0.5?(f-0.5)*2*90:0)}person(e.c,x,y,t);if(!(e.ok===false&&f>0.9)){cx.fillStyle='#c2a074';cx.fillRect(x+20,y-48,26,20)}});
 overlay(t,'BAY-2')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8902)
