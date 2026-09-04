#!/usr/bin/env python3
"""236-bike-dock: a bike-share dock clip: riders dock bikes (arrive) and undock bikes (leave). The dock count at the
start is shown. Count bikes in the dock at the END. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Bike dock clip"; HEADING = "Bike-share dock camera, Harbor St (clip, 2:00)"; QUESTION = "How many bikes are in the dock at the END of the clip (exact)?"
S = {"ev": [], "start": 0}


def reset():
    S["start"] = random.randint(4, 8); n = random.randint(16, 22); ts = sorted(random.uniform(3, 112) for _ in range(n)); cnt = S["start"]; ev = []
    for t in ts:
        d = 1 if (cnt <= 1 or (cnt < 12 and random.random() < 0.5)) else -1; cnt += d; ev.append({"t": round(t, 1), "d": d, "c": random.choice(["#dc2626", "#2563eb", "#111827", "#f59e0b", "#10b981"])})
    S["ev"] = ev


def data(): return {"ev": S["ev"], "start": S["start"]}
def answer(): return S["start"] + sum(e["d"] for e in S["ev"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#cbd5e1';cx.fillRect(0,0,800,450);cx.fillStyle='#64748b';cx.fillRect(0,330,800,120);cx.fillStyle='#334155';cx.fillRect(100,200,600,20);cx.fillStyle='#0f172a';cx.font='bold 14px system-ui';cx.fillText('Bikes docked at start: '+D.start,100,60);
 var cnt=D.start;D.ev.forEach(function(e){var P=4,dt=t-e.t;if(dt>P){cnt+=e.d;return}if(dt<0)return;var f=dt/P,x=e.d>0?-40+f*(130+(cnt%12)*46+40):130+((cnt-1)%12)*46+f*700,y=e.d>0?400-f*160:240+f*160;cx.fillStyle=e.c;cx.beginPath();cx.arc(x-14,y,10,0,6.28);cx.arc(x+14,y,10,0,6.28);cx.stroke();cx.fillRect(x-12,y-14,24,6)});
 for(var i=0;i<cnt;i++){cx.fillStyle='#1e293b';cx.fillRect(120+i*46,222,8,40);cx.fillStyle='#dc2626';cx.fillRect(112+i*46,240,24,8)}
 overlay(t,'DOCK-HARBOR')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8899)
