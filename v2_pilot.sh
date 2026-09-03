#!/bin/bash
# v2 task pilot: two cheap strong configs, serial. Results land under results/<task>/ like any run.
set -u
cd "$(dirname "$0")"
export BENCH_SET=v2
echo "$(date +%H:%M:%S) PILOT START (spark13-medium, then gemini-3.8-flash-low)"
./muse_sweep.sh medium muse-spark-1.3-contributor spark13
echo "$(date +%H:%M:%S) muse pilot rc=$?"
./agy_sweep.sh gemini-3.8-flash-low
echo "$(date +%H:%M:%S) agy pilot rc=$?"
echo "$(date +%H:%M:%S) PILOT DONE"
