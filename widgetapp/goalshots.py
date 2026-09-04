#!/usr/bin/env python3
"""223-goal-shots: a five-a-side goal camera clip: shots come in; some are saved by the keeper, some hit the post
and bounce out, some cross the line (GOAL). Count goals. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Goal camera clip"; HEADING = "Goal-line camera, pitch 2 (clip, 2:00)"; QUESTION = "How many GOALS were scored (ball fully crossing the line into the net) (exact)?"
S = {"ev": []}


def reset():
    n = random.randint(16, 22); sp = 112 / n; ts = [4 + i * sp + random.uniform(0, sp - 3.5) for i in range(n)]
    S["ev"] = [{"t": round(t, 1), "r": random.choice(["goal", "goal", "save", "post"]), "x": random.randint(300, 500)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["r"] == "goal")


SCENE_JS = r"""function scene(t){cx.fillStyle='#16a34a';cx.fillRect(0,0,800,450);cx.fillStyle='#fff';cx.fillRect(0,300,800,4);cx.fillRect(270,120,8,184);cx.fillRect(522,120,8,184);cx.fillRect(270,120,260,8);cx.fillStyle='rgba(255,255,255,.25)';cx.fillRect(278,128,244,172);
 var kx=400;D.ev.forEach(function(e){var P=3,dt=t-e.t;if(dt<-1||dt>P)return;if(dt<0){kx=e.r==='save'?e.x:400+(400-e.x)*0.3;return}var f=dt/P,x=e.x,y;if(e.r==='goal'){y=440-f*230;if(dt>1.8){cx.fillStyle='#fde047';cx.font='bold 26px system-ui';cx.fillText('GOAL',360,80)}}else if(e.r==='save'){kx=e.x;y=440-Math.min(f,0.5)*280+(f>0.5?(f-0.5)*120:0)}else{y=440-Math.min(f,0.5)*260+(f>0.5?(f-0.5)*300:0);x=e.x<400?274:526}cx.fillStyle='#fff';cx.beginPath();cx.arc(x,y,9,0,6.28);cx.fill()});
 cx.fillStyle='#f59e0b';cx.fillRect(kx-14,230,28,60);cx.beginPath();cx.arc(kx,220,12,0,6.28);cx.fill();
 overlay(t,'GOAL-CAM')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8886)
