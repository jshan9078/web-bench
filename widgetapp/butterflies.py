#!/usr/bin/env python3
"""348-butterflies: 2-minute garden clip; butterflies of several colours flutter through and some land on the big
flower for a moment. Count how many BLUE butterflies landed on the flower. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Garden clip"; HEADING = "Flower bed camera (clip, 2:00)"; QUESTION = "How many BLUE butterflies landed on the large flower (exact)?"
S = {"bf": []}


def reset(): S["bf"] = [{"t": round(random.uniform(2, 114), 1), "col": random.choice(["#3b82f6", "#f97316", "#facc15", "#3b82f6", "#a855f7", "#f472b6"]), "land": random.random() < 0.55, "y": random.randint(60, 380), "ph": random.uniform(0, 6.28)} for _ in range(random.randint(30, 40))]
def data(): return {"bf": S["bf"]}
def answer(): return sum(1 for b in S["bf"] if b["col"] == "#3b82f6" and b["land"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#86efac';cx.fillRect(0,0,800,450);cx.fillStyle='#16a34a';cx.fillRect(390,260,20,190);for(var i=0;i<8;i++){cx.fillStyle='#f472b6';cx.beginPath();cx.ellipse(400+Math.cos(i*0.785)*45,240+Math.sin(i*0.785)*45,28,16,i*0.785,0,6.28);cx.fill()}cx.fillStyle='#fde047';cx.beginPath();cx.arc(400,240,26,0,6.28);cx.fill();
 D.bf.forEach(function(b){var dt=t-b.t,T=b.land?6:4;if(dt<0||dt>T)return;var x,y;if(!b.land){var k=dt/4;x=-30+k*860;y=b.y+Math.sin(t*6+b.ph)*25}else{if(dt<2){var k=dt/2;x=-30+k*430;y=b.y+(240-b.y)*k+Math.sin(t*6+b.ph)*25*(1-k)}else if(dt<4){x=400;y=240}else{var k=(dt-4)/2;x=400+k*430;y=240+(b.y-240)*k+Math.sin(t*6+b.ph)*25*k}}
  var w=Math.abs(Math.sin(t*12+b.ph))*14+4;cx.fillStyle=b.col;cx.beginPath();cx.ellipse(x-w/2-2,y,w/2+4,9,0,0,6.28);cx.ellipse(x+w/2+2,y,w/2+4,9,0,0,6.28);cx.fill();cx.fillStyle='#111';cx.fillRect(x-1,y-8,2,16)});
 overlay(t,'BED-2')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8981)
