#!/bin/bash
# Re-captures the two JS Paint reruns whose final-state evidence the harness failed to preserve
# (no video + /tmp screenshot overwritten by a later run). Waits for the 1.3 tiers to finish, then
# runs them through env_rerun_launcher.sh (whose name holds the sweep mutex, so gemini defers).
cd "$(dirname "$0")"
until grep -q "ALL 1.3 TIERS DONE" results/spark13-tiers-sweep.log 2>/dev/null; do sleep 60; done
printf '%s\n' "36-jspaint-poster claude opus xhigh opus-xhigh-val" "36-jspaint-poster claude sonnet medium sonnet-medium-val" > results/rerun_queue.txt
echo "$(date +%H:%M:%S) recapture_jspaint: tiers done, launching 2 re-captures" >> results/env-reruns.log
./env_rerun_launcher.sh
