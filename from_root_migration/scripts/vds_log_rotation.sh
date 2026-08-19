#!/bin/bash
# VDS Log Rotation Script
# Automatically rotates and compresses old logs to prevent disk fill
# Setup: Copy to VDS /root/scripts/ and add to crontab (daily)

set -euo pipefail

LOG_DIR="/var/log"
KEEP_DAYS=7
COMPRESS_AFTER_DAYS=2
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "[$TIMESTAMP] Starting log rotation" >> /var/log/log_rotation.log

# Rotate and compress nginx logs
if [ -d "$LOG_DIR/nginx" ]; then
    find "$LOG_DIR/nginx" -name "*.log" -type f -mtime +${KEEP_DAYS} -delete
    find "$LOG_DIR/nginx" -name "*.log" -type f -mtime +${COMPRESS_AFTER_DAYS} -exec gzip {} \;
    echo "[$TIMESTAMP] Rotated nginx logs" >> /var/log/log_rotation.log
fi

# Rotate system logs
find "$LOG_DIR" -name "*.log" -type f -mtime +${KEEP_DAYS} -delete
find "$LOG_DIR" -name "*.log.[0-9]" -type f -mtime +${KEEP_DAYS} -delete

# Clean journal logs (systemd)
journalctl --vacuum-time=7d

# Clean temp files
find /tmp -type f -mtime +7 -delete 2>/dev/null || true

echo "[$TIMESTAMP] Log rotation complete" >> /var/log/log_rotation.log