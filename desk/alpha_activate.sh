#!/bin/bash
# ALPHA NODE ACTIVATION — make the idle 8c/22Gi box earn its keep.
# 1) Install ollama (fallback model lane, relieves VDS)
# 2) Set up the iron+memory watchdogs as a SECOND eye on the fleet
LOG=/var/log/alpha_activation.log
echo "== alpha activation $(date -u)" >> $LOG

echo "installing ollama" >> $LOG
curl -fsSL https://ollama.com/install.sh 2>/dev/null | sh >> $LOG 2>&1 && echo "ollama installed" >> $LOG

# set OLLAMA to bind (like the VDS) 
mkdir -p /etc/systemd/system/ollama.service.d
printf '[Service]\nEnvironment="OLLAMA_HOST=0.0.0.0:11434"\n' > /etc/systemd/system/ollama.service.d/override.conf
systemctl daemon-reload && systemctl restart ollama 2>>$LOG

echo "done" >> $LOG
tail -3 $LOG
