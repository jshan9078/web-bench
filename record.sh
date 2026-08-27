#!/bin/bash
# Record ONE headed run for footage: opens a visible Chrome window, screen-records with ffmpeg
# while `claude -p` drives it, saves results/footage/<task>.<model>.mp4 (+ the usual metrics json).
# Usage: record.sh <task> <model>
# Requires: ffmpeg, and Screen Recording permission for your terminal (System Settings > Privacy).
# First time, list capture devices to find your screen index:
#     ffmpeg -f avfoundation -list_devices true -i ""
# then set SCREEN (default "Capture screen 0"). Maximize the Chrome window for a clean frame.
set -u
cd "$(dirname "$0")"
TASK=$1; MODEL=$2
EFFORT=${EFFORT:-high}; MAX_TURNS=${MAX_TURNS:-60}
SCREEN=${SCREEN:-"Capture screen 0"}
pick_claude() {
  if [ -n "${CLAUDE_BIN:-}" ]; then echo "$CLAUDE_BIN"; return; fi
  if command -v claude >/dev/null 2>&1 && claude --help 2>&1 | grep -q -- '--effort'; then command -v claude; return; fi
  local newest; newest=$(ls -d "$HOME/Library/Application Support/Claude/claude-code/"*/claude.app/Contents/MacOS/claude 2>/dev/null | sort -V | tail -1)
  if [ -n "$newest" ] && "$newest" --help 2>&1 | grep -q -- '--effort'; then echo "$newest"; return; fi
  echo "claude"
}
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
  ENVF="$(pwd)/.env"
  if [ -f "$ENVF" ]; then
    _t=$(grep -E '^(export )?CLAUDE_CODE_OAUTH_TOKEN=' "$ENVF" | tail -1 | sed -E 's/^(export )?CLAUDE_CODE_OAUTH_TOKEN=//' | tr -d '\r' | sed -E 's/^["'"'"']//; s/["'"'"']$//')
    [ -z "$_t" ] && _t=$(grep -E '^(export )?CLAUDE_KEY=' "$ENVF" | tail -1 | sed -E 's/^(export )?CLAUDE_KEY=//' | tr -d '\r' | sed -E 's/^["'"'"']//; s/["'"'"']$//')
    [ -n "$_t" ] && export CLAUDE_CODE_OAUTH_TOKEN="$_t"
  fi
fi
CLAUDE=$(pick_claude)
EFFORT_ARG=(--effort "$EFFORT"); "$CLAUDE" --help 2>&1 | grep -q -- '--effort' || EFFORT_ARG=()
export BENCH_VISIBLE=1
export BENCH_PROFILE=${BENCH_PROFILE:-default}
PY=python3
OUT=results/footage; mkdir -p "$OUT"
MP4=$OUT/$TASK.$MODEL.mp4
CPU=results/$TASK.$MODEL-rec.cpu.jsonl

prompt=$($PY harness.py setup "$TASK") || { echo "setup failed"; exit 1; }
echo ">> window open. Maximize it, then press ENTER to start recording."; read -r _

ffmpeg -y -f avfoundation -capture_cursor 1 -framerate 30 -i "$SCREEN" \
       -pix_fmt yuv420p -movflags +faststart "$MP4" >/dev/null 2>&1 & FF=$!
$PY sample_cpu.py "$CPU" 0.25 & SAMPLER=$!

out=$("$CLAUDE" -p "$prompt" --model "$MODEL" "${EFFORT_ARG[@]}" \
        --allowedTools Bash --output-format json --max-turns "$MAX_TURNS" 2>>results/suite.log)

kill -INT $FF 2>/dev/null; wait $FF 2>/dev/null
kill $SAMPLER 2>/dev/null

text=$(printf '%s' "$out" | $PY -c "import sys,json;print(json.load(sys.stdin).get('result',''))" 2>/dev/null)
tokens=$(printf '%s' "$out" | $PY -c "import sys,json;u=json.load(sys.stdin).get('usage',{});print(sum(u.get(k,0) for k in ('input_tokens','output_tokens','cache_read_input_tokens','cache_creation_input_tokens')))" 2>/dev/null || echo 0)
ans=""; [ "$TASK" != "amazon_cart" ] && ans=$(printf '%s\n' "$text" | grep -E '^ANSWER:' | tail -1 | sed 's/^ANSWER:[[:space:]]*//')
if [ -n "$ans" ]; then CPU_SERIES=$CPU $PY harness.py verify "$TASK" "answer=$ans" "tokens=$tokens" "run=$MODEL-rec"
else CPU_SERIES=$CPU $PY harness.py verify "$TASK" "tokens=$tokens" "run=$MODEL-rec"; fi
echo ">> saved $MP4"
