#!/usr/bin/env python3
"""327-bike-lane: 2-minute clip of a path shared by cyclists and pedestrians moving in both directions; count the
CYCLISTS (two wheels) that passed the marker line, regardless of direction. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Path clip"; HEADING = "Shared path camera (clip, 2:00)"; QUESTION = "How many CYCLISTS passed the marker line during the clip (exact)?"
S = {"movers": []}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset(): S["movers"] = [{"t": round(random.uniform(2, 115), 1), "bike": random.random() < 0.5, "dir": random.choice([1, -1]), "col": random.choice(COLS), "lane": random.randint(0, 2)} for _ in range(random.randint(30, 40))]
def data(): return {"movers": S["movers"]}
def answer(): return sum(1 for m in S["movers"] if m["bike"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#65a30d';cx.fillRect(0,0,800,450);cx.fillStyle='#a8a29e';cx.fillRect(0,150,800,180);cx.strokeStyle='#fde047';cx.lineWidth=4;cx.setLineDash([12,10]);cx.beginPath();cx.moveTo(400,150);cx.lineTo(400,330);cx.stroke();cx.setLineDash([]);
 D.movers.forEach(function(m){var sp=m.bike?2.2:6,dt=t-m.t;if(dt<-sp/2||dt>sp/2)return;var f=(dt+sp/2)/sp,x=m.dir>0?-40+f*880:840-f*880,y=200+m.lane*50;
  if(m.bike){cx.strokeStyle='#1c1917';cx.lineWidth=3;cx.beginPath();cx.arc(x-16,y+12,11,0,6.28);cx.stroke();cx.beginPath();cx.arc(x+16,y+12,11,0,6.28);cx.stroke();cx.fillStyle=m.col;cx.fillRect(x-10,y-16,20,22);cx.beginPath();cx.arc(x,y-24,7,0,6.28);cx.fill()}
  else person(m.col,x-12,y+40,t)});
 overlay(t,'PATH-2')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8961)
