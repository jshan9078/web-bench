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
  harness.py score  [<task>.<run>]                  -> (re)apply verifiers + metrics -> results/*.json
  harness.py report                                 -> flat table (from results/)
  harness.py compare                                -> per-config medians + pass@k (the video's numbers)

Env: BROWSER_CLI/BROWSER_DAEMON select the impl. BENCH_VISIBLE=1 -> headed. BENCH_PROFILE=<name> ->
     persistent profile (amazon_cart/x_projects need a logged-in one). BENCH_HARNESS=agy -> emit an
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
    "a concise summary of what you found, and if asked for a value make the LAST line exactly `ANSWER: <value>`."
)

AMAZON = "www.amazon.ca"   # marketplace; book ASINs (ISBN-10) are the same across marketplaces
_dp = lambda i: f"https://{AMAZON}/dp/{i['asin']}"
# Every task tests NAVIGATION over real-world data (no puzzles/reasoning). Read tasks target CURRENT
# data that cannot be in any training set and are graded by LLM-as-judge from the captured evidence
# (raw bundle: agent answer + full stream + end_state). Action tasks keep a programmatic state check.
TASKS = {
    # read-only navigation over current real-world data, judged offline by an LLM from captured evidence
    "mlb_latest": {"kind": "judge"},
    "hn_summary": {"kind": "judge"},
    "weather_nyc": {"kind": "judge"},
    "x_projects": {"profile": True, "kind": "judge"},
    # cart actions, judged from a cart screenshot + the command trace
    "amazon_cart": {"profile": True, "kind": "judge", "cart": True},
    "amazon_search_add": {"profile": True, "kind": "judge", "cart": True},
    # vision + pixel-click, verified programmatically by the canvas server
    "pixel_click": {"kind": "pixelstate", "app": True},
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
    "16-transit-directions": {"kind": "judge"},
    "17-currency-meal-budget": {"kind": "judge"},
    "18-npm-package-audit": {"kind": "judge"},
    "19-wiktionary-wotd": {"kind": "judge"},
    "20-nasa-apod-vision": {"kind": "judge"},
    "21-amazon-office-bundle": {"profile": True, "kind": "judge", "cart": True},
    "22-amazon-earbud-compare": {"profile": True, "kind": "judge", "cart": True},
    "23-amazon-filter-hunt": {"profile": True, "kind": "judge", "cart": True},
    "24-bestbuy-console-check": {"kind": "judge"},
    "25-walmart-grocery-pricing": {"kind": "judge"},
    "26-ebay-keyboard-hunt": {"kind": "judge"},
    "27-amazon-review-mining": {"profile": True, "kind": "judge"},
    "28-price-cross-check": {"profile": True, "kind": "judge"},
    "29-excalidraw-pipeline": {"kind": "judge"},
    "30-lichess-puzzle": {"kind": "judge"},
    "31-wordle-daily": {"kind": "judge"},
    "32-desmos-intersections": {"kind": "judge"},
    "33-osm-street-read": {"kind": "judge"},
    "34-osm-route-measure": {"kind": "judge"},
    "35-gmaps-traffic-read": {"kind": "judge"},
    "36-jspaint-poster": {"kind": "judge"},
    "37-gmaps-poi-hunt": {"kind": "judge"},
    "38-seterra-europe": {"kind": "judge"},
    "39-youtube-frame-describe": {"kind": "judge"},
    "40-arxiv-pdf-figure": {"kind": "judge"},
    "41-owid-dataset-read": {"kind": "judge"},
    "42-youtube-watch-later": {"profile": True, "kind": "judge"},
    "43-gmail-self-draft": {"profile": True, "kind": "judge"},
    "44-gcal-event": {"profile": True, "kind": "judge"},
    "45-gdocs-hn-note": {"profile": True, "kind": "judge"},
    "46-github-account-audit": {"profile": True, "kind": "judge"},
    "47-reddit-save": {"profile": True, "kind": "judge"},
    "48-spotify-playlist": {"profile": True, "kind": "judge"},
    "49-x-bookmark": {"profile": True, "kind": "judge"},
    "50-google-flights-nonstop": {"kind": "judge"},
    "51-wikipedia-revision-audit": {"kind": "judge"},
    "52-regex101-dates": {"kind": "judge"},
    "53-caniuse-feature": {"kind": "judge"},
    "54-stackoverflow-live": {"kind": "judge"},
    "55-wayback-snapshot": {"kind": "judge"},
    "56-sunrise-reykjavik": {"kind": "judge"},
    "57-hn-debate-analysis": {"kind": "judge"},
}
# Prompts live in tasks/<name>/prompt.txt (one subdirectory per task; see tasks/<name>/verifier.md for
# how each run is scored). This directory is the source of truth for task prompts.
_TDIR = HERE / "tasks"
for _name, _spec in TASKS.items():
    _spec["prompt"] = (_TDIR / _name / "prompt.txt").read_text().strip()


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


def ensure_pixelapp():
    """Start the localhost canvas challenge (server-rendered scene) and reset it to a fresh layout."""
    import urllib.request
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PIXEL_PORT}/__state", timeout=1)
    except Exception:
        subprocess.Popen([sys.executable, str(HERE / "pixelapp/server.py"), str(PIXEL_PORT)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.7)
    try:
        urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{PIXEL_PORT}/__reset", data=b"{}", method="POST")).read()
    except Exception:
        pass


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
    t = TASKS[task]
    ensure_daemon()
    if t.get("app"):
        ensure_pixelapp()
    try:
        for s in json.loads(run_cli("list") or "[]"):
            run_cli(s["session_id"], "delete")
    except Exception:
        pass
    create = [*CLI, "create"]
    if os.environ.get("BENCH_VISIBLE"):
        create.append("--show")
    if t.get("profile"):
        create += ["--profile", os.environ.get("BENCH_PROFILE", "default")]
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
    if os.environ.get("BENCH_RECORD"):
        run_cli("eval", f"document.title='REC-{sid}'", sid=sid)
    META.write_text(json.dumps({"task": task, "sid": sid, "t0": time.time(),
                                "cpu0": tree_cpu(daemon_pid()),
                                "visible": bool(os.environ.get("BENCH_VISIBLE"))}))
    mode = "a VISIBLE window" if os.environ.get("BENCH_VISIBLE") else "headless (you cannot see the screen)"
    body = PREAMBLE.format(sid=sid, mode=mode) + "\n\nTASK: " + t["prompt"]
    if os.environ.get("BENCH_HARNESS") == "agy":
        # agy can't load a Claude skill; point it at the shipped SKILL.md for equivalent guidance
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
    for o in objs:  # stream-json: find the terminal result event
        if harness == "agy":
            if o.get("event") == "result":
                text = o.get("result", {}).get("response", ""); usage = o.get("result", {}).get("usage", {})
        else:
            if o.get("type") == "result":
                text = o.get("result", ""); usage = o.get("usage", {})
    return text, usage


def _answer_from(text):
    for line in reversed((text or "").splitlines()):
        if line.strip().upper().startswith("ANSWER:"):
            return line.split(":", 1)[1].strip()
    return None


def record(task, kw):
    meta = json.loads(META.read_text()); sid = meta["sid"]; t0 = meta["t0"]
    t1 = time.time(); cpu1 = tree_cpu(daemon_pid())
    harness = kw.get("harness", "claude"); run = kw["run"]
    stream_src = kw.get("stream"); cpu_src = kw.get("cpu")
    # full model trace -> raw/
    stream_dst = None
    if stream_src and Path(stream_src).exists():
        stream_dst = f"{task}.{run}.stream.txt"; shutil.copyfile(stream_src, RAW / stream_dst)
    text, usage = _parse_stream(stream_src, harness) if stream_src else ("", {})
    answer = _answer_from(text)
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
        import urllib.request
        try:
            pixel_state = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PIXEL_PORT}/__state", timeout=2))
        except Exception:
            pixel_state = None
    video = f"{task}.{run}.mp4" if (RAW / f"{task}.{run}.mp4").exists() else None
    bundle = {
        "task": task, "run": run, "harness": harness, "model": kw.get("model", ""),
        "effort": kw.get("effort", ""), "config": kw.get("config", run),
        "visible": meta.get("visible", False), "sid": sid, "t0": t0, "t1": t1,
        "agent_result_text": text, "agent_usage_raw": usage, "answer": answer,
        "stream_file": stream_dst, "video_file": video,
        "cart_before": cart_before, "cart_after": cart_after, "pixel_state": pixel_state,
        "requests_log": reqs, "cpu_series": cpu_series,
        "cpu0": meta.get("cpu0"), "cpu1": cpu1, "end_state": end_state, "cart_evidence": cart_evidence,
    }
    (RAW / f"{task}.{run}.json").write_text(json.dumps(bundle, indent=1))
    print(f"recorded raw/{task}.{run}.json  ({len(reqs)} cli calls, answer={answer!r})")
    return bundle


# ------------------------------------------------------------------ score (derive metrics + verdict)
def _judge(task, bundle):
    """Return True/False for programmatic kinds, or None for LLM-judged ('judge') kinds (pending)."""
    t = TASKS[task]; kind = t["kind"]
    if kind == "judge":
        return None
    if kind == "pixelstate":          # objective: server hit-tested the pixel clicks (ascending order)
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
        if only and f.stem != only:
            continue
        b = json.loads(f.read_text()); task = b["task"]; key = f"{task}.{b['run']}"
        raw_v = _judge(task, b)          # bool for programmatic kinds, None for LLM-judged
        needs_judge = raw_v is None
        success, note = raw_v, None
        if needs_judge and key in verdicts:                     # a prior LLM verdict exists -> use it
            success = bool(verdicts[key].get("pass")); note = verdicts[key].get("note"); needs_judge = False
        r = {"task": task, "run": b["run"], "config": b.get("config", b["run"]),
             "harness": b.get("harness", "claude"), "model": b.get("model", ""), "effort": b.get("effort", ""),
             "visible": b.get("visible", False), "success": success, "needs_judge": needs_judge,
             "judge_note": note, "answer": b.get("answer"), **_metrics(b)}
        (RES / f"{task}.{r['run']}.json").write_text(json.dumps(r, indent=1)); n += 1
    pend = sum(1 for f in RES.glob("*.json") if f.name not in ("current.json", "verdicts.json")
               and json.loads(f.read_text()).get("needs_judge"))
    print(f"scored {n} run(s) -> results/  ({pend} awaiting LLM judgment; run `judge_manifest`)")


def judge_manifest():
    """Emit the evidence for every run still awaiting an LLM verdict, as JSON for a judge to act on."""
    out = []
    for f in sorted(RAW.glob("*.json")):
        b = json.loads(f.read_text()); task = b["task"]; key = f"{task}.{b['run']}"
        if _judge(task, b) is not None or key in _verdicts():
            continue
        es = b.get("end_state") or {}
        reqs = b.get("requests_log", [])
        navigated = [e for e in reqs if e.get("action") == "navigate"]
        cmds = [(e.get("action") or "") + (":" + json.dumps(e.get("params"))[:50] if e.get("params") else "")
                for e in reqs]
        out.append({"key": key, "task": task, "is_cart": bool(TASKS[task].get("cart")),
                    "prompt": TASKS[task]["prompt"], "answer": b.get("answer"),
                    "agent_result_text": (b.get("agent_result_text") or "")[:1500],
                    "end_url": es.get("url"), "end_text_excerpt": (es.get("text") or "")[:1200],
                    "cart_evidence_text": ((b.get("cart_evidence") or {}).get("text") or "")[:1200],
                    "cli_calls": len(reqs), "navigations": len(navigated), "commands": cmds[:40],
                    "cart_before": (str(RAW / b["cart_before"]) if b.get("cart_before") else None),
                    "cart_after": (str(RAW / b["cart_after"]) if b.get("cart_after") else None),
                    "video_file": b.get("video_file"), "stream_file": b.get("stream_file")})
    print(json.dumps(out, indent=1))


def set_verdict(key, passed, note=None):
    v = _verdicts(); v[key] = {"pass": bool(passed), "note": note or ""}
    VERDICTS.write_text(json.dumps(v, indent=1))
    score(key)   # re-score just this run so results/ reflects the verdict
    print(f"verdict {key} = {'PASS' if passed else 'FAIL'}")


# ------------------------------------------------------------------ report / compare
def is_done(key):
    """A run is 'done' (skip on resume) if it PASSED, or — for LLM-judge tasks — it captured real
    data and is awaiting judgment. Empty (0 cli calls) or programmatically-failed runs are NOT done,
    so a resume retries them."""
    f = RES / f"{key}.json"
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
    return False


def _rows():
    return [json.loads(f.read_text()) for f in sorted(RES.glob("*.json"))
            if f.name not in ("current.json", "verdicts.json")]


def _ok(r):
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
    if cmd == "tasks":
        print("\n".join(TASKS))
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
    elif cmd == "set_verdict":     # set_verdict <task>.<run> <pass|fail> [note...]
        key = sys.argv[2]; passed = sys.argv[3].lower() in ("pass", "true", "1", "ok")
        note = " ".join(sys.argv[4:]) or None
        set_verdict(key, passed, note)
    elif cmd == "report":
        report()
    elif cmd == "compare":
        compare()
