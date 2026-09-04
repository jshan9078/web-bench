#!/usr/bin/env python3
"""198-pen-entry: a farm camera clip: animals move between a field and a pen through a gate in both directions.
Task: how many animals are in the pen at the END of the clip, given the count at the start shown on screen.
Net flow tracking over time. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Farm gate clip"; HEADING = "Barn camera, east gate (clip, 2:00)"; QUESTION = "How many animals are in the pen at the END of the clip (exact)?"
S = {"ev": [], "start": 0}


def reset():
    S["start"] = random.randint(3, 6); n = random.randint(18, 26); ts = sorted(random.uniform(3, 114) for _ in range(n)); inside = S["start"]; ev = []
    for t in ts:
        d = 1 if (inside == 0 or random.random() < 0.55) else -1; inside += d; ev.append({"t": round(t, 1), "d": d, "c": random.choice(["#f5f5f4", "#d6d3d1", "#a8a29e", "#78716c"])})
    S["ev"] = ev


def data(): return {"ev": S["ev"], "start": S["start"]}
def answer(): return S["start"] + sum(e["d"] for e in S["ev"])


SCENE_JS = r"""function sheep(c,x,y){cx.fillStyle=c;cx.beginPath();cx.ellipse(x,y,22,14,0,0,6.28);cx.fill();cx.fillStyle='#292524';cx.beginPath();cx.arc(x+20,y-4,7,0,6.28);cx.fill();cx.fillRect(x-14,y+10,4,10);cx.fillRect(x+8,y+10,4,10)}
function scene(t){cx.fillStyle='#65a30d';cx.fillRect(0,0,800,450);cx.fillStyle='#a16207';cx.fillRect(380,0,12,180);cx.fillRect(380,270,12,180);cx.fillStyle='#78350f';cx.fillRect(380,180,12,90);
 cx.fillStyle='#fff';cx.font='bold 16px system-ui';cx.fillText('FIELD',60,40);cx.fillText('PEN',700,40);cx.fillText('In pen at start: '+D.start,560,70);
 D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x=e.d>0?60+f*680:740-f*680;sheep(e.c,x,225+((e.t*7)%3)*20)});
 overlay(t,'BARN-E')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8874)
