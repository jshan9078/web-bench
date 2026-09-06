#!/bin/bash
# Run one shard of the final-set matrix serially. Usage: run_shard.sh <pairs-file>
# Each line: "<task> <run-label>", where run-label is <config>-val[N]. The config prefix picks the runner:
#   sonnet-*/opus-*/haiku-*  -> run_one.sh (claude -p --effort)      spark13-* -> muse_one.sh (muse-spark-1.3-contributor)
#   spark-*                  -> muse_one.sh (muse-spark-1.2-contributor)  luna-* -> codex_one.sh (gpt-5.6-luna)
#   gemini-*                 -> agy_one.sh (slug = config)
# Skips runs whose raw bundle already exists, so it can be restarted. Needs the widget servers (harness
# ensure_app is called by setup), the browser daemon, and the CLIs signed in. Log: results/matrix63.log
set -u; cd "$(dirname "$0")"; F=$1; LOG=results/matrix63.log
while read -r T R; do
  [ -z "${T:-}" ] && continue
  [ -f "raw/$T.$R.json" ] && { echo "skip $T $R"; continue; }
  CFG=${R%-val*}; EFF=${CFG##*-}; FAM=${CFG%-*}
  echo "$(date +%H:%M:%S) === $T $R" | tee -a "$LOG"
  case "$FAM" in
    sonnet|opus|haiku) env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" MAX_TURNS=500 ./run_one.sh "$T" "$FAM" "$EFF" "$R" >> "$LOG" 2>&1 ;;
    spark13)           SPARK_PREFIX=spark13 ./muse_one.sh "$T" muse-spark-1.3-contributor "$EFF" "$R" >> "$LOG" 2>&1 ;;
    spark)             ./muse_one.sh "$T" muse-spark-1.2-contributor "$EFF" "$R" >> "$LOG" 2>&1 ;;
    luna)              ./codex_one.sh "$T" gpt-5.6-luna "$EFF" "$R" >> "$LOG" 2>&1 ;;
    gemini-*)          ./agy_one.sh "$T" "$CFG" "$R" >> "$LOG" 2>&1 ;;
    *) echo "unknown config $CFG" | tee -a "$LOG" ;;
  esac
  [ -f "raw/$T.$R.json" ] || echo "$(date +%H:%M:%S) RUN FAILED: $T $R" | tee -a "$LOG"
done < "$F"
echo "$(date +%H:%M:%S) SHARD DONE $F" | tee -a "$LOG"
