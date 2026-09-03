#!/usr/bin/env python3
"""191-direction-count: a corridor clip where people cross in both directions; count only those crossing LEFT to
RIGHT. Direction-aware counting over time (a single frame cannot tell direction). complete = exact (last)."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Corridor clip"; HEADING = "Corridor camera, west wing (clip, 2:00)"; QUESTION = "How many people crossed from LEFT to RIGHT (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(18, 26); ts = sorted(random.uniform(3, 114) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "dir": random.choice([1, -1]), "color": random.choice(COLORS), "lane": random.randint(0, 2)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["dir"] > 0)


SCENE_JS = r"""function scene(t){cx.fillStyle='#e5e7eb';cx.fillRect(0,0,800,450);cx.fillStyle='#d1d5db';cx.fillRect(0,250,800,200);cx.fillStyle='#6b7280';for(var x=0;x<800;x+=100)cx.fillRect(x,250,2,200);cx.fillStyle='#374151';cx.fillRect(120,60,90,190);cx.fillRect(590,60,90,190);
 D.ev.forEach(function(e){var P=4.5,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x=e.dir>0?-40+f*880:840-f*880;person(e.color,x,380+e.lane*14,t)});overlay(t,'WEST-CORR')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8869)
