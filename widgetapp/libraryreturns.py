#!/usr/bin/env python3
"""225-library-returns: a library entrance clip: patrons return books either into the RETURN SLOT (left wall) or
by handing them over at the DESK (right). Some patrons carry no book. Count books returned via the SLOT.
complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Library clip"; HEADING = "Library entrance camera (clip, 2:00)"; QUESTION = "How many books were returned through the RETURN SLOT (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(20, 28); ts = sorted(random.uniform(2, 113) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "k": random.choice(["slot", "slot", "desk", "none"]), "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["k"] == "slot")


SCENE_JS = r"""function scene(t){cx.fillStyle='#fef3c7';cx.fillRect(0,0,800,450);cx.fillStyle='#d6d3d1';cx.fillRect(0,330,800,120);cx.fillStyle='#78350f';cx.fillRect(40,150,120,90);cx.fillStyle='#111827';cx.fillRect(80,190,40,10);cx.fillStyle='#a16207';cx.fillRect(600,220,180,90);cx.fillStyle='#111827';cx.font='bold 13px system-ui';cx.fillText('RETURN SLOT',40,140);cx.fillText('DESK',660,210);
 D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x,y;if(e.k==='slot'){x=400-f*280;y=420-f*160}else if(e.k==='desk'){x=400+f*200;y=420-f*100}else{x=400+(f-0.5)*2*400;y=420}person(e.c,x,y,t);if(e.k!=='none'&&f<0.85){cx.fillStyle='#b91c1c';cx.fillRect(x+22,y-40,14,20)}});
 overlay(t,'LIB-ENT')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8888)
