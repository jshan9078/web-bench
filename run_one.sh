#!/bin/bash
# One Claude run: setup -> CPU sampler -> `claude -p --effort <level>` (real /browser-cli skill,
# full stream captured) -> record raw bundle -> score.  RUN IN YOUR OWN TERMINAL (needs your login).
# Usage: run_one.sh <task> <model> <effort> <run_label>
#   model: opus|sonnet|haiku    effort: low|medium|high|xhigh|max
# Env: MAX_TURNS (60), BENCH_PROFILE (default), CLAUDE_BIN (override binary), BROWSER_CLI/BROWSER_DAEMON.
set -u
cd "$(dirname "$0")"
TASK=$1; MODEL=$2; EFFORT=$3; RUN=$4
CONFIG="$MODEL-$EFFORT"
MAX_TURNS=${MAX_TURNS:-60}
# BENCH_PROFILE: only pass through if the caller set it. Empty means harness omits --profile and
# the daemon's active profile (the signed-in one) applies. Do NOT default to a named profile here:
# naming a nonexistent profile silently creates a fresh logged-out one.
export BENCH_PROFILE=${BENCH_PROFILE:-}
RES=results; LOG=$RES/suite.log; PY=python3
mkdir -p raw; RAW_MP4=raw/$TASK.$RUN.mp4

# Headless claude -p auth: load a long-lived OAuth token (from `claude setup-token`) out of the repo
# root .env if not already exported. Accepts CLAUDE_CODE_OAUTH_TOKEN or (legacy) CLAUDE_KEY.
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
  ENVF="$(pwd)/.env"
  if [ -f "$ENVF" ]; then
    _t=$(grep -E '^(export )?CLAUDE_CODE_OAUTH_TOKEN=' "$ENVF" | tail -1 | sed -E 's/^(export )?CLAUDE_CODE_OAUTH_TOKEN=//' | tr -d '\r' | sed -E 's/^["'"'"']//; s/["'"'"']$//')
    [ -z "$_t" ] && _t=$(grep -E '^(export )?CLAUDE_KEY=' "$ENVF" | tail -1 | sed -E 's/^(export )?CLAUDE_KEY=//' | tr -d '\r' | sed -E 's/^["'"'"']//; s/["'"'"']$//')
    [ -n "$_t" ] && export CLAUDE_CODE_OAUTH_TOKEN="$_t"
  fi
fi

pick_claude() {
  if [ -n "${CLAUDE_BIN:-}" ]; then echo "$CLAUDE_BIN"; return; fi
  # Prefer the PATH `claude` (your logged-in CLI) IF it supports --effort. The app binary under
  # ~/Library/Application Support has --effort but its OAuth can't refresh from a plain `claude -p`
  # ("OAuth session expired"), so only fall back to it when PATH claude lacks --effort.
  if command -v claude >/dev/null 2>&1 && claude --help 2>&1 | grep -q -- '--effort'; then command -v claude; return; fi
  local newest; newest=$(ls -d "$HOME/Library/Application Support/Claude/claude-code/"*/claude.app/Contents/MacOS/claude 2>/dev/null | sort -V | tail -1)
  if [ -n "$newest" ] && "$newest" --help 2>&1 | grep -q -- '--effort'; then echo "$newest"; return; fi
  echo "claude"
}
CLAUDE=$(pick_claude)
EFFORT_ARG=(--effort "$EFFORT")
if ! "$CLAUDE" --help 2>&1 | grep -q -- '--effort'; then
  echo "WARNING: $CLAUDE has no --effort; thinking level NOT controlled." >&2; EFFORT_ARG=()
fi

export BENCH_RECORD=1
prompt=$($PY harness.py setup "$TASK" "$RUN") || { echo "setup failed"; exit 1; }
SID=$($PY -c "import json;print(json.load(open('results/current.json'))['sid'])")

STREAM=$(mktemp); mkdir -p "$RES/$TASK"; CPU=$RES/$TASK/$RUN.cpu.jsonl
$PY sample_cpu.py "$CPU" 0.25 & SAMPLER=$!
$PY record_cdp.py "$SID" "$RAW_MP4" 2>>"$LOG" & REC=$!    # headless video of this run
sleep 1.5                                                  # let the recorder attach to the target

# stream-json captures EVERY step (tool calls + outputs) = the full trace, saved before we judge.
# NOTE: `claude -p --output-format stream-json` REQUIRES --verbose (verbose logs go to stderr/$LOG;
# stdout stays clean ndjson that record() parses).
"$CLAUDE" -p "$prompt" --model "$MODEL" "${EFFORT_ARG[@]}" \
    --allowedTools Bash --dangerously-skip-permissions --verbose \
    --output-format stream-json --max-turns "$MAX_TURNS" >"$STREAM" 2>>"$LOG"
kill $SAMPLER 2>/dev/null
kill -TERM $REC 2>/dev/null; wait $REC 2>/dev/null       # finalize the mp4

$PY harness.py record "$TASK" "run=$RUN" "config=$CONFIG" "harness=claude" "model=$MODEL" "effort=$EFFORT" "stream=$STREAM" "cpu=$CPU"
$PY harness.py score "$TASK.$RUN"
rm -f "$STREAM"
echo "$(date +%H:%M:%S) $RUN $TASK $CONFIG done" >> "$LOG"
