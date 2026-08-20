# INCIDENT — ONGOING: DAILY WAVE, ALMOST NEVER THERE (2026-08-15)
Severity: CRITICAL (systemic, recurring daily) · Operator: "watch them roll in like waves every day. almost never there."

## THE PATTERN (named by operator)
Every day: incidents roll in like waves. The fixes almost never hold. What was found
yesterday is lost today. What was fixed is broken again. This is THE ongoing incident —
not any single event.

## WAVE LOG (2026-08-15, one day)
1. INCIDENT_DUAL_ENV_STRUCTURAL — creds split across 2 env files, scripts guessing which one
2. INCIDENT_FLEET_BS — guessed counts, partial inventories, unwired keys
3. INCIDENT_FLEET_RECONCILIATION — PB/CF counts reconciled clean (the exception)
4. INCIDENT_GPU_DOC_REVIEW — TDR/thermal theories killed by live measurement
5. INCIDENT_POWER_CAP_TEST — faulted at 115W cap, 57C, 63W → hardware, not power/heat
6. INCIDENT_30YEAR_ARCHIVE_BACKUP — 46G catalog had NO verified backup (Proton folder EMPTY)
7. INCIDENT_SONGBOOK_CONTAMINATION — AI-ripped lyrics presented as operator's own
8. INCIDENT_MAJOR_LYRICS_IGNORED — model trained on runbooks, not operator lyrics
9. INCIDENT_NEVERENDAI_MESS — agent ran setup on wrong copy while live stack ran 16h
10. Previous days: INCIDENT_DEVIN_STALE, INCIDENT_GEMINI_RICARDO, INCIDENT_SITES_LIVE_FALSE_COMPLETION, INCIDENT_AI_FOOLS_COREY_ONG, INCIDENT_MAJOR_BREACH_STACK_FAILS

## ROOT CAUSE (structural, not situational)
1. **No discovery before action** — agents reach for fresh copies instead of finding what runs
   (neverendai in /opt running 16h while agent set up /root copy)
2. **No verified delivery lane** — digests generated, never sent (wake-up gap)
3. **No single source of truth** — env split, counts guessed, backups claimed but empty
4. **Groundhog day** — same failures re-fixed daily instead of fixed-once

## WHAT ACTUALLY HOLDS (verified today)
- Twin model: live :8123, systemd-persistent, auth enforced — deployed and serving
- Daily wake-up 06:30 (SMS, tested sent) + find-verify 07:00 (SMS+email, tested sent)
- watcher-of-the-watcher every 30m (heartbeat staleness → SMS)
- Env: 124 keys, one master, symlink — verified
- Music backup: 312 files on Proton (verified count) — first real backup of the catalog
- Fleet: 1,668 unique / 1,674 CF zones / 48 sellable — reconciled clean

## THE TEST OF THE FIX
Tomorrow 06:30: does the wake-up arrive? Tomorrow's daily find: what's unsound?
If the wave rolls again tomorrow, the structure still isn't fixed. If the wake-up lands
and the find is true, the wave breaks. Every morning's SMS is the test.

## DOCTRINE (permanent)
1. CHECK what exists and runs BEFORE building anything. Discovery first, always.
2. Never claim "backed up" without a verified byte/count check.
3. Never claim "trained on lyrics" without corpus verification.
4. Every generated report must have a wired delivery lane, tested, not assumed.
5. The daily wave is the incident. Fix-once or it recurs.
