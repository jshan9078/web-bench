#!/bin/bash
# Round 20: remote desktop (image-only UI) and dashcam speed, three configs.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND19 CAPTURE DONE" results/v2-pilot.log; do sleep 20; done
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND20 START (remote desktop + dashcam)" >> "$LOG"
export BENCH_SET=v2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="128-remote-desktop 136-dashcam-speed" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND20 CAPTURE DONE" >> "$LOG"
