# pixel_click task — wiring to apply AFTER the current sweep finishes

Everything here is staged so it doesn't disturb the running sweep. Apply once the sweep is done.

## Prereqs (built, not yet deployed)
- **Coord-click feature** is in the Rust source and compiled: `target/release/browser`
  (`click --at X,Y` → raw viewport-pixel click via `Input.dispatchMouseEvent`). The INSTALLED
  `~/.local/bin/browser` (0.7.2) does NOT have it, so the pixel task must run against the new binary.
- **App**: `benchmarks/webbench/pixelapp/server.py` (server-rendered scene; validated).

## Run the sweep against the coord-click binary
Point the harness at the freshly built binary (its daemon has coord-click). Do this for the whole run
(other tasks are unaffected):

```bash
cd /Users/jonathan/Desktop/browser-cli/benchmarks/webbench
export BROWSER_CLI="$PWD/../../target/release/browser"
export BROWSER_DAEMON="$PWD/../../target/release/browser daemon"
# (stop the old daemon first so the new binary's daemon is the one serving:)
~/.local/bin/browser shutdown 2>/dev/null; pkill -f "browser daemon" 2>/dev/null; sleep 1
```
(Or `uv tool install` the new wheel to make it the default `browser`.)

## harness.py additions

1) Task (add to TASKS):
```python
    "pixel_click": {"kind": "pixelstate", "app": True, "prompt": (
        "Open http://127.0.0.1:8791/ . It shows several numbered colored circles drawn as an image — "
        "they are NOT in the DOM, so `snapshot`/`text`/`eval` will not reveal them. Take a `screenshot` "
        "to SEE the circles and their numbers, then CLICK them in ascending numeric order (1, then 2, …) "
        "using raw pixel coordinates: `browser <sid> click --at X,Y` (the screenshot's pixels map 1:1 to "
        "click coordinates; the image is at the top-left origin). Take another screenshot if you need to "
        "confirm. Finish once you've clicked every circle in ascending order. Do NOT read the page source "
        "or call the site's HTTP API — interact visually.")},
```

2) Constants + app ensure (near ensure_daemon):
```python
PIXEL_PORT = 8791
def ensure_pixelapp():
    import urllib.request
    try: urllib.request.urlopen(f"http://127.0.0.1:{PIXEL_PORT}/__state", timeout=1)
    except Exception:
        subprocess.Popen([sys.executable, str(HERE/"pixelapp/server.py"), str(PIXEL_PORT)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.6)
    urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{PIXEL_PORT}/__reset", data=b"{}", method="POST")).read()
```
Call `ensure_pixelapp()` inside `setup()` when `TASKS[task].get("app")` (before creating the session).

3) record(): capture the app state as evidence (like cart_evidence):
```python
    pixel_state = None
    if TASKS[task].get("app"):
        import urllib.request
        try: pixel_state = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PIXEL_PORT}/__state", timeout=2))
        except Exception: pixel_state = None
```
add `"pixel_state": pixel_state,` to the bundle.

4) _judge(): add branch
```python
    if kind == "pixelstate":
        ps = bundle.get("pixel_state") or {}
        return bool(ps.get("complete"))
```
(state-based, objective — pixel accuracy verified server-side. This is the one non-LLM-judged task,
by design, because we control the app and want exact pixel-hit verification.)

5) judge_manifest / dashboard: pixel_click is programmatic (not needs_judge), so it shows PASS/FAIL
directly — no manual judging needed.

## Add to the matrix
`run_matrix.sh` iterates `harness.py tasks`, so `pixel_click` is picked up automatically once added.

## Docs to update (after sweep)
- `SKILL.md`: document `click --at X,Y` (raw pixel click for canvas/vision).
- README Tasks table + exact-prompts: add `pixel_click`.
- Consider shipping coord-click in the next release (bump versions, rebuild wheels).

## Functional test (after deploying the new binary)
```bash
cd benchmarks/webbench && export BROWSER_CLI=... BROWSER_DAEMON=...   # new binary
./run_one_pixel_smoke.sh   # or: setup pixel_click, screenshot, click --at each circle, check /__state.complete
```
