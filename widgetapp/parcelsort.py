#!/usr/bin/env python3
"""192-parcel-sort: a sorter clip: parcels travel along a belt and a diverter sends each to the LEFT or RIGHT chute
at a junction. Count parcels sent to the LEFT chute. Tracking each item to its outcome. complete = exact (last)."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Sorter clip"; HEADING = "Parcel sorter, junction 4 (clip, 2:00)"; QUESTION = "How many parcels were diverted to the LEFT chute (exact)?"
S = {"ev": []}


def reset():
    n = random.randint(26, 36); ts = sorted(random.uniform(2, 113) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "left": random.random() < 0.45, "w": random.randint(34, 60), "h": random.randint(26, 44), "c": random.choice(["#c2a074", "#b08a5a", "#d9c1a0"])} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["left"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#374151';cx.fillRect(0,0,800,450);cx.fillStyle='#6b7280';cx.fillRect(0,200,420,60);cx.save();cx.translate(420,230);cx.rotate(-0.6);cx.fillRect(0,-30,260,60);cx.restore();cx.save();cx.translate(420,230);cx.rotate(0.6);cx.fillRect(0,-30,260,60);cx.restore();
 cx.fillStyle='#e5e7eb';cx.font='bold 14px system-ui';cx.fillText('LEFT CHUTE',560,40);cx.fillText('RIGHT CHUTE',560,430);
 D.ev.forEach(function(e){var P=6,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x,y;if(f<0.5){x=-60+f*2*480;y=230}else{var g=(f-0.5)*2;x=420+g*260*Math.cos(0.6);y=230+(e.left?-1:1)*g*260*Math.sin(0.6)}cx.fillStyle=e.c;cx.fillRect(x-e.w/2,y-e.h/2,e.w,e.h);cx.strokeStyle='#7c5a2e';cx.strokeRect(x-e.w/2,y-e.h/2,e.w,e.h)});
 cx.fillStyle='#fbbf24';cx.fillRect(414,196,12,68);overlay(t,'SORT-J4')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8870)
