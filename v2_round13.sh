#!/bin/bash
# Round 13: 95 lot occupancy (state over time) and 96 slide diff (two moments), three configs.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND13 START (95 96)" >> "$LOG"
export BENCH_SET=v2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="95-lot-occupancy 96-slide-diff" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND13 CAPTURE DONE" >> "$LOG"
