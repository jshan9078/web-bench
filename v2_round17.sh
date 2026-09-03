#!/bin/bash
# Round 17: perception batch 2 (112-115), three configs.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND16 CAPTURE DONE" results/v2-pilot.log; do sleep 20; done
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND17 START (perception 2)" >> "$LOG"
export BENCH_SET=v2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="112-gantt-read 113-pie-share 114-scatter-threshold 115-heatmap-max" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND17 CAPTURE DONE" >> "$LOG"
