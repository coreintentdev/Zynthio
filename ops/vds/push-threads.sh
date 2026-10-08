#!/usr/bin/env bash
# Rsync workspace threads to VDS /root/zynthio/_meta/threads/ when mesh SSH is real.
# Never paste keys. Never claim landed unless ssh_ok.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
KEY_PATH="${HOME}/.ssh/zynthio_dc"
VDS_HOST="${ZYNTHIO_VDS_HOST:-100.121.107.112}"
VDS_USER="${ZYNTHIO_VDS_USER:-root}"
DEST="/root/zynthio/_meta/threads/"

cd "$ROOT"
node --experimental-strip-types ops/vds/push-threads.ts
PLAN_OK=$?
if [[ "$PLAN_OK" -ne 0 ]]; then
  echo "BLOCKED: threads packed in git (_meta/threads/) but not landed on VDS. Add real ZYNTHIO_DC_SSH_KEY + HEADSCALE_PREAUTH_KEY in Cursor environment secrets."
  exit 2
fi

if [[ ! -f "$KEY_PATH" ]]; then
  echo "BLOCKED: ${KEY_PATH} missing after plan said ready."
  exit 2
fi

ssh -i "$KEY_PATH" -o BatchMode=yes -o ConnectTimeout=20 \
  "${VDS_USER}@${VDS_HOST}" "mkdir -p ${DEST} && echo ssh_ok"

rsync -az -e "ssh -i ${KEY_PATH} -o BatchMode=yes -o ConnectTimeout=20" \
  "${ROOT}/_meta/threads/" "${VDS_USER}@${VDS_HOST}:${DEST}"

echo "landed: ${VDS_USER}@${VDS_HOST}:${DEST}"
