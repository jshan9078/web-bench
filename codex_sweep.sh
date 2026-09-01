#!/bin/bash
# Serial sweep of one codex config over all tasks; skips tasks already recorded.
# Usage: codex_sweep.sh <model> <effort>
set -u
cd "$(dirname "$0")"
MODEL=$1; EFFORT=$2
SHORT=${MODEL#gpt-5.6-}
RUN="$SHORT-$EFFORT-val"
# Optional skip list: tasks solved by EVERY judged config (incl. luna-low) are not re-run
# for the remaining OpenAI configs; see results/openai_skip_tasks.txt (one task id per line).
SKIP_FILE=results/openai_skip_tasks.txt
for T in $(python3 -c "import harness; print('\n'.join(harness.TASKS))"); do
  if [ -f "$SKIP_FILE" ] && grep -qx "$T" "$SKIP_FILE"; then echo "skip $T (all-config-pass list)"; continue; fi
  if [ -f "results/$T/$RUN.json" ]; then echo "skip $T (done)"; continue; fi
  echo "=== $T $RUN $(date +%H:%M:%S)"
  ./codex_one.sh "$T" "$MODEL" "$EFFORT" "$RUN" || echo "RUN FAILED: $T"
done
echo "sweep complete: $RUN"
