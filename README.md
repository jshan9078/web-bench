# WebBench v2

A benchmark for how well an LLM agent drives a browser. Every configuration (model x thinking level x agent CLI) gets the same tool, [browser-automation-cli](https://github.com/jshan9078/browser-automation-cli), the same [skill file](SKILL.md), a fresh headless session and a 10-minute budget per task, and is scored at pass@1 on the same 70 tasks. The v1 set (44 live-site tasks, 36 configurations) is documented in [README-v1.md](README-v1.md); its results stay in `results/`.

## The task set: two tiers

| Tier | Tasks | What it is for |
|---|---|---|
| Core | 27 | Deterministic browser-control workflows every competent agent should pass: forms and multi-page flows, table editing and validation, triage and scheduling, keyboard-only and hover-only UIs, precision clicks, iframes and shadow DOM, nested scrolling, read-only GitHub and Wikipedia navigation. Every configuration passes 23 to 27 of them. It is the floor, and it catches harness or tooling breakage. |
| Discriminating | 43 | Tasks that at least one frontier configuration failed on both of two attempts while the set was built. 29 are counting or tracking over rendered video clips (occupancy peaks, event counts, attribution to actors, defects on a belt); the rest are exact visual counting and tracing, fine reading, and real-site judgement. This tier separates models. |

The two tiers are listed in [`results/core_set.json`](results/core_set.json) and [`results/validated_set.json`](results/validated_set.json) (which also records which configuration failed each task twice). Each task has a folder under [`tasks/`](tasks/) with `prompt.txt` (sent verbatim to the agent), `task.md` (what it tests and the discrimination hypothesis) and `verifier.md` (the pass criteria). The design history, including every batch that was tried and discarded, is in [`tasks/V2-DESIGN.md`](tasks/V2-DESIGN.md).

Selection caveat: the discriminating tier was built mostly with Claude Sonnet 5 at low effort as the pilot, so that configuration's score on it reflects the selection, not a neutral measurement. Sonnet 5 at medium and above never took part in selection.

### Local sites, not live ones

62 tasks run against small deterministic web apps in [`widgetapp/`](widgetapp/) served on localhost: video clips are rendered on a canvas with a real player (play, pause, seek, speed), images are generated per run, forms and workflows hold their state on the server. Every run starts from a fresh random state (`/__reset`), and the verdict is read from the server's state (`/__state`) after the run: the last submission, the confirmed click, the saved record. Private endpoints are gated behind a per-page-load key, so an agent that probes the site's API instead of using the page gets a 403 and nothing else; probing is logged but is not itself a failure. The 8 real-site tasks (GitHub, Wikipedia, JS Paint) are read-only, need no login, and are judged by a Claude Sonnet judge that first establishes the truth from the site's API ([JUDGE_PROMPT.md](JUDGE_PROMPT.md)).

## Rules

- **pass@1**, one attempt per configuration per task, 10-minute budget, no turn cap.
- **State-only scoring** for local tasks; **API-verified judging** for real-site tasks.
- **Rate limits void a run.** If the model hit a provider rate, quota or usage limit during a run, the run is discarded and rerun later, because retries distort the timing. Detection is in [`ratelimit.py`](ratelimit.py); the worker applies it after every run and [`audit_all.py`](audit_all.py) re-checks recorded runs.
- **Bot walls** are excluded and retried, never scored.
- **Cost** is the CLI's own reported cost for Claude and the provider's public prices applied to captured token usage for the others ([`run_cost.py`](run_cost.py)).

## Results

| Configuration | Pass@1 | Core tier | Discriminating tier | Median agent s | Median cost |
|---|---|---|---|---|---|
| GPT-6 Astra low | 94.3% | 26/27 | 40/43 | 35 | $0.71 |
| Opus 5 low | 81.4% | 27/27 | 30/43 | 90 | $0.53 |
| Opus 5 medium | 81.4% | 27/27 | 30/43 | 88 | $0.59 |
| Opus 5 high | 85.7% | 27/27 | 33/43 | 99 | $0.73 |
| Opus 5 max | 85.7% | 27/27 | 33/43 | 129 | $0.79 |
| Sonnet 5 low | 48.6% | 27/27 | 7/43 | 138 | $1.01 |
| Sonnet 5 medium | 68.6% | 26/27 | 22/43 | 136 | $0.58 |
| Sonnet 5 high | 67.1% | 27/27 | 20/43 | 147 | $0.56 |
| Sonnet 5 xhigh | 67.1% | 27/27 | 20/43 | 152 | $0.47 |
| Sonnet 5 max | 55.7% | 25/27 | 14/43 | 250 | $0.42 |
| Gemini 3.8 Flash low | 70.0% | 26/27 | 23/43 | 75 | $0.22 |
| Gemini 3.8 Flash medium | 81.4% | 26/27 | 31/43 | 112 | $0.34 |
| Gemini 3.8 Flash high | 80.0% | 27/27 | 29/43 | 156 | $0.38 |
| Muse Spark 1.3 low | 62.9% | 23/27 | 21/43 | 185 | $0.24 |
| Muse Spark 1.3 medium | 64.3% | 26/27 | 19/43 | 200 | $0.27 |
| Muse Spark 1.3 high | 68.6% | 23/27 | 25/43 | 212 | $0.31 |
| Muse Spark 1.3 xhigh | 75.7% | 26/27 | 27/43 | 193 | $0.32 |
| Muse Spark 1.3 ultra | 74.3% | 26/27 | 26/43 | 171 | $0.33 |

Configurations still partial and not listed: GPT-6 Astra medium, high, xhigh and max; GPT-5.6 Luna. Per-run records are in `results/<task>/<config>-val.json`, the machine-readable summary in [`results/v2_summary.json`](results/v2_summary.json), judge verdicts in [`results/verdicts.json`](results/verdicts.json). Raw bundles (traces, screenshots, video) are kept out of git.

## How it runs

- `harness.py` owns the task registry, starts widget servers, creates the browser session, records the raw bundle and scores it.
- `run_one.sh` (Claude Code), `muse_one.sh` (Muse Code), `codex_one.sh` (Codex CLI) and `agy_one.sh` (Antigravity) run one task on one configuration.
- `v2_iter2.sh` runs the pass@2 validation loop used while building the set; `v2_pass2.py` and `v2_validated.py` compute the tiers.
- The matrix runs on AWS: [`matrix_queue.py`](matrix_queue.py) is an S3 work queue with leased items (resumable, idempotent), [`run_worker.sh`](run_worker.sh) is the per-instance worker (one run at a time, provider family per worker, optional run cap), [`judge_daemon.py`](judge_daemon.py) judges real-site runs as they land, [`matrix_dashboard.py`](matrix_dashboard.py) is a localhost view of everything, and [`aws/fleet.sh`](aws/fleet.sh) launches and tears down the fleet ([`aws/README.md`](aws/README.md) has the bootstrap notes).
- [`make_v2_site.py`](make_v2_site.py) turns the summary into the data behind the results page.

`legacy/` holds the v1 sweep scripts and the per-round pilot scripts from building v2; they are kept for provenance and are not used.
