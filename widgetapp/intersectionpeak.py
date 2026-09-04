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
    cells = [(325 + (k % 4) * 50, 150 + (k // 4) * 50) for k in range(16)]
    for c in sorted(cars, key=lambda c: c["t_in"]):
        used = {c2.get("cell") for c2 in cars if "cell" in c2 and c2["t_in"] < c["t_out"] + 3 and c["t_in"] - 3 < c2["t_out"]}
        c["cell"] = random.choice([k for k in range(16) if k not in used] or list(range(16)))
    for c in cars: c["x"], c["y"] = cells[c["cell"]]
    S["cars"] = cars; S["peak"] = peak


def data(): return {"cars": S["cars"]}
def answer(): return S["peak"]


SCENE_JS = r"""function scene(t){cx.fillStyle='#4d7c0f';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(300,0,200,450);cx.fillRect(0,125,800,200);cx.strokeStyle='#fbbf24';cx.lineWidth=3;cx.strokeRect(300,125,200,200);
 var E=[[400,-40],[860,225],[400,490],[-60,225]];
 D.cars.forEach(function(c){var e=3;if(t<c.t_in-e||t>c.t_out+e)return;var x,y,en=E[c.side];
  if(t<c.t_in){var f=(t-(c.t_in-e))/e;x=en[0]+(c.x-en[0])*f;y=en[1]+(c.y-en[1])*f}
  else if(t<=c.t_out){x=c.x;y=c.y}
  else{var f=(t-c.t_out)/e,ex=E[(c.side+2)%4];x=c.x+(ex[0]-c.x)*f;y=c.y+(ex[1]-c.y)*f}
  cx.fillStyle=c.col;cx.save();cx.translate(x,y);cx.rotate(c.side%2?0:Math.PI/2);rr(-20,-11,40,22,5);cx.restore()});
 overlay(t,'XING-4')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8957)
