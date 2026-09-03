#!/bin/bash
# After round 2: re-capture the one run failed by the browser CLI text-truncation defect (fixed and
# installed during round 2): 60-form-wizard for spark-low. Archives the defective capture under raw/cli-defect/.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND2 CAPTURE DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_round2.sh" >/dev/null; do sleep 15; done
echo "$(date +%H:%M:%S) ROUND2 FIX LEG START (spark-low 60 redo after CLI fix)" >> "$LOG"
mkdir -p raw/cli-defect
for f in raw/60-form-wizard.spark-low-val.*; do [ -e "$f" ] && mv "$f" "raw/cli-defect/$(basename "$f")"; done
rm -f results/60-form-wizard/spark-low-val.json results/60-form-wizard/spark-low-val.cpu.jsonl
export BENCH_SET=v2 WIDGET_LEVEL=2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND2 FIX LEG rc=$?" >> "$LOG"
echo "$(date +%H:%M:%S) ROUND2 ALL DONE" >> "$LOG"
