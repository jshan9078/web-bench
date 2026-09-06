#!/bin/bash
# Round 18: Calendar longest gap, Maps transit arrive-by, odometer, handwritten note; three configs.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND17 CAPTURE DONE" results/v2-pilot.log; do sleep 20; done
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND18 START (judgement + photo)" >> "$LOG"
export BENCH_SET=v2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="116-gcal-longest-gap 117-gmaps-transit 118-odometer-read 119-handwritten-note" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND18 CAPTURE DONE" >> "$LOG"
