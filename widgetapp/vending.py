#!/usr/bin/env python3
"""359-vending: 2-minute clip of a vending machine; customers insert a coin and press a button; sometimes an item
drops into the tray (success), sometimes nothing drops. Count the SUCCESSFUL purchases. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Vending clip"; HEADING = "Break room camera (clip, 2:00)"; QUESTION = "How many purchases dispensed an item (exact)?"
S = {"ev": []}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset():
    ev = []; t = random.uniform(2, 5)
    while t < DUR - 8:
        ev.append({"t": round(t, 1), "ok": random.random() < 0.62, "col": random.choice(COLS), "item": random.choice(["#f97316", "#a3e635", "#38bdf8"])}); t += random.uniform(5, 9)
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["ok"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#e7e5e4';cx.fillRect(0,0,800,450);cx.fillStyle='#1e3a8a';cx.fillRect(300,60,200,360);cx.fillStyle='#0f172a';cx.fillRect(320,80,110,200);cx.fillStyle='#f8fafc';cx.fillRect(320,330,160,40);cx.fillStyle='#64748b';cx.fillRect(450,120,30,60);cx.fillStyle='#ef4444';cx.beginPath();cx.arc(465,210,10,0,6.28);cx.fill();
 D.ev.forEach(function(e){var dt=t-e.t;if(dt<0||dt>6)return;var x=dt<1?150+dt*100:dt>5?250+(dt-5)*300:250;person(e.col,x,380,t);
  if(dt>1.2&&dt<1.8){cx.fillStyle='#facc15';cx.beginPath();cx.arc(465,150,6,0,6.28);cx.fill()}
  if(dt>2&&dt<2.5){cx.fillStyle='#fca5a5';cx.beginPath();cx.arc(465,210,13,0,6.28);cx.fill()}
  if(e.ok&&dt>3&&dt<5){var k=(dt-3)/2,y=100+k*230;cx.fillStyle=e.item;cx.fillRect(360,Math.min(y,335),30,24)}});
 overlay(t,'BREAK-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8989)
