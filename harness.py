"""Real-site agent benchmark across models AND thinking levels AND CLIs.

Matrix: Claude {opus,sonnet,haiku} x effort {low,medium,high,xhigh,max} (via `claude -p --effort`)
plus Antigravity {gemini-3.7-flash-high, gemini-3.7-flash-medium} (via `agy -p`). Tasks hit real
external sites and have answers that do NOT drift with time.

CAPTURE-FIRST DESIGN: a run first writes a durable raw bundle (raw/<task>.<run>.json + the full model
stream) with EVERYTHING the model did — full agent trace, every browser command, end-state evidence,
CPU series, raw token usage. Scoring is a SEPARATE, re-runnable step (`score`) that derives metrics and
applies verifiers from those bundles. Change a verifier later -> just re-run `score`, never re-run models.

  harness.py tasks                                  -> list task names
  harness.py setup  <task>                          -> ensure daemon+session, print the agent prompt
  harness.py record <task> run=.. harness=.. model=.. effort=.. config=.. stream=<file> [cpu=<file>]
                                                    -> capture raw bundle (NO judging)
  harness.py score  [<task>.<run>]                  -> (re)apply verifiers + metrics -> results/<task>/<run>.json
  harness.py report                                 -> flat table (from results/)
  harness.py compare                                -> per-config medians + pass@k (the video's numbers)

Env: BROWSER_CLI/BROWSER_DAEMON select the impl. BENCH_VISIBLE=1 -> headed. BENCH_PROFILE=<name> ->
     override the persistent profile for signed-in tasks (default: the daemon's active profile). BENCH_HARNESS=agy -> emit an
     agy-flavored prompt (agy has no /browser-cli skill, so it reads SKILL.md instead).
"""
import json, os, shutil, statistics, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE  # repo root (standalone web-bench)
SKILL = ROOT / "SKILL.md"
RES = HERE / "results"; RES.mkdir(exist_ok=True)
RAW = HERE / "raw"; RAW.mkdir(exist_ok=True)
META = RES / "current.json"
CLI = os.environ.get("BROWSER_CLI", "").split() or ["browser"]
DAEMON = os.environ.get("BROWSER_DAEMON", "").split() or ["browser", "daemon"]
SOCK = Path.home() / ".browser-daemon" / "socket"
RLOG = Path.home() / ".browser-daemon" / "requests.log"
ENV = {**os.environ}

import procstats as bench  # per-process CPU/RSS helpers (descendants, cputimes)

AMAZON_ITEMS = [
    {"asin": "0735211299", "title": "atomic habits"},   # book: always in stock, no shipping limits
    {"asin": "0132350882", "title": "clean code"},      # book: always in stock, no shipping limits
]

X_HANDLE = "jshan9078"
X_PROJECTS = ["browser automation cli", "opencord", "ross", "microgradcpp",
              "on-device slm", "vulnerability detection", "distributed scraper"]
X_PROJECTS_MIN = 2

PREAMBLE = (
    "A browser session ALREADY EXISTS for you: its id is `{sid}`. Drive it with `browser {sid} <command>`. "
    "Do NOT create or delete sessions. The session is {mode}. Interact through the UI like a person — do not "
    "sign up, enter payment details, or place/confirm any order; decline cookie/consent banners (reject "
    "non-essential). IMPORTANT: answer ONLY from what you actually navigate to and read on the page RIGHT NOW "
    "— do not answer from prior knowledge; if you didn't see it on the page, go find it. When done, reply with "
    "a concise summary of what you found, and if asked for a value make the LAST line exactly `ANSWER: <value>`. "
    "If a CAPTCHA, robot check, or forced re-login wall stops you: first, if it looks like an automated "
    "browser check (e.g. 'Pardon Our Interruption', 'Checking your browser'), WAIT about ten seconds and "
    "retry once — these often clear on their own. If it persists or needs human input, do NOT try to "
    "bypass it and do NOT report it as a normal failure: run `browser {sid} show` to make the window "
    "visible so the user can solve it, say exactly what they need to do, and make the LAST line exactly "
    "`BLOCKED: <which site/wall stopped you>`. "
    "TIME BUDGET: you have 10 minutes of wall-clock time for this task. The run is terminated when the budget "
    "runs out, so work efficiently, avoid repeating actions, and give your final answer before then."
)

AMAZON = "www.amazon.ca"   # marketplace; book ASINs (ISBN-10) are the same across marketplaces
_dp = lambda i: f"https://{AMAZON}/dp/{i['asin']}"
# Every task tests NAVIGATION over real-world data (no puzzles/reasoning). Read tasks target CURRENT
# data that cannot be in any training set and are graded by LLM-as-judge from the captured evidence
# (raw bundle: agent answer + full stream + end_state). Action tasks keep a programmatic state check.
TASKS = {
    # read-only navigation over current real-world data, judged offline by an LLM from captured evidence
    "01-mlb-latest": {"kind": "judge"},
    "02-hn-summary": {"kind": "judge"},
    "03-weather-nyc": {"kind": "judge"},
    "04-x-projects": {"profile": True, "kind": "judge"},
    # cart actions, judged from a cart screenshot + the command trace
    "05-amazon-cart": {"profile": True, "kind": "judge", "cart": True},
    "06-amazon-search-add": {"profile": True, "kind": "judge", "cart": True},
    # vision + pixel-click, verified programmatically by the canvas server
    "07-pixel-click": {"kind": "pixelstate", "app": True},
    # ---- extended task set (08-57): live-data, vision/pixel, and signed-in tasks;
    # all LLM-judged offline from the captured evidence (see tasks/<name>/verifier.md)
    "08-airport-departures": {"kind": "judge"},
    "09-recipe-scaling": {"kind": "judge"},
    "10-arxiv-agents-paper": {"kind": "judge"},
    "11-github-trending-audit": {"kind": "judge"},
    "12-wikipedia-current-events": {"kind": "judge"},
    "13-usgs-quake-report": {"kind": "judge"},
    "14-imdb-yearly-top": {"kind": "judge"},
    "15-stock-analyst-targets": {"kind": "judge"},
    "17-currency-meal-budget": {"kind": "judge"},
    "18-npm-package-audit": {"kind": "judge"},
    "19-wiktionary-wotd": {"kind": "judge"},
    "20-nasa-apod-vision": {"kind": "judge"},
    "21-amazon-office-bundle": {"profile": True, "kind": "judge", "cart": True},
    "22-amazon-earbud-compare": {"profile": True, "kind": "judge", "cart": True},
    "26-ebay-keyboard-hunt": {"kind": "judge"},
    "27-amazon-review-mining": {"profile": True, "kind": "judge"},
    "29-excalidraw-pipeline": {"kind": "judge"},
    "32-desmos-intersections": {"kind": "judge"},
    "33-osm-street-read": {"kind": "judge"},
    "34-osm-route-measure": {"kind": "judge"},
    "36-jspaint-poster": {"kind": "judge"},
    "39-youtube-frame-describe": {"kind": "judge"},
    "40-arxiv-pdf-figure": {"kind": "judge"},
    "41-owid-dataset-read": {"kind": "judge"},
    "42-youtube-watch-later": {"profile": True, "kind": "judge"},
    "43-gmail-self-draft": {"profile": True, "kind": "judge"},
    "44-gcal-event": {"profile": True, "kind": "judge"},
    "47-reddit-save": {"profile": True, "kind": "judge"},
    "48-spotify-playlist": {"profile": True, "kind": "judge"},
    "49-x-bookmark": {"profile": True, "kind": "judge"},
    "50-google-flights-nonstop": {"kind": "judge"},
    "51-wikipedia-revision-audit": {"kind": "judge"},
    "53-caniuse-feature": {"kind": "judge"},
    "54-stackoverflow-live": {"kind": "judge"},
    "55-wayback-snapshot": {"kind": "judge"},
    "56-sunrise-reykjavik": {"kind": "judge"},
    "57-hn-debate-analysis": {"kind": "judge"},
    # ---- v2 task set (2026-09-03): designed to discriminate; see tasks/V2-DESIGN.md. Excluded from the
    # v1 sweeps/scoreboard until piloted (BENCH_SET=v2 selects them; see sweep_tasks()).
    "58-pixel-scan": {"kind": "appstate", "app": "widgetapp/pixelscan.py", "port": 8792, "v2": True, "level": 3},
    "59-spot-difference": {"kind": "appstate", "app": "widgetapp/spotdiff.py", "port": 8793, "v2": True, "level": 3},
    "60-form-wizard": {"kind": "appstate", "app": "widgetapp/wizard.py", "port": 8794, "v2": True, "saturated": True},
    "61-grid-toggle": {"kind": "appstate", "app": "widgetapp/gridtoggle.py", "port": 8795, "v2": True, "saturated": True},
    "63-wikipedia-edit-audit": {"kind": "judge", "v2": True, "saturated": True},
    "64-hn-comment-census": {"kind": "judge", "v2": True, "saturated": True},
    "65-arxiv-pdf-tables": {"kind": "judge", "v2": True, "saturated": True},
    "66-wiki-table-reconcile": {"kind": "judge", "v2": True, "saturated": True},
    "68-youtube-transcript": {"kind": "judge", "v2": True, "saturated": True},
    "69-timezone-meeting": {"kind": "judge", "v2": True, "saturated": True},
    "72-amazon-quantity-edit": {"profile": True, "kind": "judge", "cart": True, "v2": True, "saturated": True},
    "73-pdf-table-extract": {"kind": "judge", "v2": True, "saturated": True},
    # ---- v2.2 (2026-09-03): hard local test sites + real-map navigation (see tasks/V2-DESIGN.md)
    "74-dashboard-triage": {"kind": "appstate", "app": "widgetapp/dashboard.py", "port": 8796, "v2": True, "saturated": True},
    "75-map-explorer": {"kind": "appstate", "app": "widgetapp/mapexplorer.py", "port": 8797, "v2": True, "fill_from_state": True},
    "78-gmaps-directions": {"kind": "judge", "v2": True, "saturated": True, "keep": True},
    "79-gmaps-place-hours": {"kind": "judge", "v2": True, "keep": True},
    "76-settings-maze": {"kind": "appstate", "app": "widgetapp/settingsmaze.py", "port": 8798, "v2": True},
    "77-crosshair-align": {"kind": "appstate", "app": "widgetapp/crosshair.py", "port": 8799, "v2": True, "level": 2},
    "80-live-list": {"kind": "appstate", "app": "widgetapp/livelist.py", "port": 8800, "v2": True, "saturated": True},
    "81-memory-flow": {"kind": "appstate", "app": "widgetapp/memoryflow.py", "port": 8801, "v2": True, "saturated": True},
    "82-blur-validation": {"kind": "appstate", "app": "widgetapp/blurform.py", "port": 8802, "v2": True, "saturated": True},
    "83-reconcile-rule": {"kind": "appstate", "app": "widgetapp/reconcile.py", "port": 8803, "v2": True, "saturated": True, "fill_from_state": True},
    "84-ledger-audit": {"kind": "appstate", "app": "widgetapp/ledger.py", "port": 8804, "v2": True, "saturated": True},
    "85-table-diff": {"kind": "appstate", "app": "widgetapp/tablediff.py", "port": 8805, "v2": True, "saturated": True},
    "86-chart-read": {"kind": "appstate", "app": "widgetapp/chartread.py", "port": 8806, "v2": True, "saturated": True},
    "87-gcal-scheduling": {"profile": True, "kind": "judge", "v2": True},
    "88-cancel-flow": {"kind": "appstate", "app": "widgetapp/darkpatterns.py", "port": 8808, "v2": True, "saturated": True},    "89-gcal-last-free": {"profile": True, "kind": "judge", "v2": True},    "90-dial-set": {"kind": "appstate", "app": "widgetapp/dial.py", "port": 8810, "v2": True, "fill_from_state": True},
}
TASKS_V1 = [k for k, v in TASKS.items() if not v.get("v2")]
TASKS_V2 = [k for k, v in TASKS.items() if v.get("v2")]


def sweep_tasks():
    """Task names a sweep iterates: BENCH_SET=v1 (default) | v2 (discriminating v2 tasks only) | v2all | all.
    A v2 task flagged `saturated` (every pilot config passed it; see v2_saturation.py) is skipped by
    BENCH_SET=v2 unless it is also flagged `keep` (the Google Maps tasks, kept by decision)."""
    which = os.environ.get("BENCH_SET", "v1")
    if which == "v1": return TASKS_V1
    if which == "v2": return [k for k in TASKS_V2 if not (TASKS[k].get("saturated") and not TASKS[k].get("keep"))]
    if which == "v2all": return TASKS_V2
    return list(TASKS)
# Prompts live in tasks/<name>/prompt.txt (one subdirectory per task; see tasks/<name>/verifier.md for
# how each run is scored). This directory is the source of truth for task prompts.
_TDIR = HERE / "tasks"
for _name, _spec in TASKS.items():
    _spec["prompt"] = (_TDIR / _name / "prompt.txt").read_text().strip()

# The original seven tasks were renamed with 01-07 prefixes; old raw bundles and verdict keys still
# carry the unprefixed names, so canonicalize wherever a task name is read back.
LEGACY_NAMES = {
    "mlb_latest": "01-mlb-latest", "hn_summary": "02-hn-summary", "weather_nyc": "03-weather-nyc",
    "x_projects": "04-x-projects", "amazon_cart": "05-amazon-cart",
    "amazon_search_add": "06-amazon-search-add", "pixel_click": "07-pixel-click",
}
def canon(t):
    return LEGACY_NAMES.get(t, t)


def run_cli(*args, sid=None, timeout=60):
    a = [*CLI] + ([sid] if sid else []) + list(args)
    try:
        return subprocess.run(a, capture_output=True, text=True, env=ENV, timeout=timeout).stdout
    except Exception:
        return ""


def ensure_daemon():
    def alive():
        return subprocess.run(["pgrep", "-f", "daemon.server|browser-daemon|browser daemon"],
                              capture_output=True).returncode == 0
    if not SOCK.exists() or not alive():
        SOCK.unlink(missing_ok=True)
        subprocess.Popen(DAEMON, env=ENV, stdout=subprocess.DEVNULL, stderr=open(RES / "daemon.log", "a"))
        for _ in range(200):
            if SOCK.exists():
                break
            time.sleep(0.05)
        time.sleep(0.3)


def daemon_pid():
    out = subprocess.run(["pgrep", "-f", "daemon.server|browser-daemon|browser daemon"],
                         capture_output=True, text=True).stdout.split()
    return int(out[0]) if out else None


def tree_cpu(pid):
    if not pid:
        return {"cpu_s": 0.0, "rss_mb": 0.0, "pids": {}}
    pids = bench.descendants(pid); t = bench.cputimes(pids)
    return {"cpu_s": sum(v[0] for v in t.values()), "rss_mb": sum(v[1] for v in t.values()) / 1024,
            "pids": {str(k): v[0] for k, v in t.items()}}


CART_URL = f"https://{AMAZON}/gp/cart/view.html"
PIXEL_PORT = 8791


WIDGET_TOKEN_FILE = HERE / "widgetapp/.token"


def widget_token():
    """Harness-only secret for the widget servers' /__state and /__reset (created once, gitignored)."""
    if not WIDGET_TOKEN_FILE.exists():
        import secrets
        WIDGET_TOKEN_FILE.write_text(secrets.token_hex(16))
    return WIDGET_TOKEN_FILE.read_text().strip()


def _widget_req(port, path, data=None):
    import urllib.request
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", data=data, method="POST" if data is not None else "GET",
                                 headers={"X-Bench-Token": widget_token()})
    return urllib.request.urlopen(req, timeout=2).read()


def ensure_app(t):
    """Start the task's localhost widget server (pixelapp for `app: True`, else the given script) and
    reset it to a fresh random layout so every run starts clean."""
    port = t.get("port", PIXEL_PORT)
    script = HERE / "pixelapp/server.py" if t.get("app") is True else HERE / t["app"]
    widget_token()
    try:
        _widget_req(port, "/__state")
    except Exception:
        env = dict(os.environ)
        if t.get("level"): env["WIDGET_LEVEL"] = str(t["level"])      # per-task difficulty level for the widget server
        subprocess.Popen([sys.executable, str(script), str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
        time.sleep(0.9)
    try:
        _widget_req(port, "/__reset", data=b"{}")
    except Exception:
        pass


def ensure_pixelapp():
    ensure_app(TASKS["07-pixel-click"])


def _clear_cart(sid, rounds=15):
    """Best-effort empty the cart so each run starts clean (before/after shots are the real backstop)."""
    for _ in range(rounds):
        run_cli("navigate", CART_URL, sid=sid); time.sleep(1.5)
        txt = (run_cli("eval", "document.body.innerText", sid=sid) or "").lower()
        if "cart is empty" in txt:
            return
        r = run_cli("eval", "(function(){var b=document.querySelector(\"input[data-action='delete-active-item'],"
                             "input[value='Delete'],[aria-label^='Delete']\");if(b){b.click();return 'y'}return 'n'})()",
                    sid=sid)
        try:
            if json.loads(r).get("result") != "y":
                return
        except Exception:
            return
        time.sleep(1.5)


# ------------------------------------------------------------------ setup
def setup(task, run=None):
    task = canon(task)
    t = TASKS[task]
    ensure_daemon()
    if t.get("app"):
        ensure_app(t)
    prompt_text = t["prompt"]
    if t.get("fill_from_state"):      # per-run target from the app (e.g. the map explorer's place + district)
        try:
            st = json.loads(_widget_req(t.get("port", PIXEL_PORT), "/__state"))
            tgt = st.get("target") or {}
            if isinstance(tgt, dict):
                prompt_text = prompt_text.replace("{NAME}", str(tgt.get("name", ""))).replace("{DISTRICT}", str(tgt.get("district", "")))
            else:
                prompt_text = prompt_text.replace("{TARGET}", str(int(tgt)) if float(tgt).is_integer() else str(tgt))
        except Exception as e:
            print(f"[setup] fill_from_state failed: {e}")
    try:
        for s in json.loads(run_cli("list") or "[]"):
            run_cli(s["session_id"], "delete")
    except Exception:
        pass
    create = [*CLI, "create"]
    if os.environ.get("BENCH_VISIBLE"):
        create.append("--show")
    if t.get("profile"):
        # BENCH_PROFILE overrides; otherwise the daemon's active default profile applies
        # (sign in once there: `browser create --show`).
        bp = os.environ.get("BENCH_PROFILE")
        if bp:
            create += ["--profile", bp]
    else:
        create.append("--ephemeral")
    sid = subprocess.run(create, capture_output=True, text=True, env=ENV).stdout.strip()
    # cart tasks: start from a clean cart and snapshot the BEFORE state (harness-owned unique filename,
    # keyed to this run — no reliance on the agent to name files). All of this is before t0 so it is
    # excluded from the run's metrics.
    if t.get("cart"):
        _clear_cart(sid)
        if run:
            run_cli("navigate", CART_URL, sid=sid); time.sleep(1.0)
            run_cli("screenshot", "-o", str(RAW / f"{task}.{run}.cart_before.jpg"), sid=sid)
    # tag the page title so record_cdp.py can locate this exact target; do it BEFORE t0 so the
    # marker call is excluded from the run's metrics.
    rec_ws = None
    if os.environ.get("BENCH_RECORD"):
        run_cli("eval", f"document.title='REC-{sid}'", sid=sid)
        # Resolve the tab's DevTools ws URL NOW, before the agent can navigate away and the page
        # title changes: the URL is stable for the tab's lifetime, so record_cdp.py can attach by it
        # instead of racing the title marker (seven uncapped reruns lost their video that way).
        try:
            import record_cdp
            for _ in range(20):
                rec_ws = record_cdp.find_target(sid)
                if rec_ws:
                    break
                time.sleep(0.25)
        except BaseException:  # record_cdp sys.exit()s at import if websockets is missing; never abort setup
            rec_ws = None
    META.write_text(json.dumps({"task": task, "sid": sid, "t0": time.time(), "rec_ws": rec_ws,
                                "cpu0": tree_cpu(daemon_pid()),
                                "visible": bool(os.environ.get("BENCH_VISIBLE"))}))
    mode = "a VISIBLE window" if os.environ.get("BENCH_VISIBLE") else "headless (you cannot see the screen)"
    body = PREAMBLE.format(sid=sid, mode=mode) + "\n\nTASK: " + prompt_text
    if os.environ.get("BENCH_HARNESS") in ("agy", "codex", "muse"):
        # agy/codex can't load a Claude skill; point them at the shipped SKILL.md for equivalent guidance
        print(f"First, read the browser CLI reference at {SKILL} to learn the available commands and targeting "
              f"syntax. Then complete this task using only that `browser` CLI.\n\n" + body)
    else:
        print("/browser-cli\n\n" + body)


# ------------------------------------------------------------------ record (capture, no judging)
def _parse_stream(path, harness):
    """Return (result_text, usage_dict) from a stream-json (ndjson) or single-json model output file."""
    text, usage = "", {}
    lines = [l for l in Path(path).read_text().splitlines() if l.strip()] if Path(path).exists() else []
    objs = []
    for l in lines:
        try:
            objs.append(json.loads(l))
        except Exception:
            pass
    if len(objs) == 1 and isinstance(objs[0], dict):  # single-json envelope
        o = objs[0]
        text = o.get("result") or o.get("response") or ""
        usage = o.get("usage") or {}
        return text, usage
    if harness == "codex":
        # codex exec --json: agent_message items carry text; turn.completed events carry usage
        # (accumulated across turns; input_tokens already includes cached_input_tokens).
        acc = {}
        for o in objs:
            if o.get("type") == "item.completed" and o.get("item", {}).get("type") == "agent_message":
                text = o["item"].get("text", "")
            if o.get("type") == "turn.completed":
                for k, v in (o.get("usage") or {}).items():
                    if isinstance(v, (int, float)):
                        acc[k] = acc.get(k, 0) + v
        return text, acc
    if harness == "muse":
        # muse exec --json stdout + session.jsonl concatenated by muse_one.sh. Final text is the
        # run.terminal.completed event's text (stdout, bare envelope); usage comes only from the
        # session log's model_completed events (wrapped in "envelope"), accumulated across calls.
        # cached_tokens is a subset of input_tokens; reasoning_tokens a subset of output_tokens.
        acc = {}
        deltas = []
        for o in objs:
            env = o.get("envelope", o)
            if not isinstance(env, dict):
                continue
            p = env.get("payload") or {}
            if env.get("payload_type") == "run.output.delta":
                deltas.append(p.get("text") or "")
            if env.get("payload_type") == "run.terminal.completed":
                text = p.get("text") or text
            ev = p.get("event") or {}
            if isinstance(ev, dict) and ev.get("kind") == "model_completed":
                for k, v in (ev.get("usage") or {}).items():
                    if isinstance(v, (int, float)):
                        acc[k] = acc.get(k, 0) + v
        # The terminal event's text can be a late status line ("Server stopped") rather than the
        # agent's real output; the concatenated output deltas are the authoritative transcript.
        # Found in the 2026-09-02 failure re-audit (2 runs affected).
        full = "".join(deltas)
        if len(full) > len(text or ""):
            text = full
        return text, acc
    for o in objs:  # stream-json: find the terminal result event
        if harness == "agy":
            if o.get("event") == "result":
                text = o.get("result", {}).get("response", ""); usage = o.get("result", {}).get("usage", {})
        else:
            if o.get("type") == "result":
                text = o.get("result", ""); usage = o.get("usage", {})
    return text, usage


def _tagline(text, tag):
    """Find the last `TAG: value` line, tolerating markdown wrappers like `**TAG:** value`."""
    for line in reversed((text or "").splitlines()):
        s = line.strip().lstrip("*#>_-` ").rstrip()
        if s.upper().startswith(tag + ":"):
            return s.split(":", 1)[1].strip().strip("*_` ").strip()
    return None


def _answer_from(text):
    return _tagline(text, "ANSWER")


def _blocked_from(text):
    """Agent-declared environment wall (CAPTCHA / robot check / forced re-login) per the PREAMBLE
    protocol. A blocked run is neither pass nor fail: it needs the user present to clear the wall."""
    return _tagline(text, "BLOCKED")


def record(task, kw):
    task = canon(task)
    meta = json.loads(META.read_text()); sid = meta["sid"]; t0 = meta["t0"]
    t1 = time.time(); cpu1 = tree_cpu(daemon_pid())
    harness = kw.get("harness", "claude"); run = kw["run"]
    stream_src = kw.get("stream"); cpu_src = kw.get("cpu")
    # full model trace -> raw/
    stream_dst = None
    if stream_src and Path(stream_src).exists():
        stream_dst = f"{task}.{run}.stream.txt"; shutil.copyfile(stream_src, RAW / stream_dst)
    text, usage = _parse_stream(stream_src, harness) if stream_src else ("", {})
    answer = _answer_from(text); blocked = _blocked_from(text)
    # Preserve every screenshot the agent saved to an explicit path (agents pick names like
    # /tmp/jspaint_final.jpg that later runs overwrite) into raw/ NOW, while the file still holds
    # this run's pixels. Found in the 2026-09-02 re-audit: three reruns shared one /tmp name.
    preserved = []
    try:
        events = []
        for line in RLOG.read_text(errors="ignore").splitlines():
            if sid in line:
                try:
                    events.append(json.loads(line))
                except Exception:
                    pass
        for ev in events:
            if ev.get("action") != "screenshot":
                continue
            src = (ev.get("params") or {}).get("output")
            if src and Path(src).expanduser().exists():
                dst = f"{task}.{run}.shot{len(preserved)+1}.jpg"
                shutil.copyfile(Path(src).expanduser(), RAW / dst); preserved.append(dst)
    except Exception as e:
        print(f"[record] screenshot preservation skipped: {e}")
    # everything the model did through the CLI, verbatim from the daemon log
    reqs = []
    for line in (RLOG.read_text().splitlines() if RLOG.exists() else []):
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("t", 0) >= t0 and e.get("t", 0) <= t1 + 1 and e.get("session") == sid:
            reqs.append(e)
    cpu_series = []
    if cpu_src and Path(cpu_src).exists():
        cpu_series = [json.loads(x) for x in Path(cpu_src).read_text().splitlines() if x.strip()]
    # end-state evidence so future verifiers can re-judge WITHOUT the live session
    end_state = {"url": (run_cli("eval", "location.href", sid=sid) or "").strip(),
                 "title": (run_cli("eval", "document.title", sid=sid) or "").strip(),
                 "text": (run_cli("text", sid=sid) or "")[:8000],
                 "snapshot": (run_cli("snapshot", sid=sid) or "")[:8000]}
    cart_evidence = None; cart_after = None
    cart_before = f"{task}.{run}.cart_before.jpg" if (RAW / f"{task}.{run}.cart_before.jpg").exists() else None
    if TASKS[task].get("cart"):
        run_cli("navigate", CART_URL, sid=sid); time.sleep(1.5)   # AFTER state (harness-owned filename)
        cart_evidence = {
            "text": (run_cli("text", sid=sid) or "")[:12000],
            "asins": (run_cli("eval", "JSON.stringify(Array.from(document.querySelectorAll('[data-asin]')).map(e=>e.getAttribute('data-asin')).filter(Boolean))", sid=sid) or "").strip()}
        after_path = RAW / f"{task}.{run}.cart_after.jpg"
        run_cli("screenshot", "-o", str(after_path), sid=sid)
        if after_path.exists():
            cart_after = after_path.name
    pixel_state = None                       # app tasks: capture the server's click log (objective verdict)
    if TASKS[task].get("app"):
        try:
            pixel_state = json.loads(_widget_req(TASKS[task].get("port", PIXEL_PORT), "/__state"))
        except Exception:
            pixel_state = None
    video = f"{task}.{run}.mp4" if (RAW / f"{task}.{run}.mp4").exists() else None
    bundle = {
        "task": task, "run": run, "harness": harness, "model": kw.get("model", ""),
        "effort": kw.get("effort", ""), "config": kw.get("config", run),
        "visible": meta.get("visible", False), "sid": sid, "t0": t0, "t1": t1,
        "agent_result_text": text, "agent_usage_raw": usage, "answer": answer, "blocked": blocked,
        "stream_file": stream_dst, "video_file": video,
        "cart_before": cart_before, "cart_after": cart_after, "pixel_state": pixel_state,
        "budget_hit": str(kw.get("budget", "0")) == "1", "budget_s": int(kw.get("budget_s") or 0) or None,
        "requests_log": reqs, "cpu_series": cpu_series,
        "cpu0": meta.get("cpu0"), "cpu1": cpu1, "end_state": end_state, "cart_evidence": cart_evidence,
    }
    (RAW / f"{task}.{run}.json").write_text(json.dumps(bundle, indent=1))
    print(f"recorded raw/{task}.{run}.json  ({len(reqs)} cli calls, answer={answer!r})")
    return bundle


# ------------------------------------------------------------------ score (derive metrics + verdict)
WIDGET_PRIVATE = ("__submit", "__click", "__reset", "__step3", "__state", "__data", "__resolve", "__act", "__save", "__settings", "__move", "__lock", "__closelinked", "__rows", "__restart", "__start", "__choose", "__finish", "__validate", "__catalog", "__verify", "__answer", "__accept_offer", "__pause", "__keep", "__cancel", "__turn", "__confirm")


def widget_bypass(bundle):
    """True when the agent addressed the widget server's private endpoints itself (eval/fetch/navigate/curl)
    instead of interacting through the page. The page's own JS calls them legitimately; those never
    appear in the browser command log, so any appearance there is agent-driven. Reading /__scene.png is
    fine (it is what the page shows)."""
    import re
    # match URL paths only ("/__state", "fetch('/__click'", "curl .../__act"), never a bare JS identifier
    # such as `window.__state` (a Sonnet run probed that global and was wrongly flagged on 2026-09-03)
    pat = re.compile(r"/(?:" + "|".join(re.escape(p) for p in WIDGET_PRIVATE) + r")\b")
    for e in bundle.get("requests_log") or []:
        if e.get("action") in ("eval", "navigate", "goto", "open") and pat.search(json.dumps(e.get("params") or {})):
            return True
    return False


def _judge(task, bundle):
    """Return True/False for programmatic kinds, or None for LLM-judged ('judge') kinds (pending)."""
    t = TASKS[task]; kind = t["kind"]
    if kind == "judge":
        return None
    if kind in ("pixelstate", "appstate"):   # objective: the widget server judged the interaction
        if widget_bypass(bundle):             # ...unless the agent drove the server's endpoints directly
            return False
        return bool((bundle.get("pixel_state") or {}).get("complete"))
    if kind == "cart":
        ev = bundle.get("cart_evidence") or {}; hay = (ev.get("text", "") + " " + ev.get("asins", "")).lower()
        return all(it["asin"].lower() in hay or it["title"].lower() in hay for it in AMAZON_ITEMS)
    if kind == "cart_any":
        ev = bundle.get("cart_evidence") or {}; text = ev.get("text", "").lower()
        try:
            asins = json.loads(ev.get("asins") or "[]")
        except Exception:
            asins = []
        return (len(asins) > 0) or ("your amazon cart is empty" not in text and "subtotal" in text)
    if kind == "keywords":
        a = (bundle.get("answer") or "").lower(); return sum(kw in a for kw in X_PROJECTS) >= X_PROJECTS_MIN
    a = (bundle.get("answer") or "").strip().lower()
    return (a == t["expect"]) if t["match"] == "exact" else (t["expect"] in a)


def _agent_tokens(harness, usage):
    if not usage:
        return None, None
    if harness == "agy":
        return usage.get("total_tokens"), usage.get("thinking_tokens")
    if harness == "codex":
        tot = (usage.get("input_tokens", 0) + usage.get("output_tokens", 0)) or None
        return tot, usage.get("reasoning_output_tokens")
    if harness == "muse":
        tot = (usage.get("input_tokens", 0) + usage.get("output_tokens", 0)) or None
        return tot, usage.get("reasoning_tokens")
    tot = sum(usage.get(k, 0) for k in ("input_tokens", "output_tokens",
              "cache_read_input_tokens", "cache_creation_input_tokens")) or None
    return tot, usage.get("thinking_tokens")


def _metrics(bundle):
    reqs = bundle.get("requests_log", [])
    snaps = sum((e.get("action") == "snapshot") or bool(e.get("batch") and "snapshot" in e["batch"]) for e in reqs)
    shots = sum(e.get("action") == "screenshot" for e in reqs)
    cpu0 = (bundle.get("cpu0") or {}).get("pids", {}); cpu1 = (bundle.get("cpu1") or {}).get("pids", {})
    daemon_cpu_s = sum(cpu1[p] - cpu0.get(p, 0.0) for p in cpu1)
    series = bundle.get("cpu_series") or []
    at, tt = _agent_tokens(bundle.get("harness", "claude"), bundle.get("agent_usage_raw") or {})
    return {
        "wall_s": round((reqs[-1]["t"] + reqs[-1]["dur"] - reqs[0]["t"]) if reqs else 0, 2),
        "wall_total_s": round(bundle["t1"] - bundle["t0"], 1),
        "cli_calls": len(reqs), "failed_calls": sum(not e.get("ok", True) for e in reqs),
        "cli_time_s": round(sum(e.get("dur", 0) for e in reqs), 2),
        "tool_output_tokens": round(sum(e.get("bytes", 0) for e in reqs) / 4),
        "snapshots": snaps, "screenshots": shots,
        "daemon_cpu_s": round(daemon_cpu_s, 2), "daemon_rss_mb": round((bundle.get("cpu1") or {}).get("rss_mb", 0)),
        "cpu_peak_pct": round(max((p["cpu_pct"] for p in series), default=0), 1),
        "rss_peak_mb": round(max((p["rss_mb"] for p in series), default=0)),
        "agent_tokens": at, "thinking_tokens": tt,
    }


VERDICTS = RES / "verdicts.json"   # durable LLM-as-judge decisions, keyed "<task>.<run>"


def _verdicts():
    try:
        return json.loads(VERDICTS.read_text())
    except Exception:
        return {}


def score(only=None):
    verdicts = _verdicts(); n = 0
    for f in sorted(RAW.glob("*.json")):
        stem_task, _, stem_run = f.stem.partition(".")
        if only and f"{canon(stem_task)}.{stem_run}" != only:
            continue
        b = json.loads(f.read_text()); task = canon(b["task"]); key = f"{task}.{b['run']}"
        raw_v = _judge(task, b)          # bool for programmatic kinds, None for LLM-judged
        needs_judge = raw_v is None
        success, note, blocked = raw_v, None, False
        if key in verdicts:                                     # a durable verdict exists -> it wins
            v = verdicts[key]
            if v.get("blocked"):
                success, needs_judge, blocked = None, False, True
            elif needs_judge:
                success, needs_judge = bool(v.get("pass")), False
            note = v.get("note") or note
        elif b.get("blocked") and success is not True:
            # agent declared an environment wall (CAPTCHA / robot check / forced re-login):
            # neither pass nor fail; rerun interactively with the user present to clear it.
            success, needs_judge, blocked = None, False, True
            note = f"BLOCKED: {b['blocked']}"
        r = {"task": task, "run": b["run"], "config": b.get("config", b["run"]),
             "harness": b.get("harness", "claude"), "model": b.get("model", ""), "effort": b.get("effort", ""),
             "visible": b.get("visible", False), "success": success, "needs_judge": needs_judge,
             "blocked": blocked, "judge_note": note, "answer": b.get("answer"), **_metrics(b)}
        d = RES / task; d.mkdir(exist_ok=True)
        (d / f"{r['run']}.json").write_text(json.dumps(r, indent=1)); n += 1
    pend = sum(1 for f in RES.glob("*/*.json") if json.loads(f.read_text()).get("needs_judge"))
    print(f"scored {n} run(s) -> results/  ({pend} awaiting LLM judgment; run `judge_manifest`)")


def judge_manifest():
    """Emit the evidence for every run still awaiting an LLM verdict, as JSON for a judge to act on."""
    out = []
    for f in sorted(RAW.glob("*.json")):
        b = json.loads(f.read_text()); task = canon(b["task"]); key = f"{task}.{b['run']}"
        if task not in TASKS:  # culled task (e.g. 23): raw evidence retained, never judged
            continue
        if _judge(task, b) is not None or key in _verdicts():
            continue
        es = b.get("end_state") or {}
        reqs = b.get("requests_log", [])
        navigated = [e for e in reqs if e.get("action") == "navigate"]
        cmds = [(e.get("action") or "") + (":" + json.dumps(e.get("params"))[:50] if e.get("params") else "")
                for e in reqs]
        out.append({"key": key, "task": task, "is_cart": bool(TASKS[task].get("cart")),
                    # agent-declared wall: auto-scored BLKD; judge confirms from evidence and may
                    # override with set_verdict fail if the claim is bogus (no wall in video/stream)
                    "blocked_claim": b.get("blocked"),
                    "prompt": TASKS[task]["prompt"], "answer": b.get("answer"),
                    "agent_result_text": (b.get("agent_result_text") or "")[:1500],
                    "end_url": es.get("url"), "end_text_excerpt": (es.get("text") or "")[:1200],
                    "cart_evidence_text": ((b.get("cart_evidence") or {}).get("text") or "")[:1200],
                    "cli_calls": len(reqs), "navigations": len(navigated), "commands": cmds[:40],
                    "cart_before": (str(RAW / b["cart_before"]) if b.get("cart_before") else None),
                    "cart_after": (str(RAW / b["cart_after"]) if b.get("cart_after") else None),
                    "video_file": b.get("video_file"), "stream_file": b.get("stream_file")})
    print(json.dumps(out, indent=1))


def set_verdict(key, verdict, note=None):
    """verdict: 'pass' | 'fail' | 'blocked'. 'blocked' = environment wall (CAPTCHA/robot check/
    forced re-login) confirmed in the evidence: excluded from pass/fail, rerun with the user present."""
    t, _, r = key.partition("."); key = f"{canon(t)}.{r}"
    verdict = str(verdict).lower()
    if verdict in ("pass", "true", "1"):
        entry = {"pass": True, "note": note or ""}
    elif verdict == "blocked":
        entry = {"pass": None, "blocked": True, "note": note or ""}
    else:
        entry = {"pass": False, "note": note or ""}
    v = _verdicts(); v[key] = entry
    VERDICTS.write_text(json.dumps(v, indent=1))
    score(key)   # re-score just this run so results/ reflects the verdict
    print(f"verdict {key} = {'BLOCKED' if entry.get('blocked') else ('PASS' if entry['pass'] else 'FAIL')}")


# ------------------------------------------------------------------ report / compare
def is_done(key):
    """A run is 'done' (skip on resume) if it PASSED, or — for LLM-judge tasks — it captured real
    data and is awaiting judgment. Empty (0 cli calls) or programmatically-failed runs are NOT done,
    so a resume retries them."""
    t, _, r = key.partition(".")
    # A recorded verdict (pass, fail, or blocked) is FINAL: one attempt per run. Without this,
    # resume would silently retry judged-fail runs, overwriting their evidence and giving
    # failures a second chance that passes never get.
    if f"{canon(t)}.{r}" in _verdicts():
        return True
    f = RES / canon(t) / f"{r}.json"
    if not f.exists():
        return False
    try:
        r = json.loads(f.read_text())
    except Exception:
        return False
    if r.get("success") is True:
        return True
    if r.get("needs_judge") and (r.get("cli_calls") or 0) > 0:
        return True
    if r.get("blocked"):
        # environment wall: headless retries just re-hit it; rerun interactively (BENCH_VISIBLE=1,
        # user present) instead of hammering the site on resume.
        return True
    return False


def _rows():
    return [json.loads(f.read_text()) for f in sorted(RES.glob("*/*.json"))]


def _ok(r):
    if r.get("blocked"):
        return "BLKD"
    return "PEND" if r.get("needs_judge") else ("PASS" if r["success"] else "FAIL")


def report():
    print(f"{'task':16s} {'config':24s} {'ok':4s} {'calls':>5s} {'fail':>4s} {'wall s':>7s} "
          f"{'cli s':>6s} {'tool tok':>8s} {'agent tok':>9s} {'think':>6s} {'cpu s':>6s} {'rss':>6s}")
    for r in _rows():
        print(f"{r['task']:16s} {r.get('config', r['run']):24s} {_ok(r):4s} "
              f"{r['cli_calls']:5d} {r['failed_calls']:4d} {r['wall_s']:7.1f} {r['cli_time_s']:6.2f} "
              f"{r['tool_output_tokens']:8d} {str(r.get('agent_tokens') or '-'):>9s} "
              f"{str(r.get('thinking_tokens') or '-'):>6s} {r['daemon_cpu_s']:6.1f} {r['daemon_rss_mb']:6d}")


def compare():
    rows = _rows()
    cfgs = {}
    for r in rows:
        cfgs.setdefault(r.get("config", r["run"]), []).append(r)
    med = lambda a, k: statistics.median([x.get(k) or 0 for x in a]) if a else 0
    print(f"{'config':24s} {'tasks':>5s} {'att':>4s} {'pass@1':>7s} {'pend':>4s} {'med calls':>9s} "
          f"{'med wall':>8s} {'med cli s':>9s} {'med tool tok':>12s} {'med agent tok':>13s} "
          f"{'med cpu s':>9s} {'med rss':>7s}")
    for cfg in sorted(cfgs):
        att = cfgs[cfg]
        # blocked runs (CAPTCHA/bot wall/forced re-login) are neither pass nor fail: exclude entirely
        att = [r for r in att if not r.get("blocked")]
        judged = [r for r in att if not r.get("needs_judge")]
        tasks = sorted({r["task"] for r in judged})   # pass@1 over judged tasks only
        pend = len({r["task"] for r in att if r.get("needs_judge")} - set(tasks))
        p1 = sum(all(r["success"] for r in judged if r["task"] == tk) for tk in tasks)
        nt = len(tasks) + pend
        print(f"{cfg:24s} {nt:5d} {len(att):4d} {p1:4d}/{len(tasks):<2d} {pend:4d} "
              f"{med(att,'cli_calls'):9.0f} {med(att,'wall_s'):8.1f} {med(att,'cli_time_s'):9.2f} "
              f"{med(att,'tool_output_tokens'):12.0f} {med(att,'agent_tokens'):13.0f} "
              f"{med(att,'daemon_cpu_s'):9.2f} {med(att,'daemon_rss_mb'):7.0f}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    if cmd == "tasks":                 # the sweep set (BENCH_SET=v1 default | v2 | all)
        print("\n".join(sweep_tasks()))
    elif cmd == "setup":
        setup(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "record":
        kw = dict(a.split("=", 1) for a in sys.argv[3:] if "=" in a)
        record(sys.argv[2], kw)
    elif cmd == "score":
        score(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "done":          # exit 0 if <task>.<run> is complete (skip on resume), else 1
        sys.exit(0 if is_done(sys.argv[2]) else 1)
    elif cmd == "judge_manifest":
        judge_manifest()
    elif cmd == "set_verdict":     # set_verdict <task>.<run> <pass|fail|blocked> [note...]
        key = sys.argv[2]; verdict = sys.argv[3]
        note = " ".join(sys.argv[4:]) or None
        set_verdict(key, verdict, note)
    elif cmd == "report":
        report()
    elif cmd == "compare":
        compare()
