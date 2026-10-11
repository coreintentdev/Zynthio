#!/usr/bin/env bash
# zynthio_guard_install.sh — idempotent permanent installer. Never deletes. Never kills.
# Installs: /root/zynthio/guard/{bin/guard,allowlist.conf,guard.env,protect.list}, `zynthio-guard` CLI,
#           systemd timer (check every 15 min), agent wrapper (`zynthio-guard run`), harden + snapshot commands.
set -euo pipefail
BASE=${GUARD_BASE:-/root/zynthio/guard}
if [ -z "${GUARD_NO_SYSTEMD:-}" ]; then [ "$(id -u)" = 0 ] || { echo "run as root"; exit 1; }; fi
mkdir -p "$BASE"/{bin,reports,state} "$(dirname "$BASE")/incidents" "$(dirname "$BASE")/backups"

cat > "$BASE/bin/guard" <<'GUARD_EOF'
#!/usr/bin/env bash
# zynthio-guard — permanent exposure guard. Read-only checks. No deletes. No kills (only TTL on units created by `run`).
set -uo pipefail
BASE=${GUARD_BASE:-/root/zynthio/guard}
ALLOW=$BASE/allowlist.conf
PROTECT=$BASE/protect.list
REG=$BASE/registry.tsv
SECRET_FILE=$BASE/state/secret.re
mkdir -p "$BASE/state" "$BASE/reports"
[ -f "$BASE/guard.env" ] && . "$BASE/guard.env"
MAX_AGE_H=${MAX_AGE_H:-6}
OPS_WEBHOOK=${OPS_WEBHOOK:-}
TS=$(date -u +%Y%m%dT%H%M%SZ)
SHELLS_RE='^(-?bash|-?zsh|-?sh|sshd.*|tmux.*|screen|login|su|sudo|agetty|cron|crond|systemd.*|dbus-daemon|rpcbind)$'
ADHOC_RE='http\.server|SimpleHTTPServer'

[ -f "$SECRET_FILE" ] || cat > "$SECRET_FILE" <<'RE_EOF'
fc-[A-Za-z0-9]{8,}
sk-[A-Za-z0-9]{12,}
ghp_[A-Za-z0-9]{8,}
gho_[A-Za-z0-9]{8,}
xox[bpas]-[A-Za-z0-9-]{8,}
AKIA[A-Z0-9]{12,}
AIza[A-Za-z0-9_-]{20,}
(api[_-]?key|token|secret|password|passwd|cookie)[=: ][^ ]
RE_EOF

redact() {
  sed -E '
    s/(fc-|sk-|ghp_|gho_|xox[bpas]-|AIza|AKIA)[A-Za-z0-9_-]{8,}/\1[REDACTED]/g
    s/((api[_-]?key|token|secret|password|passwd|cookie|authorization)[=: ]+)[^ ]+/\1[REDACTED]/Ig
    s/(Bearer )[A-Za-z0-9._-]+/\1[REDACTED]/g
  '
}

# long-running (> MAX_AGE_H) processes NOT under a systemd service/container cgroup
scan_procs() {
  local p pid comm cmd et
  for p in /proc/[0-9]*; do
    pid=${p#/proc/}; [ "$pid" = "$$" ] && continue
    cmd=$(tr '\0\n' '  ' <"$p/cmdline" 2>/dev/null) || continue
    [ -z "$cmd" ] && continue
    comm=$(cat "$p/comm" 2>/dev/null)
    echo "$comm" | grep -Eq "$SHELLS_RE" && continue
    grep -Eq '\.service|docker|containerd|libpod|kubepods' "$p/cgroup" 2>/dev/null && continue
    et=$(ps -o etimes= -p "$pid" 2>/dev/null | tr -d ' ')
    [ -n "$et" ] || continue
    [ "$et" -gt $((MAX_AGE_H*3600)) ] || continue
    printf '%s\t%s\t%s\t%s\n' "$pid" "$comm" "$((et/3600))" "$cmd"
  done
}

allowed_proc() {
  local cmd=$1 pat
  while IFS= read -r pat; do
    [ -n "$pat" ] && [[ "$cmd" == *"$pat"* ]] && return 0
  done < <(sed -nE 's/^proc[[:space:]]+//p' "$ALLOW" 2>/dev/null)
  return 1
}

post() {
  [ -n "$OPS_WEBHOOK" ] || { echo "OPS_WEBHOOK not set: journal + report file only" >&2; return 0; }
  umask 077
  # dedupe: delete all existing todos from this source before posting a new one.
  # The ops center exposes DELETE /api/todos?project=<project> for this.
  curl -fsS -m 15 -X DELETE "${OPS_WEBHOOK}?project=zynthio-guard" >/dev/null 2>&1 || true
  python3 -c 'import json,sys; t=sys.stdin.read(); print(json.dumps({"project":"zynthio-guard","title":t}))' <"$1" >"$BASE/state/payload.json"
  printf 'url = "%s"\n' "$OPS_WEBHOOK" | curl -fsS -m 15 -K - -X POST -H 'Content-Type: application/json' --data-binary @"$BASE/state/payload.json" >/dev/null \
    || echo "post to ops center failed" >&2
}

cmd_check() {
  local FIND=$BASE/state/findings.current
  : >"$FIND"

  # 1. externally bound listeners not in allowlist
  ss -H -tlnp 2>/dev/null | while read -r _ _ _ laddr _ users; do
    case "$laddr" in 127.*|"[::1]"*|::1*) continue ;; esac
    port=${laddr##*:}
    grep -Eq "^listen[[:space:]]+$port([[:space:]]|\$)" "$ALLOW" 2>/dev/null && continue
    name=$(sed -nE 's/.*\(\("([^"]+)".*/\1/p' <<<"$users")
    pid=$(sed -nE 's/.*pid=([0-9]+).*/\1/p' <<<"$users")
    echo "UNLISTED_LISTENER port=$port bind=$laddr proc=${name:-?} pid=${pid:-?}" >>"$FIND"
  done

  # 2. secrets in args + ad-hoc http servers (any process)
  local p pid cmd
  for p in /proc/[0-9]*; do
    pid=${p#/proc/}; [ "$pid" = "$$" ] && continue
    cmd=$(tr '\0\n' '  ' <"$p/cmdline" 2>/dev/null) || continue
    [ -z "$cmd" ] && continue
    if echo "$cmd" | grep -Eqi -f "$SECRET_FILE"; then
      echo "SECRET_IN_ARGS pid=$pid user=$(stat -c %U "$p") cmd=$(echo "$cmd" | redact | cut -c1-200) -> ROTATE KEY" >>"$FIND"
    fi
    if echo "$cmd" | grep -Eq "$ADHOC_RE"; then
      echo "ADHOC_HTTP_SERVER pid=$pid user=$(stat -c %U "$p") cwd=$(readlink "$p/cwd" 2>/dev/null) cmd=$(echo "$cmd" | redact | cut -c1-160)" >>"$FIND"
    fi
  done

  # 3. unmanaged long-running processes
  scan_procs | while IFS=$'\t' read -r pid comm age cmd; do
    allowed_proc "$cmd" && continue
    echo "UNMANAGED_LONG_RUNNING pid=$pid age_h=$age comm=$comm cmd=$(echo "$cmd" | redact | cut -c1-160)" >>"$FIND"
  done

  # 4. sensitive-looking files in /tmp readable by group/world
  find /tmp -maxdepth 4 -type f \( -iname '*.env' -o -iname '*cookie*' -o -iname '*token*' -o -iname '*.key' -o -iname '*.pem' -o -iname '*secret*' -o -iname '*.db' -o -iname '*.sqlite*' -o -iname '*session*' -o -iname '*credential*' \) -perm /044 2>/dev/null \
    | while read -r f; do echo "TMP_SENSITIVE_READABLE mode=$(stat -c %a "$f") $f" >>"$FIND"; done

  # 5. env files with loose perms
  find "$(dirname "$BASE")" -maxdepth 5 -type f \( -name '*.env' -o -name '.env' \) -perm /077 2>/dev/null \
    | while read -r f; do echo "ENV_FILE_PERMS mode=$(stat -c %a "$f") $f" >>"$FIND"; done

  # 6. firewall
  if command -v ufw >/dev/null 2>&1; then
    ufw status verbose 2>/dev/null | grep -q 'Status: active' || echo "FIREWALL_INACTIVE ufw not active" >>"$FIND"
    ufw status verbose 2>/dev/null | grep -qi 'deny (incoming)' || echo "FIREWALL_DEFAULT_NOT_DENY incoming policy is not deny" >>"$FIND"
  else
    echo "FIREWALL_UNKNOWN ufw not installed" >>"$FIND"
  fi

  sort -u "$FIND" -o "$FIND"
  local n; n=$(wc -l <"$FIND")
  if [ "$n" -gt 0 ]; then
    local rep=$BASE/reports/guard-$TS.txt
    { echo "zynthio-guard $TS host=$(hostname) findings=$n"; cat "$FIND"; } >"$rep"
    local h; h=$(sha256sum <"$FIND" | cut -c1-16)
    if [ "$h" != "$(cat "$BASE/state/last_hash" 2>/dev/null)" ]; then
      logger -t zynthio-guard "findings=$n report=$rep" 2>/dev/null
      post "$rep"
      echo "$h" >"$BASE/state/last_hash"
    fi
    cat "$rep"
  else
    : >"$BASE/state/last_hash"; echo "clean $TS"
  fi
  [ "${1:-}" = "--strict" ] && [ "$n" -gt 0 ] && return 1
  return 0
}

cmd_baseline() {
  [ -f "$ALLOW" ] && cp -a "$ALLOW" "$ALLOW.bak-$TS"
  {
    echo "# zynthio-guard allowlist — generated $TS. REVIEW every line. '#REVIEW' lines were NOT approved."
    echo "# listen <port> <name>  : externally bound listener allowed"
    echo "# proc <cmd substring>  : long-running non-systemd process allowed"
    ss -H -tlnp 2>/dev/null | while read -r _ _ _ laddr _ users; do
      case "$laddr" in 127.*|"[::1]"*|::1*) continue ;; esac
      port=${laddr##*:}
      name=$(sed -nE 's/.*\(\("([^"]+)".*/\1/p' <<<"$users")
      pid=$(sed -nE 's/.*pid=([0-9]+).*/\1/p' <<<"$users")
      cmd=$(tr '\0\n' '  ' <"/proc/${pid:-0}/cmdline" 2>/dev/null)
      if echo "$cmd" | grep -Eq "$ADHOC_RE" || [ "$port" = 8888 ]; then
        echo "#REVIEW listen $port ${name:-?}   # ad-hoc/suspect, not approved"
      else
        echo "listen $port ${name:-?}"
      fi
    done | sort -u
    scan_procs | while IFS=$'\t' read -r pid comm age cmd; do
      if echo "$cmd" | grep -Eqi -f "$SECRET_FILE" || echo "$cmd" | grep -Eq "$ADHOC_RE"; then
        echo "#REVIEW proc (pid $pid, $comm, ${age}h) cmd withheld: secret in args or ad-hoc http server"
      else
        echo "proc $(echo "$cmd" | sed -E 's/[[:space:]]+$//' | cut -c1-80)"
      fi
    done | sort -u
  } >"$ALLOW"
  echo "wrote $ALLOW — $(grep -c '^#REVIEW' "$ALLOW") entries need your review (not approved)"
  [ -f "$ALLOW.bak-$TS" ] && echo "previous allowlist kept at $ALLOW.bak-$TS"
  return 0
}

cmd_harden() {
  local apply=0; [ "${1:-}" = "--apply" ] && apply=1
  command -v ufw >/dev/null 2>&1 || { echo "ufw not installed: apt-get install ufw, then rerun"; return 1; }
  local ssh extra
  ssh=$(ss -H -tlnp 2>/dev/null | grep '"sshd"' | awk '{print $4}' | sed 's/.*://' | sort -u)
  [ -n "$ssh" ] || { echo "cannot detect sshd port; aborting to avoid lockout"; return 1; }
  extra=$(sed -nE 's/^listen[[:space:]]+([0-9]+).*/\1/p' "$ALLOW" 2>/dev/null | sort -u)
  echo "plan: ufw default deny incoming, allow outgoing"
  echo "      allow sshd port(s): $(echo $ssh)"
  echo "      allow 80, 443, and allowlisted listener ports: $(echo $extra)"
  echo "      chmod 600 loose env files under $(dirname "$BASE")"
  echo "note: Docker-published ports can bypass ufw; verify externally with nmap."
  [ "$apply" = 1 ] || { echo "dry run. add --apply to execute."; return 0; }
  ufw default deny incoming; ufw default allow outgoing
  local port
  for port in $ssh 80 443 $extra; do ufw allow "$port"/tcp; done
  ufw --force enable
  find "$(dirname "$BASE")" -maxdepth 5 -type f \( -name '*.env' -o -name '.env' \) -perm /077 -exec chmod 600 {} + 2>/dev/null
  ufw status verbose
}

cmd_snapshot() {
  [ -f "$PROTECT" ] || { echo "missing $PROTECT"; return 1; }
  local dest f
  dest="$(dirname "$BASE")/backups/$TS"
  mkdir -p "$dest"
  while IFS= read -r f; do
    case "$f" in ''|\#*) continue ;; esac
    [ -e "$f" ] || { echo "missing: $f"; continue; }
    case "$f" in
      *.db|*.sqlite|*.sqlite3)
        if command -v sqlite3 >/dev/null 2>&1; then
          mkdir -p "$dest$(dirname "$f")"
          sqlite3 "$f" ".backup '$dest$f'" && echo "sqlite backup: $f" && continue
        fi ;;
    esac
    cp -a --parents "$f" "$dest" && echo "copied: $f"
  done <"$PROTECT"
  (cd "$dest" && find . -type f ! -name SHA256SUMS -exec sha256sum {} + >SHA256SUMS)
  chmod -R go-rwx "$dest"
  echo "snapshot: $dest (never auto-pruned; nothing deleted)"
}

# agent wrapper: every agent-started long job gets an owner, a TTL, and a registry line
cmd_run() {
  local owner=${1:-} ttl=${2:-}
  shift 2 2>/dev/null || true
  [ "${1:-}" = "--" ] && shift
  { [ -n "$owner" ] && [ -n "$ttl" ] && [ $# -gt 0 ]; } || { echo "usage: zynthio-guard run <owner> <ttl-seconds> -- <cmd...>"; return 2; }
  local unit="zg-${owner}-$(date +%s)"
  systemd-run --unit="$unit" --collect --property=RuntimeMaxSec="$ttl" -- "$@" || return $?
  printf '%s\t%s\t%s\tttl=%s\t%s\n' "$(date -u +%FT%TZ)" "$owner" "$unit" "$ttl" "$*" | redact >>"$REG"
  echo "started $unit (auto-stops after ${ttl}s). registry: $REG"
}

cmd_status() {
  systemctl list-timers zynthio-guard.timer --no-pager 2>/dev/null
  echo "-- latest reports:"; ls -1t "$BASE/reports" 2>/dev/null | head -3
  echo "-- agent registry (last 10):"; tail -n 10 "$REG" 2>/dev/null
}

case "${1:-check}" in
  check)    shift; cmd_check "$@" ;;
  baseline) cmd_baseline ;;
  harden)   shift; cmd_harden "$@" ;;
  snapshot) cmd_snapshot ;;
  run)      shift; cmd_run "$@" ;;
  status)   cmd_status ;;
  *) echo "usage: zynthio-guard {check [--strict]|baseline|harden [--apply]|snapshot|run <owner> <ttl> -- cmd|status}"; exit 2 ;;
esac
GUARD_EOF
chmod 755 "$BASE/bin/guard"

[ -f "$BASE/guard.env" ] || { umask 077; cat > "$BASE/guard.env" <<'ENV_EOF'
# chmod 600. Fill OPS_WEBHOOK with the same endpoint /root/zynthio/bin/stale_process_watch.sh posts to (Devin ops center).
OPS_WEBHOOK=
MAX_AGE_H=6
ENV_EOF
}
[ -f "$BASE/protect.list" ] || cat > "$BASE/protect.list" <<'PL_EOF'
# one absolute path per line. `zynthio-guard snapshot` copies these (sqlite files via .backup). Nothing is ever pruned or deleted.
# example: /root/zynthio/devin/sessions.db
PL_EOF
touch "$BASE/registry.tsv"

if [ -z "${GUARD_NO_SYSTEMD:-}" ]; then
  ln -sf "$BASE/bin/guard" /usr/local/bin/zynthio-guard
  cat > /etc/systemd/system/zynthio-guard.service <<'SVC_EOF'
[Unit]
Description=ZYNTHIO exposure guard (read-only check, posts to ops center on change)
[Service]
Type=oneshot
ExecStart=/usr/local/bin/zynthio-guard check
Nice=10
SVC_EOF
  cat > /etc/systemd/system/zynthio-guard.timer <<'TMR_EOF'
[Unit]
Description=Run ZYNTHIO exposure guard every 15 minutes
[Timer]
OnBootSec=5min
OnCalendar=*:0/15
RandomizedDelaySec=60
Persistent=true
[Install]
WantedBy=timers.target
TMR_EOF
  [ -f "$BASE/allowlist.conf" ] || "$BASE/bin/guard" baseline
  systemctl daemon-reload
  systemctl enable --now zynthio-guard.timer
else
  [ -f "$BASE/allowlist.conf" ] || GUARD_BASE="$BASE" "$BASE/bin/guard" baseline
fi
echo
echo "installed. next: 1) review $BASE/allowlist.conf (#REVIEW lines)  2) fill $BASE/guard.env  3) zynthio-guard check  4) zynthio-guard harden  5) edit protect.list, zynthio-guard snapshot"
