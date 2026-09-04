#!/usr/bin/env python3
"""218-vending-dispensed: a vending-machine clip: customers press buttons; sometimes an item drops to the tray,
sometimes the machine shows SOLD OUT and refunds. Count items actually DISPENSED. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Vending clip"; HEADING = "Break-room camera (clip, 2:00)"; QUESTION = "How many items were actually DISPENSED (dropped into the tray) during the clip (exact)?"
S = {"ev": []}


def reset():
    n = random.randint(16, 22); sp = 110 / n; ts = [4 + i * sp + random.uniform(0, sp - 4) for i in range(n)]
    S["ev"] = [{"t": round(t, 1), "ok": random.random() < 0.65, "c": random.choice(["#ef4444", "#3b82f6", "#22c55e", "#f59e0b"])} for t in ts]


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["ok"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#e5e7eb';cx.fillRect(0,0,800,450);cx.fillStyle='#1f2937';cx.fillRect(280,40,240,380);cx.fillStyle='#93c5fd';cx.fillRect(295,55,150,200);cx.fillStyle='#111827';cx.fillRect(300,300,200,60);cx.fillStyle='#374151';cx.fillRect(460,60,45,180);
 var msg='';D.ev.forEach(function(e){var dt=t-e.t;if(dt<0||dt>4)return;if(dt<1.2){msg='SELECT'}else if(e.ok){msg='VENDING';var f=(dt-1.2)/2.8;cx.fillStyle=e.c;cx.fillRect(360,120+f*190,40,26)}else{msg='SOLD OUT'}});
 cx.fillStyle='#f87171';cx.font='bold 14px ui-monospace,Menlo,monospace';cx.fillText(msg,470,140);
 overlay(t,'BREAK-RM')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8882)
