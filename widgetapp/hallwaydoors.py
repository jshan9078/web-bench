#!/usr/bin/env python3
"""350-hallway-doors: 2-minute hallway clip with five numbered doors; people walk along and enter a door (or walk
through to the far end). Count how many people entered ROOM 3. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Hallway clip"; HEADING = "Hallway camera (clip, 2:00)"; QUESTION = "How many people entered ROOM 3 (exact)?"
S = {"ppl": []}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset(): S["ppl"] = [{"t": round(random.uniform(1, 112), 1), "door": random.choice([0, 1, 2, 3, 4, None, 2]), "dir": random.choice([1, -1]), "col": random.choice(COLS)} for _ in range(random.randint(24, 32))]
def data(): return {"ppl": S["ppl"]}
def answer(): return sum(1 for p in S["ppl"] if p["door"] == 2)


SCENE_JS = r"""function scene(t){cx.fillStyle='#e5e5e5';cx.fillRect(0,0,800,450);cx.fillStyle='#a3a3a3';cx.fillRect(0,300,800,150);for(var i=0;i<5;i++){var x=120+i*140;cx.fillStyle='#7c2d12';cx.fillRect(x-30,170,60,130);cx.fillStyle='#fff';cx.font='bold 14px system-ui';cx.fillText('ROOM '+(i+1),x-26,160)}
 D.ppl.forEach(function(p){var dt=t-p.t,T=7;if(dt<0||dt>T)return;var sx=p.dir>0?-30:830,ex=p.door===null?(p.dir>0?830:-30):120+p.door*140,dist=Math.abs(ex-sx),k=Math.min(1,dt*130/dist);if(k>=1&&p.door!==null)return;var x=sx+(ex-sx)*k;var fade=1;if(p.door!==null&&k>0.92)fade=(1-k)/0.08;cx.globalAlpha=fade;person(p.col,x-12,380,t);cx.globalAlpha=1});
 overlay(t,'HALL-4')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8983)
