#!/usr/bin/env python3
"""339-birds-on-wire: 2-minute clip of birds landing on and leaving a wire; report the maximum number of birds on
the wire at the same time. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Wire clip"; HEADING = "Garden camera (clip, 2:00)"; QUESTION = "Maximum number of birds on the wire at the same time (exact)?"
S = {"birds": [], "peak": 0}


def reset():
    for _ in range(300):
        birds = []; slots = random.sample([60 + k * 31 for k in range(22)], 22)
        for i in range(random.randint(16, 22)):
            a = random.uniform(2, 108); birds.append({"t_in": round(a, 1), "t_out": round(min(DUR + 3, a + random.uniform(4, 30)), 1), "x": slots[i], "col": random.choice(["#1c1917", "#44403c", "#7c2d12", "#374151"]), "ang": random.uniform(-1, 1)})
        peak = max(sum(1 for c in birds if c["t_in"] <= x["t_in"] < c["t_out"]) for x in birds)
        if 6 <= peak <= 10: break
    S["birds"] = birds; S["peak"] = peak


def data(): return {"birds": S["birds"]}
def answer(): return S["peak"]


SCENE_JS = r"""function scene(t){cx.fillStyle='#bae6fd';cx.fillRect(0,0,800,450);cx.strokeStyle='#1c1917';cx.lineWidth=3;cx.beginPath();cx.moveTo(0,240);cx.quadraticCurveTo(400,270,800,240);cx.stroke();
 D.birds.forEach(function(b){var e=2.5,x,y,wy=240+15*Math.sin(Math.PI*b.x/800);if(t<b.t_in-e||t>b.t_out+e)return;if(t<b.t_in){var k=(t-(b.t_in-e))/e;x=b.x+b.ang*200*(1-k);y=-20+(wy-12+20)*k}else if(t<=b.t_out){x=b.x;y=wy-12}else{var k=(t-b.t_out)/e;x=b.x+b.ang*200*k;y=wy-12-k*300}
  cx.fillStyle=b.col;cx.beginPath();cx.ellipse(x,y,12,8,0,0,6.28);cx.fill();cx.beginPath();cx.arc(x+9,y-7,5,0,6.28);cx.fill()});
 overlay(t,'GARDEN')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8973)
