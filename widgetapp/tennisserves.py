#!/usr/bin/env python3
"""235-tennis-serves: a court camera clip: serves land in the service box (IN) or beyond a line (OUT, a line judge's
arm goes up). Count serves that were IN. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Tennis court clip"; HEADING = "Court 2 serve camera (clip, 2:00)"; QUESTION = "How many serves landed IN (no OUT call) (exact)?"
S = {"ev": []}


def reset():
    n = random.randint(18, 24); sp = 112 / n; ts = [4 + i * sp + random.uniform(0, sp - 3.5) for i in range(n)]
    S["ev"] = [{"t": round(t, 1), "in": random.random() < 0.6, "x": random.randint(300, 500)} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["in"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#1d4ed8';cx.fillRect(0,0,800,450);cx.fillStyle='#2563eb';cx.fillRect(150,40,500,370);cx.strokeStyle='#fff';cx.lineWidth=3;cx.strokeRect(150,40,500,370);cx.beginPath();cx.moveTo(150,225);cx.lineTo(650,225);cx.moveTo(150,120);cx.lineTo(650,120);cx.moveTo(400,120);cx.lineTo(400,225);cx.stroke();cx.fillStyle='#e5e7eb';cx.fillRect(150,222,500,6);
 var call=false;D.ev.forEach(function(e){var P=3,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,y=430-Math.min(f,0.6)/0.6*(430-(e.in?170:90)),x=e.x;if(f>0.6)y=(e.in?170:90)+(f-0.6)*60;cx.fillStyle='#fde047';cx.beginPath();cx.arc(x,y,8,0,6.28);cx.fill();if(!e.in&&f>0.6){call=true;cx.fillStyle='#fff';cx.font='bold 22px system-ui';cx.fillText('OUT',380,30)}});
 person('#f8fafc',690,120,t);if(call){cx.fillStyle='#f8fafc';cx.fillRect(712,40,6,30)}overlay(t,'COURT-2')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8898)
