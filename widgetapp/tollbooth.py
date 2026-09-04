#!/usr/bin/env python3
"""232-toll-booth: a toll plaza clip: vehicles pass through one lane; tag-equipped vehicles roll through (green
light), others stop at the booth to pay (red light, pause). Count vehicles that STOPPED to pay. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Toll plaza clip"; HEADING = "Toll plaza camera, lane 3 (clip, 2:00)"; QUESTION = "How many vehicles STOPPED at the booth to pay (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280"]


def reset():
    t = 2.0; ev = []
    while t < 110:
        stop = random.random() < 0.4; ev.append({"t": round(t, 1), "stop": stop, "c": random.choice(COLORS), "van": random.random() < 0.3}); t += (8 if stop else 4.5) + random.uniform(0, 2)
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["stop"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#93c5fd';cx.fillRect(0,0,800,180);cx.fillStyle='#4b5563';cx.fillRect(0,180,800,270);cx.fillStyle='#374151';cx.fillRect(0,280,800,80);cx.fillStyle='#d1d5db';cx.fillRect(360,120,80,160);cx.fillStyle='#1f2937';cx.fillRect(380,150,40,40);cx.fillStyle='#e5e7eb';cx.font='bold 12px system-ui';cx.fillText('TOLL',382,110);
 var light='#9ca3af';D.ev.forEach(function(e){var P=e.stop?7:4,dt=t-e.t;if(dt<0||dt>P)return;var x;if(e.stop){if(dt<2)x=-80+dt/2*370;else if(dt<5){x=290;light='#ef4444'}else x=290+(dt-5)/2*600}else{x=-80+dt/4*960;if(dt>1&&dt<2.5)light='#22c55e'}var w=e.van?100:76;cx.fillStyle=e.c;cx.fillRect(x-w/2,300,w,34);cx.fillStyle='#111827';cx.beginPath();cx.arc(x-w/2+14,338,9,0,6.28);cx.arc(x+w/2-14,338,9,0,6.28);cx.fill()});
 cx.fillStyle=light;cx.beginPath();cx.arc(400,90,12,0,6.28);cx.fill();cx.fillStyle='#fbbf24';cx.fillRect(440,250,4,40);
 overlay(t,'TOLL-L3')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8895)
