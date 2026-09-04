#!/usr/bin/env python3
"""349-train-cars: a freight train of 30-40 cars passes a level crossing over about 40 s within a 90 s clip; count
the TANK cars (cylindrical) as opposed to box cars and flat cars. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 90; TITLE = "Crossing clip"; HEADING = "Level crossing camera (clip, 1:30)"; QUESTION = "How many TANK cars did the train have (exact)?"
S = {"cars": [], "t0": 0}


def reset(): S["cars"] = [random.choice(["box", "tank", "flat", "box", "tank"]) for _ in range(random.randint(30, 40))]; S["t0"] = round(random.uniform(8, 20), 1)
def data(): return {"cars": S["cars"], "t0": S["t0"]}
def answer(): return S["cars"].count("tank")


SCENE_JS = r"""function scene(t){cx.fillStyle='#bfdbfe';cx.fillRect(0,0,800,450);cx.fillStyle='#4d7c0f';cx.fillRect(0,300,800,150);cx.fillStyle='#57534e';cx.fillRect(0,285,800,14);var speed=140,x0=900-(t-D.t0)*speed;
 D.cars.forEach(function(c,i){var x=x0+i*120;if(x<-130||x>820)return;if(c==='box'){cx.fillStyle='#b45309';cx.fillRect(x,215,110,70)}else if(c==='tank'){cx.fillStyle='#6b7280';cx.fillRect(x,240,110,45);cx.beginPath();cx.ellipse(x+55,245,55,26,0,0,6.28);cx.fill();cx.fillStyle='#374151';cx.fillRect(x+45,212,20,10)}else{cx.fillStyle='#78350f';cx.fillRect(x,268,110,17)}cx.fillStyle='#111';cx.beginPath();cx.arc(x+22,290,9,0,6.28);cx.arc(x+88,290,9,0,6.28);cx.fill()});
 if(x0-120<820&&x0-120>-140){cx.fillStyle='#dc2626';cx.fillRect(x0-120,205,115,80);cx.fillStyle='#fde68a';cx.fillRect(x0-40,220,25,20)}
 overlay(t,'XING-9')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8982)
