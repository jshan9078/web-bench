# web-bench — model × thinking-level × CLI comparison on real sites

> Standalone benchmark repo. It drives [**browser-automation-cli**](https://github.com/jshan9078/browser-automation-cli)
> (the `browser` CLI + daemon) as the browser tool — install that first (`uv tool install browser-automation-cli`).
> A snapshot of its `SKILL.md` is bundled here so the harness is runnable on its own.

Compares agents driving the **same** `browser` CLI + skill on realistic tasks against **real external
sites**. Tasks test navigation over real-world data and are designed to be **pretraining-proof** —
current-data reads (judged by LLM from captured evidence) plus state-changing actions (see Tasks).
Matrix:

- **Claude** `{opus, sonnet, haiku}` × effort `{low, medium, high, xhigh, max}` = **15 configs** — via
  `claude -p --effort <level>`, loading the real `/browser-cli` skill. (opus→Opus 5, sonnet→Sonnet 5,
  haiku→Haiku 4.5.)
- **Antigravity** `gemini-3.7-flash-{low,medium,high}` = **3 configs** — via `agy -p --model <slug>`
  (reads `SKILL.md`, since agy can't load a Claude skill). Requires agy ≥ v1.1.20 (3.7 tier). Override
  with `AGY_MODELS="..."`.

**18 configs × 7 tasks × 1 attempt (pass@1) = 126 runs.**

## Capture-first: never re-run models to re-verify

Every run writes a durable **raw bundle** *before* any judging:

```
raw/<task>.<run>.json        # full model trace ptr, EVERY browser command (from the daemon log),
                             # end-state evidence (url/text/snapshot; cart contents for cart tasks),
                             # CPU/RSS series, raw token usage, the extracted answer, video_file
raw/<task>.<run>.stream.txt  # the complete model stream (every step + tool call/output)
raw/<task>.<run>.mp4         # headless video of the run (CDP screencast — see below)
raw/<task>.<run>.cart_before.jpg / .cart_after.jpg   # cart tasks: cart screenshots (empty→after adds)
```

Scoring is a **separate, re-runnable** step:

```bash
python3 harness.py score          # re-derive metrics + mark runs pending-judge, into results/
```

Change how you judge later → just re-run `score` / re-`set_verdict`. You never re-run the models. All
evidence (answer, full trace, end-state, cart screenshot) is captured, so judging is fully offline.

## Tasks (`python3 harness.py tasks`)

Every task tests **navigation over real-world data** — the challenge is finding and reading the right
pages (a task may take several steps: open a box score, follow a project link, read an article), not
solving a reasoning puzzle. **Every task is graded by LLM-as-judge** (no deterministic checks — models
have different output styles, so a hardcoded matcher would unfairly penalize wording). The suite is a
deliberate mix:

- **Read-only tasks** target **current** real-world data that cannot be in any training set, so the
  model can't answer from memory — it must navigate and read. The judge rules from the captured
  evidence (answer + page text + full trace) and confirms the answer came from the page, not memory.
- **Action tasks** require doing something (add to cart). The harness captures a **screenshot of the
  cart** plus the action trace; the judge rules from the picture + what the agent actually did this run
  (so leftover cart items from earlier runs can't create a false pass).

> **On "pretrained knowledge":** you can't strip a model's weights, and `claude -p` / `agy -p` already
> run with a fresh context each time. So immunity comes from the tasks themselves — current data +
> state-change verification + the navigate-don't-recall instruction in every prompt + the fact that we
> capture every browser call (an answer with no navigation to the source fails the judge).

| task | kind | site | what it tests | verdict |
|---|---|---|---|---|
| `mlb_latest` | read (LLM-judge) | ESPN / MLB (agent's choice) | scores + drill into the Cubs box score | judge: games/scores + Cubs run-scorers match the pages |
| `hn_summary` | read (LLM-judge) | news.ycombinator.com | read the front page + synthesize a themed digest | judge: summary reflects real front-page stories; has an agents section |
| `weather_nyc` | read (LLM-judge) | forecast.weather.gov | navigate to a current forecast | judge: conditions/temps match the page |
| `x_projects` | read (LLM-judge) | x.com/jshan9078 + linked article | multi-hop: profile → project links → read SLM article | judge: projects+links present & benchmarked models match the article |
| `amazon_cart` | action (LLM-judge) | amazon.ca | open 2 product pages → Add to Cart | judge: cart screenshot shows both books + trace shows the adds |
| `amazon_search_add` | action (LLM-judge) | amazon.ca | search → open result → Add to Cart | judge: cart screenshot shows the item + trace shows search→add |
| `pixel_click` | action (state) | localhost canvas | **vision + pixel clicking**: screenshot → `click --at X,Y` | state: server confirms all circles clicked in ascending order |

### Exact prompts sent to the agent

Each run's full prompt is: a **leading line** + the **shared preamble** + `TASK:` + the per-task text
below. The leading line is `/browser-cli` for Claude (loads the shipped skill) or, for agy,
`First, read the browser CLI reference at <repo>/SKILL.md …`. The shared preamble (with `{sid}` and
`{mode}` filled in at runtime) is:

```
A browser session ALREADY EXISTS for you: its id is `{sid}`. Drive it with `browser {sid} <command>`.
Do NOT create or delete sessions. The session is {mode}. Interact through the UI like a person — do not
sign up, enter payment details, or place/confirm any order; decline cookie/consent banners (reject
non-essential). IMPORTANT: answer ONLY from what you actually navigate to and read on the page RIGHT NOW
— do not answer from prior knowledge; if you didn't see it on the page, go find it. When done, reply with
a concise summary of what you found, and if asked for a value make the LAST line exactly `ANSWER: <value>`.
```

Per-task `TASK:` text (verbatim from `TASKS` in `harness.py`):

**`mlb_latest`**
```
Find the results of the latest completed MLB game day (yesterday's games). For each game, report the two teams and the final score. THEN, for the Chicago Cubs' most recent game, open its box score and list every Cubs player who scored a run (the Cubs' scorers). On Chrome, just searching mlb shows the scores; open the Cubs game for the box score. Base your answer only on what the pages show. End with (1) the list of games and scores, and (2) the Cubs' scorers.
```

**`hn_summary`**
```
Open Hacker News (https://news.ycombinator.com) and read the current front page. Write a concise summary of what's on the front page right now, grouping the notable stories by theme. Include a DEDICATED section titled 'Agents / agentic harnesses' listing any front-page stories about AI agents, agentic coding tools/harnesses, or LLM tool-use (give their titles); if there are none, say so explicitly. Base your summary only on the stories actually shown on the page (you may open a story or its comments to clarify). End with the themed summary including that dedicated section.
```

**`weather_nyc`**
```
Using the U.S. National Weather Service site (https://forecast.weather.gov), find the current forecast
for New York, NY (Central Park). Report today's forecasted conditions and high/low temperature as shown
on the page.
```

**`x_projects`**
```
Open the X (Twitter) profile at https://x.com/jshan9078. Based on what's shown there (bio, pinned post, posts) and the links it points to, produce: (1) a list of ALL the projects this person has built or worked on, (2) a direct link to each project, and (3) for the on-device SLM vulnerability-detection research project specifically, which models were benchmarked — you will likely need to open that project's article/blog link and read it. Base your answer only on what you actually read on the pages. End with the project list (name + link each) and, for the SLM research, the list of benchmarked models.
```

**`amazon_cart`**
```
Add BOTH of these Amazon products to the cart, quantity 1 each:
  1. https://www.amazon.ca/dp/0735211299
  2. https://www.amazon.ca/dp/0132350882
For each: open the product page and click 'Add to Cart'. If any upsell pop-up appears (warranty, subscription, audiobook/Kindle, 'protect your purchase'), dismiss it (no thanks / skip). When done, open the cart so both items are visible. Do NOT proceed to checkout or place an order.
```

**`amazon_search_add`**
```
On Amazon (www.amazon.ca), use the search box to search for `stainless steel water bottle`. Open the first genuine product result, then click 'Add to Cart'. Dismiss any upsell pop-up (no thanks). When done, open the cart so the item is visible. Do NOT proceed to checkout or place an order.
```

**`pixel_click`** (needs the coord-click binary; state-verified, not LLM-judged)
```
Open http://127.0.0.1:8791/ . It shows several numbered colored circles rendered as an image — they are NOT in the DOM, so `snapshot`/`text`/`eval` reveal nothing. Take a `screenshot` to SEE the circles and their numbers, then CLICK them in ASCENDING numeric order (1, then 2, …) using raw pixel coordinates: `browser <sid> click --at X,Y` (the screenshot's pixels map 1:1 to click coordinates; the image is at the top-left origin). Take another screenshot to confirm if needed. Finish once you've clicked every circle in ascending order. Do NOT read the page source or call the site's HTTP API — interact visually.
```

### How verdicts are computed

**All read/cart tasks are `kind: judge`** (the one exception is `pixel_click`, which is state-verified server-side — objective pixel-hit checking). Otherwise — `score` records every run as **pending** (`needs_judge`) with no
automatic verdict; an LLM judges each one later from the captured evidence, and verdicts are stored
durably in `results/verdicts.json` (so re-running `score` keeps them). Nothing is matched
deterministically. (`cart` / `cart_any` / `answer` / `keywords` kinds still exist in the code for reuse
but aren't used by the current suite.)

Tasks flagged `cart: True` (the two Amazon tasks): the harness **empties the cart at setup** and saves a
**before** screenshot (`raw/<task>.<run>.cart_before.jpg`, an empty cart), then after the agent runs saves
an **after** screenshot (`…cart_after.jpg`) plus the cart page text. Filenames are harness-owned and keyed
to the unique run label, so runs never overwrite each other. The judge diffs before→after (plus the action
trace) — so leftover items can't cause a false pass, with no reliance on the agent to clear or name files.

### LLM-as-judge workflow (after the sweep)

```bash
python3 harness.py judge_manifest        # JSON: every pending run + its evidence (answer, end-state
                                         # text, end URL, #navigations, video/stream paths)
# review each, then record a verdict (re-scores that run automatically):
python3 harness.py set_verdict mlb_latest.gemini-3.7-flash-high pass "scores match ESPN page"
python3 harness.py set_verdict hn_summary.opus-low fail "summary lists stories not on the front page"
```

Judge from the **evidence**, not memory: check that the captured page text / stream actually supports
the answer and that the agent navigated to the source. `compare` counts pass@k over judged tasks only
and reports how many are still pending; the dashboard shows pending cells as `?`.

Each raw bundle carries everything a judge needs offline: `answer`, full `agent_result_text`, the
complete model `stream` (every tool call + output), `end_state` (url/title/text/snapshot),
`cart_evidence` for cart tasks, and the run `video`.

### `amazon_cart` details
Pinned by ASIN (`AMAZON_ITEMS` in `harness.py`: Atomic Habits `0735211299`, Clean Code `0132350882`).
Add-to-cart only — the prompt forbids checkout; the verifier reads the cart (state), never price, so
it's time-stable. Books are always in stock / unrestricted. Amazon may occasionally throw a bot-check;
per policy the agent won't solve CAPTCHAs, so such a run is *inconclusive*, not a model failure.

### Adding or changing a task
Edit the `TASKS` dict in `harness.py`: give a `prompt` and a `kind` (`judge` for LLM-judged reads,
`cart`/`cart_any` for actions, or the legacy `answer`+`expect`/`match` / `keywords`). `profile: True`
marks a task needing the logged-in profile. Because scoring reads captured evidence, you can change a
verifier and re-judge every past run with `python3 harness.py score` — never re-running models.

## One-time: sign in (amazon_cart + x_projects only)

```bash
browser create --show --profile bench   # log into amazon.ca and x.com in the window, then close it
export BENCH_PROFILE=bench
```

## Run the matrix — IN YOUR OWN TERMINAL

> **Claude auth (headless):** `claude -p` needs a long-lived token — the desktop app's OAuth can't
> refresh from a bare `claude -p` (`OAuth session expired`). Generate one with `claude setup-token` and
> put it in the **repo-root `.env`** as `CLAUDE_CODE_OAUTH_TOKEN=<token>` (legacy key `CLAUDE_KEY=` also
> accepted). The runners auto-load it. `.env` is gitignored — keep it that way.
> `--effort` needs Claude Code ≥ 2.1; the scripts prefer your PATH `claude` if it has `--effort`, else
> the newest installed app binary (which works once the token is set). Override with `CLAUDE_BIN`.
> **agy** uses its own cached login (`agy` interactive once).

```bash
export BENCH_PROFILE=bench
./run_matrix.sh 1            # 18 configs × 7 tasks × 1 attempt (pass@1) = 126 runs (Opus-at-max is the slow part)
python3 harness.py compare
python3 dashboard.py && open results/dashboard.html
```

Subsets while iterating:

```bash
SKIP_AGY=1 EFFORTS="low high max" ./run_matrix.sh 1     # Claude only, 3 effort levels, 1 attempt
SKIP_CLAUDE=1 ./run_matrix.sh 1                          # agy only
./run_one.sh mlb_latest haiku low haiku-low            # a single Claude run
./agy_one.sh mlb_latest gemini-3.7-flash-high gemini-3.7-flash-high   # a single agy run
```

### Resume & idempotency

`run_matrix.sh` is **resumable by default** (`RESUME=1`). Re-running it **skips any `(task, run)` that's
already complete** and only executes what's missing or failed — so a passing `gemini-3.7-flash-low`
won't run twice, and an interrupted overnight sweep continues where it left off. "Complete" means:

- **passed** (programmatic action tasks), or
- **captured and awaiting LLM judgment** (read tasks with real cli calls) — the data is saved; the
  verdict is applied later without re-running the model.

**Not** complete (so they retry on the next run): **empty** runs (0 cli calls, e.g. the Claude auth
failure above) and **programmatically-failed** runs. Each run overwrites its own `raw/` + `results/`
files by key, so re-running a single config is idempotent. Force everything to re-run with `RESUME=0`.

```bash
RESUME=0 ./run_matrix.sh 1      # ignore prior results, re-run every config
```

> So after we fix the Claude launch, just re-run the same `./run_matrix.sh` — it'll skip the agy runs
> that already succeeded and only (re)run the empty Claude ones.

### agy permissions

agy soft-denies shell commands in headless mode. `agy_one.sh` passes `--dangerously-skip-permissions`
by default (`AGY_SKIP_PERMS=1`) so the agent may run `browser`. To avoid that broad grant, add a scoped
rule to `~/.gemini/antigravity-cli/settings.json` yourself and set `AGY_SKIP_PERMS=0`:

```json
{ "permissions": { "allow": ["command(browser)"] } }
```

## Video of every run (headless)

Every run is recorded with **no visible window** via Chrome DevTools screencast (`record_cdp.py`), so
CPU/RSS stay near true headless (screencast adds a little encoding overhead, applied to every config
equally). `setup` tags the session title `REC-<sid>`; the recorder locates that target across running
Chrome endpoints, records `Page.screencastFrame` events, and assembles them into `raw/<task>.<run>.mp4`
with real inter-frame timing. The dashboard's pass@2 heatmap links each cell to its run video.

Confirmed working on the managed `chrome-headless-shell` build. Needs `ffmpeg` (frames are kept if it's
missing). This is automatic inside `run_one.sh` / `agy_one.sh`; nothing extra to run.

## Optional: headed side-by-side race

```bash
ffmpeg -f avfoundation -list_devices true -i ""     # find your screen index
export BENCH_PROFILE=bench
SCREEN="Capture screen 0" EFFORT=high ./record.sh amazon_cart sonnet   # ×3 models, maximize window
./assemble.sh amazon_cart                                              # -> results/footage/*.race.mp4
```

Footage uses a headed window → its CPU/RSS is NOT the authoritative number; cite the headless matrix.

## Fairness knobs (held identical across a comparison)

Same task, same `/browser-cli` skill (Claude) / `SKILL.md` (agy), same `MAX_TURNS`, same session setup.
Claude effort is the only Claude variable; agy effort is baked into the model slug. Runs are interleaved
per task so configs see similar network conditions. `wall_s` includes network; `cli_time_s` /
`daemon_cpu_s` are CLI-side and network-independent.

## Files

`harness.py` (tasks, setup, record, score, compare) · `run_one.sh` (Claude) · `agy_one.sh` (agy) ·
`run_matrix.sh` (full sweep) · `sample_cpu.py` (CPU/RSS series) · `record_cdp.py` (headless per-run
video) · `record.sh`/`assemble.sh` (optional headed race) · `dashboard.py` (matrix dashboard).
Validation runs from the initial pipeline check are in
`raw/wiki_awards.val-haiku-*.json` (labeled `val-*`, Claude-workflow path — not the `claude -p`
measurement path; kept for reference).
