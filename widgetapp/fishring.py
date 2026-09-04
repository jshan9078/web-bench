#!/usr/bin/env python3
"""351-fish-ring: 2-minute aquarium clip; fish of several colours swim around and some pass through a hoop. Count
how many times a fish swam through the hoop (any colour). complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Aquarium clip"; HEADING = "Aquarium camera (clip, 2:00)"; QUESTION = "How many times did a fish swim through the hoop (exact)?"
S = {"passes": [], "amb": []}


def reset():
    S["passes"] = [{"t": round(random.uniform(2, 116), 1), "col": random.choice(["#f97316", "#facc15", "#22d3ee", "#f43f5e"]), "dir": random.choice([1, -1])} for _ in range(random.randint(8, 14))]
    S["amb"] = [{"col": random.choice(["#f97316", "#facc15", "#22d3ee", "#f43f5e"]), "y": random.randint(60, 400), "sp": random.uniform(0.3, 0.7), "ph": random.uniform(0, 6.28), "amp": random.randint(20, 60)} for _ in range(6)]


def data(): return {"passes": S["passes"], "amb": S["amb"]}
def answer(): return len(S["passes"])


SCENE_JS = r"""function fish(col,x,y,d){cx.fillStyle=col;cx.beginPath();cx.ellipse(x,y,18,9,0,0,6.28);cx.fill();cx.beginPath();cx.moveTo(x-d*16,y);cx.lineTo(x-d*30,y-9);cx.lineTo(x-d*30,y+9);cx.closePath();cx.fill()}
function scene(t){cx.fillStyle='#0c4a6e';cx.fillRect(0,0,800,450);cx.fillStyle='#365314';cx.fillRect(0,420,800,30);cx.strokeStyle='#fbbf24';cx.lineWidth=6;cx.beginPath();cx.ellipse(400,230,14,70,0,0,6.28);cx.stroke();
 D.amb.forEach(function(a){var x=400+Math.sin(t*a.sp+a.ph)*340,d=Math.cos(t*a.sp+a.ph)>0?1:-1;if(Math.abs(x-400)<40){x=x<400?360:440}fish(a.col,x,a.y+Math.sin(t*1.3+a.ph)*a.amp,d)});
 D.passes.forEach(function(p){var dt=t-p.t;if(dt<-2.5||dt>2.5)return;var x=400+dt*140*p.dir;fish(p.col,x,230+Math.sin(dt*2)*6,p.dir)});
 overlay(t,'TANK-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8984)
