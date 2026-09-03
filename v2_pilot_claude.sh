#!/bin/bash
# Third pilot leg: Sonnet 5 low over the v2 tasks, started only after v2_pilot.sh (muse + agy legs) has
# exited. Claude is launched under `env -i` (HOME/PATH/TMPDIR only) so it authenticates normally even
# when this script is started from inside a Claude session (validated by the 2026-09-02 fairness reruns).
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
echo "$(date +%H:%M:%S) CLAUDE LEG: waiting for the muse/agy pilot to finish" >> "$LOG"
while pgrep -f "v2_pilot.sh" >/dev/null; do sleep 20; done
echo "$(date +%H:%M:%S) CLAUDE LEG START (sonnet-low-val, v2 tasks)" >> "$LOG"
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 MAX_TURNS=500 \
    CLAUDE_MODELS=sonnet EFFORTS=low SKIP_AGY=1 RUN_TAG=val ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) CLAUDE LEG rc=$?" >> "$LOG"
echo "$(date +%H:%M:%S) PILOT DONE (all three legs)" >> "$LOG"
