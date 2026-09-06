#!/bin/bash
# Round 16: perception batch (108-111) + fine print with corrected prompt (103), three configs.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND15 CAPTURE DONE" results/v2-pilot.log; do sleep 20; done
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND16 START (perception + 103)" >> "$LOG"
export BENCH_SET=v2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="103-fine-print 108-shelf-count 109-legend-match 110-analog-clock 111-fill-level" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND16 CAPTURE DONE" >> "$LOG"
