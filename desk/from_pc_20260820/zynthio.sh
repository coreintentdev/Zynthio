#!/bin/bash
# Direct-to-VDS SSH — the no-pay lane. Save as zynthio.sh, chmod +x, run.
# Usage: ./zynthio.sh            -> drop into the VDS Hermes shell
set -e
SSH_KEY="$HOME/.ssh/zynrose"
VDS_HOST="root@5.189.143.170"
# Connection options: batch, 30s keepalive, skip host check on first
exec ssh -i "$SSH_KEY" -o BatchMode=yes -o ConnectTimeout=15 \
  -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
  "$VDS_HOST" "$@"
