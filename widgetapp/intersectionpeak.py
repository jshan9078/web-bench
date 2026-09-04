#!/usr/bin/env python3
"""322-intersection-peak: top-down 2-minute clip of a four-way intersection; cars arrive from all four sides,
wait in the central box for a random time and leave. Report the maximum number of cars inside the box at the same
moment. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Intersection clip"; HEADING = "Intersection camera (clip, 2:00)"; QUESTION = "Maximum number of cars inside the central box at the same time (exact)?"
S = {"cars": [], "peak": 0}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6", "#f472b6"]


def reset():
    for _ in range(300):
        cars = []
        for i in range(random.randint(22, 30)):
            a = random.uniform(3, 110); cars.append({"t_in": round(a, 1), "t_out": round(a + random.uniform(2.5, 9), 1), "side": random.randrange(4), "col": random.choice(COLS)})
        peak = max(sum(1 for c in cars if c["t_in"] <= x["t_in"] < c["t_out"]) for x in cars)
        if 4 <= peak <= 7: break
    S["cars"] = cars; S["peak"] = peak


def data(): return {"cars": S["cars"]}
def answer(): return S["peak"]


SCENE_JS = r"""function scene(t){cx.fillStyle='#4d7c0f';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(300,0,200,450);cx.fillRect(0,125,800,200);cx.strokeStyle='#fbbf24';cx.lineWidth=3;cx.strokeRect(300,125,200,200);
 var inside=0;D.cars.forEach(function(c,i){var e=3,x,y,ang;var lane=(i%2)*60-30;if(t<c.t_in-e||t>c.t_out+e)return;var f;if(t<c.t_in){f=(t-(c.t_in-e))/e}else if(t<=c.t_out){f=null;inside++}else{f=(t-c.t_out)/e}
  var p=f===null?0:(t<c.t_in?f-1:f);var d=p*420;var cxp=400+lane*(c.side%2?1:-1),cyp=225+lane;
  if(c.side===0){x=cxp;y=cyp+d}else if(c.side===1){x=cxp+d;y=cyp}else if(c.side===2){x=cxp;y=cyp-d}else{x=cxp-d;y=cyp}
  cx.fillStyle=c.col;cx.save();cx.translate(x,y);cx.rotate(c.side%2?0:Math.PI/2);rr(-22,-12,44,24,5);cx.restore()});
 overlay(t,'XING-4')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8957)
