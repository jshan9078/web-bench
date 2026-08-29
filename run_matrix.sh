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
#   AGY_MODELS     (default "gemini-3.7-flash-low gemini-3.7-flash-medium gemini-3.7-flash-high")
#   BENCH_PROFILE  override the profile for signed-in tasks (default: the daemon's active
#                  profile, which must be signed into the task sites; see tasks/*/task.md)
#   SKIP_CLAUDE=1 / SKIP_AGY=1 to run only one side.
#   RUN_TAG=<tag>  suffix every run label (e.g. haiku-low-val); use a fresh tag to rerun configs
#                  that already have recorded runs without colliding with their raw bundles,
#                  verdicts, or results.
#
# Task selection (default: every task in harness.py tasks):
#   TASKS="01-mlb-latest 42-youtube-watch-later"   run exactly these task names (space-separated)
#   RANGE="08-20"                                  run tasks whose NN- prefix falls in the range
#   RANGE="01,05,29-41"                            commas mix single numbers and ranges
#   TASKS wins if both are set. Unknown names/numbers abort with a message before any run.
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
ALL_TASKS=$($PY harness.py tasks)
if [ -n "${TASKS:-}" ]; then
  SELECTED=""
  for t in $TASKS; do
    if printf '%s\n' $ALL_TASKS | grep -qx "$t"; then SELECTED="$SELECTED $t"; else echo "!! unknown task: $t (see: python3 harness.py tasks)"; exit 1; fi
  done
elif [ -n "${RANGE:-}" ]; then
  SELECTED=$(printf '%s\n' $ALL_TASKS | RANGE="$RANGE" $PY -c '
import os, sys
sel = set()
for part in os.environ["RANGE"].split(","):
    part = part.strip()
    if not part: continue
    a, sep, b = part.partition("-")
    if not a.isdigit() or (sep and not b.isdigit()):
        sys.exit(f"!! bad RANGE part: {part!r} (use numbers like 08 or ranges like 08-20)")
    sel.update(range(int(a), int(b) + 1) if sep else [int(a)])
names = [l.strip() for l in sys.stdin if l.strip()]
picked = [n for n in names if n[:2].isdigit() and int(n[:2]) in sel]
missing = sel - {int(n[:2]) for n in picked}
if missing: sys.exit("!! RANGE numbers with no matching task: " + ", ".join(f"{m:02d}" for m in sorted(missing)))
print("\n".join(picked))
') || { echo "$SELECTED"; exit 1; }
else
  SELECTED="$ALL_TASKS"
fi
n_tasks=$(printf '%s\n' $SELECTED | wc -l | tr -d ' ')
echo ">> matrix: $((n_claude+n_agy)) configs ($n_claude claude + $n_agy agy) x $n_tasks tasks x $ATT attempts = $(((n_claude+n_agy)*n_tasks*ATT)) runs"
echo ">> profile=${BENCH_PROFILE:-'(daemon default)'}  cli=$(command -v browser)"

# RESUME=1 (default): skip any (task,run) already complete (passed, or judge-task captured & pending).
# Empty/failed runs are NOT complete, so they retry. RESUME=0 forces every run to re-execute.
skip_done() { [ "${RESUME:-1}" = 1 ] && $PY harness.py done "$1" 2>/dev/null; }

for a in $(seq 1 "$ATT"); do
  sfx=""; [ "$a" -gt 1 ] && sfx="-a$a"
  for t in $SELECTED; do
    if [ "${SKIP_CLAUDE:-0}" != 1 ]; then
      for m in $CLAUDE_MODELS; do for e in $EFFORTS; do
        run="$m-$e${RUN_TAG:+-$RUN_TAG}$sfx"
        if skip_done "$t.$run"; then echo "--- skip (done): $t $run"; continue; fi
        echo "=== [$a] $t  $run ==="; ./run_one.sh "$t" "$m" "$e" "$run"
      done; done
    fi
    if [ "${SKIP_AGY:-0}" != 1 ]; then
      for s in $AGY_MODELS; do
        run="$s${RUN_TAG:+-$RUN_TAG}$sfx"
        if skip_done "$t.$run"; then echo "--- skip (done): $t $run"; continue; fi
        echo "=== [$a] $t  $run ==="; ./agy_one.sh "$t" "$s" "$run"
      done
    fi
  done
done
echo; echo "=== per-config comparison ==="
$PY harness.py compare
