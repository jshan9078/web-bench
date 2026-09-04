#!/usr/bin/env python3
"""196-turn-count: an intersection camera clip: vehicles approach from the bottom and either go straight (up) or
turn LEFT at the junction. Count the vehicles that turned left. Tracking each vehicle's path. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Intersection clip"; HEADING = "Intersection camera, Mill Rd and 3rd Ave (clip, 2:00)"; QUESTION = "How many vehicles turned LEFT at the junction (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981"]


def reset():
    n = random.randint(20, 28); ts = sorted(random.uniform(2, 112) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "left": random.random() < 0.4, "c": random.choice(COLORS), "van": random.random() < 0.3} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["left"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#4b5563';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(340,0,120,450);cx.fillRect(0,180,800,120);cx.fillStyle='#e5e7eb';for(var y=0;y<450;y+=40)cx.fillRect(398,y,4,20);for(var x=0;x<800;x+=40)cx.fillRect(x,238,20,4);
 D.ev.forEach(function(e){var P=6,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x=400,y;if(f<0.5){y=470-f*2*230}else{var g=(f-0.5)*2;if(e.left){x=400-g*460;y=240}else{y=240-g*260}}var w=e.van?34:26,h=e.van?56:44;cx.fillStyle=e.c;if(e.left&&f>=0.5){cx.fillRect(x-h/2,y-w/2,h,w)}else{cx.fillRect(x-w/2,y-h/2,w,h)}});
 overlay(t,'INT-MILL-3RD')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8872)
