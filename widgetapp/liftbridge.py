#!/usr/bin/env python3
"""229-bridge-boats: a canal clip: boats approach a lift bridge; when the bridge is raised they pass under it,
otherwise they wait and turn back. Count boats that PASSED under the raised bridge. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Canal bridge clip"; HEADING = "Canal camera, lift bridge (clip, 2:00)"; QUESTION = "How many boats PASSED under the bridge during the clip (exact)?"
S = {"ev": [], "raised": []}


def reset():
    raised = []; t = random.uniform(5, 15)
    while t < 115: raised.append([round(t, 1), round(t + random.uniform(10, 18), 1)]); t += random.uniform(24, 34)
    S["raised"] = raised; n = random.randint(14, 20); ts = sorted(random.uniform(2, 112) for _ in range(n))
    S["ev"] = [{"t": round(x, 1), "d": random.choice([1, -1]), "c": random.choice(["#dc2626", "#2563eb", "#f5f5f4", "#f59e0b"])} for x in ts]


def up_at(t): return any(a <= t <= b for a, b in S["raised"])
def data(): return {"ev": S["ev"], "raised": S["raised"]}
def answer(): return sum(1 for e in S["ev"] if up_at(e["t"] + 3))


SCENE_JS = r"""function upAt(t){return D.raised.some(function(r){return t>=r[0]&&t<=r[1]})}
function scene(t){cx.fillStyle='#86efac';cx.fillRect(0,0,800,450);cx.fillStyle='#0284c7';cx.fillRect(0,200,800,120);cx.fillStyle='#57534e';cx.fillRect(380,140,40,60);cx.fillRect(380,320,40,60);var up=upAt(t);cx.fillStyle='#a16207';if(up){cx.fillRect(385,60,30,80)}else{cx.fillRect(385,190,30,20);cx.fillRect(340,195,120,10)}cx.fillStyle='#111827';cx.font='bold 13px system-ui';cx.fillText(up?'BRIDGE RAISED':'BRIDGE DOWN',350,50);
 D.ev.forEach(function(e){var P=6,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,pass=upAt(e.t+3),x;if(pass){x=e.d>0?-60+f*920:860-f*920}else{var g=f<0.5?f*2:2-f*2;x=e.d>0?-60+g*380:860-g*380}cx.fillStyle=e.c;cx.fillRect(x-30,245,60,24);cx.fillStyle='#111827';cx.fillRect(x-8,230,16,15)});
 overlay(t,'CANAL-BR')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8892)
