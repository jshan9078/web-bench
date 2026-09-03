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
RUN_BUDGET_S=${RUN_BUDGET_S:-600}   # wall-clock budget per run (2026-09-03 rule: no run over 10 minutes)
TASK=$1; SLUG=$2; RUN=$3
CONFIG="$SLUG"
# BENCH_PROFILE: only pass through if the caller set it (see run_one.sh note; empty = daemon's
# active signed-in profile).
export BENCH_PROFILE=${BENCH_PROFILE:-}
export BENCH_HARNESS=agy    # setup emits a prompt that tells agy to read SKILL.md (no /browser-cli skill)
RES=results; LOG=$RES/suite.log; PY=python3
mkdir -p raw; RAW_MP4=raw/$TASK.$RUN.mp4
# 180m is a runaway safety valve only (parity with the uncapped Claude/codex harnesses, MAX_TURNS=500).
# The previous 10m default was a real cap: it killed one actively-progressing run
# (48-spotify gemini-3.8-flash-low at 606s), found in the 2026-09-02 failure re-audit and rerun.
PRINT_TIMEOUT=${PRINT_TIMEOUT:-180m}

command -v agy >/dev/null || { echo "agy not on PATH"; exit 1; }
PERM=(); [ "${AGY_SKIP_PERMS:-1}" = "1" ] && PERM=(--dangerously-skip-permissions)

export BENCH_RECORD=1
prompt=$($PY harness.py setup "$TASK" "$RUN") || { echo "setup failed"; exit 1; }
SID=$($PY -c "import json;print(json.load(open('results/current.json'))['sid'])")

STREAM=$(mktemp); AGY_ERR=$(mktemp); mkdir -p "${RES:-results}/$TASK"; CPU=${RES:-results}/$TASK/$RUN.cpu.jsonl
$PY sample_cpu.py "$CPU" 0.25 & SAMPLER=$!
$PY record_cdp.py "$SID" "$RAW_MP4" 2>>"$LOG" & REC=$!
sleep 1.5

REPO=$(pwd)   # so agy can read SKILL.md (outside the run cwd)
$PY budget_exec.py "$RUN_BUDGET_S" agy -p "$prompt" --model "$SLUG" "${PERM[@]}" --add-dir "$REPO" \
    --output-format stream-json --print-timeout "$PRINT_TIMEOUT" >"$STREAM" 2>"$AGY_ERR"
AGENT_RC=$?; BUDGET_HIT=0; [ "$AGENT_RC" -eq 124 ] && BUDGET_HIT=1 && echo "$(date +%H:%M:%S) $RUN $TASK BUDGET HIT (${RUN_BUDGET_S}s): recorded as a terminated run" >> "$LOG"
kill $SAMPLER 2>/dev/null
kill -TERM $REC 2>/dev/null; wait $REC 2>/dev/null

# Quota/rate-limit guard: decide ONLY from agy's own result event (and agy's stderr for this run),
# never from page content streamed back through tool outputs. The previous keyword grep over the
# whole stream matched ordinary page text ("quota", "limit", "FAILED" occur in a third of good
# streams) and paused the gemini-3.8-high sweep on a Wiktionary page at 78% quota (2026-09-03).
# A run with no SUCCESS result is left un-recorded (exit 3) so the sweep retries it on resume; the
# stream is preserved under raw/ as *.failstream.txt so the cause can be inspected.
RESULT=$(grep '"event":"result"' "$STREAM" 2>/dev/null | tail -1)
STATUS=$(printf '%s' "$RESULT" | $PY -c "import json,sys
try: print(json.loads(sys.stdin.read())['result'].get('status',''))
except Exception: print('')" 2>/dev/null)
QUOTA_ERR=$(grep -iE "resource_exhausted|rate.?limit|quota|too many requests|429" "$AGY_ERR" 2>/dev/null | head -2)
if [ "$BUDGET_HIT" -ne 1 ] && { [ "$STATUS" != "SUCCESS" ] || [ -n "$QUOTA_ERR" ]; }; then
  KEEP=raw/$TASK.$RUN.failstream.txt; cp "$STREAM" "$KEEP" 2>/dev/null
  echo "$(date +%H:%M:%S) $RUN $TASK $CONFIG NO-SUCCESS (status='${STATUS:-none}' stderr='${QUOTA_ERR:0:160}') - not recorded (retryable), stream kept at $KEEP" >> "$LOG"
  cat "$AGY_ERR" >> "$LOG"; rm -f "$STREAM" "$RAW_MP4" "$AGY_ERR"
  exit 3
fi
cat "$AGY_ERR" >> "$LOG"; rm -f "$AGY_ERR"

$PY harness.py record "$TASK" "run=$RUN" "config=$CONFIG" "harness=agy" "model=$SLUG" "effort=" "stream=$STREAM" "cpu=$CPU" "budget=$BUDGET_HIT" "budget_s=$RUN_BUDGET_S"
$PY harness.py score "$TASK.$RUN"
rm -f "$STREAM"
echo "$(date +%H:%M:%S) $RUN $TASK $CONFIG done" >> "$LOG"
