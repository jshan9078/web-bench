#!/usr/bin/env python3
"""323-two-lane-defects: a 90-second clip of a two-lane conveyor; items cross the frame in about 2 s; a defective
item has a small dark notch. Count the defective items on the UPPER lane only. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 90; TITLE = "Conveyor clip"; HEADING = "Packing line camera (clip, 1:30)"; QUESTION = "How many DEFECTIVE items passed on the UPPER lane (exact)?"
S = {"items": []}


def reset():
    items = []
    for lane in (0, 1):
        t = random.uniform(2, 4)
        while t < DUR - 3:
            items.append({"t": round(t, 2), "lane": lane, "bad": random.random() < 0.28, "col": random.choice(["#fbbf24", "#a3e635", "#93c5fd", "#fca5a5"])}); t += random.uniform(2.2, 4.5)
    S["items"] = items


def data(): return {"items": S["items"]}
def answer(): return sum(1 for i in S["items"] if i["lane"] == 0 and i["bad"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#1f2937';cx.fillRect(0,0,800,450);[120,300].forEach(function(y){cx.fillStyle='#4b5563';cx.fillRect(0,y,800,90);cx.fillStyle='#6b7280';for(var i=0;i<20;i++)cx.fillRect(((i*60-(t*150)%60)+800)%800,y+80,30,6)});cx.fillStyle='#e5e7eb';cx.font='bold 14px system-ui';cx.fillText('UPPER LANE',10,110);cx.fillText('LOWER LANE',10,290);
 D.items.forEach(function(it){var dt=t-it.t;if(dt<0||dt>2.2)return;var x=820-dt/2.2*860,y=(it.lane?300:120)+20;cx.fillStyle=it.col;rr(x,y,52,44,6);if(it.bad){cx.fillStyle='#111827';cx.beginPath();cx.arc(x+40,y+12,5,0,6.28);cx.fill()}});
 overlay(t,'LINE-B')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8958)
