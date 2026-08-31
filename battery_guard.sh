#!/bin/bash
# Battery watchdog for benchmark sweeps. Checks every 60s; if the machine is discharging at or
# below MIN% (default 10), it stops ALL benchmark processes (sweep loop, agent runs, recorder,
# CPU sampler, daemon Chrome) and writes BATTERY_STOP so no automation restarts anything.
# Patterns are scoped to benchmark processes only: the user's personal Chrome and interactive
# Claude session are untouched.
MIN=${1:-10}
cd "$(dirname "$0")"
echo "[battery_guard] armed: stop threshold ${MIN}%, checking every 60s"
while true; do
  out=$(pmset -g batt)
  pct=$(echo "$out" | grep -o '[0-9]\{1,3\}%' | head -1 | tr -d '%')
  if echo "$out" | grep -q discharging && [ -n "$pct" ] && [ "$pct" -le "$MIN" ]; then
    {
      echo "BATTERY_STOP $(date '+%Y-%m-%d %H:%M:%S') at ${pct}% discharging"
      echo "Benchmark halted by battery_guard.sh. Delete this file and rerun the pending phase to resume."
    } | tee BATTERY_STOP
    pkill -f run_matrix.sh
    pkill -f run_one.sh
    pkill -f agy_one.sh
    pkill -f 'agy -p'
    pkill -f 'dangerously-skip-permissions'   # bench `claude -p` runs only
    pkill -f record_cdp.py
    pkill -f sample_cpu.py
    pkill -f 'user-data-dir=.*browser-daemon' # daemon Chrome, never the personal Chrome
    pkill -f browser-daemon
    echo "[battery_guard] all benchmark processes stopped at ${pct}%"
    exit 0
  fi
  sleep 60
done
