#!/usr/bin/env python3
"""245-recycling-sort: a recycling station clip: people drop items into one of three bins (paper, glass, general);
some drop items into the WRONG bin (glass into paper, etc., shown by the item colour). Count items dropped into
the GLASS bin. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Recycling station clip"; HEADING = "Recycling station camera (clip, 2:00)"; QUESTION = "How many items were dropped into the GLASS bin (the middle, green bin) (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(20, 28); ts = sorted(random.uniform(2, 113) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "bin": random.randint(0, 2), "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["bin"] == 1)


SCENE_JS = r"""function scene(t){cx.fillStyle='#e5e7eb';cx.fillRect(0,0,800,450);cx.fillStyle='#d1d5db';cx.fillRect(0,330,800,120);var cols=['#2563eb','#16a34a','#374151'],labs=['PAPER','GLASS','GENERAL'];for(var i=0;i<3;i++){cx.fillStyle=cols[i];cx.fillRect(220+i*180,180,120,150);cx.fillStyle='#fff';cx.font='bold 13px system-ui';cx.fillText(labs[i],250+i*180,170)}
 D.ev.forEach(function(e){var P=4,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,bx=280+e.bin*180,x=f<0.6?-30+f/0.6*(bx+30):bx,y=410;person(e.c,x,y,t);if(f>=0.6&&f<0.85){var g=(f-0.6)/0.25;cx.fillStyle='#fde68a';cx.fillRect(bx+24,360-g*170,14,14)}});
 overlay(t,'RECYCLE-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8908)
