# WebBench v2

WebBench measures how well an LLM agent drives a browser. Each configuration (model, thinking level, agent CLI) gets the same tool, [browser-automation-cli](https://github.com/jshan9078/browser-automation-cli), the same [skill file](SKILL.md), a fresh headless session and a 10-minute budget per task, and is scored at pass@1 on 70 tasks.

The earlier v1 set (44 live-site tasks, 36 configurations) is described in [README-v1.md](README-v1.md). Its results remain in `results/`.

## Task design

v1 stopped discriminating: frontier models scored 90 to 100% on it. v2 was built to find where they actually fail while still covering ordinary browser work.

Candidate tasks were written in batches (see [`tasks/V2-DESIGN.md`](tasks/V2-DESIGN.md) for every batch, including the ones thrown away) and run on Claude Sonnet 5, Claude Opus 5 and Muse Spark 1.2, all at low thinking. A task entered the set if a configuration failed it on two independent attempts (pass@2), or if it exercised a browser-control property the set would otherwise lack. Tasks that every configuration solved at pass@2 were dropped unless they filled such a gap. Failures were checked by hand before a task was kept: several tasks were voided and rebuilt because the failure turned out to be a bug in the task (an ambiguous count, an endpoint name collision, a duplicate in a generated list).

What the 70 tasks contain:

- 29 tasks that count or track something in a rendered video clip: occupancy peaks, events attributed to one of several actors, direction-filtered crossings, defects on a belt, brief text. The clip plays in a canvas player with play, pause, seek and speed controls; the agent must read frames from screenshots.
- Exact visual work on generated images: counting rotated glyphs or occluded shapes, tracing a line through crossings, reading an angle or a gauge, a clock without numerals.
- Browser-control workflows on local web apps: multi-page checkout, password reset through an in-app inbox, a keyboard-only list, hover-only nested menus, a form inside a shadow root inside an iframe, nested scrolling, table editing with conflicts, triage and scheduling.
- 8 read-only tasks on live GitHub, Wikipedia and JS Paint (blame, compare, first release containing a commit, merged-PR search, a revision history, a canvas drawing). No task needs a login.

62 tasks run against small deterministic web apps in [`widgetapp/`](widgetapp/) served on localhost. Each run starts from a fresh random state and the verdict is read from the server's state afterwards: the last submitted answer, the confirmed click, the saved record. The apps' private endpoints are gated behind a per-page-load key, so an agent that calls the API instead of using the page gets a 403; the attempt is logged but is not itself a failure. Live-site tasks are judged by a Claude Sonnet judge that first establishes the truth from the site's API ([JUDGE_PROMPT.md](JUDGE_PROMPT.md)).

Known bias: because Sonnet 5 low was the pilot for most of the selection, its score on v2 measures the selection rather than the model. Configurations at other thinking levels did not take part in selection.

Each task folder under [`tasks/`](tasks/) holds `prompt.txt` (sent verbatim to the agent), `task.md` (what it tests) and `verifier.md` (the pass criteria). The task list is [`results/v2_summary.json`](results/v2_summary.json) (`tasks`).

## Scoring rules

- One attempt per configuration per task (pass@1), 10-minute budget, no turn cap.
- Local tasks are scored from server state; live-site tasks by the judge against API ground truth.
- A run in which the model hit a provider rate, quota or usage limit is void and is rerun later, because the retries distort its timing. [`ratelimit.py`](ratelimit.py) holds the markers; the worker checks every run and [`audit_all.py`](audit_all.py) re-checks recorded ones. 114 runs were voided this way, all of them recorded as failures before the check existed.
- Verified bot walls are excluded and retried.
- Cost is the CLI's reported cost for Claude and the provider's list prices applied to the captured token usage for the others ([`run_cost.py`](run_cost.py)). Time is the agent's wall-clock seconds from the start of the run to its final answer.

## Results

| Configuration | Pass@1 | Median seconds | Median cost |
|---|---|---|---|
| GPT-6 Astra low | 66/70 (94%) | 35 | $0.71 |
| Opus 5 low | 57/70 (81%) | 90 | $0.53 |
| Opus 5 medium | 57/70 (81%) | 88 | $0.59 |
| Opus 5 high | 60/70 (86%) | 99 | $0.73 |
| Opus 5 xhigh | 64/70 (91%) | 105 | $0.74 |
| Opus 5 max | 60/70 (86%) | 129 | $0.79 |
| Sonnet 5 low | 34/70 (49%) | 138 | $1.01 |
| Sonnet 5 medium | 48/70 (69%) | 136 | $0.58 |
| Sonnet 5 high | 47/70 (67%) | 147 | $0.56 |
| Sonnet 5 xhigh | 47/70 (67%) | 152 | $0.47 |
| Sonnet 5 max | 39/70 (56%) | 250 | $0.42 |
| Gemini 3.8 Flash low | 49/70 (70%) | 75 | $0.22 |
| Gemini 3.8 Flash medium | 57/70 (81%) | 112 | $0.34 |
| Gemini 3.8 Flash high | 56/70 (80%) | 156 | $0.38 |
| Muse Spark 1.3 low | 44/70 (63%) | 185 | $0.24 |
| Muse Spark 1.3 medium | 45/70 (64%) | 200 | $0.27 |
| Muse Spark 1.3 high | 48/70 (69%) | 212 | $0.31 |
| Muse Spark 1.3 xhigh | 53/70 (76%) | 193 | $0.32 |
| Muse Spark 1.3 ultra | 52/70 (74%) | 171 | $0.33 |

GPT-6 Astra at medium, high, xhigh and max, and GPT-5.6 Luna at all levels, are partial and not listed. Per-run records are in `results/<task>/<config>-val.json`, the summary with per-task outcomes in [`results/v2_summary.json`](results/v2_summary.json), judge verdicts in [`results/verdicts.json`](results/verdicts.json). Raw bundles (traces, screenshots, video) are not in git.

## Running it

- `harness.py`: task registry, widget servers, browser session, raw bundle capture, scoring.
- `run_one.sh` (Claude Code), `muse_one.sh` (Muse Code), `codex_one.sh` (Codex CLI), `agy_one.sh` (Antigravity): one task on one configuration.
- `v2_iter2.sh`, `v2_pass2.py`, `v2_validated.py`: the pass@2 validation loop used to build the set.
- The matrix ran on AWS, one run per instance: [`matrix_queue.py`](matrix_queue.py) (S3 work queue with leased items, resumable and idempotent), [`run_worker.sh`](run_worker.sh) (per-instance worker with a provider family and an optional run cap), [`judge_daemon.py`](judge_daemon.py) (judges live-site runs as they land), [`matrix_dashboard.py`](matrix_dashboard.py) (localhost status page), [`aws/fleet.sh`](aws/fleet.sh) and [`aws/README.md`](aws/README.md).
- [`make_v2_site.py`](make_v2_site.py) produces the data for the results page.

`legacy/` keeps the v1 sweep scripts and the per-round pilot scripts for provenance.
