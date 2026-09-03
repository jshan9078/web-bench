#!/bin/bash
# After round 3: redo 74-dashboard-triage for spark-low. Its first capture ran before the prompt stated the
# no-endpoints rule (it solved the task via fetch('/__data'), which the guard fails); archived under raw/prompt-fix/.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND3 CAPTURE DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_round3.sh" >/dev/null; do sleep 15; done
echo "$(date +%H:%M:%S) ROUND3 FIX LEG START (spark-low 74 redo)" >> "$LOG"
mkdir -p raw/prompt-fix
for f in raw/74-dashboard-triage.spark-low-val.*; do [ -e "$f" ] && mv "$f" "raw/prompt-fix/$(basename "$f")"; done
rm -f results/74-dashboard-triage/spark-low-val.json results/74-dashboard-triage/spark-low-val.cpu.jsonl
export BENCH_SET=v2 WIDGET_LEVEL=2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND3 FIX LEG rc=$?" >> "$LOG"
echo "$(date +%H:%M:%S) ROUND3 ALL DONE" >> "$LOG"
