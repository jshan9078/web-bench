#!/usr/bin/env python3
"""Shared server for the vision/interaction widget tasks (58-61).

Same contract as pixelapp/server.py: the challenge is rendered server-side (nothing useful in the DOM),
the page reports raw clicks / form posts back, and the harness reads objective completion from
GET /__state after the run. POST /__reset re-randomizes for a fresh run.

An app module provides: reset(), render() -> PNG bytes (or None), page() -> HTML, click(x, y) -> dict,
state() -> dict (must include "complete": bool), and optionally post(path, data) -> dict.
Run: python3 <app>.py [port]

Private-endpoint gate (2026-09-03): every /__* endpoint except the rendered scene (/__scene.png, /__frame),
the handshake (/__hello) and the harness-token endpoints (/__state, /__reset) requires an X-K header holding
a per-page-load key. serve() rewrites each HTML response: all inline <script> blocks are merged into one
closure that carries a single-use token, exchanges it for the key at load (POST /__hello), and routes the
page's own fetch('/__...') calls through api(), which adds the header. Nothing eval-able holds the key
(closure only), the token in the page source is already consumed by the time anything can read it, and a
direct fetch/navigate/curl to a private endpoint gets 403. The harness's endpoint-bypass guard remains as
the audit backstop for deliberate multi-step circumvention.
"""
import io, json, re, secrets, sys, time
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


HELPER_JS = """var __T='%T%',__K=null,__KP=null;
function __key(){if(__K)return Promise.resolve(__K);if(!__KP)__KP=fetch('/__hello',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({t:__T})}).then(function(r){return r.json()}).then(function(j){__K=j.k;return __K});return __KP}
function api(u,o){o=o||{};return __key().then(function(k){var h=Object.assign({},o.headers||{});h['X-K']=k;o.headers=h;return fetch(u,o)})}
__key();
"""
_SCRIPT_RE = re.compile(r"<script(?:\s[^>]*)?>(.*?)</script>", re.S)
OPEN_PATHS = ("/__scene.png", "/__frame", "/__hello", "/__state", "/__reset")


def inject(html, token):
    """Merge the page's inline scripts into one closure that owns the key and calls private endpoints via api()."""
    blocks = [m.group(1) for m in _SCRIPT_RE.finditer(html)]
    body = _SCRIPT_RE.sub("", html)
    js = "\n".join(blocks).replace("fetch('/__", "api('/__").replace('fetch("/__', 'api("/__').replace("fetch(p,", "api(p,")
    return body + "<script>(function(){" + HELPER_JS.replace("%T%", token) + js + "\n})();</script>"


def serve(app, default_port):
    TOKEN = _token()
    import inspect
    GET_ARGS = len(inspect.signature(app.get).parameters) if hasattr(app, "get") else 0   # get(path) or get(path, path_with_query)
    PEND = {}       # single-use page tokens -> expiry
    KEYS = set()    # keys issued to loaded pages (cleared on reset)

    def fresh_html(html):
        t = secrets.token_hex(16); PEND[t] = time.time() + 120
        return inject(html, t)

    class Handler(BaseHTTPRequestHandler):
        def _authed(self):
            return TOKEN is not None and self.headers.get("X-Bench-Token", "") == TOKEN

        def _keyed(self, path):
            """Private endpoints need the page key; the rendered scene, the handshake and harness endpoints do not."""
            if not path.startswith("/__") or path in OPEN_PATHS:
                return True
            return self.headers.get("X-K", "") in KEYS

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
                self._send(200, fresh_html(app.page()), "text/html; charset=utf-8")
            elif path == "/__scene.png":
                self._send(200, app.render(), "image/png")
            elif path == "/__state":
                if not self._authed():
                    return self._send(403, b"forbidden", "text/plain")
                self._send(200, json.dumps(app.state()), "application/json")
            elif not self._keyed(path):
                self._send(403, b"forbidden: private endpoint", "text/plain")
            elif hasattr(app, "get") and (r := (app.get(path, self.path) if GET_ARGS >= 2 else app.get(path))) is not None:
                body, ctype = r
                if ctype.startswith("text/html") and isinstance(body, str):
                    body = fresh_html(body)      # e.g. an iframe document: it gets its own token and key
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
                KEYS.clear(); PEND.clear()
                app.reset(); self._send(200, json.dumps({"ok": True}), "application/json")
            elif path == "/__hello":
                t = str(data.get("t", "")); now = time.time()
                for k in [k for k, exp in PEND.items() if exp < now]: del PEND[k]
                if t not in PEND:
                    return self._send(403, b"forbidden: token unknown or already used", "text/plain")
                del PEND[t]; k = secrets.token_hex(16); KEYS.add(k)
                self._send(200, json.dumps({"k": k}), "application/json")
            elif not self._keyed(path):
                self._send(403, b"forbidden: private endpoint", "text/plain")
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
