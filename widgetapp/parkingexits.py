#!/usr/bin/env python3
"""355-parking-exits: 2-minute clip of a car park with two exits (A top, B right); parked cars leave through one of
them, others arrive. Count the cars that left through EXIT B. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Car park exits clip"; HEADING = "Car park camera (clip, 2:00)"; QUESTION = "How many cars left through EXIT B (exact)?"
S = {"ev": []}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6"]


def reset():
    ev = []; busy = [0] * 10
    for _ in range(random.randint(26, 34)):
        t = random.uniform(2, 112); sp = random.randrange(10)
        if busy[sp] > t - 1: continue
        ev.append({"t": round(t, 1), "sp": sp, "kind": random.choice(["leaveA", "leaveB", "leaveB", "arrive"]), "col": random.choice(COLS)}); busy[sp] = t + 5
    S["ev"] = sorted(ev, key=lambda e: e["t"])


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["kind"] == "leaveB")


SCENE_JS = r"""function scene(t){cx.fillStyle='#4b5563';cx.fillRect(0,0,800,450);cx.strokeStyle='#f3f4f6';cx.lineWidth=2;for(var i=0;i<10;i++){cx.strokeRect(40+(i%5)*150,i<5?120:260,130,80)}cx.fillStyle='#166534';cx.fillRect(300,0,120,40);cx.fillRect(760,180,40,120);cx.fillStyle='#fff';cx.font='bold 14px system-ui';cx.fillText('EXIT A',330,26);cx.save();cx.translate(786,240);cx.rotate(-Math.PI/2);cx.fillText('EXIT B',-24,0);cx.restore();
 var parked={};D.ev.forEach(function(e){if(t>=e.t+4){parked[e.sp]=e.kind==='arrive'?e.col:null}});
 D.ev.forEach(function(e){var dt=t-e.t;if(e.kind==='arrive'){if(dt>=0&&dt<4){}}});
 // static parked cars: initial occupancy = spots whose first event is a leave
 var first={};D.ev.forEach(function(e){if(!(e.sp in first))first[e.sp]=e});
 for(var sp=0;sp<10;sp++){var x=40+(sp%5)*150+65,y=(sp<5?120:260)+40;var col=null;var f=first[sp];if(f&&f.kind!=='arrive'&&t<f.t)col=f.col;D.ev.forEach(function(e){if(e.sp===sp){if(e.kind==='arrive'&&t>=e.t+4)col=e.col;if(e.kind!=='arrive'&&t>=e.t)col=null;if(e.kind!=='arrive'&&t<e.t&&e.t>(first[sp]&&first[sp].t||0))col=e.col}});if(col){cx.fillStyle=col;rr(x-40,y-22,80,44,8)}}
 D.ev.forEach(function(e){var dt=t-e.t;if(dt<0||dt>4)return;var k=dt/4,sx=40+(e.sp%5)*150+65,sy=(e.sp<5?120:260)+40,tx,ty;if(e.kind==='leaveA'){tx=360;ty=-40}else if(e.kind==='leaveB'){tx=840;ty=240}else{tx=sx;ty=sy;sx=-60;sy=240}var x=sx+(tx-sx)*k,y=sy+(ty-sy)*k;cx.fillStyle=e.col;rr(x-40,y-22,80,44,8)});
 overlay(t,'LOT-B')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8986)
