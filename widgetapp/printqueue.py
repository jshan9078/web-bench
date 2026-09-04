#!/usr/bin/env python3
"""241-printer-jams: an office printer clip: jobs print one after another (pages emerge to the tray); some jobs jam
(red light, no page, someone opens the cover). Count jobs that printed successfully. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Printer clip"; HEADING = "Print room camera (clip, 2:00)"; QUESTION = "How many print jobs completed successfully (a page came out) (exact)?"
S = {"ev": []}


def reset():
    n = random.randint(20, 26); sp = 112 / n; ts = [3 + i * sp + random.uniform(0, sp - 3.5) for i in range(n)]
    S["ev"] = [{"t": round(t, 1), "ok": random.random() < 0.7} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["ok"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#f5f5f4';cx.fillRect(0,0,800,450);cx.fillStyle='#57534e';cx.fillRect(250,160,300,180);cx.fillStyle='#292524';cx.fillRect(270,180,260,30);cx.fillStyle='#a8a29e';cx.fillRect(250,340,300,20);
 var light='#9ca3af',pages=0;D.ev.forEach(function(e){var P=3,dt=t-e.t;if(dt>P){if(e.ok)pages++;return}if(dt<0)return;var f=dt/P;if(e.ok){light='#22c55e';cx.fillStyle='#fff';cx.fillRect(360,300+f*50,80,14)}else{light='#ef4444';if(f>0.4){cx.fillStyle='#78716c';cx.fillRect(250,120,300,40)}}});
 cx.fillStyle='#fff';for(var i=0;i<pages;i++)cx.fillRect(360,352-i*2,80,3);cx.fillStyle=light;cx.beginPath();cx.arc(520,195,8,0,6.28);cx.fill();
 overlay(t,'PRINT-RM')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8904)
