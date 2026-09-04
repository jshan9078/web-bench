# Running the final-set matrix on AWS (bootstrap checklist)

One instance = one serial benchmark process (the harness rule). Parallelism comes from several instances, each
running one shard. Suggested: 8 x c7i.2xlarge (or similar 8 vCPU / 16 GB) with Ubuntu 24.04; the run takes
about 110 instance-hours total for 1,312 runs, so 8 instances finish in roughly 14 hours.

Per instance (the operator does the sign-ins; they use personal accounts):
1. `git clone <web-bench repo>` and `pip install -r requirements.txt` (Pillow, numpy); Python 3.11+.
2. Install browser-cli (`browser` on PATH) and its Playwright Chromium; start `browser daemon --auto`.
3. Install and sign in the agent CLIs needed by the shard: `claude` (needs `--effort`), `muse`, `codex`, `agy`.
   Verify each with a trivial `-p` prompt before starting.
4. Copy `results/shards/shard_<i>.txt` (generated locally with `python3 matrix63.py shards 8`).
5. `nohup ./run_shard.sh results/shards/shard_<i>.txt &` (restart-safe: completed runs are skipped).
6. When `SHARD DONE` appears in results/matrix63.log, rsync `raw/` and `results/` back to the workstation
   (raw/ is never committed), then run `python3 harness.py score` and the judge pass for judge-kind tasks.

Notes: widget servers are started on demand by `harness.py setup`; the real-site tasks need outbound HTTPS to
github.com, en.wikipedia.org and jspaint.app; keep the instance clock in UTC; do not run two shards on one
instance (shared browser daemon and CPU sampler would confound timings).

## Seed sign-in notes (2026-09-04)

- claude: `npm install -g @anthropic-ai/claude-code`, sign in interactively; the browser-cli skill must be copied to
  `~/.claude/skills/browser-cli` (scp from the workstation; `mkdir -p ~/.claude/skills` first).
- codex: `npm install -g @openai/codex`, `codex login`; the runner passes `--skip-git-repo-check`. The account must
  have quota: a free-tier login reports "You've hit your usage limit" and every Luna run fails.
- muse: the Linux build is a single static binary (muse-bin-<ver>); `chmod +x` and symlink it to `~/.local/bin/muse`.
- agy: installed by the operator (no public Linux install source in this repo); `agy -p "..." --model <slug>` must answer.
- Verify each CLI with a trivial prompt from ~/web-bench before baking the AMI; the AMI carries the logins.

## Linux worker lessons (2026-09-04)

- The daemon must run under a virtual display (`xvfb-run -a browser daemon --auto`): the default profile launches a
  headed Chromium, and without a display session creation fails intermittently and can stop the daemon. The
  harness now retries `browser create` three times and aborts the run if no session id comes back.
- Ubuntu's apt botocore predates S3 conditional writes; the worker upgrades boto3/botocore at boot.
- `record_cdp.py` needs the `websockets` module for video capture; it is installed at boot.
- macOS AppleDouble files (`._*.json`) in the tarball broke `harness.py score` on Linux; the bundle step strips them.
- A fleet instance runs one worker; `aws/fleet.sh launch <ami> N <lane> <family>` spreads providers across workers.

AMIs: ami-08449c48154d36209 (claude, muse, agy signed in; codex on an exhausted account) and ami-0b32d4721497dc0e2 (adds the Codex API-key login for Luna). Seed i-00d609dd25ff82ec5 is stopped, keep it for future re-logins.
