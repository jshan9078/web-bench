#!/bin/bash
# Serial sweep of one Antigravity (agy) model over all tasks; skips tasks already recorded.
# Usage: agy_sweep.sh <model-slug>    e.g. agy_sweep.sh gemini-3.8-flash-low
# RUN label == model slug (matches the existing gemini-3.x-flash-<level> convention).
set -u
cd "$(dirname "$0")"
SLUG=$1
RUN="$SLUG"
for T in $(python3 -c "import harness; print('\n'.join(harness.TASKS))"); do
  if [ -f "results/$T/$RUN.json" ]; then echo "skip $T (done)"; continue; fi
  echo "=== $T $RUN $(date +%H:%M:%S)"
  ./agy_one.sh "$T" "$SLUG" "$RUN" || echo "RUN FAILED: $T"
done
echo "sweep complete: $RUN"
