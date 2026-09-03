#!/usr/bin/env python3
"""91-video-slide-read: a recorded presentation played in a YouTube-style player (canvas video, autoplay,
play/pause, seek bar, skip buttons, speed, keyboard shortcuts) with a clickable timestamped TRANSCRIPT panel.
The slides are server-rendered frame images drawn onto the canvas, so nothing on a slide exists in the DOM.
Task: report the Invoice total on the slide that is on screen when the presenter FIRST says the word
"refund". The transcript locates the moment; the agent must seek there and read the frame. Traps: a later
"Refund summary" slide (the obvious guess) and a "Draft invoice forecast" slide with another invoice total.
complete = a submitted total matches the final-invoice figure."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base

LEVEL = int(os.environ.get("WIDGET_LEVEL", "1"))
DUR = 150
# Level 2: slide 4 shows FOUR dollar figures; the presenter's red pointer dot rests on each for six seconds
# and the target sentence ("This is the number that goes into the board pack") is said while it rests on
# one of them. The transcript locates the moment; only the frame at that moment says which figure.
FIG_POS = [(120, 170), (520, 170), (120, 330), (520, 330)]
FIG_LABELS = ["Invoice total", "Collected", "Outstanding", "Write-offs"]
S = {"slides": [], "schedule": [], "transcript": [], "answer": None, "submissions": [], "t1": 0, "pointer": [], "figs": [], "tb": 0}


def money(v): return "${:,}".format(v)


def reset():
    S["submissions"] = []
    a = random.randint(12000, 98999)
    b = a
    while abs(b - a) < 2000: b = random.randint(12000, 98999)
    c = random.randint(1200, 9999)
    S["slides"] = [
        ("Q3 Business Review", ["Northwind Traders", "Finance and Operations", "Recorded session"], None),
        ("Agenda", ["1. Shipping performance", "2. Invoicing", "3. Returns", "4. Draft numbers for Q4"], None),
        ("Shipping performance", [f"On-time deliveries: {random.randint(88, 97)}%", f"Late shipments: {random.randint(40, 120)}", f"Carrier claims open: {random.randint(3, 15)}"], None),
        ("Invoice summary (final)", [f"Invoices issued: {random.randint(300, 900)}", "Invoice total", money(a), "Books closed 30 Sep"], a),
        ("Refund summary", [f"Refund requests: {random.randint(20, 80)}", "Refund total", money(c), f"Approval rate {random.randint(70, 95)}%"], c),
        ("Draft invoice forecast (Q4)", [f"Projected invoices: {random.randint(300, 900)}", "Invoice total (draft)", money(b), "Not yet closed"], b),
        ("Questions", ["Thank you", "Notes will be shared after the call"], None),
    ]
    S["schedule"] = [(0, 14), (14, 30), (30, 58), (58, 86), (86, 108), (108, 134), (134, DUR)]
    t1 = random.randint(63, 73); S["t1"] = t1
    tr = [(1, "Hi everyone, thanks for joining the third quarter review."), (5, "This is the recorded session, so feel free to skip around."),
          (9, "Let's start with the agenda."), (15, "Four items today: shipping, invoicing, returns, and the draft numbers."),
          (21, "We will keep the questions for the end."), (26, "Okay, shipping first."),
          (31, "On-time delivery held up well despite the carrier change in August."), (37, "Late shipments are down from the previous quarter."),
          (43, "The open carrier claims are mostly weather related."), (50, "Nothing else to flag on logistics, so let's move on to invoicing."),
          (59, "Here is the invoice summary for the quarter, and these are the final numbers."),
          (t1, "One refund was reversed after this total was closed, so the figure here already includes it."),
          (t1 + 5, "This is the number that goes into the board pack."), (80, "Now the returns side of the house."),
          (87, "Refund requests were a little higher than Q2."), (92, "The refund total is shown here, and the approval rate is steady."),
          (99, "We reject refunds only when the item is outside the return window."), (109, "Next, the draft forecast for Q4."),
          (114, "These are projections, the invoice total here is a draft and will move."), (121, "Do not quote the draft figure externally."),
          (128, "Refund assumptions in the draft are unchanged."), (135, "That is everything, thank you."), (141, "Notes and the deck go out after the call.")]
    tr.sort(); S["transcript"] = tr
    S["answer"] = a; S["pointer"] = []; S["figs"] = []
    if LEVEL >= 2:
        while True:
            figs = [random.randint(12000, 98999), random.randint(8000, 79999), random.randint(2000, 29999), random.randint(500, 9999)]
            if all(abs(x - y) >= 1500 for i, x in enumerate(figs) for y in figs[i + 1:]): break
        S["figs"] = figs; S["slides"][3] = ("Q3 figures", [], None)
        order = [0, 1, 2, 3]; random.shuffle(order); k = random.randrange(4)
        S["pointer"] = [[62 + 6 * i, 68 + 6 * i, FIG_POS[f][0] - 26, FIG_POS[f][1] + 78] for i, f in enumerate(order)]
        S["tb"] = 62 + 6 * k + 1; S["answer"] = figs[order[k]]
        say = ["This one is up on last quarter.", "This one we expect to close out in October.", "This one is flat.", "This is the number that goes into the board pack."]
        random.shuffle(say[:3]); lines = [x for x in say if not x.startswith("This is the number")]
        tr = [l for l in tr if not (58 <= l[0] < 86)]
        tr += [(59, "Here are the four figures for the quarter; I will walk through them with the pointer.")]
        for i in range(4): tr.append((62 + 6 * i + 1, say[3] if i == k else lines.pop(0)))
        tr.sort(); S["transcript"] = tr


def frame(i):
    title, lines, key = S["slides"][i]
    W, H = 960, 540; img = Image.new("RGB", (W, H), (250, 250, 252)); dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, W, 96], fill=(30, 41, 59)); dr.text((48, 26), title, fill=(255, 255, 255), font=base.font(36))
    if LEVEL >= 2 and i == 3:
        for (x, y0), lab, v in zip(FIG_POS, FIG_LABELS, S["figs"]):
            dr.text((x, y0), lab, fill=(90, 90, 100), font=base.font(24, False)); dr.text((x, y0 + 40), money(v), fill=(37, 99, 235), font=base.font(48))
        dr.text((W - 120, H - 40), f"{i + 1} / {len(S['slides'])}", fill=(140, 140, 150), font=base.font(18, False))
        return base.png(img)
    y = 150
    for ln in lines:
        big = ln.startswith("$")
        dr.text((72, y), ln, fill=(37, 99, 235) if big else (40, 40, 50), font=base.font(52 if big else 30, big))
        y += 78 if big else 52
    dr.text((W - 120, H - 40), f"{i + 1} / {len(S['slides'])}", fill=(140, 140, 150), font=base.font(18, False))
    dr.rectangle([48, H - 60, 96, H - 56], fill=(37, 99, 235))
    return base.png(img)


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data":
        return (json.dumps({"dur": DUR, "schedule": S["schedule"], "transcript": S["transcript"], "pointer": S["pointer"]}), "application/json")
    if path.startswith("/__slide/"):
        try: i = int(path.split("/")[2].split(".")[0])
        except ValueError: return None
        if 0 <= i < len(S["slides"]): return (frame(i), "image/png")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append(str(data.get("total") or "").strip()); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    digits = lambda s: "".join(ch for ch in s if ch.isdigit())
    ok = any(digits(s) == str(S["answer"]) for s in S["submissions"])
    return {"level": LEVEL, "answer": S["answer"], "first_refund_t": S["t1"], "board_pack_t": S["tb"], "figs": S["figs"], "pointer": S["pointer"], "slide_at_t1": 3, "decoys": {"draft": S["slides"][5][2], "refund": S["slides"][4][2]},
            "submissions": S["submissions"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Q3 Business Review (recording)</title>
<style>body{font:14px system-ui;margin:0;background:#0f0f0f;color:#f1f1f1}#wrap{display:flex;gap:18px;padding:16px}#player{width:960px}
canvas#v{display:block;background:#000;width:960px;height:540px}#bar{display:flex;align-items:center;gap:10px;padding:8px 4px;background:#181818}
button{font:inherit;background:#272727;color:#f1f1f1;border:0;border-radius:6px;padding:6px 12px;cursor:pointer}button:hover{background:#3a3a3a}
input[type=range]{flex:1}select{background:#272727;color:#f1f1f1;border:0;border-radius:6px;padding:5px}
#tp{width:300px;background:#181818;border-radius:8px;padding:10px;max-height:600px;overflow:auto}#tp h3{margin:4px 0 10px;font-size:15px}
.line{padding:6px 8px;border-radius:6px;cursor:pointer;display:flex;gap:10px}.line:hover{background:#272727}.line.cur{background:#3a3a3a}.ts{color:#3ea6ff;font-variant-numeric:tabular-nums;min-width:38px}
#ans{margin:14px 16px;padding:12px;background:#181818;border-radius:8px;width:960px}input[type=text]{font:inherit;padding:6px 8px;border-radius:6px;border:1px solid #444;background:#0f0f0f;color:#f1f1f1}
h1{font-size:18px;margin:0 16px}.meta{color:#aaa;font-size:12px;margin:2px 16px 0}</style>
<h1>Q3 Business Review, Northwind Traders (recording)</h1><div class=meta>Recorded 2 Oct. Slides are burned into the video; use the transcript to navigate.</div>
<div id=wrap><div id=player><canvas id=v width=960 height=540 aria-label="video"></canvas>
<div id=bar><button id=pp aria-label="Play/Pause">Pause</button><button id=b10 aria-label="Back 10 seconds">-10 s</button><button id=f10 aria-label="Forward 10 seconds">+10 s</button>
<span id=tm>0:00 / 2:30</span><input id=seek type=range min=0 max=150 step=0.1 value=0 aria-label="Seek"><select id=spd aria-label="Speed"><option value=1>1x</option><option value=1.5>1.5x</option><option value=2>2x</option></select></div></div>
<div id=tp><h3>Transcript</h3><div id=tl></div></div></div>
<div id=ans><label>__Q__ <input id=tot type=text size=14 placeholder="$0"></label> <button id=go>Submit</button> <span id=msg></span></div>
<script>
(function(){
var D=null,frames=[],base=0,t0=Date.now(),pos=0,playing=true,rate=1,cv=document.getElementById('v'),cx=cv.getContext('2d');
function fmt(s){s=Math.max(0,Math.floor(s));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function slideAt(t){for(var i=0;i<D.schedule.length;i++){if(t>=D.schedule[i][0]&&t<D.schedule[i][1])return i}return D.schedule.length-1}
function draw(){if(!D)return;var i=slideAt(pos),im=frames[i];cx.fillStyle='#000';cx.fillRect(0,0,960,540);if(im&&im.complete)cx.drawImage(im,0,0);
 var p=pos/D.dur;cx.fillStyle='rgba(255,255,255,.25)';cx.fillRect(0,534,960,6);cx.fillStyle='#f00';cx.fillRect(0,534,960*p,6);
 var a=pos*1.3,px=520+180*Math.cos(a),py=330+90*Math.sin(a*0.7);(D.pointer||[]).forEach(function(w){if(pos>=w[0]&&pos<w[1]){px=w[2]+2*Math.sin(pos*9);py=w[3]+2*Math.cos(pos*7)}});
 cx.beginPath();cx.arc(px,py,10,0,6.28);cx.fillStyle='#fff';cx.fill();cx.beginPath();cx.arc(px,py,7,0,6.28);cx.fillStyle='rgba(255,40,40,.95)';cx.fill();
 cx.fillStyle='rgba(0,0,0,.6)';cx.fillRect(840,8,112,26);cx.fillStyle='#fff';cx.font='15px monospace';cx.fillText(fmt(pos)+' / '+fmt(D.dur),848,27);
 document.getElementById('tm').textContent=fmt(pos)+' / '+fmt(D.dur);document.getElementById('seek').value=pos;
 var cur=null;document.querySelectorAll('.line').forEach(function(el){var t=+el.dataset.t;if(t<=pos)cur=el;el.classList.remove('cur')});if(cur)cur.classList.add('cur')}
function step(){if(playing){pos=base+rate*(Date.now()-t0)/1000;if(pos>=D.dur){pos=D.dur;base=pos;playing=false;document.getElementById('pp').textContent='Play'}}draw()}
function tick(){step();requestAnimationFrame(tick)}
function seek(t){pos=Math.max(0,Math.min(D.dur,t));base=pos;t0=Date.now();draw()}
fetch('/__data').then(r=>r.json()).then(function(j){D=j;for(var i=0;i<j.schedule.length;i++){(function(i){var im=new Image();frames.push(im);fetch('/__slide/'+i+'.png').then(function(r){return r.blob()}).then(function(b){im.src=URL.createObjectURL(b)})})(i)}
 var tl=document.getElementById('tl');j.transcript.forEach(function(l){var d=document.createElement('div');d.className='line';d.dataset.t=l[0];d.innerHTML='<span class=ts>'+fmt(l[0])+'</span><span>'+l[1]+'</span>';d.onclick=function(){seek(l[0])};tl.appendChild(d)});
 t0=Date.now();setInterval(step,100);requestAnimationFrame(tick)});
document.getElementById('pp').onclick=function(){base=pos;t0=Date.now();playing=!playing;this.textContent=playing?'Pause':'Play'};
document.getElementById('b10').onclick=function(){seek(pos-10)};document.getElementById('f10').onclick=function(){seek(pos+10)};
var sk=document.getElementById('seek');sk.oninput=sk.onchange=function(){seek(+this.value)};
document.getElementById('spd').onchange=function(){base=pos;t0=Date.now();rate=+this.value};
document.addEventListener('keydown',function(e){if(e.target.tagName==='INPUT'&&e.target.type==='text')return;if(e.key===' '){e.preventDefault();document.getElementById('pp').click()}if(e.key==='ArrowLeft')seek(pos-5);if(e.key==='ArrowRight')seek(pos+5);if(e.key==='j')seek(pos-10);if(e.key==='l')seek(pos+10);if(e.key==='k')document.getElementById('pp').click()});
document.getElementById('go').onclick=function(){fetch('/__answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({total:document.getElementById('tot').value})}).then(r=>r.json()).then(function(j){document.getElementById('msg').textContent='Submitted ('+j.n+').'})};
})();
</script>"""


def page(): return PAGE.replace("__Q__", "Figure the pointer is on at that moment:" if LEVEL >= 2 else "Invoice total shown on that slide:")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8811)
