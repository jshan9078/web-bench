#!/usr/bin/env python3
"""357-swim-laps: 2-minute pool clip with four swimmers in four lanes at different speeds, turning at each wall;
count the lengths (wall to wall) completed by the swimmer with the RED cap. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Pool clip"; HEADING = "Pool camera (clip, 2:00)"; QUESTION = "How many pool lengths (wall to wall) did the RED-cap swimmer complete (exact)?"
S = {"sw": []}


def reset():
    caps = ["#dc2626", "#2563eb", "#facc15", "#22c55e"]; random.shuffle(caps)
    S["sw"] = [{"cap": c, "speed": round(random.uniform(38, 62), 1), "pause": round(random.uniform(0.5, 2.0), 1), "start": round(random.uniform(0, 3), 1), "lane": i} for i, c in enumerate(caps)]


def data(): return {"sw": S["sw"]}


def lengths(s, t=DUR):
    L = 640; tt = t - s["start"]; n = 0
    if tt <= 0: return 0
    per = L / s["speed"] + s["pause"]; n = int(tt // per); rem = tt - n * per
    return n if rem < L / s["speed"] else n + 1 if False else n + (1 if rem >= L / s["speed"] else 0)


def answer(): return lengths(next(s for s in S["sw"] if s["cap"] == "#dc2626"))


SCENE_JS = r"""function scene(t){cx.fillStyle='#0369a1';cx.fillRect(0,0,800,450);cx.fillStyle='#f8fafc';cx.fillRect(70,0,10,450);cx.fillRect(720,0,10,450);for(var i=1;i<4;i++){cx.fillStyle='#bae6fd';cx.fillRect(80,i*112,640,3)}
 D.sw.forEach(function(s){var L=640,tt=t-s.start,y=56+s.lane*112,x=80;if(tt>0){var per=L/s.speed+s.pause,n=Math.floor(tt/per),rem=tt-n*per,frac=Math.min(1,rem/(L/s.speed)),dir=n%2===0?1:-1;x=dir>0?80+frac*L:720-frac*L}
  cx.fillStyle='#fde68a';cx.beginPath();cx.ellipse(x,y,26,9,0,0,6.28);cx.fill();cx.fillStyle=s.cap;cx.beginPath();cx.arc(x+(t>s.start&&Math.floor((t-s.start)/(L/s.speed+s.pause))%2===0?20:-20),y,8,0,6.28);cx.fill()});
 overlay(t,'POOL-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8988)
