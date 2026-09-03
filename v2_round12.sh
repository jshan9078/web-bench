#!/bin/bash
# Round 12: level-2 video tasks (91 pointer, 92 correlation, 94 direction) + gated endpoints, three configs, serial: Spark 1.2 low, then Sonnet 5 low and Opus 5 low.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND12 START (91 92 94 @L2)" >> "$LOG"
export BENCH_SET=v2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="91-video-slide-read 92-log-stream 94-cctv-review" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND12 CAPTURE DONE" >> "$LOG"
