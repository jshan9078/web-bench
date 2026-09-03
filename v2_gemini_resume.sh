#!/bin/bash
# Resume Gemini 3.7 Flash low's remaining v2 tasks (quota reached 04:27, resets ~05:14) after every other
# pilot leg has finished; agy_autoresume probes the quota every 15 min and runs the sweep when available.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND3 ALL DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_round3.sh|v2_round3_fix.sh|v2_round2_fix.sh" >/dev/null; do sleep 20; done
echo "$(date +%H:%M:%S) GEMINI V2 RESUME: waiting for quota, then sweeping the missing v2 tasks" >> "$LOG"
BENCH_SET=v2 WIDGET_LEVEL=2 ./agy_autoresume.sh gemini-3.7-flash-low 61
echo "$(date +%H:%M:%S) GEMINI V2 RESUME DONE" >> "$LOG"
