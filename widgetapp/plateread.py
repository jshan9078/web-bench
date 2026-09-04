#!/usr/bin/env python3
"""305-plate-read: a 45-second roadside clip; several cars pass, each visible for about 1.3 s. Read the licence
plate of the RED car (7 characters, small text). complete = exact plate (case/space-insensitive)."""
import random, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 45; TITLE = "Roadside clip"; HEADING = "Roadside camera (clip, 0:45)"; QUESTION = "Licence plate of the RED car (7 characters)?"
S = {"cars": []}


def plate(): return "".join(random.choice("ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(3)) + "-" + "".join(random.choice("0123456789") for _ in range(4))


def reset():
    cols = ["#dc2626", "#2563eb", "#eab308", "#6b7280", "#16a34a", "#f97316"]; random.shuffle(cols); ts = sorted(random.sample(range(4, 41, 3), 6))
    S["cars"] = [{"t": t + random.uniform(0, 1.5), "col": c, "plate": plate(), "dir": random.choice([1, -1])} for t, c in zip(ts, cols)]


def data(): return {"cars": S["cars"]}
def answer(): return next(c["plate"] for c in S["cars"] if c["col"] == "#dc2626")


SCENE_JS = r"""function scene(t){cx.fillStyle='#9ca3af';cx.fillRect(0,0,800,450);cx.fillStyle='#4b5563';cx.fillRect(0,250,800,200);cx.fillStyle='#e5e7eb';for(var i=0;i<10;i++)cx.fillRect(i*90,345,50,6);cx.fillStyle='#65a30d';cx.fillRect(0,230,800,20);
 D.cars.forEach(function(c){var dt=t-c.t;if(dt<0||dt>1.3)return;var x=c.dir>0?-200+dt/1.3*1000:1000-dt/1.3*1000;cx.fillStyle=c.col;rr(x,270,190,70,12);cx.fillStyle='#111827';cx.fillRect(x+30,255,120,30);cx.fillStyle='#1f2937';cx.beginPath();cx.arc(x+40,342,18,0,6.28);cx.arc(x+150,342,18,0,6.28);cx.fill();cx.fillStyle='#f9fafb';cx.fillRect(x+70,318,54,14);cx.fillStyle='#111827';cx.font='bold 11px ui-monospace,Menlo,monospace';cx.fillText(c.plate,x+72,329)});
 overlay(t,'ROAD-7')}"""
clipapp.make(sys.modules[__name__])
_inner_state = state


def state():
    st = _inner_state(); subs = st["submissions"]; norm = lambda s: s.upper().replace(" ", "").replace("-", "")
    st["complete"] = bool(subs) and norm(subs[-1]) == norm(answer()); return st


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8945)
