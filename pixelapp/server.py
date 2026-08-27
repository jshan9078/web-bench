#!/usr/bin/env python3
"""A deliberately vision-only web challenge for the pixel-click task.

The scene (numbered colored circles at RANDOM positions) is rendered SERVER-SIDE as a PNG — the client
page only shows that image and reports raw click (x,y) back. No target coordinates ever reach the
browser (not in the DOM, not in JS), so `snapshot`/`text`/`eval` reveal nothing: the ONLY way to know
where to click is to LOOK (screenshot), and the only way to click is raw pixels (`click --at X,Y`).

Endpoints:
  GET  /              -> HTML: <img src=/__scene.png> at (0,0) + JS that POSTs clicks to /__click
  GET  /__scene.png   -> the rendered scene (900x600)
  POST /__click {x,y} -> hit-test against stored circles; append to the click log
  POST /__reset       -> new random layout; clears clicks; RETURNS the layout (for the harness only)
  GET  /__state       -> {n_targets, clicks:[{x,y,hit}], hit_order:[nums], complete:bool}

`complete` is true when the distinct circles hit, in click order, are exactly 1..N ascending.
Run: python3 server.py [port]   (default 8791)
"""
import io, json, random, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image, ImageDraw, ImageFont

W, H, R, N = 900, 600, 42, 5
COLORS = [(219, 68, 55), (66, 133, 244), (15, 157, 88), (244, 180, 0), (171, 71, 188)]
STATE = {"targets": [], "clicks": []}


def _font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def new_layout():
    pts = []
    while len(pts) < N:
        x = random.randint(R + 20, W - R - 20)
        y = random.randint(R + 20, H - R - 20)
        if all((x - px) ** 2 + (y - py) ** 2 > (2.4 * R) ** 2 for px, py, _ in pts):
            pts.append((x, y, None))
    nums = list(range(1, N + 1)); random.shuffle(nums)
    STATE["targets"] = [{"n": nums[i], "x": pts[i][0], "y": pts[i][1], "r": R} for i in range(N)]
    STATE["clicks"] = []
    return STATE["targets"]


def render_png():
    img = Image.new("RGB", (W, H), (247, 248, 250))
    d = ImageDraw.Draw(img)
    d.text((16, 12), "Click the circles in ascending order (1..%d)" % N, fill=(90, 96, 105), font=_font(20))
    f = _font(34)
    for i, t in enumerate(STATE["targets"]):
        c = COLORS[(t["n"] - 1) % len(COLORS)]
        d.ellipse([t["x"] - R, t["y"] - R, t["x"] + R, t["y"] + R], fill=c)
        s = str(t["n"]); bb = d.textbbox((0, 0), s, font=f)
        d.text((t["x"] - (bb[2] - bb[0]) / 2, t["y"] - (bb[3] - bb[1]) / 2 - bb[1]), s, fill=(255, 255, 255), font=f)
    buf = io.BytesIO(); img.save(buf, "PNG"); return buf.getvalue()


def hit_order():
    order = []
    for c in STATE["clicks"]:
        if c["hit"] is not None and c["hit"] not in order:
            order.append(c["hit"])
    return order


PAGE = """<!doctype html><meta charset=utf-8><title>Pixel Challenge</title>
<style>html,body{margin:0;padding:0;background:#fff}#s{display:block;position:absolute;left:0;top:0}</style>
<img id=s src="/__scene.png" width="%d" height="%d">
<script>
document.getElementById('s').addEventListener('click',function(e){
  var r=this.getBoundingClientRect();
  fetch('/__click',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({x:Math.round(e.clientX-r.left),y:Math.round(e.clientY-r.top)})});
});
</script>""" % (W, H)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype):
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            if not STATE["targets"]:
                new_layout()
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        elif self.path == "/__scene.png":
            self._send(200, render_png(), "image/png")
        elif self.path == "/__state":
            ho = hit_order()
            body = json.dumps({"n_targets": N, "clicks": STATE["clicks"], "hit_order": ho,
                               "complete": ho == list(range(1, N + 1))}).encode()
            self._send(200, body, "application/json")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); raw = self.rfile.read(n) if n else b"{}"
        if self.path == "/__reset":
            targets = new_layout()
            self._send(200, json.dumps({"targets": targets}).encode(), "application/json")
        elif self.path == "/__click":
            try:
                d = json.loads(raw); x, y = float(d["x"]), float(d["y"])
            except Exception:
                return self._send(400, b"bad", "text/plain")
            hit = next((t["n"] for t in STATE["targets"] if (x - t["x"]) ** 2 + (y - t["y"]) ** 2 <= t["r"] ** 2), None)
            STATE["clicks"].append({"x": x, "y": y, "hit": hit})
            self._send(200, json.dumps({"hit": hit}).encode(), "application/json")
        else:
            self._send(404, b"not found", "text/plain")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8791
    new_layout()
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
