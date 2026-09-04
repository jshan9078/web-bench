#!/bin/bash
# One pass@2 iteration over a batch of appstate tasks: attempt 1 for the three pilot configs, attempt 2 for every
# failing pair, then the summary. Usage: v2_iter.sh <tag> <task...>   (serial; writes results/v2-pilot.log)
set -u
cd "$(dirname "$0")"
TAG=$1; shift; LOG=results/v2-pilot.log
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) ITER $TAG START ($*)" >> "$LOG"
run() { # task config(label)
  local T=$1 R=$2
  [ -f "results/$T/$R.json" ] && return 0
  echo "$(date +%H:%M:%S) === $TAG: $T $R" >> "$LOG"
  case "$R" in
    spark-low-val*)  ./muse_one.sh "$T" muse-spark-1.2-contributor low "$R" >> "$LOG" 2>&1 ;;
    sonnet-low-val*) env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" MAX_TURNS=500 ./run_one.sh "$T" sonnet low "$R" >> "$LOG" 2>&1 ;;
    opus-low-val*)   env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" MAX_TURNS=500 ./run_one.sh "$T" opus low "$R" >> "$LOG" 2>&1 ;;
  esac
  [ $? -ne 0 ] && echo "$(date +%H:%M:%S) RUN FAILED: $T $R" >> "$LOG"
}
for T in "$@"; do for C in $(echo "${PILOT_CFGS:-sonnet-low-val,opus-low-val}" | tr , " "); do run "$T" "$C"; done; done
python3 v2_pass2.py pairs "$@" > "results/pairs_$TAG.txt"; while read -r T C; do [ -n "$T" ] && run "$T" "${C}2" </dev/null; done < "results/pairs_$TAG.txt"
python3 v2_pass2.py summary "$@" >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ITER $TAG DONE" >> "$LOG"
