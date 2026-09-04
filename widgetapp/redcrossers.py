#!/usr/bin/env python3
"""208-red-crossers: a crosswalk clip with a pedestrian signal cycling WALK (white) / DON'T WALK (red). People
cross at random times. Count those who started crossing while the signal showed DON'T WALK. Correlating two
visual states over time. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Crosswalk clip"; HEADING = "Crosswalk camera, Harbor St (clip, 2:00)"; QUESTION = "How many people STARTED crossing while the signal showed DON'T WALK (red hand) (exact)?"
S = {"ev": [], "cycle": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    t = 0.0; cyc = []
    while t < DUR:
        w = random.uniform(8, 14); r = random.uniform(10, 18); cyc.append({"t": round(t, 1), "walk": w}); t += w + r
    S["cycle"] = cyc; n = random.randint(16, 24); ts = sorted(random.uniform(2, 114) for _ in range(n))
    S["ev"] = [{"t": round(x, 1), "dir": random.choice([1, -1]), "c": random.choice(COLORS)} for x in ts]


def walk_at(t): return any(c["t"] <= t < c["t"] + c["walk"] for c in S["cycle"])
def data(): return {"ev": S["ev"], "cycle": S["cycle"]}
def answer(): return sum(1 for e in S["ev"] if not walk_at(e["t"]))


SCENE_JS = r"""function walkAt(t){return D.cycle.some(function(c){return t>=c.t&&t<c.t+c.walk})}
function scene(t){cx.fillStyle='#4b5563';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(0,120,800,200);cx.fillStyle='#e5e7eb';for(var x=40;x<800;x+=60)cx.fillRect(x,130,30,180);
 var w=walkAt(t);cx.fillStyle='#111827';cx.fillRect(700,20,70,90);cx.fillStyle=w?'#f9fafb':'#ef4444';cx.font='bold 13px system-ui';cx.fillText(w?'WALK':"DON'T",708,60);cx.fillText(w?'':'WALK',708,80);cx.fillStyle=w?'#f9fafb':'#ef4444';cx.beginPath();cx.arc(735,95,8,0,6.28);cx.fill();
 D.ev.forEach(function(e){var P=4,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,y=e.dir>0?100+f*240:340-f*240;person(e.c,380+((e.t*3)%5)*10,y,t)});
 overlay(t,'XWALK-HARBOR')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8876)
