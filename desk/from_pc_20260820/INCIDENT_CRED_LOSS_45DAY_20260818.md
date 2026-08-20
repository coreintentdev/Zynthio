# INCIDENT — 45+ DAY PASSWORD/API LOSS RECURRING (2026-08-18)
Operator: "report incidents api a day passwords pass that word goes where
45+ day hermes i still lost lil bot"

## THE PATTERN (45+ days, recurring)
Every few days the operator gives a password / API key / credential and
it "passes" (gets used once) then the SAME credential is lost again —
each session re-hunts instead of reading one canonical store. Same class
as: Kimi key (hunt), Grok keys (hunt, 7 found), the Cloudzy/DELTA panel
credential (hunt).

## THE EVIDENCE (credential locations today)
- /root/.zynthio.env — the LIVE env (KEY 1 groq restored, 56 chars)
- /root/STACK_LIVE.env + 3 dated .bak — the environment backups
- /root/zynthio-tools/STATE_BACKUP_336ZM_20260529/zynthio.env (May 30)
- /root/zynthio-tools/proton-onboarding/{herms.env,zynthio.env}
- /root/zynthio-tools/zynthio/evny/{twilio.env} — the evny dir (mac
  STACK_LIVE.env path per zyn CLI: 18JUNE/evny/STACK_LIVE.env)
- Mac side: ~/Desktop/zynthio-tools/18JUNE/evny/STACK_LIVE.env (the
  zyn CLI "single key file")
- desk/: API_PLANS_LIVE.md, HERMES_GO_RUNPOD_KEY_MESH, CF_ACCOUNT_TOKENS
  (some empty stubs: INCIDENT_API_A_DAY_GROUNDHOG_20260814 = 0 bytes)

## THE ROOT CAUSE
NO single canonical credential store that every session reads FIRST.
Credentials are scattered across env copies, dated backups, and desk
md stubs — so "the word goes where" = nowhere guaranteed.

## THE FIX (build the canonical store)
1. A single /root/zynthio-tools/zynthio/secure/vault.enc (age/gpg
   encrypted) holding ALL passwords + API keys with a manifest
2. A CREDENTIAL_MAP.md (names only, values in the vault) listing every
   platform + where its credential lives
3. Every session starts by reading CREDENTIAL_MAP.md -> vault, not
   re-hunting corpus
4. Mac STACK_LIVE.env mirrored into the vault daily

## STATUS
OPEN — canonical vault to be built.
