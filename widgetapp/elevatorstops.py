#!/usr/bin/env python3
"""206-elevator-stops: a lobby-panel clip: an elevator indicator shows the current floor; the car stops (doors open)
at some floors and passes others. Count the floors where it STOPPED (doors opened). complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Elevator clip"; HEADING = "Elevator B indicator camera (clip, 2:00)"; QUESTION = "How many times did the elevator STOP with its doors opening during the clip (exact)?"
S = {"seg": []}


def reset():
    t = 2.0; floor = random.randint(1, 4); seg = []
    while t < 110:
        target = random.choice([f for f in range(1, 13) if f != floor]); travel = abs(target - floor) * 1.4
        seg.append({"t0": round(t, 1), "f0": floor, "f1": target, "dur": round(travel, 1), "stop": random.random() < 0.6}); t += travel
        if seg[-1]["stop"]: t += 4.0
        floor = target
    S["seg"] = seg


def data(): return {"seg": S["seg"]}
def answer(): return sum(1 for s in S["seg"] if s["stop"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#e5e7eb';cx.fillRect(0,0,800,450);cx.fillStyle='#1f2937';cx.fillRect(250,40,300,380);var floor=D.seg.length?D.seg[0].f0:1,open=0;
 D.seg.forEach(function(s){var end=s.t0+s.dur;if(t>=s.t0&&t<end){floor=s.f0+(s.f1-s.f0)*((t-s.t0)/s.dur)}else if(t>=end){floor=s.f1;if(s.stop&&t<end+4){var dt=t-end;open=dt<1?dt:dt>3?4-dt:1}}});
 cx.fillStyle='#9ca3af';cx.fillRect(270,60,260,300);cx.fillStyle='#374151';cx.fillRect(270,60,130-open*125,300);cx.fillRect(400+open*125,60,130-open*125,300);
 cx.fillStyle='#111827';cx.fillRect(330,380,140,32);cx.fillStyle='#f87171';cx.font='bold 22px ui-monospace,Menlo,monospace';cx.fillText('FLOOR '+Math.round(floor),340,404);
 overlay(t,'ELEV-B')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8875)
