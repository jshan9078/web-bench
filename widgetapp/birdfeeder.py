#!/usr/bin/env python3
"""360-bird-feeder: 2-minute clip of a bird feeder visited by birds of three colours; a visit is a landing followed
by a departure. Count the visits by BLUE birds (several blue birds may visit, sometimes two at once). complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Feeder clip"; HEADING = "Bird feeder camera (clip, 2:00)"; QUESTION = "How many visits did BLUE birds make to the feeder (exact)?"
S = {"v": []}


def reset(): S["v"] = [{"t": round(random.uniform(2, 112), 1), "d": round(random.uniform(2, 7), 1), "col": random.choice(["#2563eb", "#dc2626", "#ca8a04", "#2563eb"]), "perch": random.randrange(4), "side": random.choice([1, -1])} for _ in range(random.randint(22, 30))]
def data(): return {"v": S["v"]}
def answer(): return sum(1 for x in S["v"] if x["col"] == "#2563eb")


SCENE_JS = r"""function scene(t){cx.fillStyle='#bbf7d0';cx.fillRect(0,0,800,450);cx.fillStyle='#78350f';cx.fillRect(390,40,20,120);cx.fillRect(330,160,140,120);cx.fillStyle='#fcd34d';cx.fillRect(340,170,120,100);var P=[[320,300],[480,300],[340,330],[460,330]];cx.fillStyle='#78350f';P.forEach(function(p){cx.fillRect(p[0]-30,p[1],60,8)});
 D.v.forEach(function(v){var e=1.5,dt=t-v.t;if(dt<-e||dt>v.d+e)return;var p=P[v.perch],x,y,sx=p[0]+v.side*400,sy=60;if(dt<0){var k=(dt+e)/e;x=sx+(p[0]-sx)*k;y=sy+(p[1]-12-sy)*k}else if(dt<=v.d){x=p[0];y=p[1]-12}else{var k=(dt-v.d)/e;x=p[0]+(sx-p[0])*k;y=p[1]-12+(sy-p[1]+12)*k}
  cx.fillStyle=v.col;cx.beginPath();cx.ellipse(x,y,13,8,0,0,6.28);cx.fill();cx.beginPath();cx.arc(x+10*v.side,y-6,5,0,6.28);cx.fill()});
 overlay(t,'FEEDER')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8990)
