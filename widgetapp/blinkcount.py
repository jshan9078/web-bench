#!/usr/bin/env python3
"""296-blink-count: a 60-second clip of a control panel with three indicator lamps; the AMBER lamp blinks a random
number of times (each blink 0.8 s on), while the others blink on their own schedules. Count the amber blinks.
complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 60; TITLE = "Panel clip"; HEADING = "Control panel camera (clip, 1:00)"; QUESTION = "How many times did the AMBER lamp blink during the clip (exact)?"
S = {"amber": [], "red": [], "green": []}


def reset():
    def sched(n, lo, hi):
        ts = sorted(random.uniform(lo, hi) for _ in range(n)); out = []
        for t in ts:
            if not out or t - out[-1] >= 1.6: out.append(round(t, 1))
        return out
    S["amber"] = sched(random.randint(9, 16), 2, 57); S["red"] = sched(random.randint(6, 12), 2, 57); S["green"] = sched(random.randint(6, 12), 2, 57)


def data(): return {"amber": S["amber"], "red": S["red"], "green": S["green"]}
def answer(): return len(S["amber"])


SCENE_JS = r"""function on(list,t){return list.some(function(s){return t>=s&&t<s+0.8})}
function scene(t){cx.fillStyle='#374151';cx.fillRect(0,0,800,450);cx.fillStyle='#1f2937';cx.fillRect(150,100,500,250);[['#ef4444','RED',D.red],['#f59e0b','AMBER',D.amber],['#22c55e','GREEN',D.green]].forEach(function(l,i){var x=250+i*150,lit=on(l[2],t);cx.fillStyle=lit?l[0]:'#111827';cx.beginPath();cx.arc(x,200,40,0,6.28);cx.fill();if(lit){cx.fillStyle='rgba(255,255,255,.35)';cx.beginPath();cx.arc(x-12,188,10,0,6.28);cx.fill()}cx.fillStyle='#e5e7eb';cx.font='bold 14px system-ui';cx.fillText(l[1],x-22,280)});
 overlay(t,'PANEL-3')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8940)
