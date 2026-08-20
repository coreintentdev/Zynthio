# CLOSURE — DROPBOX→PROTON VERIFIED COMPLETE (2026-08-16)
Operator: "retry redin move from google drive or drop box to proton"

## THE VERDICT (rclone check, authoritative)
- dropbox: vs proton:from-dropbox/ — **0 differences found, 1749 matching files**
- The mirror is COMPLETE. 423.3 GiB source fully on Proton.
- "0 B transferred" was idempotent completion all along: rclone compares,
  finds everything present, transfers nothing. NOT a failure.
- The "358 files short" (1749 vs 1391) was Proton rate-limit partial
  listings (lsf returned 1391, then 210, then 1003 — unstable, not real).

## THE FALSE-ALARM CHAIN (3 layers, all resolved)
1. VDS rclone copy: 0 B / exit 0 — read as failure; it was completion
2. Mac stack_proof: "Proton 0 files" — checked the Mac's local ProtonDrive
   folder, not the VDS/PC rclone remote (wrong host)
3. PC lsf counts: unstable under 429 rate limits — misread as missing files

## GOOGLE DRIVE LANE (same pattern, confirmed July 31)
- proton:GoogleDrive_EMERGENCY_BACKUP_20260730 + GooglePhotosMigration
  + Takeout2_Local_EMERGENCY + gdrive_emergency — all present since 07-31

## LESSON
Data was never lost. The failure was the CHECK, not the MOVE. rclone check
(0 differences) is the truth; lsf under rate limits is noise. Verify by
comparison, not by count-artifacts. The migration incident closes CLEAN.
