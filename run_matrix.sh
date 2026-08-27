#!/bin/bash
# FULL matrix sweep for the model x thinking-level x CLI comparison.
# RUN THIS IN YOUR OWN TERMINAL (agents authenticate with your normal Claude / agy login).
#
#   Claude:  {opus,sonnet,haiku} x effort {low,medium,high,xhigh,max}   = 15 configs  (claude -p --effort)
#   agy:     each slug in $AGY_MODELS                                    (agy -p --model <slug>)
#
# Usage: ./run_matrix.sh [attempts]        (default 2 -> pass@2)
# Env:
#   CLAUDE_MODELS  (default "opus sonnet haiku")
#   EFFORTS        (default "low medium high xhigh max")
#   AGY_MODELS     (default "gemini-3.6-flash-high gemini-3.6-flash-medium"; set to the slugs you want)
#   BENCH_PROFILE  (default "default"; must be logged into Amazon + X for amazon_cart / x_projects)
#   SKIP_CLAUDE=1 / SKIP_AGY=1 to run only one side.
# Everything is captured raw first (raw/*.json); scoring is re-runnable via `harness.py score`.
set -u
cd "$(dirname "$0")"
ATT=${1:-2}
CLAUDE_MODELS=${CLAUDE_MODELS:-"opus sonnet haiku"}
EFFORTS=${EFFORTS:-"low medium high xhigh max"}
AGY_MODELS=${AGY_MODELS:-"gemini-3.7-flash-low gemini-3.7-flash-medium gemini-3.7-flash-high"}
PY=python3

n_claude=0; [ "${SKIP_CLAUDE:-0}" = 1 ] || for m in $CLAUDE_MODELS; do for e in $EFFORTS; do n_claude=$((n_claude+1)); done; done
n_agy=0; [ "${SKIP_AGY:-0}" = 1 ] || for s in $AGY_MODELS; do n_agy=$((n_agy+1)); done
n_tasks=$($PY harness.py tasks | wc -l | tr -d ' ')
echo ">> matrix: $((n_claude+n_agy)) configs ($n_claude claude + $n_agy agy) x $n_tasks tasks x $ATT attempts = $(((n_claude+n_agy)*n_tasks*ATT)) runs"
echo ">> profile=${BENCH_PROFILE:-default}  cli=$(command -v browser)"

# RESUME=1 (default): skip any (task,run) already complete (passed, or judge-task captured & pending).
# Empty/failed runs are NOT complete, so they retry. RESUME=0 forces every run to re-execute.
skip_done() { [ "${RESUME:-1}" = 1 ] && $PY harness.py done "$1" 2>/dev/null; }

for a in $(seq 1 "$ATT"); do
  sfx=""; [ "$a" -gt 1 ] && sfx="-a$a"
  for t in $($PY harness.py tasks); do
    if [ "${SKIP_CLAUDE:-0}" != 1 ]; then
      for m in $CLAUDE_MODELS; do for e in $EFFORTS; do
        run="$m-$e$sfx"
        if skip_done "$t.$run"; then echo "--- skip (done): $t $run"; continue; fi
        echo "=== [$a] $t  $run ==="; ./run_one.sh "$t" "$m" "$e" "$run"
      done; done
    fi
    if [ "${SKIP_AGY:-0}" != 1 ]; then
      for s in $AGY_MODELS; do
        run="$s$sfx"
        if skip_done "$t.$run"; then echo "--- skip (done): $t $run"; continue; fi
        echo "=== [$a] $t  $run ==="; ./agy_one.sh "$t" "$s" "$run"
      done
    fi
  done
done
echo; echo "=== per-config comparison ==="
$PY harness.py compare
