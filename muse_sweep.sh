#!/bin/bash
# Serial sweep of one muse config over all tasks; skips tasks already recorded.
# Usage: muse_sweep.sh <effort>
set -u
cd "$(dirname "$0")"
MODEL=muse-spark-1.2-contributor
EFFORT=$1
RUN="spark-$EFFORT-val"
for T in $(python3 -c "import harness; print('\n'.join(harness.TASKS))"); do
  if [ -f "results/$T/$RUN.json" ]; then echo "skip $T (done)"; continue; fi
  echo "=== $T $RUN $(date +%H:%M:%S)"
  ./muse_one.sh "$T" "$MODEL" "$EFFORT" "$RUN" || echo "RUN FAILED: $T"
done
echo "sweep complete: $RUN"
