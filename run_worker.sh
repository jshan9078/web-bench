#!/bin/bash
# Fleet worker: claim -> run -> upload, until the queue is empty. Usage: run_worker.sh <worker-name> [lane] [family]
#   family: comma-separated config prefixes (spark13,sonnet,opus,gemini-3.8-flash,luna) so parallel workers hit different providers
#   lane: local (default on the fleet) | realsite | all.  Env: MATRIX_STORE=s3://bucket/prefix, DRY=1 to fake runs.
# Idempotent: a claimed item whose bundle exists is completed without re-running; leases are heartbeated every
# 60 s so a dead worker's items are reclaimed after LEASE_S (default 1500 s).
set -u; cd "$(dirname "$0")"; W=${1:-$(hostname)}; LANE=${2:-local}; FAMILY=${3:-${FAMILY:-all}}; LOG=results/matrix63.log; Q="python3 matrix_queue.py"
LANEARG=(); [ "$LANE" != all ] && LANEARG=(--lane "$LANE"); [ "$FAMILY" != all ] && LANEARG+=(--family "$FAMILY")
while :; do
  read -r T R < <($Q claim "$W" "${LANEARG[@]}")
  [ -z "${T:-}" ] && { echo "$(date +%H:%M:%S) queue empty for lane $LANE" | tee -a "$LOG"; break; }
  echo "$(date +%H:%M:%S) === $T $R ($W)" | tee -a "$LOG"
  ( while :; do sleep 60; $Q heartbeat "$T" "$R" "$W" >/dev/null 2>&1 || true; done ) & HB=$!
  if [ ! -f "raw/$T.$R.json" ]; then
    CFG=${R%-val*}; EFF=${CFG##*-}; FAM=${CFG%-*}
    if [ "${DRY:-0}" = 1 ]; then mkdir -p "results/$T"; echo '{"dry":true}' > "raw/$T.$R.json"; echo '{"pixel_state":{"complete":false}}' > "results/$T/$R.json"; sleep 1
    else case "$FAM" in
      sonnet|opus|haiku) env -i HOME="$HOME" PATH="$PATH" TMPDIR="${TMPDIR:-}" MAX_TURNS=500 ./run_one.sh "$T" "$FAM" "$EFF" "$R" >> "$LOG" 2>&1 ;;
      spark13)           SPARK_PREFIX=spark13 ./muse_one.sh "$T" muse-spark-1.3-contributor "$EFF" "$R" >> "$LOG" 2>&1 ;;
      spark)             ./muse_one.sh "$T" muse-spark-1.2-contributor "$EFF" "$R" >> "$LOG" 2>&1 ;;
      luna)              ./codex_one.sh "$T" gpt-5.6-luna "$EFF" "$R" >> "$LOG" 2>&1 ;;
      gemini-*)          ./agy_one.sh "$T" "$CFG" "$R" >> "$LOG" 2>&1 ;;
      *) echo "unknown config $CFG" | tee -a "$LOG" ;;
    esac; fi
  fi
  kill $HB 2>/dev/null; wait $HB 2>/dev/null
  if [ ! -f "raw/$T.$R.json" ]; then $Q complete "$T" "$R" "$W" --error "no raw bundle (harness failure)" | tee -a "$LOG"
  elif python3 - "$T" "$R" <<'PY'
import json,sys; t,r=sys.argv[1:3]; d=json.load(open(f"raw/{t}.{r}.json")); txt=(d.get("agent_result_text") or "")
sys.exit(0 if ("BLOCKED:" in txt or "Verify you are human" in txt or "Whoa there" in txt) else 1)
PY
  then $Q complete "$T" "$R" "$W" --blocked | tee -a "$LOG"
  else $Q complete "$T" "$R" "$W" | tee -a "$LOG"; fi
done
