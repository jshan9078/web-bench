#!/bin/bash
# Resume Gemini 3.7 Flash low's remaining v2 tasks (quota reached 04:27, resets ~05:14) after every other
# pilot leg has finished. agy_autoresume probes the quota every 15 min and sweeps when available; its
# completion target is the current bundle count plus the v2 tasks still missing for this label.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
SLUG=gemini-3.7-flash-low
until grep -q "ROUND3 ALL DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_round3.sh|v2_round3_fix.sh|v2_round2_fix.sh" >/dev/null; do sleep 20; done
HAVE=$(ls results/*/$SLUG.json 2>/dev/null | wc -l | tr -d ' ')
MISSING=$(python3 -c "import harness,os; print(sum(1 for t in harness.TASKS_V2 if not os.path.exists(f'results/{t}/$SLUG.json')))")
echo "$(date +%H:%M:%S) GEMINI V2 RESUME: $MISSING v2 tasks missing; waiting for quota" >> "$LOG"
BENCH_SET=v2 WIDGET_LEVEL=2 ./agy_autoresume.sh $SLUG $((HAVE + MISSING))
echo "$(date +%H:%M:%S) GEMINI V2 RESUME DONE" >> "$LOG"
