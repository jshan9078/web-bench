#!/usr/bin/env python3
"""222-escalator-up: a mall clip with a pair of escalators (up on the left, down on the right). People ride in
both directions; some walk past without riding. Count riders who went UP. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Mall clip"; HEADING = "Mall atrium camera, escalators (clip, 2:00)"; QUESTION = "How many people rode the UP escalator (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6", "#f472b6"]


def reset():
    n = random.randint(22, 30); ts = sorted(random.uniform(2, 113) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "k": random.choice(["up", "up", "down", "pass"]), "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["k"] == "up")


SCENE_JS = r"""function scene(t){cx.fillStyle='#f5f5f4';cx.fillRect(0,0,800,450);cx.fillStyle='#d6d3d1';cx.fillRect(0,380,800,70);cx.fillStyle='#a8a29e';cx.beginPath();cx.moveTo(200,380);cx.lineTo(360,120);cx.lineTo(400,120);cx.lineTo(240,380);cx.fill();cx.beginPath();cx.moveTo(440,120);cx.lineTo(600,380);cx.lineTo(560,380);cx.lineTo(400,120);cx.fill();cx.fillStyle='#78716c';cx.fillRect(360,100,80,20);cx.fillStyle='#111827';cx.font='bold 13px system-ui';cx.fillText('UP',210,400);cx.fillText('DOWN',560,400);
 D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x,y;if(e.k==='up'){x=220+f*160;y=380-f*260}else if(e.k==='down'){x=420+f*160;y=120+f*260}else{x=-30+f*860;y=420}person(e.c,x,y,t)});
 overlay(t,'ATRIUM')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8885)
