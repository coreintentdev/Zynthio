# INCIDENT REPORT — 40 DAYS IN: THE STATE OF LOSS (VPS / PORKBUN / CLOUDFLARE / PROTON)
Date: 2026-08-15 · Source: live system checks this session (Hermes, PC + VDS), not memory

## WHAT IS LOST — verified state
### 1. VPS FLEET (vmi3205024, ai, cloudvps30) — UNREACHABLE
- NOT on the tailnet (tailscale status: only vds/android/mac/pc/kelvin — no VPS)
- No ssh config aliases on VDS, hostnames do NOT resolve
- No IPs recorded in any map found (only 5.189.143.170 = VDS itself appears)
- Probe: 159.89.100.1:22 is OPEN but "Permission denied (publickey)" — a VPS exists there but no key on the VDS
- => VPS state: no IPs, no keys, no inventory. Effectively lost until operator supplies IPs or keys.

### 2. PORKBUN API — DEAD KEY
- /root/.env AND C:\...\vds_keys.env both carry PORKBUN_API_KEY + PORKBUN_SECRET_KEY
- API test this session: INVALID_API_KEYS_001 (both files — same dead pair)
- /root/secure/porkbun-webhook.env = webhook secret only (not API keys)
- Registry truth still reachable: RDAP works fine (22-domain wishlist check passed) — domains are NOT lost, the API key is
- PORKBUN_LIVE_FETCH_LIVE.json exists on VDS (operator UI count vs api_count delta recorded)

### 3. CLOUDFLARE — TOKENS PARTIAL
- CF_API_TOKEN (cfut_...): verifies OK (user/tokens/verify = OK) but ZONE-scoped — CANNOT read account registrar list (auth error 10000 on accounts/registrar)
- CF_API_TOKEN_FLEET: INVALID (1000)
- CLOUDFLARE_API_TOKEN: OK (same scope class)
- 117-domain registrar list was operator dashboard paste, NOT API-verifiable with current tokens
- => CF zones work with existing tokens; registrar-level (account scope) token needed for full authority

### 4. PROTON DRIVE — TOKEN EXPIRED
- rclone `proton:` remote: 401 Invalid access token (drive-api.proton.me) — token needs refresh via `rclone config update proton:`
- Config fields exist (username=sky-stay, client_uid, salted key) but auth token expired
- Suno backup `suno_library_backup_20260802` EXISTS on proton (listing confirmed 2026-08-02) but size/count unverifiable while 401

### 5. DROPBOX→PROTON LANE — MIRRORED, NOW BLOCKED
- ONE_LANE_HIGHWAY=ACTIVE, policy=SINGLE_PROTON_WRITER_ONLY, active_job=dropbox:→proton:from-dropbox FULL GO (owner Grok_ALL_GO, 2026-08-10)
- Top-level mirror MATCHES: Apps, id-all, nica-print, zynthio_ingest on both dropbox: and proton:from-dropbox
- BUT: proton 401 now blocks the lane, and no rclone job is currently running

## WHAT WORKS
- Hermes VDS = v0.20.1 (2026.8.13) — SAME as PC. The "new update for the portable key" is ALREADY live on the VDS.
- RDAP registry checks: fully working (no key needed) — domain truth is never lost
- CF zone tokens: working for zone-level work
- Orico data: secured 72,651 files byte-verified on C:
- USB installer: verified bootable (CD001)
- Local .py inventory: 73 scripts mapped

## THE PATTERN — why this repeats
Every lane depends on a credential that lives in ONE place and expires/rotates with no
watchdog. When it dies (PB key, proton token), the lane dies silently and the operator
re-asks. The fix is not more asking — it is:
1. REGENERATE once: Porkbun API key (operator, porkbun.com/account/api) + proton token
   (rclone config update proton:) — the only two human actions
2. CENTRALIZE: single /root/secure/creds.env with tested-live markers + expiry dates,
   checked by an overwatcher (like the existing VDS_CAPACITY watchers)
3. AUTHORITY: one CF account-scope token for registrar (operator dashboard → token)
4. VPS: operator supplies IPs + keys ONCE, then they join the tailnet (tailscale) so
   hostnames resolve forever
