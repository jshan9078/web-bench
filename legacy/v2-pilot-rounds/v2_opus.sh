#!/bin/bash
# Opus 5 low on the full v2 set (19 tasks), same harness rules as the pilot (level-2 widgets, 10-minute budget).
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
echo "$(date +%H:%M:%S) OPUS LEG START (opus-low-val, all v2 tasks)" >> "$LOG"
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 WIDGET_LEVEL=2 MAX_TURNS=500 \
    CLAUDE_MODELS=opus EFFORTS=low SKIP_AGY=1 RUN_TAG=val ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) OPUS LEG DONE" >> "$LOG"
