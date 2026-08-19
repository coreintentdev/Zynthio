#!/bin/bash
# delta light-lane: fleet watchdog - checks VDS + alpha every 10min
LOG=/var/log/delta_watchdog.log
NOW=$(date -u +%H:%M:%SZ)
VDS=$(timeout 6 bash -c "echo > /dev/tcp/5.189.143.170/22" 2>/dev/null && echo UP || echo DOWN)
ALPHA=$(timeout 6 bash -c "echo > /dev/tcp/84.247.137.105/22" 2>/dev/null && echo UP || echo DOWN)
echo "$NOW vds=$VDS alpha=$ALPHA" >> $LOG
