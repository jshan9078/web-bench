#!/usr/bin/env python3
"""221-drone-drops: an overhead clip of two houses (A left, B right): delivery drones fly in and drop a parcel at
one house or the other; some drones abort and fly out without dropping. Count parcels dropped at HOUSE B.
complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Drone delivery clip"; HEADING = "Rooftop camera, delivery pad (clip, 2:00)"; QUESTION = "How many parcels were dropped at HOUSE B (exact)?"
S = {"ev": []}


def reset():
    n = random.randint(18, 24); ts = sorted(random.uniform(3, 112) for _ in range(n))
    S["ev"] = [{"t": round(t, 1), "target": random.choice(["A", "B", "B", "none"]), "y": random.randint(120, 300)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["target"] == "B")


SCENE_JS = r"""function scene(t){cx.fillStyle='#65a30d';cx.fillRect(0,0,800,450);cx.fillStyle='#78716c';cx.fillRect(360,0,80,450);cx.fillStyle='#b91c1c';cx.fillRect(80,140,180,160);cx.fillStyle='#1d4ed8';cx.fillRect(540,140,180,160);cx.fillStyle='#fff';cx.font='bold 22px system-ui';cx.fillText('A',160,230);cx.fillText('B',620,230);cx.fillStyle='#fde68a';cx.fillRect(120,320,100,50);cx.fillRect(580,320,100,50);
 var dropsA=0,dropsB=0;D.ev.forEach(function(e){var P=5,dt=t-e.t;if(dt>P){if(e.target==='A')dropsA++;if(e.target==='B')dropsB++;return}if(dt<0)return;var f=dt/P,tx=e.target==='A'?170:e.target==='B'?630:400,x=400+(tx-400)*Math.min(1,f*2),y=-30+f*(e.y+30);if(e.target==='none'){y=-30+f*480;x=400+Math.sin(f*6)*60}
 cx.fillStyle='#111827';cx.fillRect(x-22,y-6,44,12);cx.beginPath();cx.arc(x-22,y,9,0,6.28);cx.arc(x+22,y,9,0,6.28);cx.fill();if(e.target!=='none'&&f>0.6){var g=(f-0.6)/0.4;cx.fillStyle='#c2a074';cx.fillRect(tx-10,y+10+g*(345-y),20,16)}});
 cx.fillStyle='#c2a074';for(var i=0;i<dropsA;i++)cx.fillRect(125+(i%4)*24,325+Math.floor(i/4)*12,20,10);for(var i=0;i<dropsB;i++)cx.fillRect(585+(i%4)*24,325+Math.floor(i/4)*12,20,10);
 overlay(t,'PAD-CAM')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8884)
