#!/bin/bash
# Round 3 (v2.2 tasks 74, 75, 78, 79) for Sonnet 5 low. Spark and Gemini pick these tasks up in the
# post-round-2 fix leg's sweeps (they run every missing v2 task). Starts after that leg has finished.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND2 ALL DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_round2_fix.sh" >/dev/null; do sleep 15; done
echo "$(date +%H:%M:%S) ROUND3 claude leg (sonnet-low on 63 64 68 + 74 75 78 79)" >> "$LOG"
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 WIDGET_LEVEL=2 MAX_TURNS=500 \
    CLAUDE_MODELS=sonnet EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="63-wikipedia-edit-audit 64-hn-comment-census 68-youtube-transcript 74-dashboard-triage 75-map-explorer 76-settings-maze 78-gmaps-directions 79-gmaps-place-hours" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND3 CAPTURE DONE" >> "$LOG"
