#!/usr/bin/env bash
# PUSH_TO_VDS_336 — ship Cowork canon (incident + verify + scripts) to the VDS
#
# Default target: Tailscale path for Contabo per zero-trust doctrine
# (VPS direct IPs are firewalled — UFW closed to public per Gemini Sovereign spec).
#
# Default Tailscale host: root@vmi3205024 (preferred current host).
# Override with VDS_HOST=root@<host> when needed.
#
# Default key: ~/.ssh/zynthio_dc, falls back to ~/.ssh/id_ed25519.
# Default path: /root/zynthio/cowork/
#
# Override any of:
#   VDS_HOST=root@<host_or_ip> VDS_PATH=/root/zynthio/cowork/ SSH_KEY=~/.ssh/zynthio_dc \
#     bash push_to_vds_336.sh
#
# Run from Mac iTerm — sandbox cannot SSH.
# macOS bash 3.2 compatible (no mapfile, no set -u on arrays).

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
VDS_HOST="${VDS_HOST:-root@vmi3205024}"
VDS_PATH="${VDS_PATH:-/root/zynthio/cowork/}"

# Pick the first existing SSH key
KEY=""
if [ -n "${SSH_KEY:-}" ] && [ -f "${SSH_KEY:-}" ]; then
  KEY="$SSH_KEY"
elif [ -f "$HOME/.ssh/zynthio_dc" ]; then
  KEY="$HOME/.ssh/zynthio_dc"
elif [ -f "$HOME/.ssh/id_ed25519" ]; then
  KEY="$HOME/.ssh/id_ed25519"
else
  echo "ERROR: no SSH key found at ~/.ssh/zynthio_dc or ~/.ssh/id_ed25519. Set SSH_KEY=path." >&2
  exit 1
fi

# Resolve the file set (portable — bash 3.2 friendly, no mapfile)
RESOLVED=()
while IFS= read -r f; do
  [ -n "$f" ] && [ -f "$f" ] && RESOLVED+=("$f")
done < <(
  ls -1 "$DIR/INCIDENT_COWORK_"*.md      2>/dev/null
  ls -1 "$DIR/COWORK_VERIFY_336_"*.md    2>/dev/null
  ls -1 "$DIR/verify_336.sh"             2>/dev/null
  ls -1 "$DIR/push_to_vds_336.sh"        2>/dev/null
)

if [ "${#RESOLVED[@]}" -eq 0 ]; then
  echo "ERROR: no canon files found in $DIR" >&2
  echo "Expected at least: INCIDENT_COWORK_*.md, verify_336.sh, push_to_vds_336.sh" >&2
  exit 1
fi

echo "============================================"
echo "PUSH TO VDS"
echo "============================================"
echo "Host: $VDS_HOST"
echo "Path: $VDS_PATH"
echo "Key:  $KEY"
echo "Files: ${#RESOLVED[@]}"
for f in "${RESOLVED[@]}"; do echo "  - $(basename "$f")"; done
echo

# Ensure remote dir exists
echo "Ensuring remote dir..."
ssh -i "$KEY" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 "$VDS_HOST" "mkdir -p $VDS_PATH" || {
  echo "ERROR: ssh failed. Verify VDS_HOST=$VDS_HOST and SSH key works:" >&2
  echo "  ssh -i $KEY $VDS_HOST 'echo ok'" >&2
  exit 1
}

# Ship via rsync if available, else scp
echo "Shipping..."
if command -v rsync >/dev/null 2>&1; then
  rsync -avz --progress \
    -e "ssh -i $KEY -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10" \
    "${RESOLVED[@]}" "$VDS_HOST:$VDS_PATH"
else
  scp -i "$KEY" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 \
    "${RESOLVED[@]}" "$VDS_HOST:$VDS_PATH"
fi

# Confirm
echo
echo "============================================"
echo "POSTED TO VDS"
echo "============================================"
ssh -i "$KEY" "$VDS_HOST" "ls -la $VDS_PATH"

# Tag a local manifest of what was shipped
MANIFEST="$DIR/PUSH_MANIFEST_$(date -u +%Y%m%d_%H%M).txt"
{
  echo "# Cowork push manifest — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "# Target: $VDS_HOST:$VDS_PATH"
  echo "# Key:    $KEY"
  echo
  for f in "${RESOLVED[@]}"; do
    sz=$(wc -c < "$f" | tr -d ' ')
    sha=$(shasum -a 256 "$f" 2>/dev/null | awk '{print $1}')
    printf "%s\t%sB\t%s\n" "$(basename "$f")" "$sz" "$sha"
  done
} > "$MANIFEST"

echo
echo "Local manifest: $MANIFEST"
echo
echo "336."
