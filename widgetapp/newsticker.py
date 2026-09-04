#!/usr/bin/env python3
"""332-ticker-mentions: 2-minute news-channel clip with a scrolling ticker; count the headlines that mention the
word HARBOR. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "News clip"; HEADING = "News channel (clip, 2:00)"; QUESTION = "How many ticker headlines mentioned HARBOR (exact)?"
S = {"items": []}
BASE = ["Council approves new bridge budget", "Rain expected through Thursday", "Local team wins regional final", "Ferry timetable changes from Monday", "Museum extends late opening hours", "Road works on Elm Street continue", "School fair raises record sum", "Library launches evening classes", "Market moves to the square", "Tram line reopens after repairs"]
H = ["HARBOR cleanup volunteers wanted", "New cranes arrive at HARBOR terminal", "HARBOR festival dates announced", "HARBOR bridge closed overnight", "Fishing boats return to HARBOR", "HARBOR office hours change", "Storm damages HARBOR pier"]


def reset():
    n = random.randint(20, 26); k = random.randint(5, 9); items = random.sample(BASE * 3, n - k) + random.sample(H * 2, k); random.shuffle(items); S["items"] = items


def data(): return {"items": S["items"]}
def answer(): return sum(1 for i in S["items"] if "HARBOR" in i)


SCENE_JS = r"""function scene(t){cx.fillStyle='#0c4a6e';cx.fillRect(0,0,800,450);cx.fillStyle='#075985';cx.fillRect(40,40,720,300);cx.fillStyle='#e0f2fe';cx.font='bold 26px system-ui';cx.fillText('CHANNEL 9  LIVE',60,90);cx.fillStyle='#bae6fd';cx.font='16px system-ui';cx.fillText('Studio '+(Math.floor(t/30)%2?'B':'A'),60,130);
 cx.fillStyle='#dc2626';cx.fillRect(0,380,800,50);cx.save();cx.beginPath();cx.rect(0,380,800,50);cx.clip();cx.fillStyle='#fff';cx.font='bold 22px system-ui';var speed=180,total=0,ws=D.items.map(function(s){var w=cx.measureText(s).width+90;total+=w;return w});var off=(t*speed)%total,x=800-off;
 for(var pass=0;pass<2;pass++){D.items.forEach(function(s,i){if(x>-ws[i]&&x<800)cx.fillText(s,x,414);x+=ws[i]})}cx.restore();
 overlay(t,'CH9')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8966)
