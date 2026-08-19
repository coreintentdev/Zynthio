#!/usr/bin/env bash
set -euo pipefail
source /root/.zynthio.env 2>/dev/null || true
: "${PROTON_USER:?PROTON_USER missing in /root/.zynthio.env}"
: "${PROTON_PASS:?PROTON_PASS missing in /root/.zynthio.env}"

systemctl stop proton-mail-bridge.service 2>/dev/null || true
sleep 2

export BRIDGE_CLI=true
export PASSWORD_STORE_DIR="${PASSWORD_STORE_DIR:-/root/.password-store}"
PROTON_TOTP="${PROTON_TOTP:-}"
INFO_LOG="/tmp/proton_bridge_info_$$.log"
rm -f "$INFO_LOG"

expect <<EOF
log_file -a "$INFO_LOG"
set timeout 180
spawn protonmail-bridge -c
expect ">>"
send "login\r"
expect {
  -re "(?i)username|email" { send "$PROTON_USER\r"; exp_continue }
  -re "(?i)password" { send "$PROTON_PASS\r"; exp_continue }
  -re "(?i)two.factor|2fa|authenticator|code" {
    if { "$PROTON_TOTP" ne "" } { send "$PROTON_TOTP\r"; exp_continue }
    puts "NEEDS_PROTON_TOTP=1"; exit 3
  }
  ">>" {}
  timeout { exit 2 }
}
send "info\r"
expect ">>"
send "quit\r"
EOF
LOGIN_RC=$?
if [[ $LOGIN_RC -eq 3 ]]; then
  echo "BLOCKER: add PROTON_TOTP to /root/.zynthio.env and re-run"
  exit 3
fi

python3 - "$INFO_LOG" <<'PY'
import re, sys
from pathlib import Path
text = Path(sys.argv[1]).read_text(errors="replace") if Path(sys.argv[1]).exists() else ""
user = ""
password = ""
for line in text.splitlines():
    if re.search(r"username", line, re.I):
        m = re.search(r":\s*(\S+@\S+)", line)
        if m:
            user = m.group(1)
    if re.search(r"password", line, re.I) and "store" not in line.lower():
        m = re.search(r":\s*(\S+)", line)
        if m and "@" not in m.group(1):
            password = m.group(1)
if user and password:
    env = Path("/root/.zynthio.env")
    lines = env.read_text().splitlines() if env.exists() else []
    keep = [l for l in lines if not re.match(r"^export PROTON_BRIDGE_(USER|PASS)=", l.strip())]
    keep.append(f"export PROTON_BRIDGE_USER='{user}'")
    keep.append(f"export PROTON_BRIDGE_PASS='{password}'")
    env.write_text("\n".join(keep) + "\n")
    env.chmod(0o600)
    print(f"PROTON_BRIDGE_IMAP creds written for {user}")
else:
    print("WARN: could not parse bridge info output — add PROTON_BRIDGE_USER/PASS manually")
PY
rm -f "$INFO_LOG"

systemctl start proton-mail-bridge.service
sleep 3
systemctl is-active proton-mail-bridge.service || journalctl -u proton-mail-bridge -n 20 --no-pager
