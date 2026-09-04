#!/usr/bin/env python3
"""242-ski-lift: a chairlift base clip: chairs pass every few seconds; skiers board some chairs (one or two per
chair), other chairs go up empty. Count skiers who boarded. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Chairlift clip"; HEADING = "Chairlift base camera (clip, 2:00)"; QUESTION = "How many skiers boarded the chairlift during the clip (exact)?"
S = {"ch": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    t = 3.0; ch = []
    while t < 112:
        n = random.choice([0, 0, 1, 1, 2]); ch.append({"t": round(t, 1), "n": n, "c": [random.choice(COLORS) for _ in range(n)]}); t += random.uniform(5, 7)
    S["ch"] = ch


def data(): return {"ch": S["ch"]}
def answer(): return sum(c["n"] for c in S["ch"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#e0f2fe';cx.fillRect(0,0,800,450);cx.fillStyle='#f8fafc';cx.fillRect(0,300,800,150);cx.strokeStyle='#334155';cx.lineWidth=3;cx.beginPath();cx.moveTo(0,260);cx.lineTo(800,60);cx.stroke();
 D.ch.forEach(function(c){var P=7,dt=t-c.t;if(dt<0||dt>P)return;var f=dt/P,x=-40+f*880,y=270-f*220;cx.strokeStyle='#334155';cx.beginPath();cx.moveTo(x,y-10);cx.lineTo(x,y+30);cx.stroke();cx.fillStyle='#475569';cx.fillRect(x-30,y+30,60,10);if(f>0.25){for(var i=0;i<c.n;i++){cx.fillStyle=c.c[i];cx.fillRect(x-22+i*26,y+2,18,28)}}else{for(var i=0;i<c.n;i++)person(c.c[i],x-30+i*30,300,t)}});
 overlay(t,'LIFT-BASE')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8905)
