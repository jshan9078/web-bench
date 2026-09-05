#!/usr/bin/env python3
"""365-sorter-errors: 90-second clip of a colour sorter: items arrive on a belt and a diverter sends BLUE items left
and everything else right; sometimes it misroutes. Count the items that went to the WRONG side. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 90; TITLE = "Sorter clip"; HEADING = "Sorting line camera (clip, 1:30)"; QUESTION = "How many items were routed to the WRONG side (blue should go LEFT, all others RIGHT) (exact)?"
S = {"items": []}


def reset():
    items = []; t = random.uniform(1, 3)
    while t < DUR - 4:
        col = random.choice(["#2563eb", "#f59e0b", "#22c55e", "#2563eb", "#ef4444"]); correct = "L" if col == "#2563eb" else "R"; side = correct if random.random() < 0.8 else ("R" if correct == "L" else "L")
        items.append({"t": round(t, 1), "col": col, "side": side, "wrong": side != correct}); t += random.uniform(1.8, 3.2)
    S["items"] = items


def data(): return {"items": S["items"]}
def answer(): return sum(1 for i in S["items"] if i["wrong"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#1f2937';cx.fillRect(0,0,800,450);cx.fillStyle='#4b5563';cx.fillRect(360,0,80,260);cx.fillRect(40,260,720,60);cx.fillStyle='#e5e7eb';cx.font='bold 14px system-ui';cx.fillText('LEFT BIN (blue)',50,350);cx.fillText('RIGHT BIN (others)',600,350);cx.fillStyle='#374151';cx.fillRect(40,330,140,100);cx.fillRect(620,330,140,100);
 D.items.forEach(function(it){var dt=t-it.t;if(dt<0||dt>3.5)return;var x=400,y;if(dt<2){y=-20+dt*140}else{y=260;var k=(dt-2)/1.5;x=400+(it.side==='L'?-1:1)*k*290;if(k>0.85)y=260+(k-0.85)*400}cx.fillStyle=it.col;rr(x-18,y-18,36,36,6)});
 overlay(t,'SORT-2')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8992)
