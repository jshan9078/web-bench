#!/bin/bash
# Judge instance: runs judge_daemon.py forever against the queue (Sonnet via headless claude with the repo token).
set -eux
export DEBIAN_FRONTEND=noninteractive; apt-get install -y -qq jq >/dev/null 2>&1 || true
sudo -u ubuntu bash -lc '
  set -eux; export PATH=$HOME/.local/bin:$PATH; cd ~
  python3 -m pip install --break-system-packages --user -U boto3 botocore "botocore[crt]" >/dev/null 2>&1 || true
  for i in $(seq 1 30); do aws sts get-caller-identity >/dev/null 2>&1 && break; sleep 5; done   # wait for the instance role credentials
  aws s3 cp s3://__BUCKET__/bundle/web-bench.tar.gz /tmp/web-bench.tar.gz && mkdir -p ~/web-bench && tar -C ~/web-bench -xzf /tmp/web-bench.tar.gz
  cd ~/web-bench; mkdir -p raw results; : > results/judge_daemon.log
  export MATRIX_STORE=s3://__BUCKET__/final63 JUDGE_GH=curl
  nohup python3 judge_daemon.py >> results/judge_daemon.out 2>&1 &
  ( while :; do sleep 600; aws s3 cp results/judge_daemon.log s3://__BUCKET__/logs/judge_daemon.log >/dev/null 2>&1 || true; done ) &
  echo started'
