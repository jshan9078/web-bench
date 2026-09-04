#!/usr/bin/env python3
"""240-trolley-returns: a supermarket car-park clip: shoppers push trolleys to their cars; some return the trolley
to the bay afterwards, others leave it by the car. Count trolleys LEFT by cars (not returned). complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Car park clip"; HEADING = "Supermarket car park camera (clip, 2:00)"; QUESTION = "How many trolleys were left by a car instead of being returned to the bay (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(14, 20); sp = 112 / n; ts = [3 + i * sp + random.uniform(0, sp - 5) for i in range(n)]
    S["ev"] = [{"t": round(t, 1), "ret": random.random() < 0.55, "car": random.randint(0, 4), "c": random.choice(COLORS)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if not e["ret"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#6b7280';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(40,40,120,120);cx.fillStyle='#e5e7eb';cx.font='bold 12px system-ui';cx.fillText('TROLLEY BAY',36,30);for(var i=0;i<5;i++){cx.fillStyle=['#dc2626','#2563eb','#e5e7eb','#111827','#f59e0b'][i];cx.fillRect(240+i*110,300,80,40)}
 var left={};D.ev.forEach(function(e){var P=8,dt=t-e.t,cxp=280+e.car*110;if(dt<0)return;if(dt>P){if(!e.ret)left[e.car]=(left[e.car]||0)+1;return}var f=dt/P,x,y;if(f<0.4){x=100+(cxp-100)/0.4*f;y=120+(260-120)/0.4*f}else if(f<0.6){x=cxp;y=260}else{var g=(f-0.6)/0.4;if(e.ret){x=cxp-(cxp-100)*g;y=260-140*g}else{x=cxp+40*g;y=260+120*g}}person(e.c,x,y,t);if(e.ret||f<0.6){cx.strokeStyle='#d1d5db';cx.lineWidth=2;cx.strokeRect(x+22,y-30,22,18)}});
 Object.keys(left).forEach(function(k){for(var i=0;i<left[k];i++){cx.strokeStyle='#d1d5db';cx.lineWidth=2;cx.strokeRect(300+k*110+i*8,262-i*6,22,18)}});
 overlay(t,'CARPARK-S')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8903)
