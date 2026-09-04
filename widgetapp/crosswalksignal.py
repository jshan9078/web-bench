#!/usr/bin/env python3
"""326-crosswalk-signal: 2-minute clip of a crosswalk with a pedestrian signal that alternates WALK (green) and
DON'T WALK (red). People cross in both directions at any time. Count the people who crossed RIGHT-TO-LEFT while
the signal showed WALK (judged at the moment they stepped onto the crossing). complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Crosswalk clip"; HEADING = "Crosswalk camera (clip, 2:00)"; QUESTION = "How many people crossed RIGHT-TO-LEFT while the signal showed WALK (exact)?"
S = {"phases": [], "walkers": []}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6", "#f472b6"]


def walk_at(t): return any(a <= t < b for a, b in S["phases"])


def reset():
    ph = []; t = random.uniform(0, 6)
    while t < DUR:
        w = random.uniform(8, 16); ph.append((round(t, 1), round(t + w, 1))); t += w + random.uniform(10, 20)
    S["phases"] = ph
    S["walkers"] = [{"t": round(random.uniform(2, 112), 1), "dir": random.choice([1, -1]), "col": random.choice(COLS), "lane": random.randint(0, 3)} for _ in range(random.randint(22, 30))]


def data(): return {"phases": S["phases"], "walkers": S["walkers"]}
def answer(): return sum(1 for w in S["walkers"] if w["dir"] == -1 and walk_at(w["t"]))


SCENE_JS = r"""function scene(t){cx.fillStyle='#374151';cx.fillRect(0,0,800,450);cx.fillStyle='#9ca3af';cx.fillRect(0,0,800,90);cx.fillRect(0,360,800,90);cx.fillStyle='#f3f4f6';for(var i=0;i<8;i++)cx.fillRect(180+i*60,100,36,250);
 var walk=D.phases.some(function(p){return t>=p[0]&&t<p[1]});cx.fillStyle='#111827';cx.fillRect(700,20,60,60);cx.fillStyle=walk?'#22c55e':'#ef4444';cx.font='bold 13px system-ui';cx.fillText(walk?'WALK':"DON'T",708,45);cx.fillText(walk?'':'WALK',708,65);
 D.walkers.forEach(function(w){var dt=t-w.t;if(dt<-1||dt>7)return;var f=(dt+1)/8,x=w.dir>0?60+f*680:740-f*680,y=130+w.lane*60;person(w.col,x,y+70,t)});
 overlay(t,'XWALK-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8960)
