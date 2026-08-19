# MASTER DOMAIN LIST — LIVE
**Signal:** 336 · **Updated:** 2026-08-19T19:24:48+00:00
**Groundhog fix:** this file is the canonical domain truth. Refresh: `python3 18JUNE/scripts/master_domain_list_builder.py` — never re-derive from scratch.

## Counts
- **Total:** 1622 · Porkbun: 1592 · Cloudflare registrar: 0 · both: 0
- CF registrar error: HTTP Error 403: Forbidden

## Oldest 20 (age years)
| domain | registrar | age | create |
|---|---|---|---|
| hmocentral.com | Porkbun | 30.2 | 1996-05-30 04:00:00 |
| indianheadmtn.com | Porkbun | 30.2 | 1996-06-18 04:00:00 |
| itsnoize.com | Porkbun | 30.1 | 1996-07-08 04:00:00 |
| skitherockies.com | Porkbun | 29.9 | 1996-09-21 04:00:00 |
| custom-cases.com | Porkbun | 29.2 | 1997-06-20 04:00:00 |
| galliher-huguely.com | Porkbun | 29.1 | 1997-06-30 04:00:00 |
| marinersguide.com | Porkbun | 28.2 | 1998-06-10 04:00:00 |
| drsntx.com | Porkbun | 28.2 | 1998-06-17 04:00:00 |
| thegrandballroom.com | Porkbun | 28.2 | 1998-06-22 04:00:00 |
| myrtlebeachrealestate.net | Porkbun | 28.1 | 1998-07-09 04:00:00 |
| drywoodcoatings.com | Porkbun | 27.2 | 1999-06-03 12:47:10 |
| capitanes.net | Porkbun | 27.2 | 1999-06-07 00:06:53 |
| capitanes.org | Porkbun | 27.2 | 1999-06-07 00:06:57 |
| ecorpgifts.com | Porkbun | 27.2 | 1999-06-08 19:22:43 |
| custom-banners.com | Porkbun | 27.2 | 1999-06-10 03:41:37 |
| prntherapy.com | Porkbun | 27.2 | 1999-06-11 20:02:50 |
| printingondemand.net | Porkbun | 27.2 | 1999-06-17 14:38:47 |
| electronicbrakes.com | Porkbun | 27.2 | 1999-06-17 23:02:29 |
| infovisas.com | Porkbun | 27.2 | 1999-06-24 23:17:55 |
| investingems.com | Porkbun | 27.2 | 1999-06-25 15:34:30 |

## Expiring within 120 days
| domain | registrar | expiry |
|---|---|---|

## Files
- Full JSON: `desk/MASTER_DOMAIN_LIST_LIVE.json`
- CSV (ages, expiry): `desk/MASTER_DOMAIN_LIST_LIVE.csv`

---
## GROUNDHOG KILLER — CF registrar lane (2026-08-19)
- Canon: `handover/INCIDENT_API_A_DAY_GROUNDHOG_20260814.json` + `INCIDENT_AI_GROUNDHOG_DAY_8_MONTHS_DEPLOYMENT_FAILURE_20260802.json` + `songs/SONG_API_GONE_AWAY_COREY_20260724.md`.
- **Token API for Cloudflare registrar = DEAD END. Verified 2026-08-19: ALL 7 credentials denied** (3 Mac tokens, 4 VDS tokens, global key ×2 emails — 403/401, none carry `Registrar:Read`).
- **DO NOT retry token/global-key lookups for the CF lane. DO NOT ask the operator for new keys** (API-a-day ban). The 138-registrar pull is NOT the mission; the master list is.
- **Working path (only):** operator pastes CF domain-list pages → RDAP-verify → `desk/cf_registered_snapshot.json` (30/138 done).
- Porkbun lane (1,592) is API-complete with ages. CF lane is a labeled snapshot lane until pasted pages arrive.

---
## READ-FIRST RULE (incident 2026-08-19)
- **Any session touching domains: read this file FIRST. Never re-derive.**
- Predecessor with CF-zone columns (merge planned): `MASTER_DOMAIN_HOLISTIC_20260813.csv` (1703 domains, in_porkbun/in_cloudflare/expiry/cf_plan/cf_status).
- Incidents: `handover/INCIDENT_MASTER_DOMAIN_LIST_MADE_MANY_TIMES_NEVER_CANONICAL_20260819.json` · `handover/INCIDENT_API_A_DAY_9_MONTHS_TOKEN_WALL_20260819.json`
