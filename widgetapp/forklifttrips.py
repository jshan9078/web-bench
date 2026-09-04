#!/usr/bin/env python3
"""338-forklift-trips: 2-minute warehouse clip; two forklifts shuttle between the left rack and the right dock.
Count the trips that carried a pallet from LEFT to RIGHT (empty runs and right-to-left carries do not count).
complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Warehouse clip"; HEADING = "Warehouse camera (clip, 2:00)"; QUESTION = "How many trips carried a pallet from LEFT to RIGHT (exact)?"
S = {"trips": []}


def reset():
    trips = []
    for lane in (0, 1):
        t = random.uniform(1, 4); d = 1
        while t < DUR - 6:
            trips.append({"t": round(t, 1), "lane": lane, "dir": d, "load": random.random() < 0.6}); t += 6 + random.uniform(0.5, 4); d = -d
    S["trips"] = trips


def data(): return {"trips": S["trips"]}
def answer(): return sum(1 for x in S["trips"] if x["dir"] == 1 and x["load"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#78716c';cx.fillRect(0,0,800,450);cx.fillStyle='#a16207';cx.fillRect(0,60,90,330);cx.fillStyle='#1e40af';cx.fillRect(710,60,90,330);cx.fillStyle='#fff';cx.font='bold 13px system-ui';cx.fillText('RACK',22,45);cx.fillText('DOCK',735,45);
 D.trips.forEach(function(x){var dt=t-x.t;if(dt<0||dt>5)return;var f=dt/5,px=x.dir>0?110+f*560:670-f*560,y=150+x.lane*140;cx.fillStyle='#facc15';rr(px-30,y,60,36,6);cx.fillStyle='#111';cx.beginPath();cx.arc(px-18,y+40,8,0,6.28);cx.arc(px+18,y+40,8,0,6.28);cx.fill();if(x.load){cx.fillStyle='#92400e';cx.fillRect(px+(x.dir>0?34:-70),y+6,36,26);cx.fillStyle='#d97706';cx.fillRect(px+(x.dir>0?34:-70),y+26,36,6)}});
 overlay(t,'WH-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8972)
