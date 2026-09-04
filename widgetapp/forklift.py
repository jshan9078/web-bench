#!/usr/bin/env python3
"""216-forklift-trips: a warehouse clip: a forklift shuttles between the dock (right) and racks (left); on some
trips it carries a pallet, on others it runs empty. Count the LOADED trips from right to left. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Warehouse clip"; HEADING = "Warehouse dock camera (clip, 2:00)"; QUESTION = "How many LOADED forklift trips went from the dock (right) to the racks (left) (exact)?"
S = {"trips": []}


def reset():
    t = 2.0; trips = []
    while t < 108:
        loaded = random.random() < 0.55; trips.append({"t": round(t, 1), "d": -1, "loaded": loaded}); t += 5.5
        trips.append({"t": round(t, 1), "d": 1, "loaded": random.random() < 0.15}); t += 5.5 + random.uniform(0, 3)
    S["trips"] = trips


def data(): return {"trips": S["trips"]}
def answer(): return sum(1 for x in S["trips"] if x["d"] < 0 and x["loaded"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#3f3f46';cx.fillRect(0,0,800,450);cx.fillStyle='#52525b';cx.fillRect(0,300,800,150);cx.fillStyle='#a16207';cx.fillRect(0,80,120,220);cx.fillStyle='#78716c';cx.fillRect(700,120,100,180);cx.fillStyle='#e5e7eb';cx.font='bold 15px system-ui';cx.fillText('RACKS',20,60);cx.fillText('DOCK',720,100);
 D.trips.forEach(function(tr){var P=5,dt=t-tr.t;if(dt<0||dt>P)return;var f=dt/P,x=tr.d<0?680-f*540:140+f*540;cx.fillStyle='#f59e0b';cx.fillRect(x-40,250,80,50);cx.fillStyle='#111827';cx.beginPath();cx.arc(x-25,305,12,0,6.28);cx.arc(x+25,305,12,0,6.28);cx.fill();cx.fillStyle='#374151';cx.fillRect(tr.d<0?x-70:x+40,240,30,8);if(tr.loaded){cx.fillStyle='#c2a074';cx.fillRect(tr.d<0?x-110:x+40,200,70,50);cx.strokeStyle='#7c5a2e';cx.strokeRect(tr.d<0?x-110:x+40,200,70,50)}});
 overlay(t,'WH-DOCK')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8879)
