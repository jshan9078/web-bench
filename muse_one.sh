#!/bin/bash
# One Muse Code run: setup -> CPU sampler -> `muse exec --json` (SKILL.md-pointer prompt) ->
# concatenate stdout stream + session.jsonl (usage lives only in the session log) -> record -> score.
# Usage: muse_one.sh <task> <model> <effort> <run_label>
#   model: muse-spark-1.2-contributor    effort: low|medium|high|xhigh|ultra
# Parity notes vs run_one.sh: --yolo disables approval + sandbox and trusts the workspace (same
# trust level as claude --dangerously-skip-permissions / codex bypass); muse exec has no turn cap,
# matching the uncapped harness.
set -u
cd "$(dirname "$0")"
RUN_BUDGET_S=${RUN_BUDGET_S:-600}   # wall-clock budget per run (2026-09-03 rule: no run over 10 minutes)
TASK=$1; MODEL=$2; EFFORT=$3; RUN=$4
CONFIG="${SPARK_PREFIX:-spark}-$EFFORT"   # SPARK_PREFIX=spark13 for the 1.3 family
export BENCH_PROFILE=${BENCH_PROFILE:-}
export BENCH_HARNESS=muse
RES=results; LOG=$RES/suite.log; PY=python3
mkdir -p raw; RAW_MP4=raw/$TASK.$RUN.mp4

export BENCH_RECORD=1
prompt=$($PY harness.py setup "$TASK" "$RUN") || { echo "setup failed"; exit 1; }
SID=$($PY -c "import json;print(json.load(open('results/current.json'))['sid'])")

STREAM=$(mktemp); mkdir -p "$RES/$TASK"; CPU=$RES/$TASK/$RUN.cpu.jsonl
$PY sample_cpu.py "$CPU" 0.25 & SAMPLER=$!
$PY record_cdp.py "$SID" "$RAW_MP4" 2>>"$LOG" & REC=$!
sleep 1.5

$PY budget_exec.py "$RUN_BUDGET_S" muse exec --json --yolo \
    --model "$MODEL" --reasoning-effort "$EFFORT" \
    "$prompt" < /dev/null > "$STREAM" 2>>"$LOG"
AGENT_RC=$?; BUDGET_HIT=0; [ "$AGENT_RC" -eq 124 ] && BUDGET_HIT=1 && echo "$(date +%H:%M:%S) $RUN $TASK BUDGET HIT (${RUN_BUDGET_S}s): recorded as a terminated run" >> "$LOG"
kill $SAMPLER 2>/dev/null
kill -TERM $REC 2>/dev/null; wait $REC 2>/dev/null

# append the session log (usage source): session id is stream.id on the stdout events
MSID=$($PY -c "
import json,sys
for l in open('$STREAM'):
    try: print(json.loads(l)['stream']['id']); break
    except Exception: pass")
if [ -n "$MSID" ]; then
  SLOG=$(ls "$HOME"/.local/share/muse/sessions/*/*/*/"$MSID"/session.jsonl 2>/dev/null | head -1)
  [ -n "$SLOG" ] && cat "$SLOG" >> "$STREAM"
fi

$PY harness.py record "$TASK" "run=$RUN" "config=$CONFIG" "harness=muse" "model=$MODEL" "effort=$EFFORT" "stream=$STREAM" "cpu=$CPU" "budget=$BUDGET_HIT" "budget_s=$RUN_BUDGET_S"
$PY harness.py score "$TASK.$RUN"
rm -f "$STREAM"
echo "$(date +%H:%M:%S) $RUN $TASK $CONFIG done" >> "$LOG"
