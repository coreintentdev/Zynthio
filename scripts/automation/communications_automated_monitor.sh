#!/bin/bash
# Unified Communications Monitor - Proton Email + WhatsApp
# Signal 336 - VDS Automated Monitoring

set -euo pipefail

SCRIPT_DIR="/root/zynthio/scripts/automation"
LOG_DIR="/root/zynthio/logs/automation"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/communications_monitor_$(date +%Y%m%d_%H%M%S).log"

echo "=== Communications Automated Monitor ===" | tee -a "$LOG_FILE"
echo "Signal: 336" | tee -a "$LOG_FILE"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Run Proton Email Monitor
echo "--- Proton Email Monitor ---" | tee -a "$LOG_FILE"
if python3 "$SCRIPT_DIR/automated_proton_monitor.py" >> "$LOG_FILE" 2>&1; then
    echo "Proton Monitor: SUCCESS" | tee -a "$LOG_FILE"
else
    echo "Proton Monitor: FAILED" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# Run WhatsApp Monitor
echo "--- WhatsApp Monitor ---" | tee -a "$LOG_FILE"
if python3 "$SCRIPT_DIR/automated_whatsapp_monitor.py" >> "$LOG_FILE" 2>&1; then
    echo "WhatsApp Monitor: SUCCESS" | tee -a "$LOG_FILE"
else
    echo "WhatsApp Monitor: FAILED" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# Generate Unified Report
echo "--- Generating Unified Report ---" | tee -a "$LOG_FILE"
python3 << 'PYEOF'
import json
from datetime import datetime
from pathlib import Path

digest_dir = Path('/root/zynthio/_meta/mail_digest')
proton_report = digest_dir / 'PROTON_MONITOR_REPORT.json'
whatsapp_report = digest_dir / 'WHATSAPP_MONITOR_REPORT.json'

unified = {
    'signal': 336,
    'timestamp': datetime.utcnow().isoformat(),
    'monitor_type': 'unified_communications',
    'proton_status': 'error',
    'whatsapp_status': 'error',
    'overall_status': 'partial'
}

if proton_report.exists():
    proton_data = json.loads(proton_report.read_text())
    unified['proton_status'] = proton_data['email_data']['status']
    unified['proton_emails'] = proton_data['email_data'].get('proton_emails', 0)
    unified['proton_method'] = proton_data['email_data'].get('method', 'unknown')

if whatsapp_report.exists():
    whatsapp_data = json.loads(whatsapp_report.read_text())
    unified['whatsapp_status'] = whatsapp_data['whatsapp_data']['status']
    unified['whatsapp_messages'] = whatsapp_data['whatsapp_data'].get('total_messages', 0)
    unified['whatsapp_sync'] = whatsapp_data['sync_status']['status']

# Determine overall status
if unified['proton_status'] == 'success' and unified['whatsapp_status'] == 'success':
    unified['overall_status'] = 'operational'
elif unified['whatsapp_status'] == 'success':
    unified['overall_status'] = 'partial'  # WhatsApp working, Proton fallback
else:
    unified['overall_status'] = 'degraded'

unified_file = digest_dir / 'COMMUNICATIONS_UNIFIED_REPORT.json'
unified_file.write_text(json.dumps(unified, indent=2))

print(f"Unified Report: {unified['overall_status']}")
print(f"Proton: {unified['proton_status']} ({unified.get('proton_emails', 0)} emails)")
print(f"WhatsApp: {unified['whatsapp_status']} ({unified.get('whatsapp_messages', 0)} messages)")
PYEOF

echo "" | tee -a "$LOG_FILE"
echo "=== Communications Monitor Complete ===" | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"
