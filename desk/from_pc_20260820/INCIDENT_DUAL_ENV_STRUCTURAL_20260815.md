# INCIDENT — DUAL ENV FILE STRUCTURAL FAILURE (2026-08-15)
Severity: MAJOR (root cause of repeated daily "lost" reports)
Model: deepseek-v4-flash · Source: PC Hermes session

## THE INCIDENT
Operator: "there is a fault and now 2x separate env files that is operating structural bs everyday lost ai"

Credentials are split across TWO env files on the VDS:
- /root/zynthio/.env        → TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER (proven, used by vds_disk_alert.sh)
- /root/.zynthio.env        → SMS_HOME_CHANNEL, SMS_ALLOWED_USERS, PROTON_USER/PASS, BRIDGE_IMAP (used by proton_bridge_login.sh)

Every script guesses which file holds its keys. This session: send_daily_sms.sh read the wrong file 3×, SMS_CONFIG_MISSING 3×, before the split was confirmed. The disk alert "works" only because it hardcodes the To number. This is the concrete mechanism behind "ask for the same thing every day / no feedback / lost-until-found."

## ROOT CAUSE
Multi-env scattering — already documented as a root cause in MASTER_SCOPE_LIVE doctrine:
"Consolidate secrets to ONE file (/root/.zynthio.env) and symlink the rest. Multi-env scattering is a root cause of context loss."
Violated: /root/zynthio/.env still holds a parallel credential set.

## FIX APPLIED
- [ ] Merge TWILIO_* + SMS_* into /root/.zynthio.env (single source of truth)
- [ ] Symlink /root/zynthio/.env → /root/.zynthio.env (or vice versa) so ALL scripts read ONE file
- [ ] Re-test send_daily_sms.sh → expect SMS_SENT
- [ ] Wire daily 07:00 cron: SMS (Twilio) + desktop cron job (job 80f7f87e003e)
- [ ] Verify no script references BOTH files independently

## INCIDENT CLASS
stale-credential-pattern / multi-env-scattering → per skill zynthio-infra-ops "Stale-credential pattern (systemic incident, 2026-08-06)". Fix = one live store + monthly probe, NOT daily re-derivation.
