#!/usr/bin/env python3
"""335-chat-stream: 2-minute clip of a live chat panel where messages scroll in quickly; count the messages from
user "mira" that contain a question mark. complete = exact."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Live chat clip"; HEADING = "Stream chat recording (clip, 2:00)"; QUESTION = "How many messages from mira contained a question mark (exact)?"
S = {"msgs": []}
USERS = ["mira", "jon_k", "pixel8", "mira", "devi", "tomas", "quill", "mira_b"]
Q = ["is the replay up?", "what map is next?", "anyone else lagging?", "did we win?", "when does it start?", "who is casting?"]
A = ["gg", "nice shot", "that was close", "brb", "lol", "great game", "hello everyone", "first time here", "so fast", "wow"]


def reset():
    msgs = []; t = 1.0
    while t < DUR - 2:
        u = random.choice(USERS); q = random.random() < 0.4; msgs.append({"t": round(t, 1), "u": u, "m": random.choice(Q if q else A)}); t += random.uniform(0.8, 2.5)
    S["msgs"] = msgs


def data(): return {"msgs": S["msgs"]}
def answer(): return sum(1 for m in S["msgs"] if m["u"] == "mira" and "?" in m["m"])


SCENE_JS = r"""function scene(t){cx.fillStyle='#18181b';cx.fillRect(0,0,800,450);cx.fillStyle='#3f3f46';cx.fillRect(0,0,520,450);cx.fillStyle='#a1a1aa';cx.font='14px system-ui';cx.fillText('GAME FEED',20,30);cx.fillStyle='#27272a';cx.fillRect(520,0,280,450);cx.fillStyle='#e4e4e7';cx.font='bold 14px system-ui';cx.fillText('CHAT',536,26);
 var vis=D.msgs.filter(function(m){return m.t<=t}).slice(-14);cx.font='13px system-ui';vis.forEach(function(m,i){var y=52+i*28;cx.fillStyle=m.u==='mira'?'#f472b6':'#93c5fd';cx.fillText(m.u+':',536,y);cx.fillStyle='#e4e4e7';cx.fillText(m.m,536+cx.measureText(m.u+': ').width,y)});
 overlay(t,'STREAM')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8969)
