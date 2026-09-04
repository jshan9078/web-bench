#!/usr/bin/env python3
"""210-tray-racks: a cafeteria clip: diners return trays to either the LEFT rack or the RIGHT rack. Count trays
placed on the LEFT rack. Outcome attribution over time. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Cafeteria clip"; HEADING = "Cafeteria tray return (clip, 2:00)"; QUESTION = "How many trays were placed on the LEFT rack (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(20, 28); ts = sorted(random.uniform(2, 114) for _ in range(n))
    S["ev"] = [{"t": round(x, 1), "left": random.random() < 0.5, "c": random.choice(COLORS)} for x in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["left"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#f3f4f6';cx.fillRect(0,0,800,450);cx.fillStyle='#d1d5db';cx.fillRect(0,320,800,130);cx.fillStyle='#6b7280';cx.fillRect(60,120,160,200);cx.fillRect(580,120,160,200);cx.fillStyle='#111827';cx.font='bold 15px system-ui';cx.fillText('LEFT RACK',90,100);cx.fillText('RIGHT RACK',600,100);
 var lc=0,rc=0;D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt>=P){if(e.left)lc++;else rc++;return}if(dt<0)return;var f=dt/P,x=400+(e.left?-1:1)*f*260,y=420-f*80;person(e.c,x,y,t);cx.fillStyle='#a16207';cx.fillRect(x-6,y-70,36,8)});
 for(var i=0;i<lc;i++){cx.fillStyle='#a16207';cx.fillRect(80,300-i*9,120,6)}for(var i=0;i<rc;i++){cx.fillStyle='#a16207';cx.fillRect(600,300-i*9,120,6)}
 overlay(t,'CAFE-TRAYS')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8877)
