# web-bench

A benchmark for **how efficiently an LLM drives a browser** on real websites. Every configuration
gets the same browser tool and the same task set on live sites; the benchmark measures the **cost
of success**, time, tokens, tool calls, and dollars per task.

The suite is **44 live-validated tasks** spanning reading, e-commerce, vision and canvas work,
signed-in productivity, and interactive web tools. Candidate tasks were culled during validation
under three design rules: no task whose outcome is one clean API call for a connected agent, no
task whose pass/fail hinges on puzzle or pretraining knowledge rather than browsing skill, and no
task dominated by bot walls across configurations. Task directory numbers are stable identifiers,
so the numbering has gaps where culled candidates used to sit. One task was culled after the
full matrix ran: an Amazon compound-filter hunt whose accumulated page context requires a single
API request larger than common provider rate tiers permit (a 200k tokens-per-minute tier rejects
its ~204-220k-token requests outright), making it undeliverable to some providers for account-tier
reasons unrelated to browsing skill.

## Results (full matrix, 2026-08-29 to 2026-09-02)

**28 configurations x 44 tasks = 1,232 runs, all judged, pass@1.** Six model families: **Claude
Opus 5, Sonnet 5, and Haiku 4.5** via Claude Code, **Gemini 3.7 Flash** (its three levels)
via Antigravity, **GPT-5.6 Luna** via the Codex CLI, and **Muse Spark 1.2** via Muse Code. Opus, Sonnet, Luna, and Spark swept five thinking levels each (Spark's scale
tops out at `ultra` rather than `max`). Haiku 4.5 does not support the
effort parameter (Claude Code silently ignores `--effort` on it; run telemetry confirms zero
dose-response in thinking volume, turns, or time), so its five sweeps are replicate runs of one
configuration and are reported below as a single averaged row. Every run used the same browser tool
([browser-automation-cli](https://github.com/jshan9078/browser-automation-cli)), no turn or time cap, and ran serially on one dedicated machine (M4, 10 cores). Every LLM-judged verdict was
issued by a Claude Sonnet judge from captured evidence (screenshots, full traces, cart/end-state
ground truth), with a hostile second-opinion audit over every contested failure. Truth is
evaluated at capture time: these are live sites, and the same question can have different correct
answers an hour apart.

| model | thinking | pass | rate | median time | median cost |
|---|---|---|---|---|---|
| Haiku 4.5 | n/a (5 replicate sweeps) | 153/220 | 69.5% | 51s | $0.198 |
| Gemini 3.7 Flash | low | 42/44 | 95.5% | 26s | $0.117 |
| Gemini 3.7 Flash | medium | 44/44 | 100.0% | 45s | $0.254 |
| Gemini 3.7 Flash | high | 43/44 | 97.7% | 35s | $0.187 |
| GPT-5.6 Luna | low | 36/43 | 83.7% | 30s | $0.014 |
| GPT-5.6 Luna | medium | 38/43 | 88.4% | 40s | $0.016 |
| GPT-5.6 Luna | high | 37/44 | 84.1% | 49s | $0.022 |
| GPT-5.6 Luna | xhigh | 42/44 | 95.5% | 66s | $0.023 |
| GPT-5.6 Luna | max | 40/43 | 93.0% | 101s | $0.030 |
| Muse Spark 1.2 | low | 43/44 | 97.7% | 52s | $0.156 |
| Muse Spark 1.2 | medium | 40/44 | 90.9% | 69s | $0.215 |
| Muse Spark 1.2 | high | 43/44 | 97.7% | 80s | $0.222 |
| Muse Spark 1.2 | xhigh | 43/44 | 97.7% | 65s | $0.254 |
| Muse Spark 1.2 | ultra | 44/44 | 100.0% | 80s | $0.280 |
| Sonnet 5 | low | 43/44 | 97.7% | 21s | $0.313 |
| Sonnet 5 | medium | 41/44 | 93.2% | 27s | $0.393 |
| Sonnet 5 | high | 41/44 | 93.2% | 39s | $0.454 |
| Sonnet 5 | xhigh | 43/44 | 97.7% | 44s | $0.511 |
| Sonnet 5 | max | 42/44 | 95.5% | 60s | $0.594 |
| Opus 5 | low | 43/44 | 97.7% | 31s | $0.403 |
| Opus 5 | medium | 43/44 | 97.7% | 39s | $0.508 |
| Opus 5 | high | 44/44 | 100.0% | 55s | $0.583 |
| Opus 5 | xhigh | 42/44 | 95.5% | 67s | $0.685 |
| Opus 5 | max | 43/44 | 97.7% | 95s | $0.842 |

Claude costs are the CLI's own reported `total_cost_usd` per run; Gemini costs are computed from
each run's measured token split at the introductory pricing in effect ($0.75/M input, $3.75/M
output including thinking, $0.075/M cache read; these rates double on 2027-01-01). Luna costs
use OpenAI's published rates including the promotional 80% cut ($0.20/M input, $0.02/M cached,
$0.25/M cache write, $1.20/M output). Muse Spark costs use Meta's list rates ($1.25/M input,
$0.15/M cached, $4.25/M output); the three Luna cells shown /43 are verified bot walls
(hCaptcha, a sign-in wall), excluded per the wall policy rather than scored as failures.

### What excelled where

- **Muse Spark 1.2 is the most consistent family in the matrix.** It holds 97.7% at nearly
  every tier, and spark-ultra posted a perfect 44/44 — one of only three perfect configurations
  — at $0.28 median, roughly half of what any Claude tier costs and in the same band as
  Gemini. Zero bot walls across its 220 runs, and per-call cache hit rates of 85-99% keep even
  its six-thousand-token reasoning tiers economical.
- **GPT-5.6 Luna is the cost frontier, and the one family where thinking bought accuracy.**
  At $0.014-0.030 per task it undercuts everything else by an order of magnitude, and it
  climbs from 83.7% at low to 95.5% at xhigh with reasoning telemetry rising in lockstep — the
  clearest effort dose-response in the matrix — though from a lower floor: its low tiers make
  careless errors the other families' low tiers don't.
- **Gemini 3.7 Flash is the speed-efficiency frontier.** Its low tier is the fastest cheap
  config in the matrix (26s, $0.117, 95.5%) and its medium tier posted a perfect 44/44. It was the
  only family to reliably clear the two hardest interaction tasks (the Desmos math-input editor
  and JS Paint under a no-GPU WebGL error dialog) at every level, suggesting its agent harness
  paces keystroke-heavy widget input better than the Claude-side agents.
- **Opus 5 is the accuracy frontier, and its LOW tier is its best value.** Opus-low hit 43/44 at
  a third of opus-max's time and half its cost, beating every trap in the suite: the arXiv
  first-mention scan, live departure-board timing, date discipline on UTC sites. Opus never
  produced a careless factual error; its only failures were running out of turns on
  interaction-dense tasks while over-verifying.
- **Sonnet 5 is the speed frontier.** Sonnet-low's 21s median is the fastest config in the
  matrix at 97.7%, making it the best latency-sensitive pick.
- **Haiku 4.5 is the cautionary tale.** Its five sweeps (64-73% each, binomial noise around the
  69.5% pooled rate) double as a run-to-run variance estimate for the suite, and its failures
  are browsing discipline, not reasoning budget. Recurring patterns, invariant across
  tiers: trusting URL parameters instead of the page's own state (an invalid IMDb sort parameter
  silently fell back to popularity order at every tier), accepting the first search autocomplete
  without verifying it (OSM resolved "St. Lawrence Market" to Union Station five times out of
  five), assuming dates from memory instead of reading the highlighted row, and claiming actions
  (cart adds, bookmarks) that ground-truth screenshots show never happened.

### Shortcomings and lessons

- **More thinking buys little browsing accuracy.** The effort knob demonstrably worked where
  the model supports it (Opus and Sonnet scale monotonically from low to max: 2.4x output
  tokens, up to 2x tool calls, 3x wall time), yet accuracy moves only a point or two across
  levels (Opus 97.8-100%, Sonnet 93.3-97.8%), well inside per-cell noise. What thinking mostly
  buys is patience: given no turn cap, higher tiers grind out the hardest interaction tasks
  slowly rather than failing them, so the cost of thinking shows up in the time and dollar
  columns, not the score column. Luna is the exception (a real 83.7% to 95.5% climb), and
  Spark's knob saturates: its reasoning volume plateaus between xhigh and ultra even as ultra
  cleaned up the family's last failure.
- **Widget input is hard but tractable given patience.** The tasks demanding sustained precise
  input into canvas/custom editors (Desmos, JS Paint) account for most non-Haiku failures.
  Uncapped, Opus and Sonnet solve the Desmos math-input task at every level (some runs grinding
  5-22 minutes to produce the rendered coordinate label); JS Paint under its no-GPU WebGL error
  dialog remains the suite's least-solved interaction task.
- **Anti-bot walls are an environment fact.** Walls are never scored as failures here: agents
  declare `BLOCKED`, judges verify the wall from the trace, and such runs are excluded and
  retried (interactively if needed). During validation this rule removed one task entirely
  (Walmart, walled on every config) and taught a prompt lesson now in the preamble: soft
  "checking your browser" interstitials clear on their own in about ten seconds, so agents wait
  and retry once before declaring a wall.
- **Grounding enforcement caught real fabrications.** Judges failed runs whose confident answers
  contradicted their own captured evidence, including an agent reporting a two-item cart while
  the harness's cart screenshot showed it empty.

Results are published under [`results/`](results/), one directory per task with one file per
configuration (`results/<task>/<config>.json`, plus that run's CPU series alongside). Raw run
artifacts (videos, full traces, screenshots) stay local and git-ignored.

## Tasks

| task | kind | site | what it tests |
|---|---|---|---|
| `01-mlb-latest` | read | ESPN / MLB (agent's choice) | latest scores, then drill into the Cubs box score for run-scorers |
| `02-hn-summary` | read | news.ycombinator.com | read the front page and synthesize a themed digest with an agents section |
| `03-weather-nyc` | read | forecast.weather.gov | navigate to the current NYC (Central Park) forecast |
| `04-x-projects` | read | x.com profile + a linked article | multi-hop: profile, then project links, then read the SLM article |
| `05-amazon-cart` | action | amazon.ca | open two product pages and add both to the cart |
| `06-amazon-search-add` | action | amazon.ca | search, open the first genuine result, add to cart |
| `07-pixel-click` | action (state) | local canvas app (127.0.0.1:8791) | vision + raw-pixel clicking: screenshot, then click circles in ascending order |
| `08-airport-departures` | read | flightaware.com | live departures board: find, filter, and read structured flight data |
| `09-recipe-scaling` | read + arithmetic | allrecipes.com | search, filter by rating/review volume, then scale ingredient quantities |
| `10-arxiv-agents-paper` | read | arxiv.org | navigate a daily listing, select by content, read an abstract |
| `11-github-trending-audit` | read | github.com | trending discovery plus repo metadata drill-down across tabs |
| `12-wikipedia-current-events` | read | en.wikipedia.org | portal navigation for date-specific current events |
| `13-usgs-quake-report` | read | earthquake.usgs.gov | interactive data map/list filtering and event-page reading |
| `14-imdb-yearly-top` | read | imdb.com | advanced search with multiple constraints, then a person-page pivot |
| `15-stock-analyst-targets` | read | finance.yahoo.com | quote page reading plus a tab pivot for analyst data |
| `17-currency-meal-budget` | read + arithmetic, cross-site | xe.com + numbeo.com | cross-site data gathering with a computation joining the two |
| `18-npm-package-audit` | read, cross-site | npmjs.com + github.com | registry metadata reading plus a repository pivot |
| `19-wiktionary-wotd` | read | en.wiktionary.org | locating a daily-rotating feature and reading a structured dictionary entry |
| `20-nasa-apod-vision` | read + vision | apod.nasa.gov | reading a daily page plus genuinely describing an image from a screenshot |
| `21-amazon-office-bundle` | action + cart | amazon.ca | multi-item constrained shopping, budget arithmetic, cart verification |
| `22-amazon-earbud-compare` | action + cart | amazon.ca | comparing two live product pages on price, rating, and a spec before acting |
| `26-ebay-keyboard-hunt` | action | ebay.ca | marketplace filtering on price/format/seller quality before acting |
| `27-amazon-review-mining` | read | amazon.ca | review filtering and synthesis of recurring complaints from recent reviews |
| `29-excalidraw-pipeline` | action + vision + pixel | excalidraw.com | canvas toolbar use, pixel-placed text elements, screenshot proof |
| `32-desmos-intersections` | action + vision | desmos.com | plotting expressions, then reading tool-computed intersection coordinates |
| `33-osm-street-read` | read + vision | openstreetmap.org | map search, zooming, and reading street names off rendered map tiles |
| `34-osm-route-measure` | read + vision | openstreetmap.org | using a routing widget and reading live-computed distance/time plus the drawn route |
| `36-jspaint-poster` | action + vision + pixel | jspaint.app | palette and tool selection by pixel clicks, flood fill, text typed onto a canvas |
| `39-youtube-frame-describe` | read + vision | youtube.com | finding a channel's newest upload and visually describing a paused frame |
| `40-arxiv-pdf-figure` | read + vision | arxiv.org | opening a fresh PDF in the browser and reading it visually via screenshots |
| `41-owid-dataset-read` | read | ourworldindata.org | interactive chart manipulation and reading the latest datapoint from the tool |
| `42-youtube-watch-later` | signed-in action | youtube.com | menu-driven playlist state change on the user's account, then verification |
| `43-gmail-self-draft` | signed-in action, cross-site | mail.google.com + news.ycombinator.com | composing and saving (not sending) a draft whose content requires live cross-site research |
| `44-gcal-event` | signed-in action | calendar.google.com | date navigation and event creation with fields, then visual verification |
| `47-reddit-save` | signed-in action | reddit.com | feed sorting, a private save action, and verification in the saved list |
| `48-spotify-playlist` | signed-in action | open.spotify.com | playlist creation, search, and adding a track in a web player |
| `49-x-bookmark` | signed-in action | x.com | reading a live timeline and using a private bookmark action, then verifying |
| `50-google-flights-nonstop` | read | google.com/travel/flights | date pickers, round-trip configuration, filtering, and reading live fares |
| `51-wikipedia-revision-audit` | read | en.wikipedia.org | article history inspection: who edited what, when |
| `53-caniuse-feature` | read | caniuse.com | reading live support tables and usage statistics |
| `54-stackoverflow-live` | read | stackoverflow.com | live feed reading: the newest activity in a tag |
| `55-wayback-snapshot` | read + vision | web.archive.org | archive navigation to a dated snapshot and precise visual reading of it |
| `56-sunrise-reykjavik` | read | timeanddate.com | location lookup and reading precise, date-specific astronomical times |
| `57-hn-debate-analysis` | read | news.ycombinator.com | reading a live discussion thread and synthesizing opposing arguments |

Each task has its own directory under [`tasks/`](tasks/) with the verbatim `prompt.txt` (the
runtime source), a `task.md` (kind, site, what it tests, verdict), and a `verifier.md` explaining
exactly how the run is scored. Every prompt carries a navigate-don't-recall instruction, every run
captures full evidence before judging, and every verifier enforces grounding (a correct-sounding
answer with no supporting navigation in the trace fails). Tasks are deliberately
pretraining-proof: they target live data (prices, feeds, schedules, rankings), account-private
state, or state the agent must create and screenshot. `07-pixel-click` is checked programmatically
by its canvas server; all other tasks are graded by an LLM judge offline from the captured
evidence.

Signed-in tasks (the 42-49 range) assume the browser profile is already authenticated; agents are
instructed never to handle credentials (the user signs in through a visible window). Action tasks
may add items to carts but never check out, and account changes are private and reversible
(drafts saved not sent, bookmarks, saves, playlists), created, screenshotted, then undone by the
run itself.

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
| `tasks/<NN-name>/` | one directory per task (numbering has gaps by design): `prompt.txt` (source of truth), `task.md`, `verifier.md` |
| `harness.py` | runner, offline scoring, and the report table (loads prompts from `tasks/`) |
| `run_matrix.sh`, `run_one.sh`, `agy_one.sh` | run scripts (Claude via `claude -p`, Gemini via `agy -p`) |
| `record_cdp.py` | headless CDP screencast recorder (per-run video) |
| `pixelapp/` | the local canvas app for `pixel_click` |
| `dashboard.py` | builds an HTML results dashboard from `results/` |
| `results/<task>/` | published results, one file per configuration (`<config>.json` + `<config>.cpu.jsonl`) |
| `raw/` | local run artifacts, traces, videos, screenshots (git-ignored) |
