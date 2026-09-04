#!/bin/bash
# Seed-instance bootstrap (Ubuntu 24.04). Installs everything that needs no personal login. After it finishes, the
# operator SSHes in, signs in the agent CLIs (claude, muse, codex, agy) as ubuntu, verifies each, and makes the AMI.
set -eux
export DEBIAN_FRONTEND=noninteractive
apt-get update && apt-get install -y python3-pip python3-venv git curl unzip jq ffmpeg fonts-dejavu-core \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2t64 libpango-1.0-0 libcairo2 libxfixes3 libxshmfence1
curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip && unzip -q /tmp/awscliv2.zip -d /tmp && /tmp/aws/install
sudo -u ubuntu bash -lc '
  set -eux; cd ~
  pip3 install --break-system-packages --user pillow numpy boto3 "botocore[crt]" websockets
  mkdir -p ~/.local/bin; echo "export PATH=\$HOME/.local/bin:\$PATH" >> ~/.bashrc
  curl -fsSL https://raw.githubusercontent.com/jshan9078/browser-automation-cli/main/install.sh | BROWSER_CLI_BIN=$HOME/.local/bin sh
  PATH=$HOME/.local/bin:$PATH browser install
  npm config set prefix ~/.local; npm install -g @anthropic-ai/claude-code @openai/codex
  aws s3 cp s3://__BUCKET__/bundle/web-bench.tar.gz /tmp/web-bench.tar.gz && mkdir -p ~/web-bench && tar -C ~/web-bench -xzf /tmp/web-bench.tar.gz
  echo "SEED BOOTSTRAP DONE" > ~/SEED_DONE'
