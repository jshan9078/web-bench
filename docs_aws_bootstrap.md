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
