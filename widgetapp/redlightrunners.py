#!/usr/bin/env python3
"""336-red-light-runners: 2-minute clip of a road with a traffic light and a stop line; count the cars that crossed
the stop line while the light was RED. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Junction clip"; HEADING = "Junction camera (clip, 2:00)"; QUESTION = "How many cars crossed the stop line while the light was RED (exact)?"
S = {"phases": [], "cars": []}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def red_at(t): return any(a <= t < b for a, b in S["phases"])


def reset():
    ph = []; t = random.uniform(0, 5)
    while t < DUR:
        r = random.uniform(10, 18); ph.append((round(t, 1), round(t + r, 1))); t += r + random.uniform(12, 20)
    S["phases"] = ph; S["cars"] = [{"t": round(random.uniform(2, 116), 1), "col": random.choice(COLS), "lane": random.randint(0, 1)} for _ in range(random.randint(26, 34))]


def data(): return {"phases": S["phases"], "cars": S["cars"]}
def answer(): return sum(1 for c in S["cars"] if red_at(c["t"]))


SCENE_JS = r"""function scene(t){cx.fillStyle='#365314';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(0,150,800,180);cx.fillStyle='#f9fafb';cx.fillRect(500,150,10,180);var red=D.phases.some(function(p){return t>=p[0]&&t<p[1]});cx.fillStyle='#111827';cx.fillRect(520,60,40,90);cx.fillStyle=red?'#ef4444':'#374151';cx.beginPath();cx.arc(540,80,13,0,6.28);cx.fill();cx.fillStyle=red?'#374151':'#22c55e';cx.beginPath();cx.arc(540,125,13,0,6.28);cx.fill();cx.fillStyle='#f9fafb';cx.font='bold 12px system-ui';cx.fillText('STOP LINE',470,345);
 D.cars.forEach(function(c){var dt=t-c.t;if(dt<-2.5||dt>1.5)return;var x=505+dt*200,y=190+c.lane*80;cx.fillStyle=c.col;rr(x-40,y,80,44,8)});
 overlay(t,'JCT-5')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8970)
