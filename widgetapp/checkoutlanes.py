#!/usr/bin/env python3
"""347-checkout-lanes: 2-minute clip of three checkout lanes; customers queue, are served (a brief flash of the
lane display) and leave. Count the customers served at LANE 2. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Checkout clip"; HEADING = "Store checkout camera (clip, 2:00)"; QUESTION = "How many customers were served at LANE 2 (exact)?"
S = {"serv": []}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset():
    serv = []
    for lane in range(3):
        t = random.uniform(2, 6)
        while t < DUR - 8:
            d = random.uniform(4, 9); serv.append({"lane": lane, "t0": round(t, 1), "t1": round(t + d, 1), "col": random.choice(COLS)}); t += d + random.uniform(0.5, 3)
    S["serv"] = serv


def data(): return {"serv": S["serv"]}
def answer(): return sum(1 for s in S["serv"] if s["lane"] == 1)


SCENE_JS = r"""function scene(t){cx.fillStyle='#e7e5e4';cx.fillRect(0,0,800,450);[0,1,2].forEach(function(l){var x=160+l*240;cx.fillStyle='#57534e';cx.fillRect(x-70,120,140,40);cx.fillStyle='#1c1917';cx.fillRect(x-30,70,60,40);cx.fillStyle='#f5f5f4';cx.font='bold 16px system-ui';cx.fillText('LANE '+(l+1),x-30,97)});
 D.serv.forEach(function(s){var x=160+s.lane*240,e=2.5;if(t<s.t0-e||t>s.t1+e)return;var y;if(t<s.t0){y=450-(t-(s.t0-e))/e*200}else if(t<=s.t1){y=250;if(t>s.t1-0.8){cx.fillStyle='#22c55e';cx.fillRect(x-30,70,60,40);cx.fillStyle='#fff';cx.font='bold 14px system-ui';cx.fillText('PAID',x-18,96)}}else{y=250;var k=(t-s.t1)/e;x=x+k*(l2(s.lane))}person(s.col,x-12,y+60,t)});
 function l2(l){return l===2?300:-300}
 overlay(t,'STORE-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8980)
