#!/usr/bin/env python3
"""226-fare-gates: a station gate-line clip: passengers pass through three gates; a valid tap opens the gate
(green), while some passengers push through a gate that stays red (no tap). Count passengers who passed WITHOUT a
valid tap. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Gate-line clip"; HEADING = "Station gate-line camera (clip, 2:00)"; QUESTION = "How many passengers passed through a gate WITHOUT a valid tap (gate stayed red) (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(22, 30); ts = sorted(random.uniform(2, 113) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "gate": random.randint(0, 2), "ok": random.random() < 0.7, "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if not e["ok"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#e7e5e4';cx.fillRect(0,0,800,450);cx.fillStyle='#a8a29e';cx.fillRect(0,300,800,150);for(var g=0;g<3;g++){var gx=200+g*200;cx.fillStyle='#57534e';cx.fillRect(gx-70,200,30,110);cx.fillRect(gx+40,200,30,110)}
 D.ev.forEach(function(e){var P=4,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,gx=200+e.gate*200,y=430-f*260;var st=(f>0.25&&f<0.75)?(e.ok?'#22c55e':'#ef4444'):null;if(st){cx.fillStyle=st;cx.fillRect(gx-40,205,10,10);cx.fillRect(gx+30,205,10,10)}person(e.c,gx-12,y,t)});
 for(var g=0;g<3;g++){var gx=200+g*200;var lit=D.ev.some(function(e){var dt=t-e.t;return e.gate===g&&dt>1&&dt<3});if(!lit){cx.fillStyle='#9ca3af';cx.fillRect(gx-40,205,10,10);cx.fillRect(gx+30,205,10,10)}}
 overlay(t,'GATELINE-A')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8889)
