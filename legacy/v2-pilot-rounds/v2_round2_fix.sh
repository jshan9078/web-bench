#!/bin/bash
# After round 2: re-capture runs failed by harness defects found during round 2.
#  - 60-form-wizard spark-low: browser CLI text truncation (fixed and installed 03:52).
#  - 58-pixel-scan gemini-3.7-flash-low: in flight while the swapped CLI binary was unrunnable
#    (03:52:01-03:52:56, code-signature invalidation on an in-place copy; repaired with a fresh copy + ad-hoc sign).
# Defective captures are archived under raw/cli-defect/.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND2 CAPTURE DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_round2.sh" >/dev/null; do sleep 15; done
echo "$(date +%H:%M:%S) ROUND2 FIX LEG START" >> "$LOG"
mkdir -p raw/cli-defect
archive() { for f in raw/"$1.$2".*; do [ -e "$f" ] && mv "$f" "raw/cli-defect/$(basename "$f")"; done; rm -f "results/$1/$2.json" "results/$1/$2.cpu.jsonl"; }
archive 60-form-wizard spark-low-val
archive 58-pixel-scan gemini-3.7-flash-low
export BENCH_SET=v2 WIDGET_LEVEL=2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) fix leg muse rc=$?" >> "$LOG"
./agy_sweep.sh gemini-3.7-flash-low >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) fix leg agy rc=$?" >> "$LOG"
echo "$(date +%H:%M:%S) ROUND2 ALL DONE" >> "$LOG"
