#!/usr/bin/env python3
"""224-crane-lifts: a port clip: a gantry crane moves containers from the ship (right) to the quay (left) and
sometimes back. Count containers moved SHIP TO QUAY. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Port crane clip"; HEADING = "Berth 4 crane camera (clip, 2:00)"; QUESTION = "How many containers were moved from the SHIP to the QUAY (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#f59e0b", "#10b981", "#6b7280"]


def reset():
    t = 2.0; ev = []
    while t < 108:
        ev.append({"t": round(t, 1), "to_quay": random.random() < 0.7, "c": random.choice(COLORS)}); t += random.uniform(6.5, 9)
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["to_quay"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#bae6fd';cx.fillRect(0,0,800,250);cx.fillStyle='#0369a1';cx.fillRect(0,250,800,200);cx.fillStyle='#57534e';cx.fillRect(0,250,300,200);cx.fillStyle='#1f2937';cx.fillRect(500,230,300,120);cx.fillStyle='#e5e7eb';cx.font='bold 14px system-ui';cx.fillText('QUAY',40,240);cx.fillText('SHIP',700,225);cx.fillStyle='#374151';cx.fillRect(100,40,600,16);cx.fillRect(100,40,16,210);cx.fillRect(684,40,16,210);
 var cx0=400,q=0,s=0;D.ev.forEach(function(e){var P=6,dt=t-e.t;if(dt>P){if(e.to_quay)q++;else s++;return}if(dt<0)return;var f=dt/P,from=e.to_quay?620:180,to=e.to_quay?180:620,x=from+(to-from)*f,y=f<0.2?230-f*5*130:f>0.8?100+(f-0.8)*5*130:100;cx0=x;cx.fillStyle='#374151';cx.fillRect(x-2,56,4,y-56-20);cx.fillStyle=e.c;cx.fillRect(x-40,y-20,80,40)});
 cx.fillStyle='#374151';cx.fillRect(cx0-30,44,60,14);
 cx.fillStyle='#6b7280';for(var i=0;i<q;i++)cx.fillRect(40+(i%3)*85,250-(Math.floor(i/3)+1)*22,80,20);
 overlay(t,'BERTH-4')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8887)
