#!/bin/bash
# ALPHA SECOND-EYE WATCHDOG — redundant fleet monitoring on the idle box.
# Mirrors the VDS's iron+memory watchdogs so the fleet stays watched even
# if the VDS itself goes down. Runs every 10 min.
LOG=/var/log/alpha_watchdog.log
mkdir -p /var/log
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

state_line="$NOW alpha_watchdog_alive"
# check the VDS (gamma) reachability
GAMMA=$(timeout 8 bash -c 'echo > /dev/tcp/5.189.143.170/22' 2>/dev/null && echo UP || echo DOWN)
# check own ollama
OLL=$(curl -sS -m 5 http://127.0.0.1:11434/api/version 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin).get('version','?'))" 2>/dev/null || echo down)
echo "$NOW gamma=$GAMMA alpha_ollama=$OLL" >> $LOG

# only alert if something CHANGES vs last
LAST=""
[ -f /var/log/alpha_watchdog.state ] && LAST=$(cat /var/log/alpha_watchdog.state)
CUR="gamma=$GAMMA oll=$OLL"
if [ "$CUR" != "$LAST" ]; then
  echo "$CUR" > /var/log/alpha_watchdog.state
  echo "$NOW STATE_CHANGE $LAST -> $CUR" >> $LOG
fi
exit 0
