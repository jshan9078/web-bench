#!/bin/bash
# Round 5: the live fleet console (80) on Spark 1.2 low and Sonnet 5 low. Starts once no run is active.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
while pgrep -f "muse_one.sh|run_one.sh|agy_one.sh|budget_exec.py|v2_round4.sh" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND5 START (80-live-list)" >> "$LOG"
export BENCH_SET=v2 WIDGET_LEVEL=2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 WIDGET_LEVEL=2 MAX_TURNS=500 \
    CLAUDE_MODELS=sonnet EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="80-live-list" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND5 CAPTURE DONE" >> "$LOG"
