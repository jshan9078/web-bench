#!/bin/bash
# One Codex run: setup -> CPU sampler -> `codex exec --json` (SKILL.md-pointer prompt, full event
# stream captured) -> record raw bundle -> score.
# Usage: codex_one.sh <task> <model> <effort> <run_label>
#   model: gpt-5.6-terra|gpt-5.6-luna    effort: low|medium|high|xhigh|max
# Parity notes vs run_one.sh: sandbox/approvals fully bypassed (same trust level as claude
# --dangerously-skip-permissions); codex exec has no turn cap, so the 60-turn budget is not
# enforced for this harness (recorded as a harness difference, like Antigravity's own loop).
set -u
cd "$(dirname "$0")"
RUN_BUDGET_S=${RUN_BUDGET_S:-600}   # wall-clock budget per run (2026-09-03 rule: no run over 10 minutes)
TASK=$1; MODEL=$2; EFFORT=$3; RUN=$4
SHORT=${MODEL#gpt-5.6-}
CONFIG="$SHORT-$EFFORT"
export BENCH_PROFILE=${BENCH_PROFILE:-}
export BENCH_HARNESS=codex
RES=results; LOG=$RES/suite.log; PY=python3
mkdir -p raw; RAW_MP4=raw/$TASK.$RUN.mp4

export BENCH_RECORD=1
prompt=$($PY harness.py setup "$TASK" "$RUN") || { echo "setup failed"; exit 1; }
SID=$($PY -c "import json;print(json.load(open('results/current.json'))['sid'])")

STREAM=$(mktemp); mkdir -p "$RES/$TASK"; CPU=$RES/$TASK/$RUN.cpu.jsonl
$PY sample_cpu.py "$CPU" 0.25 & SAMPLER=$!
$PY record_cdp.py "$SID" "$RAW_MP4" 2>>"$LOG" & REC=$!
sleep 1.5

$PY budget_exec.py "$RUN_BUDGET_S" codex exec --json --skip-git-repo-check \
    -m "$MODEL" -c model_reasoning_effort="$EFFORT" \
    --dangerously-bypass-approvals-and-sandbox \
    "$prompt" < /dev/null > "$STREAM" 2>>"$LOG"
AGENT_RC=$?; BUDGET_HIT=0; [ "$AGENT_RC" -eq 124 ] && BUDGET_HIT=1 && echo "$(date +%H:%M:%S) $RUN $TASK BUDGET HIT (${RUN_BUDGET_S}s): recorded as a terminated run" >> "$LOG"
kill $SAMPLER 2>/dev/null
kill -TERM $REC 2>/dev/null; wait $REC 2>/dev/null

$PY harness.py record "$TASK" "run=$RUN" "config=$CONFIG" "harness=codex" "model=$MODEL" "effort=$EFFORT" "stream=$STREAM" "cpu=$CPU" "budget=$BUDGET_HIT" "budget_s=$RUN_BUDGET_S"
$PY harness.py score "$TASK.$RUN"
rm -f "$STREAM"
echo "$(date +%H:%M:%S) $RUN $TASK $CONFIG done" >> "$LOG"
