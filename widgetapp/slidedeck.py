#!/usr/bin/env python3
"""337-slide-deck-value: 2-minute recording of a presentation (about 24 slides, 3-8 s each); report the Q3 revenue
figure shown on the slide titled "Regional results". complete = exact number."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base, clipapp
DUR = 120; TITLE = "Presentation recording"; HEADING = "Town hall recording (clip, 2:00)"; QUESTION = "On the slide titled \"Regional results\", what was the Q3 revenue figure (number only, in k)?"
S = {"slides": [], "answer": 0}
TITLES = ["Agenda", "Welcome", "Team updates", "Hiring plan", "Product roadmap", "Customer stories", "Support metrics", "Infrastructure", "Security review", "Marketing", "Regional results", "Budget outlook", "Q and A", "Partnerships", "Events", "Training", "Office move", "Wellbeing", "Open roles", "Next steps", "Thank you", "Regional overview", "Results summary", "Numbers"]


def reset():
    n = random.randint(20, 24); titles = random.sample(TITLES, n); t = 0.5; slides = []
    for ti in titles:
        d = random.uniform(3, 8); rows = [(r, random.randint(100, 999), random.randint(100, 999), random.randint(100, 999)) for r in ["North", "South", "East", "West"]]
        slides.append({"t": round(t, 1), "title": ti, "rows": rows}); t += d
    S["slides"] = slides; tgt = next(s for s in slides if s["title"] == "Regional results"); S["answer"] = sum(r[3] for r in tgt["rows"])


def data(): return {"slides": S["slides"]}
def answer(): return S["answer"]


SCENE_JS = r"""function scene(t){cx.fillStyle='#f8fafc';cx.fillRect(0,0,800,450);var s=D.slides[0];D.slides.forEach(function(x){if(t>=x.t)s=x});cx.fillStyle='#1e3a8a';cx.fillRect(0,0,800,70);cx.fillStyle='#fff';cx.font='bold 28px system-ui';cx.fillText(s.title,30,48);
 cx.fillStyle='#0f172a';cx.font='16px system-ui';['Region','Q1','Q2','Q3'].forEach(function(h,i){cx.fillText(h,80+i*160,130)});var tot=[0,0,0];s.rows.forEach(function(r,j){var y=175+j*40;cx.fillText(r[0],80,y);for(var i=1;i<4;i++){cx.fillText(r[i]+'k',80+i*160,y);tot[i-1]+=r[i]}});cx.font='bold 16px system-ui';cx.fillText('Total',80,345);for(var i=0;i<3;i++)cx.fillText(tot[i]+'k',240+i*160,345);
 cx.fillStyle='#94a3b8';cx.font='12px system-ui';cx.fillText('slide '+(D.slides.indexOf(s)+1)+' / '+D.slides.length,700,430);
 overlay(t,'TOWNHALL')}"""
clipapp.make(sys.modules[__name__])
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8971)
