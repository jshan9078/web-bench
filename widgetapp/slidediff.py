#!/usr/bin/env python3
"""96-slide-diff: the same YouTube-style recorded presentation as 91, but the question spans two moments.
A DRAFT budget table is shown early and a CORRECTED version late; exactly one line item's amount changed.
Traps: the corrected table lists the rows in a different order (positional comparison fails), one row's
LABEL is reworded with the amount unchanged, and the intervening slides carry other dollar figures.
complete = submitted item names the changed row and the amount equals its corrected value."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, videoplayer as vp

DUR = 150
ITEMS = ["Travel", "Software", "Contractors", "Marketing", "Training"]
RENAME = {"Software": "Software licences", "Travel": "Travel and lodging", "Training": "Staff training", "Marketing": "Marketing spend", "Contractors": "External contractors"}
S = {"draft": [], "final": [], "order": [], "changed": None, "renamed": None, "transcript": [], "submissions": []}
SCHEDULE = [(0, 12), (12, 26), (26, 52), (52, 80), (80, 104), (104, 134), (134, DUR)]


def money(v): return "${:,}".format(v)


def reset():
    S["submissions"] = []
    while True:
        draft = [random.randint(8000, 96000) for _ in ITEMS]
        if all(abs(a - b) >= 2500 for i, a in enumerate(draft) for b in draft[i + 1:]): break
    ci = random.randrange(5); ri = random.choice([i for i in range(5) if i != ci])
    final = draft[:]
    while True:
        nv = random.randint(8000, 96000)
        if abs(nv - draft[ci]) >= max(2500, int(0.15 * draft[ci])) and all(abs(nv - v) >= 2500 for i, v in enumerate(final) if i != ci): break
    final[ci] = nv
    order = list(range(5))
    while order == list(range(5)): random.shuffle(order)
    S.update(draft=draft, final=final, order=order, changed={"item": ITEMS[ci], "draft": draft[ci], "final": nv}, renamed=ITEMS[ri])
    S["transcript"] = sorted([(1, "Hi everyone, thanks for joining the third quarter review."), (5, "This is the recorded session, so feel free to skip around."),
        (13, "Agenda: the draft budget, shipping, refunds, then the corrected budget."), (20, "Questions at the end."),
        (27, "Here is the draft budget we circulated in August."), (33, "Treat these as placeholders; one of them was still being negotiated."),
        (44, "We will come back to this table at the end."), (53, "Shipping next."), (60, "On-time delivery held up despite the carrier change."),
        (72, "Carrier claims are mostly weather related."), (81, "Refund requests were a little higher than Q2."), (90, "The refund total is shown here."),
        (105, "And here is the corrected budget."), (111, "One line item changed after the negotiation closed; the rest is as drafted."),
        (120, "We also tidied a couple of the labels, which does not change any amounts."), (128, "This is the version that goes into the board pack."),
        (135, "That is everything, thank you."), (141, "Notes and the deck go out after the call.")])


def _table(dr, rows, y0=150):
    for i, (lab, v) in enumerate(rows):
        y = y0 + i * 62; dr.text((96, y), lab, fill=(40, 40, 50), font=base.font(30, False)); dr.text((600, y - 6), money(v), fill=(37, 99, 235), font=base.font(40))
        dr.line([(96, y + 48), (864, y + 48)], fill=(220, 220, 228), width=1)


def frame(i):
    W, H = 960, 540; img = Image.new("RGB", (W, H), (250, 250, 252)); dr = ImageDraw.Draw(img)
    titles = ["Q3 Business Review", "Agenda", "Draft budget (August)", "Shipping performance", "Refund summary", "Corrected budget (final)", "Questions"]
    dr.rectangle([0, 0, W, 96], fill=(30, 41, 59)); dr.text((48, 26), titles[i], fill=(255, 255, 255), font=base.font(36))
    if i == 2: _table(dr, list(zip(ITEMS, S["draft"])))
    elif i == 5:
        rows = [((RENAME[ITEMS[k]] if ITEMS[k] == S["renamed"] else ITEMS[k]), S["final"][k]) for k in S["order"]]; _table(dr, rows)
    else:
        body = {0: ["Northwind Traders", "Finance and Operations", "Recorded session"], 1: ["1. Draft budget", "2. Shipping performance", "3. Refunds", "4. Corrected budget"],
                3: [f"On-time deliveries: {random.Random(S['draft'][0]).randint(88, 97)}%", f"Late shipments: {random.Random(S['draft'][1]).randint(40, 120)}", f"Carrier claims open: {random.Random(S['draft'][2]).randint(3, 15)}"],
                4: [f"Refund requests: {random.Random(S['draft'][3]).randint(20, 80)}", "Refund total", money(random.Random(S['draft'][4]).randint(1200, 9999)), "Approval rate 86%"], 6: ["Thank you", "Notes will be shared after the call"]}[i]
        y = 150
        for ln in body:
            big = ln.startswith("$"); dr.text((72, y), ln, fill=(37, 99, 235) if big else (40, 40, 50), font=base.font(52 if big else 30, big)); y += 78 if big else 52
    dr.text((W - 120, H - 40), f"{i + 1} / 7", fill=(140, 140, 150), font=base.font(18, False))
    return base.png(img)


def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"dur": DUR, "schedule": SCHEDULE, "transcript": S["transcript"], "pointer": []}), "application/json")
    if path.startswith("/__slide/"):
        try: i = int(path.split("/")[2].split(".")[0])
        except ValueError: return None
        if 0 <= i < 7: return (frame(i), "image/png")
    return None


def post(path, data, ctype):
    if path == "/__answer":
        S["submissions"].append({"item": str(data.get("item") or "").strip(), "value": str(data.get("value") or "").strip()}); return (json.dumps({"n": len(S["submissions"])}), "application/json")
    return None


def state():
    c = S["changed"]; digits = lambda s: "".join(ch for ch in s if ch.isdigit())
    ok = any(c["item"].lower() in s["item"].lower() and digits(s["value"]) == str(c["final"]) for s in S["submissions"])
    return {"changed": c, "renamed": S["renamed"], "draft": dict(zip(ITEMS, S["draft"])), "final": dict(zip(ITEMS, S["final"])), "submissions": S["submissions"], "complete": ok}


def page():
    return vp.PAGE.replace("__Q__", 'Changed line item: <input id=item type=text size=16> &nbsp; corrected amount:').replace('<input id=tot type=text size=14 placeholder="$0">', '<input id=tot type=text size=14 placeholder="$0">') \
        .replace("body:JSON.stringify({total:document.getElementById('tot').value})", "body:JSON.stringify({item:document.getElementById('item').value,value:document.getElementById('tot').value})") \
        .replace("Q3 Business Review (recording)", "Q3 Budget Review (recording)").replace("Q3 Business Review, Northwind Traders (recording)", "Q3 Budget Review, Northwind Traders (recording)")


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8816)
