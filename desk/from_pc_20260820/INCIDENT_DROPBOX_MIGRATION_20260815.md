# INCIDENT — DROPBOX→PROTON MIGRATION FAILED FOR 1+ MONTH (2026-08-15)
Severity: CRITICAL (data at risk of cull; operator: "not a joke")
Operator: "oh look something important still not done. after month plus and still fails and no time left."

## THE FACTS (verified live 2026-08-15 12:43)
- Dropbox total: 423.3 GiB (454,519,929,096 bytes) — Apps 422.6 GiB + id-all + nica-print + zynthio_ingest
- Proton free: 480.8 GiB (fits — 423.3 < 480.8)
- proton:from-dropbox/ EXISTS but is a SHELL: Apps/ contains only "Google Download Your Data"
  — the 422 GiB of Apps content was NEVER transferred
- rclone size on the mirror times out (Proton 429 rate limits); subdir listing shows near-empty
- No migration job running (0 rclone processes); no migration log found
- Dropbox trial ended; Google storage being paid ~1.5 months; Google WILL cull data;
  operator will NOT pay Google again

## THE RIDDLE (operator)
"how can the model be made if the data is not ever moved to be read any way"
- The twin model was trained on runbooks/docs (175 docs, 1 lyric) because the real data
  (Dropbox 423 GiB, lyrics, archives) was never moved to where it could be read.
- Model build blocked by data that never migrates. Same structural disease.

## ACTION (started 2026-08-15)
- Full rclone copy dropbox: → proton:from-dropbox/ started in background, resumable,
  --transfers 4, --retries 10, logs to /root/zynthio/logs/dropbox_migrate.log
- ETA: hours-to-days at Proton's rate limits; resumable so every retry continues
- THIS IS THE MOVE. Not "soon" — started now.

## DOCTRINE
- "Move it today or tell me you cannot" — no more month-long silent partials.
- Every migration job gets a log + a completion check + an SMS at done/fail.
