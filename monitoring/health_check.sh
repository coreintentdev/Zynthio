#!/bin/bash
LOG_FILE='/root/zynthio/monitoring/health.log'
ALERT_FILE='/root/zynthio/monitoring/alerts.log'
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting health check..." >> $LOG_FILE

DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "[$TIMESTAMP] ALERT: Disk usage at $DISK_USAGE%" >> $ALERT_FILE
    echo "[$TIMESTAMP] CRITICAL: Disk usage at $DISK_USAGE%" >> $LOG_FILE
else
    echo "[$TIMESTAMP] OK: Disk usage at $DISK_USAGE%" >> $LOG_FILE
fi

MEM_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3*100/$2}')
if [ $MEM_USAGE -gt 90 ]; then
    echo "[$TIMESTAMP] ALERT: Memory usage at $MEM_USAGE%" >> $ALERT_FILE
    echo "[$TIMESTAMP] CRITICAL: Memory usage at $MEM_USAGE%" >> $LOG_FILE
else
    echo "[$TIMESTAMP] OK: Memory usage at $MEM_USAGE%" >> $LOG_FILE
fi

SERVICES=("nginx" "search-app.service" "rag-search.service" "fail2ban" "hermes-gateway.service")
for service in "${SERVICES[@]}"; do
    if systemctl is-active --quiet "$service"; then
        echo "[$TIMESTAMP] OK: $service is running" >> $LOG_FILE
    else
        echo "[$TIMESTAMP] ALERT: $service is not running" >> $ALERT_FILE
        echo "[$TIMESTAMP] CRITICAL: $service is not running" >> $LOG_FILE
    fi
done

if [ -f '/root/zynthio/corpus/corpus_FINAL_20260820.index' ]; then
    echo "[$TIMESTAMP] OK: Corpus file exists" >> $LOG_FILE
else
    echo "[$TIMESTAMP] ALERT: Corpus file missing" >> $ALERT_FILE
    echo "[$TIMESTAMP] CRITICAL: Corpus file missing" >> $LOG_FILE
fi

echo "[$TIMESTAMP] Health check complete" >> $LOG_FILE
