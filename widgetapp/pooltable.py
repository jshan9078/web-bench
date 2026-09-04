#!/usr/bin/env python3
"""228-pool-pots: a pool-table overhead clip: shots are played; some pot a ball (it disappears into a pocket),
some miss. Count balls potted. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Pool table clip"; HEADING = "Pool hall overhead camera, table 3 (clip, 2:00)"; QUESTION = "How many balls were POTTED (went into a pocket) during the clip (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#facc15", "#16a34a", "#7c3aed", "#f97316", "#111827"]


def reset():
    n = random.randint(18, 24); sp = 112 / n; ts = [4 + i * sp + random.uniform(0, sp - 3.5) for i in range(n)]
    S["ev"] = [{"t": round(t, 1), "pot": random.random() < 0.55, "c": random.choice(COLORS), "sx": random.randint(200, 600), "sy": random.randint(150, 300), "pk": random.randint(0, 5)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["pot"])


SCENE_JS = r"""var PK=[[110,90],[400,90],[690,90],[110,360],[400,360],[690,360]];
function scene(t){cx.fillStyle='#78350f';cx.fillRect(60,50,680,350);cx.fillStyle='#15803d';cx.fillRect(100,80,600,290);cx.fillStyle='#111827';PK.forEach(function(p){cx.beginPath();cx.arc(p[0],p[1],16,0,6.28);cx.fill()});
 D.ev.forEach(function(e){var P=3,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,px=PK[e.pk][0],py=PK[e.pk][1],x,y;if(e.pot){if(f>0.85)return;x=e.sx+(px-e.sx)*(f/0.85);y=e.sy+(py-e.sy)*(f/0.85)}else{var mx=px+(e.sx<400?60:-60),my=py+(e.sy<225?70:-70);x=e.sx+(mx-e.sx)*Math.min(1,f*1.4);y=e.sy+(my-e.sy)*Math.min(1,f*1.4)}cx.fillStyle=e.c;cx.beginPath();cx.arc(x,y,11,0,6.28);cx.fill()});
 cx.fillStyle='#f5f5f4';cx.beginPath();cx.arc(400,225,11,0,6.28);cx.fill();overlay(t,'TABLE-3')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8891)
