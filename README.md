# web-bench

A benchmark for **how efficiently an LLM drives a browser** on real websites. Every configuration
gets the same browser tool and the same task set on live sites; the benchmark measures the **cost
of success**, time, tokens, tool calls, and dollars per task.

The suite is **45 tasks**: the original scored seven (`01`-`07`) plus the extended set
(`08`-`57`, with numbering gaps), all live-validated. Twelve extended tasks were removed after
validation under three design rules: tasks whose outcome is one clean API call (16-transit,
35-gmaps-traffic, 37-gmaps-poi, 45-gdocs, 46-gmaps-save), tasks whose pass/fail hinges on
puzzle or pretraining knowledge rather than browsing skill (30-lichess, 31-wordle, 38-seterra,
52-regex101), and tasks dominated by bot walls across configurations (25-walmart, blocked on all configs; 24-bestbuy and 28-price-cross-check, Akamai-walled on most).
Directory numbers are stable identifiers, so gaps are intentional.

## Results (full matrix, 2026-08-29/30)

**18 configurations x 45 tasks = 810 runs, all judged, pass@1.** Four model families: **Claude
Opus 5, Sonnet 5, and Haiku 4.5** (five thinking levels each) via Claude Code, and **Gemini 3.7
Flash** (its three levels) via Antigravity. Every run used the same browser tool
([browser-automation-cli](https://github.com/jshan9078/browser-automation-cli)), the same 60-turn
budget, and ran serially on one dedicated machine (M4, 10 cores). Every LLM-judged verdict was
issued by a Claude Sonnet judge from captured evidence (screenshots, full traces, cart/end-state
ground truth), with a hostile second-opinion audit over every contested failure. Truth is
evaluated at capture time: these are live sites, and the same question can have different correct
answers an hour apart.

| model | thinking | pass | rate | median time | median cost |
|---|---|---|---|---|---|
| Haiku 4.5 | low | 31/45 | 68.9% | 64s | $0.224 |
| Haiku 4.5 | medium | 28/45 | 62.2% | 51s | $0.210 |
| Haiku 4.5 | high | 32/45 | 71.1% | 52s | $0.203 |
| Haiku 4.5 | xhigh | 30/45 | 66.7% | 45s | $0.207 |
| Haiku 4.5 | max | 31/45 | 68.9% | 56s | $0.171 |
| Gemini 3.7 Flash | low | 43/45 | 95.6% | 26s | $0.118 |
| Gemini 3.7 Flash | medium | 45/45 | 100.0% | 46s | $0.237 |
| Gemini 3.7 Flash | high | 44/45 | 97.8% | 35s | $0.176 |
| Sonnet 5 | low | 43/45 | 95.6% | 23s | $0.317 |
| Sonnet 5 | medium | 41/45 | 91.1% | 27s | $0.395 |
| Sonnet 5 | high | 41/45 | 91.1% | 40s | $0.459 |
| Sonnet 5 | xhigh | 43/45 | 95.6% | 44s | $0.553 |
| Sonnet 5 | max | 41/45 | 91.1% | 62s | $0.633 |
| Opus 5 | low | 44/45 | 97.8% | 31s | $0.405 |
| Opus 5 | medium | 44/45 | 97.8% | 42s | $0.528 |
| Opus 5 | high | 43/45 | 95.6% | 59s | $0.598 |
| Opus 5 | xhigh | 42/45 | 93.3% | 76s | $0.688 |
| Opus 5 | max | 43/45 | 95.6% | 96s | $0.843 |

Claude costs are the CLI's own reported `total_cost_usd` per run; Gemini costs are computed from
each run's measured token split at the introductory pricing in effect ($0.75/M input, $3.75/M
output including thinking, $0.075/M cache read; these rates double on 2027-01-01).

### What excelled where

- **Gemini 3.7 Flash is the efficiency frontier.** Its low tier is the fastest cheap config in
  the matrix (26s, $0.118, 95.6%) and its medium tier posted the only perfect 45/45. It was the
  only family to reliably clear the two hardest interaction tasks (the Desmos math-input editor
  and JS Paint under a no-GPU WebGL error dialog) at every level, suggesting its agent harness
  paces keystroke-heavy widget input better than the Claude-side agents.
- **Opus 5 is the accuracy frontier, and its LOW tier is its best value.** Opus-low hit 44/45 at
  a third of opus-max's time and half its cost, beating every trap in the suite: the arXiv
  first-mention scan, live departure-board timing, date discipline on UTC sites. Opus never
  produced a careless factual error; its only failures were running out of turns on
  interaction-dense tasks while over-verifying.
- **Sonnet 5 is the speed frontier.** Sonnet-low's 23s median is the fastest config in the
  matrix at 95.6%, making it the best latency-sensitive pick.
- **Haiku 4.5 is the cautionary tale.** A flat 62-71% band across ALL five thinking levels: its
  failures are browsing discipline, not reasoning budget. Recurring patterns, invariant across
  tiers: trusting URL parameters instead of the page's own state (an invalid IMDb sort parameter
  silently fell back to popularity order at every tier), accepting the first search autocomplete
  without verifying it (OSM resolved "St. Lawrence Market" to Union Station five times out of
  five), assuming dates from memory instead of reading the highlighted row, and claiming actions
  (cart adds, bookmarks) that ground-truth screenshots show never happened.

### Shortcomings and lessons

- **More thinking does not buy better browsing.** No family shows a positive accuracy slope with
  thinking level; Opus and Sonnet peak at low. Fifteen of the 23 upper-tier Claude failures were
  60-turn budget exhaustion on keystroke-heavy widget tasks: higher tiers spend turns
  re-verifying where low tiers act, an over-verification tax. Opus-low passed the Desmos task
  that all four higher Opus tiers timed out on.
- **Widget input is the open frontier.** The three tasks demanding sustained precise input into
  canvas/custom editors (Desmos, JS Paint, and eBay's flow for some tiers) account for most
  non-Haiku failures matrix-wide.
- **Anti-bot walls are an environment fact.** Walls are never scored as failures here: agents
  declare `BLOCKED`, judges verify the wall from the trace, and such runs are excluded and
  retried (interactively if needed). During validation this rule removed one task entirely
  (Walmart, walled on every config) and taught a prompt lesson now in the preamble: soft
  "checking your browser" interstitials clear on their own in about ten seconds, so agents wait
  and retry once before declaring a wall.
- **Grounding enforcement caught real fabrications.** Judges failed runs whose confident answers
  contradicted their own captured evidence, including an agent reporting a two-item cart while
  the harness's cart screenshot showed it empty.

The original seven-task pilot (time/cost frontier across the same 18 configurations) is preserved
in [`docs/`](docs/): ![cost vs time per configuration](docs/webbench-graph.png)

Results are published under [`results/`](results/), one directory per task with one file per
configuration (`results/<task>/<config>.json`, plus that run's CPU series alongside). Raw run
artifacts (videos, full traces, screenshots) stay local and git-ignored.

## Tasks

| task | kind | site | what it tests |
|---|---|---|---|
| `01-mlb-latest` | read | ESPN / MLB | latest scores, then drill into a box score |
| `02-hn-summary` | read | Hacker News | read the front page and synthesize a themed digest |
| `03-weather-nyc` | read | weather.gov | navigate to a current forecast |
| `04-x-projects` | read | x.com + linked article | multi-hop: profile → project links → read an article |
| `05-amazon-cart` | action | amazon.ca | open two products → add both to cart |
| `06-amazon-search-add` | action | amazon.ca | search → open a result → add to cart |
| `07-pixel-click` | action | local canvas | vision + raw-pixel clicking (`click --at X,Y`) |

Each task has its own directory under [`tasks/`](tasks/) with the verbatim `prompt.txt` (the runtime
source), a `task.md` (kind, site, what it tests, verdict), and a `verifier.md` explaining exactly how the
run is scored. Read tasks target **current** data (unanswerable from training, the agent must navigate
and read); `pixel_click` is checked programmatically by the canvas server, and the rest are graded by an
LLM judge (Claude) offline from the captured evidence.

## Extended task set (08-57)

The extended set expands the suite beyond the original seven (now numbered 01-07): fifty tasks were
authored and live-validated, of which thirty-eight remain after the design-rule removals above. All
run under the same rules: every
prompt carries the navigate-don't-recall instruction, every run captures full evidence before
judging, and every verifier enforces grounding (a correct-sounding answer with no supporting
navigation in the trace fails). Tasks are deliberately pretraining-proof: they target live data
(prices, feeds, schedules, rankings), account-private state, or state the agent must create and
screenshot. Each task directory (`tasks/NN-name/`) holds its `prompt.txt`, `task.md`, and
`verifier.md`.

| range | theme | techniques |
|---|---|---|
| 08-20 | multi-hop research over live data (flights, quakes, markets, arXiv, transit) | DOM navigation, cross-site reads, arithmetic |
| 21-28 | e-commerce: constrained shopping, comparisons, review mining | filters, sorting, carts (no checkout), cross-retailer checks |
| 29-41 | vision, canvas, and pixel work (drawing, chess, maps, PDFs, charts, games) | screenshots, `click --at X,Y`, keyboard play, visual reading |
| 42-49 | signed-in productivity on the user's profile (YouTube, Gmail, Calendar, Docs, Maps, Reddit, Spotify, X) | private, reversible account state: drafts, saves, bookmarks, playlists |
| 50-57 | live web utilities and widgets (flights, revision history, regex tool, caniuse, Wayback, sun times, HN threads) | date pickers, interactive tools, tables, archives |

Signed-in tasks assume the browser profile is already authenticated; agents are instructed never
to handle credentials (the user signs in through a visible window). Action tasks may add items to
carts but never check out, and account changes are private and reversible (drafts saved not sent,
bookmarks, saves, playlists).

## Methodology

- **Capture-first.** Each run writes a durable raw bundle, full model trace, end-state evidence,
  screenshots, token usage, and a headless video, *before* any judging, so verdicts can be re-derived
  offline without ever re-running the models.
- **Held constant.** Same tasks, same browser tool, same session setup, same turn limit across every
  configuration; only the model, thinking level, and the harness exposing it vary.
- **Repeatable.** Every task starts fresh on any rerun: non-signed-in tasks run in throwaway
  ephemeral browser contexts (site state dies with the session), Amazon cart tasks begin from a
  harness-cleared cart (with before/after snapshots as the judging backstop), and signed-in tasks
  (42-49) both remove any residue at the start and undo their own created state after the
  verification screenshot, with the undo required by the verifier.
- **Pretraining-proof.** Current-data reads + state-change verification + a navigate-don't-recall
  instruction in every prompt, with every browser call captured (an answer with no navigation fails).
- **Bot walls are not failures.** A CAPTCHA, robot check, or forced re-login is an environment
  condition, not a model error. The agent is instructed never to bypass one: it makes the window
  visible, tells the user what to solve, and ends with `BLOCKED: <wall>`. Such runs score as
  `BLKD`, excluded from pass/fail entirely (the judge confirms the wall from the video/trace and
  can override a bogus claim to FAIL). Blocked runs are rerun interactively (`BENCH_VISIBLE=1`)
  with the user present to clear the wall.

## Running it

Needs the `browser` CLI ([browser-automation-cli](https://github.com/jshan9078/browser-automation-cli),
the fixed browser tool) plus the Claude and/or Antigravity CLI. Put a `CLAUDE_CODE_OAUTH_TOKEN` in a
`.env` at the repo root.

```bash
uv tool install browser-automation-cli   # the browser tool under test
python3 harness.py tasks                 # list tasks + prompts
./run_matrix.sh                          # run the full matrix (captures raw bundles)
python3 harness.py score                 # derive metrics into results/
python3 harness.py report                # print the results table
```

## Layout

| path | what it is |
|---|---|
| `tasks/<NN-name>/` | one directory per task (numbered 01-57): `prompt.txt` (source of truth), `task.md`, `verifier.md` |
| `harness.py` | runner, offline scoring, and the report table (loads prompts from `tasks/`) |
| `run_matrix.sh`, `run_one.sh`, `agy_one.sh` | run scripts (Claude via `claude -p`, Gemini via `agy -p`) |
| `record_cdp.py` | headless CDP screencast recorder (per-run video) |
| `pixelapp/` | the local canvas app for `pixel_click` |
| `dashboard.py` | builds an HTML results dashboard from `results/` |
| `results/<task>/` | published results, one file per configuration (`<config>.json` + `<config>.cpu.jsonl`) |
| `raw/` | local run artifacts, traces, videos, screenshots (git-ignored) |
