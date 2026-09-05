#!/usr/bin/env python3
"""Real-time LLM judge for the fleet. As soon as a done marker of a judge-kind task appears in the queue without a
verdict, this daemon (one run at a time): downloads the bundle, builds the canonical manifest item, runs the Sonnet
judge (`claude -p`, JUDGE_PROMPT.md verbatim + the item + API-verification instructions), lets it record the
verdict via harness.set_verdict (which re-scores the run), then uploads the verdict, the result json and an updated
done marker to S3. Log: results/judge_daemon.log. Usage: MATRIX_STORE=s3://... python3 judge_daemon.py [--once]"""
import os, sys, json, time, subprocess, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matrix_queue as mq, harness
S = mq.store(); LOG = "results/judge_daemon.log"; TRIES = {}
def log(msg):
    line = f"{datetime.datetime.now().strftime('%H:%M:%S')} {msg}"; print(line, flush=True); open(LOG, "a").write(line + "\n")
def pending():
    out = []
    for k in S.list("done/"):
        d = json.loads(S.get(k) or b"{}")
        if d.get("needs_judge") and d.get("success") is None and not d.get("verdict") and TRIES.get(k, 0) < 3: out.append((k, d))
    return sorted(out, key=lambda kd: kd[1].get("ts", 0))
def fetch(t, l):
    for k in S.list(f"raw/{t}.{l}.") + S.list(f"results/{t}/{l}."):
        if not k.endswith(".mp4") and not os.path.exists(k): S.get_file(k, k)
def manifest_item(key):
    items = json.loads(subprocess.run(["python3", "harness.py", "judge_manifest"], capture_output=True, text=True).stdout or "[]")
    return next((i for i in items if i["key"] == key), None)
def judge(t, l):
    key = f"{t}.{l}"; item = manifest_item(key)
    if item is None: return "no manifest item (already judged or auto-scored)"
    shots = sorted(glob.glob(f"raw/{t}.{l}.shot*.jpg"))[:12]
    prompt = open("JUDGE_PROMPT.md").read() + f"""

---
MANIFEST (one item):
{json.dumps(item, indent=1)}

Instructions for this item: work in {os.getcwd()}. Read tasks/{t}/verifier.md and establish the ground truth with the
API method it describes (gh api, curl to the MediaWiki API, etc.) before reading the agent's claims. Evidence files:
raw/{t}.{l}.json (requests_log, end_state, agent_result_text), screenshots {', '.join(shots) if shots else '(none)'}
(use the Read tool on a few if the page state matters), stream raw/{t}.{l}.stream.txt (grep it, it is large).
Then record exactly one verdict with:
  python3 harness.py set_verdict "{key}" pass|fail|blocked "<one-line reason> [judge: sonnet daemon]"
Do not modify any other file. End with one line: VERDICT: pass|fail|blocked."""
    env = {"HOME": os.environ["HOME"], "PATH": os.environ["PATH"], "TMPDIR": os.environ.get("TMPDIR", "/tmp")}
    try:
        cp = subprocess.run(["claude", "-p", prompt, "--model", "sonnet", "--effort", "medium", "--allowedTools", "Bash,Read,Grep", "--dangerously-skip-permissions", "--max-turns", "60"], capture_output=True, text=True, env=env, timeout=900)
        tail = (cp.stdout or "").strip().splitlines()[-1:] 
    except subprocess.TimeoutExpired: return "judge timed out"
    v = harness._verdicts().get(key)
    if v is None: return "judge finished without recording a verdict: " + (tail[0][:160] if tail else "")
    return v
def publish(k, t, l, v):
    key = f"{t}.{l}"; d = json.loads(S.get(k) or b"{}")
    res = json.load(open(f"results/{t}/{l}.json")) if os.path.exists(f"results/{t}/{l}.json") else {}
    d.update(success=res.get("success"), needs_judge=False, blocked=bool(v.get("blocked")), verdict="blocked" if v.get("blocked") else ("pass" if v.get("pass") else "fail"), judge_note=v.get("note", ""), judged_ts=time.time())
    S.put(k, mq.j(d)); S.put(f"verdicts/{mq.key(t, l)}", mq.j(v))
    if os.path.exists(f"results/{t}/{l}.json"): S.put_file(f"results/{t}/{l}.json", f"results/{t}/{l}.json")
def main():
    once = "--once" in sys.argv; log(f"judge daemon started, store {mq.STORE}")
    while True:
        items = pending()
        if not items:
            if once: return
            time.sleep(30); continue
        k, d = items[0]; t, l = d["task"], d["label"]; TRIES[k] = TRIES.get(k, 0) + 1
        log(f"judging {t} {l} (attempt {TRIES[k]})")
        try:
            fetch(t, l); v = judge(t, l)
            if isinstance(v, dict): publish(k, t, l, v); log(f"verdict {t} {l} = {'blocked' if v.get('blocked') else ('pass' if v.get('pass') else 'fail')}: {v.get('note','')[:140]}")
            else: log(f"judge problem {t} {l}: {v}")
        except Exception as e: log(f"error {t} {l}: {type(e).__name__}: {e}")
        if once: return
if __name__ == "__main__": main()
