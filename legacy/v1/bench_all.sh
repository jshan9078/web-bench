#!/bin/bash
# Full numbers run for the video's metrics: every task x {haiku,sonnet,opus}, interleaved per task
# (so all three models see similar network conditions), N attempts each -> pass@2.
# RUN THIS IN YOUR OWN TERMINAL (the agents authenticate with your normal Claude login).
# Usage: EFFORT=high ./bench_all.sh [attempts]   (attempts default 2)
# Env: EFFORT = thinking level for ALL models (low|medium|high|xhigh|max, default high).
# Produces results/<task>/<run>.json; see them with:  python3 harness.py compare
set -u
cd "$(dirname "$0")"
ATT=${1:-2}
MODELS="haiku sonnet opus"
PY=python3
echo ">> effort=${EFFORT:-high}  attempts=$ATT  models=$MODELS  cli=$(command -v browser)"
for a in $(seq 1 "$ATT"); do
  for t in $($PY harness.py tasks); do
    for m in $MODELS; do
      run=$m; [ "$a" -gt 1 ] && run="$m-$a"
      echo "=== attempt $a  task $t  model $m ==="
      ./run_one.sh "$t" "$m" "$run"
    done
  done
done
echo; echo "=== per-model comparison ==="
$PY harness.py compare
