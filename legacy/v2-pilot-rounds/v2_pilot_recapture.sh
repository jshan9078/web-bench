#!/bin/bash
# Fourth pilot leg: re-captures after pilot fixes, once the other legs have exited.
#  - spark-low on 58-61: first captures read the widget's /__state (now token-gated).
#  - spark-low and gemini-3.7-flash-low on 65/73: captured before the browser-only PDF rule was added.
# Originals are archived under raw/attempt1/.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
while pgrep -f "v2_pilot.sh|v2_pilot_claude.sh" >/dev/null; do sleep 20; done
echo "$(date +%H:%M:%S) RECAPTURE LEG START" >> "$LOG"
mkdir -p raw/attempt1
archive() { for f in raw/"$1.$2".*; do [ -e "$f" ] && mv "$f" "raw/attempt1/$(basename "$f")"; done; rm -f "results/$1/$2.json" "results/$1/$2.cpu.jsonl"; }
for T in 58-pixel-scan 59-spot-difference 60-form-wizard 61-grid-toggle 65-arxiv-pdf-tables 73-pdf-table-extract; do archive "$T" spark-low-val; done
for T in 65-arxiv-pdf-tables 73-pdf-table-extract; do archive "$T" gemini-3.7-flash-low; done
pkill -f "widgetapp/" 2>/dev/null; sleep 1
export BENCH_SET=v2
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) recapture muse rc=$?" >> "$LOG"
./agy_sweep.sh gemini-3.7-flash-low >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) recapture agy rc=$?" >> "$LOG"
echo "$(date +%H:%M:%S) PILOT DONE (all four legs)" >> "$LOG"
