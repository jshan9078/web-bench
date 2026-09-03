#!/usr/bin/env python3
"""Shared server for the vision/interaction widget tasks (58-61).

Same contract as pixelapp/server.py: the challenge is rendered server-side (nothing useful in the DOM),
the page reports raw clicks / form posts back, and the harness reads objective completion from
GET /__state after the run. POST /__reset re-randomizes for a fresh run.

An app module provides: reset(), render() -> PNG bytes (or None), page() -> HTML, click(x, y) -> dict,
state() -> dict (must include "complete": bool), and optionally post(path, data) -> dict.
Run: python3 <app>.py [port]
"""
import io, json, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import ImageFont


def font(size, bold=True):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def png(img):
    buf = io.BytesIO(); img.save(buf, "PNG"); return buf.getvalue()


# Standard page: the scene image at the top-left origin, clicks POSTed in IMAGE coordinates (the
# client subtracts the image's bounding rect, so page scrolling is transparent to the server).
def image_page(title, w, h, extra_html=""):
    return """<!doctype html><meta charset=utf-8><title>%s</title>
<style>html,body{margin:0;padding:0;background:#fff}#s{display:block;position:absolute;left:0;top:0}</style>
<img id=s src="/__scene.png" width="%d" height="%d">%s
<script>
document.getElementById('s').addEventListener('click',function(e){
  var r=this.getBoundingClientRect();
  fetch('/__click',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({x:Math.round(e.clientX-r.left),y:Math.round(e.clientY-r.top)})});
});
</script>""" % (title, w, h, extra_html)


def _token():
    """Harness-only secret gating /__state and /__reset. Created by the harness (ensure_app) and read
    here at startup, so the agent's browser never sees it; without it those endpoints answer 403."""
    import os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".token")
    try:
        return open(p).read().strip()
    except Exception:
        return None


def serve(app, default_port):
    TOKEN = _token()

    class Handler(BaseHTTPRequestHandler):
        def _authed(self):
            return TOKEN is not None and self.headers.get("X-Bench-Token", "") == TOKEN

        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype):
            if isinstance(body, str):
                body = body.encode()
            self.send_response(code); self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/":
                self._send(200, app.page(), "text/html; charset=utf-8")
            elif path == "/__scene.png":
                self._send(200, app.render(), "image/png")
            elif path == "/__state":
                if not self._authed():
                    return self._send(403, b"forbidden", "text/plain")
                self._send(200, json.dumps(app.state()), "application/json")
            elif hasattr(app, "get") and app.get(path) is not None:
                body, ctype = app.get(path)
                self._send(200, body, ctype)
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0)); raw = self.rfile.read(n) if n else b"{}"
            try:
                data = json.loads(raw or b"{}")
            except Exception:
                data = {"_raw": raw.decode(errors="ignore")}
            path = self.path.split("?")[0]
            if path == "/__reset":
                if not self._authed():
                    return self._send(403, b"forbidden", "text/plain")
                app.reset(); self._send(200, json.dumps({"ok": True}), "application/json")
            elif path == "/__click":
                try:
                    x, y = float(data["x"]), float(data["y"])
                except Exception:
                    return self._send(400, b"bad", "text/plain")
                self._send(200, json.dumps(app.click(x, y)), "application/json")
            elif hasattr(app, "post"):
                r = app.post(path, data, self.headers.get("Content-Type", ""))
                if r is None:
                    return self._send(404, b"not found", "text/plain")
                body, ctype = r
                self._send(200, body, ctype)
            else:
                self._send(404, b"not found", "text/plain")

    port = int(sys.argv[1]) if len(sys.argv) > 1 else default_port
    app.reset()
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
