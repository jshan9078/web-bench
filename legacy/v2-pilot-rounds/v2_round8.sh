#!/bin/bash
# Round 8 (v2.7): spot-the-difference at level 3 (design-QA subtleties) and the cancellation dark-pattern flow (88),
# on Spark 1.2 low, Sonnet 5 low, Opus 5 low. Starts after round 7.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND7 CAPTURE DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_round7.sh|muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 15; done
echo "$(date +%H:%M:%S) ROUND8 START (59@L3 88)" >> "$LOG"
export BENCH_SET=v2 WIDGET_LEVEL=2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 WIDGET_LEVEL=2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="59-spot-difference 88-cancel-flow" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND8 CAPTURE DONE" >> "$LOG"
