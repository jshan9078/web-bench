#!/usr/bin/env python3
"""344-graph-degree: an image of a network diagram with 22 labelled nodes and ~30 edges; count the nodes with
exactly 3 edges. complete = exact."""
import random, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import base, perception
TITLE = "Network"; W, H = 960, 640; QUESTION = "How many nodes have exactly 3 edges (exact)?"
S = {"nodes": [], "edges": []}


def reset():
    nodes = []
    while len(nodes) < 22:
        x, y = random.randint(50, W - 50), random.randint(50, H - 50)
        if all((x - n[0]) ** 2 + (y - n[1]) ** 2 > 90 ** 2 for n in nodes): nodes.append((x, y))
    edges = set()
    while len(edges) < 30:
        a, b = random.sample(range(22), 2); edges.add((min(a, b), max(a, b)))
    S["nodes"] = nodes; S["edges"] = sorted(edges)


def deg3(): return sum(1 for i in range(22) if sum(1 for a, b in S["edges"] if i in (a, b)) == 3)


def draw():
    img = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    for a, b in S["edges"]: d.line([S["nodes"][a], S["nodes"][b]], fill=(90, 90, 90), width=2)
    for i, (x, y) in enumerate(S["nodes"]): d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(255, 255, 255), outline=(20, 20, 20), width=2); d.text((x - 7 if i >= 10 else x - 4, y - 8), str(i), fill=(20, 20, 20), font=base.font(13))
    return img


def check(s):
    try: return int(perception.num(s)) == deg3()
    except Exception: return False


def answer_state(): return {"degree3": deg3(), "degrees": [sum(1 for a, b in S["edges"] if i in (a, b)) for i in range(22)]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8978)
