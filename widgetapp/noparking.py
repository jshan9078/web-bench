#!/usr/bin/env python3
"""219-no-parking: a street clip with a hatched NO PARKING zone and legal bays; cars arrive and park in either.
Count DISTINCT cars that parked (stopped) in the no-parking zone during the clip. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Street clip"; HEADING = "Street camera, Church St loading zone (clip, 2:00)"; QUESTION = "How many different cars stopped in the hatched NO PARKING zone during the clip (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981"]


def reset():
    t = 3.0; ev = []
    while t < 105:
        ev.append({"t": round(t, 1), "zone": random.random() < 0.45, "stay": round(random.uniform(4, 9), 1), "c": random.choice(COLORS), "pass": random.random() < 0.25}); t += random.uniform(6, 11)
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["zone"] and not e["pass"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#374151';cx.fillRect(0,0,800,450);cx.fillStyle='#9ca3af';cx.fillRect(0,0,800,90);cx.fillStyle='#4b5563';cx.fillRect(0,90,800,80);cx.strokeStyle='#fbbf24';cx.lineWidth=3;for(var i=0;i<12;i++){cx.beginPath();cx.moveTo(60+i*20,92);cx.lineTo(40+i*20,168);cx.stroke()}cx.fillStyle='#fff';cx.font='bold 13px system-ui';cx.fillText('NO PARKING',80,60);
 cx.strokeStyle='#e5e7eb';cx.lineWidth=2;for(var k=0;k<3;k++){cx.strokeRect(420+k*120,92,110,76)}cx.fillText('BAYS',560,60);
 D.ev.forEach(function(e){var dt=t-e.t;if(dt<0)return;var tx=e.zone?150:e.pass?900:440+((e.t*7)%3)*120,y=e.pass?260:130;var x;if(e.pass){if(dt>5)return;x=-100+dt/5*1000;y=260}else if(dt<3){x=-100+dt/3*(tx+100)}else if(dt<3+e.stay){x=tx}else if(dt<6+e.stay){x=tx+(dt-3-e.stay)/3*(900-tx)}else return;cx.fillStyle=e.c;cx.fillRect(x-45,y-18,90,36);cx.fillStyle='#111827';cx.beginPath();cx.arc(x-28,y+20,9,0,6.28);cx.arc(x+28,y+20,9,0,6.28);cx.fill()});
 overlay(t,'CHURCH-ST')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8881)
