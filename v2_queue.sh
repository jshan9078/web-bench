#!/bin/bash
# Run an iteration after a log marker appears. Usage: v2_queue.sh "<marker>" <tag> <task...>
set -u; cd "$(dirname "$0")"; M=$1; shift
until grep -q "$M" results/v2-pilot.log; do sleep 20; done
exec ./v2_iter.sh "$@"
