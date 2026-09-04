#!/usr/bin/env python3
"""330-ball-bins: 90-second clip of balls dropping through a peg board into three bins; count the balls that ended
in the RIGHT bin. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 90; TITLE = "Ball drop clip"; HEADING = "Ball drop camera (clip, 1:30)"; QUESTION = "How many balls ended in the RIGHT bin (exact)?"
S = {"balls": []}


def reset(): S["balls"] = [{"t": round(random.uniform(1, 86), 1), "bin": random.choices([0, 1, 2], [3, 4, 3])[0], "wob": random.uniform(0, 6.28), "col": random.choice(["#f87171", "#60a5fa", "#fbbf24", "#a3e635"])} for _ in range(random.randint(34, 44))]
def data(): return {"balls": S["balls"]}
def answer(): return sum(1 for b in S["balls"] if b["bin"] == 2)


SCENE_JS = r"""function scene(t){cx.fillStyle='#0f172a';cx.fillRect(0,0,800,450);cx.fillStyle='#94a3b8';for(var r=0;r<6;r++)for(var c=0;c<9;c++){cx.beginPath();cx.arc(120+c*70+(r%2)*35,90+r*45,5,0,6.28);cx.fill()}
 cx.fillStyle='#334155';[[130,'LEFT'],[400,'MIDDLE'],[670,'RIGHT']].forEach(function(b){cx.fillRect(b[0]-110,370,220,70);cx.fillStyle='#e2e8f0';cx.font='bold 13px system-ui';cx.fillText(b[1],b[0]-22,410);cx.fillStyle='#334155'});
 D.balls.forEach(function(b){var dt=t-b.t;if(dt<0||dt>3.5)return;var k=dt/3.2,tx=[130,400,670][b.bin],x=400+(tx-400)*Math.min(1,k)+Math.sin(t*9+b.wob)*(1-Math.min(1,k))*30,y=Math.min(395,20+k*380);cx.fillStyle=b.col;cx.beginPath();cx.arc(x,y,9,0,6.28);cx.fill()});
 overlay(t,'DROP-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8964)
