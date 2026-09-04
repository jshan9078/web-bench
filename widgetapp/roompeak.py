#!/usr/bin/env python3
"""324-room-peak: a 2-minute top-down clip of a meeting room with two doors; people enter and leave through
either door and wander inside. Report the maximum number of people in the room at once. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Room clip"; HEADING = "Meeting room camera (clip, 2:00)"; QUESTION = "Maximum number of people in the room at the same time (exact)?"
S = {"people": [], "peak": 0}
COLS = ["#dc2626", "#2563eb", "#e5e7eb", "#111827", "#f59e0b", "#6b7280", "#10b981", "#8b5cf6", "#f472b6", "#fbbf24"]


def reset():
    for _ in range(300):
        ppl = []
        for i in range(random.randint(14, 20)):
            a = random.uniform(3, 105); ppl.append({"t_in": round(a, 1), "t_out": round(min(DUR + 5, a + random.uniform(6, 40)), 1), "din": random.randrange(2), "dout": random.randrange(2), "col": random.choice(COLS), "sx": random.randint(150, 650), "sy": random.randint(120, 330), "ph": random.uniform(0, 6.28)})
        peak = max(sum(1 for c in ppl if c["t_in"] <= x["t_in"] < c["t_out"]) for x in ppl)
        if 6 <= peak <= 10: break
    S["people"] = ppl; S["peak"] = peak


def data(): return {"people": S["people"]}
def answer(): return S["peak"]


SCENE_JS = r"""function scene(t){cx.fillStyle='#d6d3d1';cx.fillRect(0,0,800,450);cx.fillStyle='#f5f5f4';cx.fillRect(80,60,640,340);cx.fillStyle='#78350f';cx.fillRect(280,180,240,90);cx.fillStyle='#a8a29e';cx.fillRect(80,140,10,60);cx.fillRect(710,300,10,60);cx.fillStyle='#292524';cx.font='12px system-ui';cx.fillText('DOOR A',20,175);cx.fillText('DOOR B',730,335);
 var doors=[[85,170],[715,330]];
 D.people.forEach(function(p){var e=2.5;if(t<p.t_in-e||t>p.t_out+e)return;var x,y;var tx=p.sx+Math.sin(t*0.6+p.ph)*40,ty=p.sy+Math.cos(t*0.5+p.ph)*30;
  if(t<p.t_in){var f=(t-(p.t_in-e))/e,d=doors[p.din];x=d[0]-(1-f)*60*(p.din?-1:1)+f*(tx-d[0]);y=d[1]+f*(ty-d[1]);x=f<0.5?d[0]-(0.5-f)*2*60*(p.din?-1:1):d[0]+(f-0.5)*2*(tx-d[0]);y=f<0.5?d[1]:d[1]+(f-0.5)*2*(ty-d[1])}
  else if(t<=p.t_out){x=tx;y=ty}
  else{var f=(t-p.t_out)/e,d=doors[p.dout];x=f<0.5?tx+f*2*(d[0]-tx):d[0]+(f-0.5)*2*60*(p.dout?1:-1);y=f<0.5?ty+f*2*(d[1]-ty):d[1]}
  cx.fillStyle=p.col;cx.beginPath();cx.arc(x,y,11,0,6.28);cx.fill();cx.strokeStyle='#1c1917';cx.lineWidth=1.5;cx.stroke()});
 overlay(t,'ROOM-3')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8959)
