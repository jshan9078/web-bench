#!/bin/bash
# Resumes the muse 1.3 chain (high from where it stopped, then xhigh, ultra) after the deferred
# fairness reruns finish. Lives in a file so its process name never matches sweep mutex patterns.
cd "$(dirname "$0")"
until grep -q "ENV RERUNS DONE" results/env-reruns.log 2>/dev/null; do sleep 30; done
for E in high xhigh ultra; do ./muse_sweep.sh $E muse-spark-1.3-contributor spark13; done
echo "ALL 1.3 TIERS DONE"
