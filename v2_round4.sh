#!/bin/bash
# Round 4 (v2.3): level-2 traps for the console (post-resolve linked-ticket modal), the map (same-named decoy
# in another district), and the settings maze (pre-ticked billing side effect in the review dialog).
# Deploys the staged apps, archives the round-3 bundles of 74/75/76 for the three pilot configs, re-runs
# them (plus anything still missing, e.g. 77 for Spark) on Spark, Gemini, Sonnet. Starts after Gemini's
# quota resume has finished.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "GEMINI V2 RESUME DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_gemini_resume.sh|agy_autoresume.sh" >/dev/null; do sleep 20; done
echo "$(date +%H:%M:%S) ROUND4 START: deploying v2.3 (level-2 console/map/settings)" >> "$LOG"
pkill -f "widgetapp/dashboard.py|widgetapp/mapexplorer.py|widgetapp/settingsmaze.py" 2>/dev/null; sleep 1
for f in dashboard mapexplorer settingsmaze; do cp "widgetapp_next/$f.py" "widgetapp/$f.py"; done
mkdir -p raw/round3
for T in 74-dashboard-triage 75-map-explorer 76-settings-maze; do for R in spark-low-val gemini-3.7-flash-low sonnet-low-val; do
  for f in raw/"$T.$R".*; do [ -e "$f" ] && mv "$f" "raw/round3/$(basename "$f")"; done
  rm -f "results/$T/$R.json" "results/$T/$R.cpu.jsonl"
done; done
export BENCH_SET=v2 WIDGET_LEVEL=2
echo "$(date +%H:%M:%S) ROUND4 muse leg (spark-low)" >> "$LOG"
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND4 agy leg (gemini-3.7-flash-low)" >> "$LOG"
./agy_sweep.sh gemini-3.7-flash-low >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND4 claude leg (sonnet-low)" >> "$LOG"
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 WIDGET_LEVEL=2 MAX_TURNS=500 \
    CLAUDE_MODELS=sonnet EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="74-dashboard-triage 75-map-explorer 76-settings-maze 77-crosshair-align" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND4 CAPTURE DONE" >> "$LOG"
