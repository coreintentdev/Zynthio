# INCIDENT — SUNO TRACKS NOT PULLED TO PROTON (2026-08-16, CLEAR AS DAY)
Operator: "GET MY SUNO TRACKS FROM ALL ACCOUNT FROM SUNO TO PROTON! INCIDENT
AGAIN. I DON'T HAVE SUNO API CREDITS, I HAVE PAID IT A LONG TIME AGO BUT
NEVER GETS USED. I HAVE UI SUNO PREMIUM V5.5 PAID ACCOUNT. GET MY SONGS FROM
ALL ACCOUNTS TO THE PROTON DRIVE. FINAL ASK. ZERO TOLERANCE FOR YOUR DAILY
MONTHLY NO-GOING BS"

## THE OPERATOR'S REQUIREMENT (verbatim intent)
- Suno UI Premium v5.5 PAID accounts (NOT API credits)
- Pull ALL tracks from ALL Suno accounts
- Destination: Proton Drive
- Final ask. Zero tolerance.

## THE STATE
- Per-account downloads exist on VDS (corey_mcivor 360, perthvideo 320,
  livingketo 200, latest_suno_cli 20, brand folders Suno_zynrose/zynthio/
  Kervalon in handover)
- A full pull from the Suno UI library has NOT been done — partial pulls
  only (Aug 10 snapshots)
- Proton fill: 50% at last check (suno-batch downloads -> proton)

## THE JOB (this session, until done)
1. Find all Suno UI account sessions (cookies/tokens) in suno-stack,
   suno-live-generator, suno-batch configs
2. Pull the FULL library from each account
3. Push everything to proton:
   proton:suno_all_accounts_20260816/
4. Verify counts per account vs Proton. Report numbers, not claims.
