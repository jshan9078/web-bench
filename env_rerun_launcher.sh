#!/bin/bash
# Deferred fairness reruns from the 2026-09-02 failure re-audit. Waits for the running muse 1.3
# chain to finish, then serially re-captures each queued run under the uncapped harness
# (Claude: MAX_TURNS=500; agy: PRINT_TIMEOUT=180m; codex: already uncapped), archiving the
# original evidence to raw/attempt1/ first. The queue is read at WAKE time so items appended
# while waiting are included. This script's own name is in agy_sweep.sh's mutex pattern, so the
# gemini auto-resume defers for its whole lifetime (no browser contention between reruns).
# Queue format (results/rerun_queue.txt), one per line:  <task> <harness> <model> <effort> <run_label>
#   harness: claude|agy|codex
set -u
cd "$(dirname "$0")"
LOG=results/env-reruns.log
echo "$(date +%H:%M:%S) launcher: waiting for the browser to be free (in-flight muse task to finish)" >> "$LOG"
until ! pgrep -f "muse_sweep.sh|muse_one.sh|muse exec" >/dev/null; do sleep 15; done
mkdir -p raw/attempt1
while read -r TASK HARNESS MODEL EFFORT RUN; do
  [ -z "${TASK:-}" ] && continue
  echo "$(date +%H:%M:%S) === rerun: $TASK $RUN ($HARNESS)" >> "$LOG"
  for f in raw/"$TASK.$RUN".*; do [ -e "$f" ] && mv "$f" "raw/attempt1/$(basename "$f")"; done
  rm -f "results/$TASK/$RUN.json" "results/$TASK/$RUN.cpu.jsonl"
  case "$HARNESS" in
    claude) env -i HOME="$HOME" PATH="$PATH" MAX_TURNS=500 ./run_one.sh "$TASK" "$MODEL" "$EFFORT" "$RUN" >> "$LOG" 2>&1 ;;
    agy)    PRINT_TIMEOUT=180m ./agy_one.sh "$TASK" "$MODEL" "$RUN" >> "$LOG" 2>&1 ;;
    codex)  ./codex_one.sh "$TASK" "$MODEL" "$EFFORT" "$RUN" >> "$LOG" 2>&1 ;;
    *)      echo "unknown harness $HARNESS" >> "$LOG" ;;
  esac
  rc=$?; [ $rc -ne 0 ] && echo "$(date +%H:%M:%S) RERUN FAILED rc=$rc: $TASK $RUN" >> "$LOG"
done < results/rerun_queue.txt
echo "$(date +%H:%M:%S) ENV RERUNS DONE" >> "$LOG"
