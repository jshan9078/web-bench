#!/bin/bash
# pass@2: second attempt for every (task, config) that failed among the 20 discriminating tasks. Run labels get a
# "2" suffix (spark-low-val2, sonnet-low-val2, opus-low-val2) so attempt 1 stays on record. Serial.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
while pgrep -f "muse_one.sh|run_one.sh|budget_exec.py" >/dev/null; do sleep 10; done
echo "$(date +%H:%M:%S) PASS2 START ($(wc -l < results/pass2_pairs.txt) pairs)" >> "$LOG"
while read -r TASK CFG; do
  [ -z "${TASK:-}" ] && continue
  RUN="${CFG}2"
  if [ -f "results/$TASK/$RUN.json" ]; then echo "skip $TASK $RUN (done)" >> "$LOG"; continue; fi
  echo "$(date +%H:%M:%S) === pass2: $TASK $RUN" >> "$LOG"
  case "$CFG" in
    spark-low-val)  ./muse_one.sh "$TASK" muse-spark-1.2-contributor low "$RUN" >> "$LOG" 2>&1 ;;
    sonnet-low-val) env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" MAX_TURNS=500 ./run_one.sh "$TASK" sonnet low "$RUN" >> "$LOG" 2>&1 ;;
    opus-low-val)   env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" MAX_TURNS=500 ./run_one.sh "$TASK" opus low "$RUN" >> "$LOG" 2>&1 ;;
  esac
  rc=$?; [ $rc -ne 0 ] && echo "$(date +%H:%M:%S) PASS2 RUN FAILED rc=$rc: $TASK $RUN" >> "$LOG"
done < results/pass2_pairs.txt
echo "$(date +%H:%M:%S) PASS2 CAPTURE DONE" >> "$LOG"
