#!/bin/bash
# Serial sweep of one Antigravity (agy) model over all tasks; skips tasks already recorded.
# Usage: agy_sweep.sh <model-slug>    e.g. agy_sweep.sh gemini-3.8-flash-low
# RUN label == model slug (matches the existing gemini-3.x-flash-<level> convention).
set -u
cd "$(dirname "$0")"
SLUG=$1
RUN="$SLUG"
# Mutual exclusion: one benchmark process on this machine at a time. If a muse sweep is driving
# the browser, defer this pass (exit 3 = "pause", so agy_autoresume waits 15m and retries).
if pgrep -f "muse_sweep.sh|muse_one.sh|run_one.sh|rerun_uncapped.sh|codex_one.sh|env_rerun_launcher.sh" >/dev/null 2>&1; then
  echo "BUSY: another benchmark sweep is driving the browser, deferring agy pass"; exit 3
fi
for T in $(python3 -c "import harness; print('\n'.join(harness.TASKS))"); do
  if [ -f "results/$T/$RUN.json" ]; then echo "skip $T (done)"; continue; fi
  echo "=== $T $RUN $(date +%H:%M:%S)"
  ./agy_one.sh "$T" "$SLUG" "$RUN"; rc=$?
  if [ $rc -eq 3 ]; then echo "QUOTA hit at $T - pausing sweep (task retryable on resume)"; exit 3; fi
  [ $rc -ne 0 ] && echo "RUN FAILED: $T"
done
echo "sweep complete: $RUN"
