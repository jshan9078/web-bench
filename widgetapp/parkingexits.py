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
    occ = [random.random() < 0.6 for _ in range(10)]; cols = [random.choice(COLS) for _ in range(10)]; ev = []; busy = [0.0] * 10
    for _ in range(300):
        t = random.uniform(2, 112); sp = random.randrange(10)
        if any(e["sp"] == sp and abs(e["t"] - t) < 6 for e in ev): continue
        # keep each spot's timeline consistent: a leave needs a parked car, an arrival needs an empty spot
        later = [e for e in ev if e["sp"] == sp and e["t"] > t]; state = occ[sp]
        for e in sorted([e for e in ev if e["sp"] == sp and e["t"] < t], key=lambda e: e["t"]): state = e["kind"] == "arrive"
        kind = random.choice(["leaveA", "leaveB", "leaveB"]) if state else "arrive"
        if later and (later[0]["kind"] == "arrive") == (kind == "arrive"): continue
        ev.append({"t": round(t, 1), "sp": sp, "kind": kind, "col": cols[sp] if kind != "arrive" else random.choice(COLS)})
        if kind == "arrive": cols[sp] = ev[-1]["col"]
        if len(ev) >= 30: break
    S["ev"] = sorted(ev, key=lambda e: e["t"]); S["init"] = [{"occ": o, "col": c} for o, c in zip(occ, [e["col"] for e in [next((x for x in S["ev"] if x["sp"] == i and x["kind"] != "arrive"), {"col": cols[i]}) for i in range(10)]])]


def data(): return {"ev": S["ev"], "init": S["init"]}
def answer(): return sum(1 for e in S["ev"] if e["kind"] == "leaveB")


SCENE_JS = r"""function scene(t){cx.fillStyle='#4b5563';cx.fillRect(0,0,800,450);cx.strokeStyle='#f3f4f6';cx.lineWidth=2;for(var i=0;i<10;i++){cx.strokeRect(40+(i%5)*150,i<5?120:260,130,80)}cx.fillStyle='#166534';cx.fillRect(300,0,120,40);cx.fillRect(760,180,40,120);cx.fillStyle='#fff';cx.font='bold 14px system-ui';cx.fillText('EXIT A',330,26);cx.save();cx.translate(786,240);cx.rotate(-Math.PI/2);cx.fillText('EXIT B',-24,0);cx.restore();
 for(var sp=0;sp<10;sp++){var x=40+(sp%5)*150+65,y=(sp<5?120:260)+40,col=D.init[sp].occ?D.init[sp].col:null;
  D.ev.forEach(function(e){if(e.sp!==sp)return;if(e.kind==='arrive'){if(t>=e.t+4)col=e.col}else{if(t>=e.t)col=null}});
  if(col){cx.fillStyle=col;rr(x-40,y-22,80,44,8)}}
 D.ev.forEach(function(e){var dt=t-e.t;if(dt<0||dt>4)return;var k=dt/4,sx=40+(e.sp%5)*150+65,sy=(e.sp<5?120:260)+40,tx,ty;if(e.kind==='leaveA'){tx=360;ty=-40}else if(e.kind==='leaveB'){tx=840;ty=240}else{tx=sx;ty=sy;sx=-60;sy=240}var x=sx+(tx-sx)*k,y=sy+(ty-sy)*k;cx.fillStyle=e.col;rr(x-40,y-22,80,44,8)});
 overlay(t,'LOT-B')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8986)
