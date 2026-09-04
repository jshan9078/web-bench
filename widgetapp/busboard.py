#!/usr/bin/env python3
"""211-bus-boarding: a bus-stop clip: a bus stops several times; at each stop some passengers alight (exit) and
some board (enter). Count the passengers who BOARDED over the whole clip. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Bus stop clip"; HEADING = "Bus stop camera, route 94 (clip, 2:00)"; QUESTION = "How many passengers BOARDED the bus during the clip (exact)?"
S = {"stops": []}
COLORS = ["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981", "#8b5cf6"]


def reset():
    t = 4.0; stops = []
    while t < 100:
        off = random.randint(0, 4); on = random.randint(0, 5); ev = [{"d": -1, "c": random.choice(COLORS)} for _ in range(off)] + [{"d": 1, "c": random.choice(COLORS)} for _ in range(on)]
        stops.append({"t": round(t, 1), "ev": ev}); t += 6 + 2.2 * len(ev) + random.uniform(6, 14)
    S["stops"] = stops


def data(): return {"stops": S["stops"]}
def answer(): return sum(1 for s in S["stops"] for e in s["ev"] if e["d"] > 0)


SCENE_JS = r"""function scene(t){cx.fillStyle='#93c5fd';cx.fillRect(0,0,800,200);cx.fillStyle='#4b5563';cx.fillRect(0,200,800,250);cx.fillStyle='#d1d5db';cx.fillRect(0,330,800,120);
 D.stops.forEach(function(s){var n=s.ev.length,stay=4+2.2*n,dt=t-s.t;if(dt<-3||dt>stay+3)return;var bx=dt<0?-400+((dt+3)/3)*500:dt>stay?100+((dt-stay)/3)*900:100;cx.fillStyle='#f59e0b';cx.fillRect(bx,180,400,130);cx.fillStyle='#1f2937';for(var i=0;i<4;i++)cx.fillRect(bx+20+i*95,195,70,50);cx.fillStyle='#111827';cx.beginPath();cx.arc(bx+70,312,18,0,6.28);cx.arc(bx+330,312,18,0,6.28);cx.fill();cx.fillStyle='#fff';cx.font='bold 16px system-ui';cx.fillText('94',bx+360,205);
 if(dt>=0&&dt<=stay){cx.fillStyle='#9ca3af';cx.fillRect(bx+150,190,60,120);s.ev.forEach(function(e,i){var a=2+i*2.2,q=t-s.t-a;if(q<0||q>2.2)return;var f=q/2.2,y=e.d>0?400-f*100:300+f*100;person(e.c,bx+170,y,t)})}});
 overlay(t,'STOP-94')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8878)
