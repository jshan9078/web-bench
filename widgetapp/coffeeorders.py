#!/usr/bin/env python3
"""230-coffee-cups: a cafe counter clip: the barista places finished drinks on the pickup shelf; customers take
them. Some cups sit on the shelf a while. Count cups placed on the shelf in total. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Cafe counter clip"; HEADING = "Cafe pickup counter camera (clip, 2:00)"; QUESTION = "How many drinks did the barista place on the pickup shelf during the clip (exact)?"
S = {"ev": []}
COLORS = ["#f5f5f4", "#fde68a", "#fca5a5", "#bfdbfe"]


def reset():
    n = random.randint(18, 26); ts = sorted(random.uniform(2, 110) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "wait": round(random.uniform(3, 12), 1), "c": random.choice(COLORS), "slot": random.randint(0, 5)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return len(S["ev"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#fef3c7';cx.fillRect(0,0,800,450);cx.fillStyle='#78350f';cx.fillRect(100,240,600,20);cx.fillStyle='#1f2937';cx.fillRect(560,60,200,120);cx.fillStyle='#e5e7eb';cx.font='bold 13px system-ui';cx.fillText('PICKUP',360,230);
 var slots={};D.ev.forEach(function(e){var dt=t-e.t;if(dt<0)return;if(dt<1.5){var f=dt/1.5;cx.fillStyle=e.c;cx.fillRect(660-(f)*(660-(150+e.slot*90)),120+f*100,26,34)}else if(dt<1.5+e.wait){slots[e.slot]=e}else if(dt<1.5+e.wait+1.5){var f=(dt-1.5-e.wait)/1.5;cx.fillStyle=e.c;cx.fillRect(150+e.slot*90,220+f*200,26,34);person('#6b7280',150+e.slot*90+40,430,t)}});
 Object.keys(slots).forEach(function(k){var e=slots[k];cx.fillStyle=e.c;cx.fillRect(150+e.slot*90,206,26,34)});
 overlay(t,'CAFE-PICKUP')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8893)
