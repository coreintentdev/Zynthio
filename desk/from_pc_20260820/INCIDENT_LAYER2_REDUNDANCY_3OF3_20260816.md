# INCIDENT — LAYER-2 REDUNDANCY 3-OF-3 FAILED (2026-08-16)
Operator: "check all functions updated and system updated and redundancy not
just layer. see local git. made"

## THE CHECK (live)
- System: 0 upgradable, kernel 6.8.0-134, uptime 5w6d — CURRENT
- Core: gateway ACTIVE · twin ACTIVE · chroma ×3 (neverend) — HOLDS
- Crons: 31 active · Git: committed 2cc43e1633 (75 changes, data-backup)
- FAILED UNITS:
  1. zynthio-billing-ingest — failed 18:45 today (exit 1)
  2. zynthio-frankfurt-backup — failed Aug 12, 4 DAYS (exit 255)
  3. zynthio-gdrive-backup — failed 05:06 today (exit 1)
  (networkd-wait-online = boot-time, benign)

## THE TRUTH
Layer 1 (core services) holds. Layer 2 (backups) is 3-of-3 failed.
The Frankfurt mirror has been dead 4 days — the "redundancy" was a list,
not a state. Not just layer — every layer, checked.

## THE FIX (queued)
- billing-ingest: run the script manually, capture the exit-1 error
- frankfurt-backup: 4-day-old failure — restart + verify the mirror
- gdrive-backup: run vds_gdrive_weekly_backup.sh, capture the error
- Re-check all three after repair; commit the fix.

## STATUS
OPEN — layer 2 down, repair queued, git committed.
