#!/usr/bin/env python3
"""193-door-events: an entrance clip: an automatic door opens many times; sometimes a person walks through,
sometimes it opens with nobody passing (false trigger). Count the openings with NOBODY passing. Event
detection over time. complete = exact (last)."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Entrance clip"; HEADING = "Main entrance camera (clip, 2:00)"; QUESTION = "How many times did the door open with NOBODY passing through (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(16, 22); sp = 109 / n
    ts = [3 + i * sp + random.uniform(0, sp - 4.5) for i in range(n)]      # consecutive gaps are at least 4.5 s
    S["ev"] = [{"t": round(t, 1), "person": random.random() < 0.6, "color": random.choice(COLORS), "dir": random.choice([1, -1])} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if not e["person"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#cbd5e1';cx.fillRect(0,0,800,450);cx.fillStyle='#94a3b8';cx.fillRect(0,300,800,150);cx.fillStyle='#1f2937';cx.fillRect(300,80,200,230);
 var open=0,cur=null;D.ev.forEach(function(e){var dt=t-e.t;if(dt>=0&&dt<4){open=dt<1?dt:dt>3?4-dt:1;cur=e}});
 cx.fillStyle='#93c5fd';cx.fillRect(310,90,180,210);cx.fillStyle='#e2e8f0';cx.fillRect(310,90,90-open*85,210);cx.fillRect(400+open*85,90,90-open*85,210);
 if(cur&&cur.person){var dt=t-cur.t,f=(dt-0.6)/2.8;if(f>0&&f<1){var y=cur.dir>0?150+f*220:370-f*220;person(cur.color,388,y,t)}}
 overlay(t,'ENTRANCE')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8871)
