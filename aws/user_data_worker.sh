#!/bin/bash
# Fleet worker bootstrap (instance launched from the baked AMI): refresh the repo bundle, start the browser daemon,
# run the queue worker as ubuntu until the lane is empty, upload the log, then shut down (terminate).
set -eux
sudo -u ubuntu bash -lc '
  set -eux; export PATH=$HOME/.local/bin:$PATH; cd ~
  python3 -m pip install --break-system-packages --user -U boto3 botocore "botocore[crt]" >/dev/null 2>&1 || true   # the apt botocore predates S3 conditional writes
  python3 -c "import botocore,sys; print(\"botocore\", botocore.__version__)"
  aws s3 cp s3://__BUCKET__/bundle/web-bench.tar.gz /tmp/web-bench.tar.gz && mkdir -p ~/web-bench && tar -C ~/web-bench -xzf /tmp/web-bench.tar.gz
  cd ~/web-bench; mkdir -p raw results
  nohup browser daemon --auto > ~/daemon.log 2>&1 &
  sleep 3
  export MATRIX_STORE=s3://__BUCKET__/final63 LEASE_S=1500
  TOK=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 300" || true)
  W=$(curl -s -H "X-aws-ec2-metadata-token: $TOK" http://169.254.169.254/latest/meta-data/instance-id || true); W=${W:-$(hostname)}
  ./run_worker.sh "$W" __LANE__ __FAMILY__ > ~/worker.log 2>&1 || true
  aws s3 cp ~/worker.log s3://__BUCKET__/logs/$W.worker.log || true'
__SHUTDOWN__
