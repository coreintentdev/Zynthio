#!/bin/bash
echo '=== Proton Migration Status ==='
echo 'Time: 'Mon Aug 17 12:03:30 CAST 2026''
echo ''
echo 'Active rclone processes:'
ps aux | grep rclone | grep -v grep | head -5
echo ''
echo 'Latest log files:'
ls -lht /root/proton_migration_logs/*.log | head -5
echo ''
echo 'Dropbox latest:'
tail -5 /root/proton_migration_logs/dropbox_to_proton_*.log 2>/dev/null
echo ''
echo 'Proton space:'
rclone about proton: 2>/dev/null | head -5
