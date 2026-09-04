#!/usr/bin/env python3
"""238-jaywalkers: a road clip with a marked zebra crossing in the middle; pedestrians cross the road either on
the zebra or away from it. Count those who crossed AWAY from the zebra. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Road camera clip"; HEADING = "Road camera, Harbor Rd (clip, 2:00)"; QUESTION = "How many people crossed the road AWAY from the zebra crossing (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(18, 26); ts = sorted(random.uniform(2, 113) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "zebra": random.random() < 0.55, "x": random.choice([90, 160, 620, 700]), "d": random.choice([1, -1]), "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if not e["zebra"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#9ca3af';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(0,150,800,160);cx.fillStyle='#e5e7eb';for(var i=0;i<7;i++)cx.fillRect(340+i*18,155,10,150);cx.fillStyle='#fbbf24';cx.fillRect(330,145,140,4);cx.fillRect(330,311,140,4);
 D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x=e.zebra?400:e.x,y=e.d>0?120+f*220:340-f*220;person(e.c,x,y,t)});
 overlay(t,'HARBOR-RD')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8901)
