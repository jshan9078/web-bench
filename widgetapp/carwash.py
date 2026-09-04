#!/usr/bin/env python3
"""231-car-wash: a car-wash exit clip: cars leave the tunnel; an attendant hand-dries some (stops the car, towel
motion) and waves others straight through. Count cars that were hand-dried. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Car wash clip"; HEADING = "Car wash exit camera (clip, 2:00)"; QUESTION = "How many cars were HAND-DRIED by the attendant (stopped for towelling) during the clip (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280"]


def reset():
    t = 3.0; ev = []
    while t < 108:
        d = random.random() < 0.5; ev.append({"t": round(t, 1), "dry": d, "c": random.choice(COLORS)}); t += (9 if d else 5) + random.uniform(0, 2)
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["dry"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#cbd5e1';cx.fillRect(0,0,800,450);cx.fillStyle='#1e3a8a';cx.fillRect(0,120,220,220);cx.fillStyle='#0f172a';cx.fillRect(160,160,60,150);cx.fillStyle='#475569';cx.fillRect(220,300,580,60);
 var att=520;D.ev.forEach(function(e){var dt=t-e.t;if(dt<0)return;var x,P=e.dry?8:4;if(dt>P)return;if(e.dry){if(dt<2)x=200+dt/2*300;else if(dt<6){x=500;att=560;if(Math.floor(dt*4)%2===0){cx.fillStyle='#fde047';cx.fillRect(540,270,20,12)}}else x=500+(dt-6)/2*400}else{x=200+dt/4*700}cx.fillStyle=e.c;cx.fillRect(x-45,290,90,36);cx.fillStyle='#111827';cx.beginPath();cx.arc(x-28,330,9,0,6.28);cx.arc(x+28,330,9,0,6.28);cx.fill()});
 person('#f59e0b',att,290,t);overlay(t,'WASH-EXIT')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8894)
