#!/usr/bin/env python3
"""331-counter-pickups: 2-minute clip of a restaurant pass: plates appear on the counter and one of three waiters
(red, blue, green aprons) picks each up. Count the plates picked up by the BLUE waiter. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Pass clip"; HEADING = "Kitchen pass camera (clip, 2:00)"; QUESTION = "How many plates did the BLUE waiter pick up (exact)?"
S = {"plates": []}


def reset():
    pl = []; t = random.uniform(2, 5)
    while t < DUR - 6:
        pl.append({"t": round(t, 1), "wait": round(random.uniform(1.5, 4), 1), "w": random.randrange(3), "slot": random.randrange(5)}); t += random.uniform(2.5, 5)
    S["plates"] = pl


def data(): return {"plates": S["plates"]}
def answer(): return sum(1 for p in S["plates"] if p["w"] == 1)


SCENE_JS = r"""function scene(t){cx.fillStyle='#292524';cx.fillRect(0,0,800,450);cx.fillStyle='#a16207';cx.fillRect(100,200,600,40);cx.fillStyle='#57534e';cx.fillRect(100,240,600,210);var W=['#dc2626','#2563eb','#16a34a'];
 D.plates.forEach(function(p){var dt=t-p.t,x=150+p.slot*125;if(dt<0||dt>p.wait+2.5)return;if(dt<=p.wait){cx.fillStyle='#f5f5f4';cx.beginPath();cx.arc(x,205,22,0,6.28);cx.fill()}
  else{var k=(dt-p.wait)/2.5,y=260+(1-Math.abs(k-0.5)*2)*-40+k*180;person(W[p.w],x-12,y+70,t);if(k<0.6){cx.fillStyle='#f5f5f4';cx.beginPath();cx.arc(x+18,y-20,14,0,6.28);cx.fill()}}});
 overlay(t,'PASS-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8965)
