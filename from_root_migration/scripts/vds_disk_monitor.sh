#!/bin/bash
# VDS Disk Monitoring Script
# Alerts when disk usage reaches critical thresholds
# Setup: Copy to VDS /root/scripts/ and add to crontab

set -euo pipefail

THRESHOLD_WARNING=70
THRESHOLD_CRITICAL=80
THRESHOLD_EMERGENCY=90
LOG_FILE="/var/log/vds_disk_monitor.log"
ALERT_FILE="/root/handover/disk_alert_$(date +%Y%m%d_%H%M%S).stamp"

# Get disk usage percentage
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_AVAILABLE=$(df -h / | awk 'NR==2 {print $4}')
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

log_alert() {
    local level="$1"
    local message="$2"
    echo "[$TIMESTAMP] [$level] Disk usage: ${DISK_USAGE}% | Available: ${DISK_AVAILABLE} | $message" >> "$LOG_FILE"
    echo "$message" > "$ALERT_FILE"
}

if [ "$DISK_USAGE" -ge "$THRESHOLD_EMERGENCY" ]; then
    log_alert "EMERGENCY" "Disk usage at ${DISK_USAGE}% - IMMEDIATE ACTION REQUIRED"
    # SMS alert (Twilio) - wired 2026-08-15 after 3 days >95% with 0 delivery
    for f in /root/.zynthio.env; do
      [ -f "$f" ] && while IFS="=" read -r k v; do case "$k" in TWILIO_ACCOUNT_SID|TWILIO_AUTH_TOKEN|TWILIO_PHONE_NUMBER|SMS_HOME_CHANNEL) export "$k=$v";; esac; done < "$f"
    done
    curl -s -X POST "https://api.twilio.com/2010-04-01/Accounts/${TWILIO_ACCOUNT_SID}/Messages.json"       --data-urlencode "Body=DISK EMERGENCY: ${DISK_USAGE}% used (${DISK_AVAILABLE} free). VDS crash risk. Check now."       --data-urlencode "To=${SMS_HOME_CHANNEL:-}" --data-urlencode "From=${TWILIO_PHONE_NUMBER:-}"       -u "${TWILIO_ACCOUNT_SID}:${TWILIO_AUTH_TOKEN}" > /dev/null 2>&1 && echo "SMS_SENT ${DISK_USAGE}%" >> "$LOG_FILE"
elif [ "$DISK_USAGE" -ge "$THRESHOLD_CRITICAL" ]; then
    log_alert "CRITICAL" "Disk usage at ${DISK_USAGE}% - Critical threshold reached"
elif [ "$DISK_USAGE" -ge "$THRESHOLD_WARNING" ]; then
    log_alert "WARNING" "Disk usage at ${DISK_USAGE}% - Warning threshold reached"
else
    # Normal - just log status
    echo "[$TIMESTAMP] [INFO] Disk usage: ${DISK_USAGE}% | Available: ${DISK_AVAILABLE}" >> "$LOG_FILE"
fi

echo "Disk monitoring complete: ${DISK_USAGE}% used, ${DISK_AVAILABLE} available"