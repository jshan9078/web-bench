#!/bin/bash
# Round 19: fine precision (gauge, drop pin, custom slider, tick-only clock), three configs.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND18 CAPTURE DONE" results/v2-pilot.log; do sleep 20; done
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND19 START (precision)" >> "$LOG"
export BENCH_SET=v2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="120-gauge-needle 122-drop-pin 125-custom-slider 127-clock-ticks" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND19 CAPTURE DONE" >> "$LOG"
