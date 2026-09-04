#!/usr/bin/env python3
"""329-parking-lot: 2-minute clip of an 8-space car park; cars arrive, park in a free space for a while and leave.
Report the maximum number of cars parked at the same time. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Car park clip"; HEADING = "Car park camera (clip, 2:00)"; QUESTION = "Maximum number of cars parked at the same time (exact)?"
S = {"cars": [], "peak": 0}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset():
    for _ in range(300):
        cars = []; free_at = [0] * 8
        for _ in range(random.randint(16, 22)):
            a = random.uniform(2, 105); opts = [i for i in range(8) if free_at[i] <= a - 2]
            if not opts: continue
            sp = random.choice(opts); d = random.uniform(6, 35); cars.append({"t_in": round(a, 1), "t_out": round(min(a + d, DUR + 4), 1), "space": sp, "col": random.choice(COLS)}); free_at[sp] = a + d + 4
        peak = max(sum(1 for c in cars if c["t_in"] <= x["t_in"] < c["t_out"]) for x in cars)
        if 5 <= peak <= 8: break
    S["cars"] = cars; S["peak"] = peak


def data(): return {"cars": S["cars"]}
def answer(): return S["peak"]


SCENE_JS = r"""function scene(t){cx.fillStyle='#4b5563';cx.fillRect(0,0,800,450);cx.strokeStyle='#f3f4f6';cx.lineWidth=2;for(var i=0;i<8;i++){var x=60+(i%4)*180,y=i<4?40:280;cx.strokeRect(x,y,150,110)}cx.fillStyle='#9ca3af';cx.fillRect(0,190,800,60);
 D.cars.forEach(function(c){var e=3,sx=60+(c.space%4)*180+75,sy=(c.space<4?40:280)+55,dt=t-c.t_in;if(dt<-e||t>c.t_out+e)return;var x,y;
  if(dt<0){var k=(dt+e)/e;x=-60+(sx+60)*k;y=220+(sy-220)*Math.max(0,(k-0.5)*2)}else if(t<=c.t_out){x=sx;y=sy}else{var k=(t-c.t_out)/e;x=sx+(860-sx)*k;y=sy+(220-sy)*Math.min(1,k*2)}
  cx.fillStyle=c.col;rr(x-45,y-24,90,48,8)});
 overlay(t,'LOT-A')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8963)
