#!/usr/bin/env python3
"""334-elevator-stops: 2-minute clip of an elevator floor indicator (floors G, 1-8) with a doors-open lamp; the car
moves between floors and opens its doors at some of them. Count the stops (doors opened) at floor 5.
complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Elevator clip"; HEADING = "Elevator indicator camera (clip, 2:00)"; QUESTION = "How many times did the elevator stop (doors opened) at floor 5 (exact)?"
S = {"stops": []}


def reset():
    for _ in range(300):
        stops = []; t = 1.0; f = 0
        while t < DUR - 6:
            nf = random.choice([x for x in range(9) if x != f]); t += abs(nf - f) * 1.4; f = nf; stops.append({"t": round(t, 1), "floor": f, "open": random.random() < 0.7}); t += 4 if stops[-1]["open"] else 0.6
        n5 = sum(1 for s in stops if s["floor"] == 5 and s["open"])
        if 3 <= n5 <= 6: break
    S["stops"] = stops


def data(): return {"stops": S["stops"]}
def answer(): return sum(1 for s in S["stops"] if s["floor"] == 5 and s["open"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#1f2937';cx.fillRect(0,0,800,450);var f=0,pf=0,pt=0,open=false;var prev={t:0,floor:0};D.stops.forEach(function(s){if(t>=s.t){prev=s}});var nxt=D.stops.find(function(s){return s.t>t});var cur=prev.floor;if(nxt){var dur=Math.abs(nxt.floor-prev.floor)*1.4,st=nxt.t-dur;if(t>st)cur=prev.floor+(nxt.floor-prev.floor)*Math.min(1,(t-st)/dur)}
 open=prev.open&&t<prev.t+4&&t>=prev.t;var lit=Math.round(cur);
 cx.fillStyle='#111827';cx.fillRect(250,60,300,330);['G','1','2','3','4','5','6','7','8'].forEach(function(l,i){var y=350-i*35;cx.fillStyle=i===lit?'#fbbf24':'#374151';cx.beginPath();cx.arc(300,y,12,0,6.28);cx.fill();cx.fillStyle='#e5e7eb';cx.font='bold 20px system-ui';cx.fillText(l,330,y+7)});
 cx.fillStyle=open?'#22c55e':'#3f3f46';cx.fillRect(420,300,100,60);cx.fillStyle='#fff';cx.font='bold 14px system-ui';cx.fillText(open?'DOORS OPEN':'DOORS SHUT',428,335);
 overlay(t,'LIFT-2')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8968)
