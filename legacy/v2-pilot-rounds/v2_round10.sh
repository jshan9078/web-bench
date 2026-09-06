#!/bin/bash
# Round 10: the dial precision task (90) on Spark 1.2 low, Sonnet 5 low, Opus 5 low.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND10 START (90-dial-set)" >> "$LOG"
export BENCH_SET=v2 WIDGET_LEVEL=2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 WIDGET_LEVEL=2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="90-dial-set" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND10 CAPTURE DONE" >> "$LOG"
