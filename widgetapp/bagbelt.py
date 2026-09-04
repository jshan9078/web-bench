#!/usr/bin/env python3
"""233-bag-belt: a baggage-reclaim clip: bags appear on the carousel; passengers pick some up. Count bags STILL on
the belt at the end of the clip. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Baggage reclaim clip"; HEADING = "Baggage reclaim camera, belt 6 (clip, 2:00)"; QUESTION = "How many bags are STILL on the belt at the end of the clip (exact)?"
S = {"bags": []}
COLORS = ["#111827", "#7c2d12", "#1e3a8a", "#9f1239", "#365314", "#6b7280"]


def reset():
    n = random.randint(14, 20); bags = []
    for i in range(n):
        t = round(random.uniform(2, 90), 1); taken = random.random() < 0.6
        bags.append({"t": t, "take": round(t + random.uniform(8, 28), 1) if taken else None, "c": random.choice(COLORS), "w": random.randint(28, 44)})
    S["bags"] = bags


def data(): return {"bags": S["bags"]}
def answer(): return sum(1 for b in S["bags"] if b["take"] is None or b["take"] > DUR)


SCENE_JS = r"""function bpos(u){u=((u%1)+1)%1;var L=2*600+2*220;var d=u*L;if(d<600)return [100+d,120];d-=600;if(d<220)return [700,120+d];d-=220;if(d<600)return [700-d,340];d-=600;return [100,340-d]}
function scene(t){cx.fillStyle='#e5e7eb';cx.fillRect(0,0,800,450);cx.fillStyle='#6b7280';cx.beginPath();cx.roundRect(60,90,680,290,40);cx.fill();cx.fillStyle='#e5e7eb';cx.beginPath();cx.roundRect(130,160,540,150,30);cx.fill();
 D.bags.forEach(function(b){var dt=t-b.t;if(dt<0)return;if(b.take!==null&&t>b.take+1.5)return;var u=(b.t*0.13+dt/40)%1,p=bpos(u);if(b.take!==null&&t>b.take){var f=(t-b.take)/1.5;p=[p[0],p[1]+(p[1]<230?-1:1)*f*80];person('#374151',p[0]+30,p[1]<230?60:430,t)}cx.fillStyle=b.c;cx.fillRect(p[0]-b.w/2,p[1]-14,b.w,28)});
 overlay(t,'RECLAIM-6')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8896)
