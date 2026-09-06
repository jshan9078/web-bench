#!/bin/bash
# Serial sweep of one muse config over all tasks; skips tasks already recorded.
# Usage: muse_sweep.sh <effort>
set -u
cd "$(dirname "$0")"
# Usage: muse_sweep.sh <effort> [model] [config-prefix]
#   defaults: model=muse-spark-1.2-contributor prefix=spark   (1.3: muse-spark-1.3-contributor spark13)
EFFORT=$1
MODEL=${2:-muse-spark-1.2-contributor}
export SPARK_PREFIX=${3:-spark}
RUN="$SPARK_PREFIX-$EFFORT-val"
for T in $(python3 -c "import harness; print('\n'.join(harness.sweep_tasks()))"); do
  if [ -f "results/$T/$RUN.json" ]; then echo "skip $T (done)"; continue; fi
  echo "=== $T $RUN $(date +%H:%M:%S)"
  ./muse_one.sh "$T" "$MODEL" "$EFFORT" "$RUN" || echo "RUN FAILED: $T"
done
echo "sweep complete: $RUN"
