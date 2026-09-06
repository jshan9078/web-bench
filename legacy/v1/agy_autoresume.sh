#!/bin/bash
# Self-healing auto-resume for an agy sweep across quota windows. Probes the 5-hour limit with a
# cheap call; when quota is available, runs a sweep pass (which stops cleanly on the next QUOTA hit
# via agy_sweep.sh's exit-3 handling). Repeats until all TARGET tasks are captured. Husk-safe:
# quota-failed tasks never record, so each pass only advances real captures.
# Usage: agy_autoresume.sh <model-slug> <expected-count>
set -u
cd "$(dirname "$0")"
SLUG=$1; NEED=$2; LOG=results/agy-3.8-sweep.log
probe() {  # returns 0 if quota available
  out=$(echo x | agy -p "Reply with the word OK only." --model gemini-3.8-flash-low \
        --output-format stream-json 2>/dev/null)
  echo "$out" | grep -qiE "resource_exhausted|rate limit|quota|too many requests" && return 1
  echo "$out" | grep -q '"status":"SUCCESS"' && return 0
  return 1
}
while true; do
  DONE=$(ls results/*/"$SLUG".json 2>/dev/null | wc -l | tr -d ' ')
  if [ "$DONE" -ge "$NEED" ]; then echo "$(date +%H:%M:%S) AUTORESUME: all $NEED $SLUG captured" >> "$LOG"; break; fi
  # Do not spend a probe call while another benchmark holds the browser; just wait.
  if pgrep -f "muse_sweep.sh|muse_one.sh|run_one.sh|rerun_uncapped.sh|codex_one.sh|env_rerun_launcher.sh|resume_tiers.sh" >/dev/null 2>&1; then
    sleep 900; continue
  fi
  if probe; then
    echo "$(date +%H:%M:%S) AUTORESUME: quota available ($DONE/$NEED done) - running sweep pass" >> "$LOG"
    ./agy_sweep.sh "$SLUG" >> "$LOG" 2>&1; rc=$?
    [ $rc -eq 3 ] && sleep 900   # deferred (busy) or quota hit mid-pass: back off before re-probing
  else
    echo "$(date +%H:%M:%S) AUTORESUME: quota still exhausted ($DONE/$NEED) - waiting 15m" >> "$LOG"
    sleep 900
  fi
done
