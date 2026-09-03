#!/bin/bash
# v2 task pilot, serial: Muse Spark 1.2 low, then Gemini 3.7 Flash low. (Sonnet 5 low runs from the
# user's own terminal: BENCH_SET=v2 ./sweep.sh sonnet low   -- see README.)
set -u
cd "$(dirname "$0")"
export BENCH_SET=v2
echo "$(date +%H:%M:%S) PILOT START (spark-low, then gemini-3.7-flash-low)"
./muse_sweep.sh low muse-spark-1.2-contributor spark
echo "$(date +%H:%M:%S) muse pilot rc=$?"
./agy_sweep.sh gemini-3.7-flash-low
echo "$(date +%H:%M:%S) agy pilot rc=$?"
echo "$(date +%H:%M:%S) PILOT DONE"
