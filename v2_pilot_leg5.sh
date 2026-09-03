#!/bin/bash
# Fifth pilot leg: redo 59-spot-difference for spark-low (its re-capture died when muse_one.sh was
# patched mid-run: bash executes scripts incrementally). Runs after the re-capture leg, still at widget
# level 1 so round 1 stays comparable. muse_sweep skips every task that already has a bundle.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
while pgrep -f "v2_pilot_recapture.sh" >/dev/null; do sleep 15; done
echo "$(date +%H:%M:%S) LEG5 START (spark-low 59 redo, level 1)" >> "$LOG"
pkill -f "widgetapp/" 2>/dev/null; sleep 1
BENCH_SET=v2 ./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) LEG5 rc=$?" >> "$LOG"
echo "$(date +%H:%M:%S) ROUND1 CAPTURE DONE" >> "$LOG"
