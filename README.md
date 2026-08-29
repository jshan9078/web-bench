# web-bench

A benchmark for **how efficiently an LLM drives a browser** on real websites. Every configuration
gets the same browser tool and the same task set on live sites; the benchmark measures the **cost
of success**, time, tokens, tool calls, and dollars per task.

The suite is **57 tasks**: the original scored seven (`01`-`07`) plus fifty extended tasks
(`08`-`57`), all live-validated. Scored so far: 18 configurations, **Claude** (Opus 5 / Sonnet 5 /
Haiku 4.5 across five thinking levels) via Claude Code and **Gemini 3.7 Flash** (three levels) via
Antigravity, over tasks 01-07 at pass@1.

## Results

Every configuration passed all seven original tasks (01-07), so the axes are **time vs cost**:
the efficiency frontier. The extended set (08-57) is not scored yet.

![cost vs time per configuration](docs/webbench-graph.png)

![results table](docs/webbench-table.png)

Results are published under [`results/`](results/), one directory per task with one file per
configuration (`results/<task>/<config>.json`, plus that run's CPU series alongside); `cost` is
derived from measured token usage (input, output, cache) at each model's public pricing.

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

Fifty additional tasks expand the suite beyond the original seven (now numbered 01-07), under the same rules: every
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
