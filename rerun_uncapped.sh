#!/bin/bash
# Fairness reruns: the 15 Claude runs that failed by exhausting the 60-turn budget,
# re-captured with MAX_TURNS=500 (effectively uncapped, parity with codex's uncapped
# harness; 500 is a runaway safety valve). Waits for any codex sweep to finish first.
# Old evidence is preserved under raw/attempt1/ before each rerun. RUN IN YOUR OWN TERMINAL.
set -u
cd "$(dirname "$0")"
echo "waiting for any running codex sweep to finish..."
while pgrep -f codex_sweep.sh >/dev/null || pgrep -f 'codex exec' >/dev/null; do sleep 30; done
mkdir -p raw/attempt1
RERUNS=(
  "23-amazon-filter-hunt opus high"
  "23-amazon-filter-hunt opus max"
  "23-amazon-filter-hunt opus xhigh"
  "32-desmos-intersections haiku high"
  "32-desmos-intersections haiku max"
  "32-desmos-intersections opus high"
  "32-desmos-intersections sonnet high"
  "32-desmos-intersections sonnet low"
  "32-desmos-intersections sonnet max"
  "32-desmos-intersections sonnet medium"
  "32-desmos-intersections sonnet xhigh"
  "36-jspaint-poster haiku high"
  "36-jspaint-poster haiku max"
  "36-jspaint-poster sonnet max"
  "48-spotify-playlist sonnet max"
)
for R in "${RERUNS[@]}"; do
  set -- $R; TASK=$1; MODEL=$2; EFFORT=$3; RUN="$MODEL-$EFFORT-val"
  echo "=== uncapped rerun: $TASK $RUN $(date +%H:%M:%S)"
  for f in raw/$TASK.$RUN.*; do [ -e "$f" ] && mv "$f" "raw/attempt1/$(basename "$f")"; done
  MAX_TURNS=500 ./run_one.sh "$TASK" "$MODEL" "$EFFORT" "$RUN" || echo "RERUN FAILED: $TASK $RUN"
done
echo "UNCAPPED RERUNS DONE"
