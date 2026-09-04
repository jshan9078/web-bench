#!/usr/bin/env python3
"""316-clock-at-event: a 45 s timelapse clip (clock runs 20x) of a wall clock and a status lamp; the lamp turns
GREEN once. Report the clock time shown at that moment, HH:MM within 1 minute."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 45; TITLE = "Office timelapse"; HEADING = "Office camera (timelapse, 0:45)"; QUESTION = "What time did the wall clock show when the lamp turned GREEN? (HH:MM)"
S = {"h": 0, "m": 0, "t_on": 0.0}


def reset(): S["h"] = random.randint(1, 12); S["m"] = random.randint(0, 44); S["t_on"] = round(random.uniform(8, 40), 1)


def data(): return {"h": S["h"], "m": S["m"], "t_on": S["t_on"]}


def answer_minutes():
    total = (S["h"] % 12) * 60 + S["m"] + S["t_on"] * 20 / 60; return total


def answer(): return int(round(answer_minutes())) % 720


SCENE_JS = r"""function scene(t){cx.fillStyle='#e7e5e4';cx.fillRect(0,0,800,450);var cxc=400,cyc=210,r=150,mins=(D.h%12)*60+D.m+t*20/60;cx.fillStyle='#fff';cx.beginPath();cx.arc(cxc,cyc,r,0,6.28);cx.fill();cx.strokeStyle='#1c1917';cx.lineWidth=6;cx.stroke();
 for(var k=0;k<60;k++){var a=k*Math.PI/30,L=k%5?6:14;cx.beginPath();cx.moveTo(cxc+(r-12)*Math.sin(a),cyc-(r-12)*Math.cos(a));cx.lineTo(cxc+(r-12-L)*Math.sin(a),cyc-(r-12-L)*Math.cos(a));cx.lineWidth=k%5?1:3;cx.stroke()}
 var ha=(mins/60)*Math.PI/6,ma=(mins%60)*Math.PI/30;cx.lineWidth=8;cx.beginPath();cx.moveTo(cxc,cyc);cx.lineTo(cxc+75*Math.sin(ha),cyc-75*Math.cos(ha));cx.stroke();cx.lineWidth=4;cx.beginPath();cx.moveTo(cxc,cyc);cx.lineTo(cxc+120*Math.sin(ma),cyc-120*Math.cos(ma));cx.stroke();
 var on=t>=D.t_on;cx.fillStyle=on?'#22c55e':'#7f1d1d';cx.beginPath();cx.arc(700,380,28,0,6.28);cx.fill();cx.fillStyle='#1c1917';cx.font='13px system-ui';cx.fillText('STATUS',676,425);
 overlay(t,'OFFICE-2')}"""
clipapp.make(sys.modules[__name__])
_inner_state = state


def state():
    st = _inner_state(); subs = st["submissions"]; ok = False
    if subs:
        try:
            hh, mm = subs[-1].strip().lower().replace("am", "").replace("pm", "").split(":"); got = (int(hh) % 12) * 60 + int(mm); want = answer_minutes() % 720
            diff = abs(got - want); ok = min(diff, 720 - diff) <= 1.0
        except Exception: ok = False
    st["answer"] = "%d:%02d" % (int(answer_minutes() // 60) % 12 or 12, int(answer_minutes() % 60)); st["complete"] = ok; return st


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8954)
