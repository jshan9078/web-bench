#!/bin/bash
# One Antigravity (agy) run: setup -> CPU sampler -> `agy -p --model <slug>` (reads SKILL.md, full
# stream captured) -> record raw bundle -> score.  RUN IN YOUR OWN TERMINAL (needs agy cached auth).
# Usage: agy_one.sh <task> <model-slug> <run_label>
#   e.g. agy_one.sh wiki_awards gemini-3.6-flash-high gemini-3.6-flash-high
# Env: AGY_SKIP_PERMS=1 (default) passes --dangerously-skip-permissions so the agent may run the
#      `browser` shell command headlessly. Set AGY_SKIP_PERMS=0 if you instead added a scoped
#      "command(browser)" rule to ~/.gemini/antigravity-cli/settings.json yourself.
#      PRINT_TIMEOUT (default 10m), BENCH_PROFILE, BROWSER_CLI/BROWSER_DAEMON.
set -u
cd "$(dirname "$0")"
TASK=$1; SLUG=$2; RUN=$3
CONFIG="$SLUG"
export BENCH_PROFILE=${BENCH_PROFILE:-default}
export BENCH_HARNESS=agy    # setup emits a prompt that tells agy to read SKILL.md (no /browser-cli skill)
RES=results; LOG=$RES/suite.log; PY=python3
mkdir -p raw; RAW_MP4=raw/$TASK.$RUN.mp4
PRINT_TIMEOUT=${PRINT_TIMEOUT:-10m}

command -v agy >/dev/null || { echo "agy not on PATH"; exit 1; }
PERM=(); [ "${AGY_SKIP_PERMS:-1}" = "1" ] && PERM=(--dangerously-skip-permissions)

export BENCH_RECORD=1
prompt=$($PY harness.py setup "$TASK" "$RUN") || { echo "setup failed"; exit 1; }
SID=$($PY -c "import json;print(json.load(open('results/current.json'))['sid'])")

STREAM=$(mktemp); CPU=$RES/$TASK.$RUN.cpu.jsonl
$PY sample_cpu.py "$CPU" 0.25 & SAMPLER=$!
$PY record_cdp.py "$SID" "$RAW_MP4" 2>>"$LOG" & REC=$!
sleep 1.5

REPO=$(pwd)   # so agy can read SKILL.md (outside the run cwd)
agy -p "$prompt" --model "$SLUG" "${PERM[@]}" --add-dir "$REPO" \
    --output-format stream-json --print-timeout "$PRINT_TIMEOUT" >"$STREAM" 2>>"$LOG"
kill $SAMPLER 2>/dev/null
kill -TERM $REC 2>/dev/null; wait $REC 2>/dev/null

$PY harness.py record "$TASK" "run=$RUN" "config=$CONFIG" "harness=agy" "model=$SLUG" "effort=" "stream=$STREAM" "cpu=$CPU"
$PY harness.py score "$TASK.$RUN"
rm -f "$STREAM"
echo "$(date +%H:%M:%S) $RUN $TASK $CONFIG done" >> "$LOG"
