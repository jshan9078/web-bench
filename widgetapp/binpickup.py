#!/usr/bin/env python3
"""227-bin-pickup: a street clip: a refuse truck stops along a row of eight bins and the crew empties some bins
(tipped into the truck) and skips others (lid stays down, bin untouched). Count bins that were emptied. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Refuse truck clip"; HEADING = "Street camera, bin collection (clip, 2:00)"; QUESTION = "How many bins were EMPTIED into the truck during the clip (exact)?"
S = {"bins": []}


def reset():
    n = 8; S["bins"] = [{"x": 90 + i * 90, "t": round(6 + i * 13 + random.uniform(0, 4), 1), "empty": random.random() < 0.6, "c": random.choice(["#16a34a", "#2563eb", "#1f2937", "#a16207"])} for i in range(n)]


def data(): return {"bins": S["bins"]}
def answer(): return sum(1 for b in S["bins"] if b["empty"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#9ca3af';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(0,260,800,190);cx.fillStyle='#d6d3d1';cx.fillRect(0,230,800,30);
 var tx=-200;D.bins.forEach(function(b){if(t>=b.t-4)tx=Math.max(tx,b.x+40)});if(t<D.bins[0].t-4)tx=-200+(t/(D.bins[0].t-4))*(D.bins[0].x+240);
 cx.fillStyle='#f59e0b';cx.fillRect(tx-160,280,220,110);cx.fillStyle='#78350f';cx.fillRect(tx+60,300,60,90);cx.fillStyle='#111827';cx.beginPath();cx.arc(tx-120,395,20,0,6.28);cx.arc(tx+80,395,20,0,6.28);cx.fill();
 D.bins.forEach(function(b){var dt=t-b.t,lift=0,done=false;if(b.empty){if(dt>0&&dt<4)lift=dt<2?dt/2:(4-dt)/2;if(dt>=4)done=true}cx.fillStyle=b.c;var y=228-lift*110,x=b.x+lift*(tx-140-b.x);cx.fillRect(x-16,y-50,32,50);cx.fillStyle=done?'#e5e7eb':'#111827';cx.fillRect(x-18,y-56,36,8)});
 overlay(t,'BIN-DAY')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8890)
