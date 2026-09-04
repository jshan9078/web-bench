#!/usr/bin/env python3
"""217-queue-leavers: a queue clip: people join a queue; most are served at the counter, some give up and walk
away (leave to the right) before being served. Count those who LEFT WITHOUT being served. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Ticket counter clip"; HEADING = "Ticket counter camera (clip, 2:00)"; QUESTION = "How many people LEFT the queue without being served (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset():
    n = random.randint(14, 20); arr = sorted(random.uniform(3, 100) for _ in range(n)); ev = []
    for a in arr: ev.append({"a": round(a, 1), "leave": random.random() < 0.3, "wait": round(random.uniform(6, 14), 1), "c": random.choice(COLORS)})
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["leave"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#e5e7eb';cx.fillRect(0,0,800,450);cx.fillStyle='#d1d5db';cx.fillRect(0,300,800,150);cx.fillStyle='#374151';cx.fillRect(40,150,160,110);cx.fillStyle='#111827';cx.font='bold 14px system-ui';cx.fillText('TICKETS',80,205);
 var q=0;D.ev.forEach(function(e){var dt=t-e.a;if(dt<0)return;var end=e.a+e.wait;if(t<end-3){if(dt<3){person(e.c,800-dt/3*(560-q*46),360,t)}else{person(e.c,240+q*46,360,t)}q++}else if(t<end){var f=(t-(end-3))/3;if(e.leave){person(e.c,240+q*46+f*560,360+f*40,t)}else{person(e.c,240-f*160,360-f*60,t)}}});
 overlay(t,'TICKETS-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8880)
