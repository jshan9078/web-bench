#!/bin/bash
# Round 7 (v2.6): dense-perception tasks 84 85 86, pixel scan at level 3 (58), Google Calendar scheduling (87),
# on Spark 1.2 low, Sonnet 5 low, Opus 5 low.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ROUND7 START (58@L3 84 85 86 87)" >> "$LOG"
export BENCH_SET=v2 WIDGET_LEVEL=2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 WIDGET_LEVEL=2 MAX_TURNS=500 \
    CLAUDE_MODELS="sonnet opus" EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="58-pixel-scan 84-ledger-audit 85-table-diff 86-chart-read 87-gcal-scheduling" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND7 CAPTURE DONE" >> "$LOG"
