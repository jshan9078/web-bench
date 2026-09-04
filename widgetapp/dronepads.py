#!/usr/bin/env python3
"""328-drone-landings: 2-minute clip of three landing pads A, B, C; drones fly in, land on one pad for a while and
take off again. Count the landings on pad B. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Pads clip"; HEADING = "Landing pads camera (clip, 2:00)"; QUESTION = "How many drones LANDED on pad B during the clip (exact)?"
S = {"flights": []}


def reset():
    fl = []; pads_free = {0: 0, 1: 0, 2: 0}
    for _ in range(random.randint(18, 24)):
        pad = random.randrange(3); t = max(pads_free[pad], random.uniform(2, 100)) + random.uniform(0, 4); stay = random.uniform(3, 8)
        if t + stay > DUR - 2: continue
        fl.append({"t": round(t, 1), "stay": round(stay, 1), "pad": pad, "col": random.choice(["#f8fafc", "#fbbf24", "#60a5fa", "#f87171"]), "ang": random.uniform(0, 6.28)}); pads_free[pad] = t + stay + 3
    S["flights"] = fl


def data(): return {"flights": S["flights"]}
def answer(): return sum(1 for f in S["flights"] if f["pad"] == 1)


SCENE_JS = r"""function scene(t){cx.fillStyle='#1e293b';cx.fillRect(0,0,800,450);var P=[[180,250],[400,250],[620,250]];P.forEach(function(p,i){cx.fillStyle='#334155';cx.beginPath();cx.arc(p[0],p[1],60,0,6.28);cx.fill();cx.strokeStyle='#facc15';cx.lineWidth=3;cx.stroke();cx.fillStyle='#facc15';cx.font='bold 26px system-ui';cx.fillText('ABC'[i],p[0]-9,p[1]+9)});
 D.flights.forEach(function(f){var e=3,p=P[f.pad],dt=t-f.t;if(dt<-e||dt>f.stay+e)return;var x,y,s;var ox=p[0]+Math.cos(f.ang)*500,oy=p[1]+Math.sin(f.ang)*500;
  if(dt<0){var k=(dt+e)/e;x=ox+(p[0]-ox)*k;y=oy+(p[1]-oy)*k;s=1.4-0.4*k}else if(dt<=f.stay){x=p[0];y=p[1];s=1}else{var k=(dt-f.stay)/e;x=p[0]+(ox-p[0])*k;y=p[1]+(oy-p[1])*k;s=1+0.4*k}
  cx.fillStyle=f.col;[[-14,-14],[14,-14],[-14,14],[14,14]].forEach(function(a){cx.beginPath();cx.arc(x+a[0]*s,y+a[1]*s,7*s,0,6.28);cx.fill()});cx.fillRect(x-6*s,y-6*s,12*s,12*s)});
 overlay(t,'PADS-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8962)
