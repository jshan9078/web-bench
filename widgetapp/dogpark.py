#!/usr/bin/env python3
"""244-dog-park: a park gate clip: people enter through the gate with a dog on a lead or without a dog. Count dogs
that entered. Some people bring two dogs. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Park gate clip"; HEADING = "Dog park gate camera (clip, 2:00)"; QUESTION = "How many DOGS entered through the gate during the clip (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(16, 22); ts = sorted(random.uniform(2, 113) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "dogs": random.choice([0, 1, 1, 1, 2]), "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(e["dogs"] for e in S["ev"])


SCENE_JS = r"""function dog(x,y){cx.fillStyle='#78350f';cx.fillRect(x,y-14,26,12);cx.fillRect(x+22,y-22,10,10);cx.fillRect(x+2,y-2,4,8);cx.fillRect(x+20,y-2,4,8)}
function scene(t){cx.fillStyle='#86efac';cx.fillRect(0,0,800,450);cx.fillStyle='#a16207';cx.fillRect(380,120,12,220);cx.fillRect(420,120,12,220);cx.fillStyle='#65a30d';cx.fillRect(0,340,800,110);
 D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x=-40+f*880;person(e.c,x,400,t);for(var i=0;i<e.dogs;i++)dog(x+30+i*36,404)});
 overlay(t,'DOGPARK-GATE')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8907)
