#!/usr/bin/env bash
# Deploy Bondzee artist pages → bondzee.live + bondzee.bond (shared vhost root)
set -euo pipefail

VDS="${VDS:-100.64.0.2}"
DEPLOY_USER="${DEPLOY_USER:-root}"
KEY="${KEY:-$HOME/.ssh/zynthio_dc}"
LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)"
SHARED_LOCAL="$(cd "$LOCAL_DIR/../_shared" && pwd)"
REMOTES=("/var/www/bondzee.bond" "/var/www/bondzee.live")

CONF_LOCAL="$LOCAL_DIR/pork_bondzee_lookcy.conf"
if [[ -f "$CONF_LOCAL" ]]; then
  echo "=== nginx vhost (fixes HTTPS Brisas bleed) ==="
  scp -i "$KEY" "$CONF_LOCAL" "$DEPLOY_USER@$VDS:/etc/nginx/sites-available/pork_bondzee_lookcy.conf"
  ssh -i "$KEY" "$DEPLOY_USER@$VDS" "ln -sf /etc/nginx/sites-available/pork_bondzee_lookcy.conf /etc/nginx/sites-enabled/pork_bondzee_lookcy.conf && nginx -t && systemctl reload nginx"
fi

for REMOTE in "${REMOTES[@]}"; do
  echo "=== Bondzee deploy → $DEPLOY_USER@$VDS:$REMOTE ==="
  ssh -i "$KEY" "$DEPLOY_USER@$VDS" "mkdir -p $REMOTE/stack $REMOTE/song $REMOTE/i18n /var/www/zyn-shared"
  rsync -avz -e "ssh -i $KEY" "$SHARED_LOCAL/zyn-evolve-i18n.js" "$SHARED_LOCAL/zyn-evolve-i18n.css" "$DEPLOY_USER@$VDS:/var/www/zyn-shared/"
  rsync -avz -e "ssh -i $KEY" \
    "$LOCAL_DIR/index.html" \
    "$DEPLOY_USER@$VDS:$REMOTE/index.html"
  rsync -avz -e "ssh -i $KEY" \
    "$LOCAL_DIR/stack/index.html" \
    "$DEPLOY_USER@$VDS:$REMOTE/stack/index.html"
  rsync -avz -e "ssh -i $KEY" \
    "$LOCAL_DIR/song/index.html" \
    "$DEPLOY_USER@$VDS:$REMOTE/song/index.html"
  rsync -avz -e "ssh -i $KEY" \
    "$LOCAL_DIR/i18n/manifest.json" \
    "$DEPLOY_USER@$VDS:$REMOTE/i18n/manifest.json"
done

echo ""
echo "✅ Live (purge CF cache if placeholder persists):"
echo "   https://bondzee.live/"
echo "   https://bondzee.bond/"
echo "   https://bondzee.live/stack/"
echo "   https://bondzee.live/song/"
echo ""
echo "Walkthrough: corey@zynthio.ai"