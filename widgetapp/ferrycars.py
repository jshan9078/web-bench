#!/usr/bin/env python3
"""220-ferry-boarding: a ferry ramp clip: vehicles queue and drive onto the ferry; when the deck is full the
barrier closes and remaining vehicles are turned away (reverse out). Count vehicles that BOARDED. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Ferry ramp clip"; HEADING = "Ferry ramp camera (clip, 2:00)"; QUESTION = "How many vehicles BOARDED the ferry (drove onto the deck) during the clip (exact)?"
S = {"ev": []}
COLORS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981"]


def reset():
    t = 3.0; ev = []
    while t < 108:
        ev.append({"t": round(t, 1), "board": random.random() < 0.65, "c": random.choice(COLORS), "van": random.random() < 0.3}); t += random.uniform(4.5, 8)
    S["ev"] = ev


def data(): return {"ev": S["ev"]}
def answer(): return sum(1 for e in S["ev"] if e["board"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#0ea5e9';cx.fillRect(0,0,800,450);cx.fillStyle='#374151';cx.fillRect(0,260,420,190);cx.fillStyle='#1e3a8a';cx.fillRect(500,120,300,260);cx.fillStyle='#93c5fd';cx.fillRect(520,140,260,40);cx.fillStyle='#4b5563';cx.fillRect(420,300,80,60);
 var closed=false;D.ev.forEach(function(e){var P=6,dt=t-e.t;if(dt<0||dt>P)return;var f=dt/P,x,y=330;if(f<0.5){x=-60+f*2*440}else{var g=(f-0.5)*2;if(e.board){x=380+g*260;y=330-g*90}else{closed=true;x=380-g*440}}var w=e.van?70:56;cx.fillStyle=e.c;cx.fillRect(x-w/2,y-16,w,32);cx.fillStyle='#111827';cx.beginPath();cx.arc(x-w/2+12,y+18,7,0,6.28);cx.arc(x+w/2-12,y+18,7,0,6.28);cx.fill()});
 cx.fillStyle=closed?'#ef4444':'#22c55e';cx.fillRect(470,270,8,60);if(closed){cx.fillStyle='#ef4444';cx.fillRect(420,286,80,6)}
 cx.fillStyle='#fff';cx.font='bold 14px system-ui';cx.fillText('FERRY DECK',600,110);cx.fillText(closed?'BARRIER CLOSED':'BARRIER OPEN',380,250);
 overlay(t,'RAMP-2')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8883)
