#!/bin/bash
# Assemble the three per-model recordings of ONE task into a labeled side-by-side race.
# The shorter clips freeze on their last frame until the slowest finishes (shows who wins).
# Usage: assemble.sh <task>   -> results/footage/<task>.race.mp4
# Requires ffmpeg. Expects results/footage/<task>.{haiku,sonnet,opus}.mp4
set -eu
cd "$(dirname "$0")"
TASK=$1
D=results/footage
H=$D/$TASK.haiku.mp4; S=$D/$TASK.sonnet.mp4; O=$D/$TASK.opus.mp4
for f in "$H" "$S" "$O"; do [ -f "$f" ] || { echo "missing $f (record it first)"; exit 1; }; done
OUT=$D/$TASK.race.mp4
W=640  # per-pane width; total 1920

# scale each to same height, pad each to the longest with a frozen last frame, label it, then hstack
ffmpeg -y -i "$H" -i "$S" -i "$O" -filter_complex "
 [0:v]scale=${W}:-2,tpad=stop=-1:stop_mode=clone,fps=30,setsar=1[a];
 [1:v]scale=${W}:-2,tpad=stop=-1:stop_mode=clone,fps=30,setsar=1[b];
 [2:v]scale=${W}:-2,tpad=stop=-1:stop_mode=clone,fps=30,setsar=1[c];
 [a]drawtext=text='HAIKU':x=(w-tw)/2:y=8:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=8[a2];
 [b]drawtext=text='SONNET':x=(w-tw)/2:y=8:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=8[b2];
 [c]drawtext=text='OPUS':x=(w-tw)/2:y=8:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=8[c2];
 [a2][b2][c2]hstack=inputs=3,
 drawtext=text='%{eif\:t\:d}s':x=w-140:y=8:fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=8[v]
" -map "[v]" -shortest -pix_fmt yuv420p -movflags +faststart "$OUT"
echo ">> $OUT"
