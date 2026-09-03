#!/bin/bash
# Round 2 of the v2 pilot: deploy the level-2 widgets and prompts (v2.1), archive the round-1 bundles of the
# seven changed tasks (58-61, 63, 64, 68) for the three pilot configs, and re-run those tasks on all three.
# Starts only after round-1 capture is complete (marker in the pilot log) and no pilot leg is running.
set -u
cd "$(dirname "$0")"
LOG=results/v2-pilot.log
until grep -q "ROUND1 CAPTURE DONE" "$LOG" 2>/dev/null && ! pgrep -f "v2_pilot_recapture.sh|v2_pilot_leg5.sh" >/dev/null; do sleep 15; done
echo "$(date +%H:%M:%S) ROUND2 START: deploying v2.1 (level-2 widgets + trap prompts)" >> "$LOG"
pkill -f "widgetapp/" 2>/dev/null; sleep 1
for f in pixelscan spotdiff wizard gridtoggle base; do cp "widgetapp_next/$f.py" "widgetapp/$f.py"; done
for T in 58-pixel-scan 59-spot-difference 60-form-wizard 61-grid-toggle; do cp "tasks_next/$T/prompt.txt" "tasks/$T/prompt.txt"; done
python3 - <<'PY'
import re
for t in ('58-pixel-scan','59-spot-difference','60-form-wizard','61-grid-toggle'):
    p=open(f'tasks/{t}/prompt.txt').read().strip(); m=f'tasks/{t}/task.md'; ms=open(m).read()
    ms=re.sub(r'```\n.*?\n```', '```\n'+p+'\n```', ms, count=1, flags=re.S); open(m,'w').write(ms)
PY
CHANGED="58-pixel-scan 59-spot-difference 60-form-wizard 61-grid-toggle 63-wikipedia-edit-audit 64-hn-comment-census 68-youtube-transcript"
mkdir -p raw/round1
for T in $CHANGED; do for R in spark-low-val gemini-3.7-flash-low sonnet-low-val spark13-medium-val; do
  for f in raw/"$T.$R".*; do [ -e "$f" ] && mv "$f" "raw/round1/$(basename "$f")"; done
  rm -f "results/$T/$R.json" "results/$T/$R.cpu.jsonl"
done; done
export BENCH_SET=v2
export WIDGET_LEVEL=2
echo "$(date +%H:%M:%S) ROUND2 muse leg (spark-low)" >> "$LOG"
./muse_sweep.sh low muse-spark-1.2-contributor spark >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND2 agy leg (gemini-3.7-flash-low)" >> "$LOG"
./agy_sweep.sh gemini-3.7-flash-low >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND2 claude leg (sonnet-low)" >> "$LOG"
env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" BENCH_SET=v2 WIDGET_LEVEL=2 MAX_TURNS=500 \
    CLAUDE_MODELS=sonnet EFFORTS=low SKIP_AGY=1 RUN_TAG=val TASKS="$CHANGED" ./run_matrix.sh 1 >> "$LOG" 2>&1
echo "$(date +%H:%M:%S) ROUND2 CAPTURE DONE" >> "$LOG"
