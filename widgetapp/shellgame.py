#!/usr/bin/env python3
"""306-shell-game: three identical cups; the ball is shown under one at the start, then the cups are swapped 14
times over 40 s with the cups sliding past each other. Report the ball's final position (1 = left, 3 = right).
complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 45; TITLE = "Cups clip"; HEADING = "Table camera (clip, 0:45)"; QUESTION = "Which position is the ball under at the end (1 = left, 2 = middle, 3 = right)?"
S = {"start": 0, "swaps": []}


def reset():
    S["start"] = random.randrange(3); sw = []; t = 4.0
    for _ in range(14):
        a = random.randrange(3); b = random.choice([x for x in range(3) if x != a]); sw.append({"t": round(t, 2), "a": a, "b": b, "d": round(random.uniform(0.7, 1.3), 2)}); t += random.uniform(1.6, 2.6)
    S["swaps"] = sw


def data(): return {"start": S["start"], "swaps": S["swaps"]}


def answer():
    pos = S["start"]
    for s in S["swaps"]:
        if pos == s["a"]: pos = s["b"]
        elif pos == s["b"]: pos = s["a"]
    return pos + 1


SCENE_JS = r"""function scene(t){cx.fillStyle='#14532d';cx.fillRect(0,0,800,450);var slots=[200,400,600],cups=[0,1,2],xs=[200,400,600],ball=D.start,lift=t<3?1-Math.min(1,Math.max(0,(t-2))):0;
 D.swaps.forEach(function(s){if(t<s.t)return;var p=Math.min(1,(t-s.t)/s.d),e=(1-Math.cos(p*Math.PI))/2,ax=slots[s.a],bx=slots[s.b];if(p<1){xs[s.a]=ax+(bx-ax)*e;xs[s.b]=bx+(ax-bx)*e;var ya=Math.sin(p*Math.PI)*40;xs['ya'+s.a]=ya;xs['ya'+s.b]=-ya}else{var tmp=slots[s.a];slots[s.a]=slots[s.b];slots[s.b]=tmp;xs[s.a]=slots[s.a];xs[s.b]=slots[s.b]}});
 var order=[0,1,2].sort(function(i,j){return (xs['ya'+i]||0)-(xs['ya'+j]||0)});
 if(t<3){cx.fillStyle='#f59e0b';cx.beginPath();cx.arc(slots[ball],300,14,0,6.28);cx.fill()}
 order.forEach(function(i){var x=xs[i],y=290+(xs['ya'+i]||0)-(i===ball?lift*70:0);cx.fillStyle='#b91c1c';cx.beginPath();cx.moveTo(x-45,y+30);cx.lineTo(x+45,y+30);cx.lineTo(x+30,y-70);cx.lineTo(x-30,y-70);cx.closePath();cx.fill();cx.fillStyle='#7f1d1d';cx.fillRect(x-48,y+26,96,10)});
 overlay(t,'TABLE-1')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8946)
