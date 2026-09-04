#!/usr/bin/env python3
"""333-lead-changes: 2-minute scoreboard clip of a basketball game (scores update every few seconds); count how
many times the LEAD CHANGED (a tie followed by the same team regaining the lead is not a change). complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Scoreboard clip"; HEADING = "Arena scoreboard (clip, 2:00)"; QUESTION = "How many times did the LEAD change hands during the clip (exact)?"
S = {"events": [], "changes": 0}


def reset():
    for _ in range(300):
        ev = []; t = 2.0; a = b = 0
        while t < DUR - 2:
            team = random.choice("AB"); pts = random.choice([1, 2, 2, 3])
            if team == "A": a += pts
            else: b += pts
            ev.append({"t": round(t, 1), "a": a, "b": b}); t += random.uniform(3, 7)
        leader = None; changes = 0
        for e in ev:
            cur = "A" if e["a"] > e["b"] else ("B" if e["b"] > e["a"] else None)
            if cur and leader and cur != leader: changes += 1
            if cur: leader = cur
        if 4 <= changes <= 9: break
    S["events"] = ev; S["changes"] = changes


def data(): return {"events": S["events"]}
def answer(): return S["changes"]


SCENE_JS = r"""function scene(t){cx.fillStyle='#111';cx.fillRect(0,0,800,450);var a=0,b=0;D.events.forEach(function(e){if(t>=e.t){a=e.a;b=e.b}});cx.fillStyle='#222';cx.fillRect(60,80,320,250);cx.fillRect(420,80,320,250);cx.fillStyle='#f87171';cx.font='bold 28px system-ui';cx.fillText('HAWKS',150,120);cx.fillStyle='#60a5fa';cx.fillText('OTTERS',505,120);cx.fillStyle='#fde047';cx.font='bold 120px ui-monospace,Menlo,monospace';cx.fillText(String(a).padStart(2,'0'),150,270);cx.fillText(String(b).padStart(2,'0'),510,270);
 cx.fillStyle='#e5e7eb';cx.font='18px system-ui';cx.fillText('PERIOD '+(1+Math.floor(t/40)),340,370);
 overlay(t,'ARENA')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8967)
