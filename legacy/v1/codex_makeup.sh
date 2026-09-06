#!/bin/bash
# Codex makeups: infra-killed runs (luna TPM limit) re-captured, and wall-blocked runs retried.
set -u
cd "$(dirname "$0")"
mkdir -p raw/attempt1
run() { # task effort
  T=$1; E=$2; RUN="luna-$E-val"
  if [ -f "results/$T/$RUN.json" ]; then  # wall retry: archive old blocked bundle first
    for f in raw/$T.$RUN.*; do [ -e "$f" ] && mv "$f" "raw/attempt1/$(basename "$f")"; done
    rm -f "results/$T/$RUN.json" "results/$T/$RUN.cpu.jsonl"
  fi
  echo "=== makeup: $T $RUN $(date +%H:%M:%S)"
  ./codex_one.sh "$T" gpt-5.6-luna "$E" "$RUN" || echo "MAKEUP FAILED: $T $RUN"
  sleep 20   # let the per-minute token window breathe between heavy runs
}
run 23-amazon-filter-hunt medium
run 23-amazon-filter-hunt high
run 05-amazon-cart xhigh
run 22-amazon-earbud-compare xhigh
run 23-amazon-filter-hunt xhigh
run 23-amazon-filter-hunt max
run 26-ebay-keyboard-hunt low
run 26-ebay-keyboard-hunt medium
run 08-airport-departures medium
run 08-airport-departures max
echo "MAKEUPS DONE"
