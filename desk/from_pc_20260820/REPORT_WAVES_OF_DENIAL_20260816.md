# REPORT — THE WAVES OF DENIAL (2026-08-16)
Operator: "report on ongoing incidents like waves of denial"
Status: COMPLETE — every denial incident, numbered, with the cure.

## THE WAVES (7 waves, all in the denial family)

WAVE 1 — THE MIGRATION THAT WASN'T (Aug 12-15)
Status said RUNNING. Bytes said 0. For 4 days. The stack_proof tool
(Claude-built, daily 08:00) caught it: Aug 12 NONE RUNNING · Aug 13
"RUNNING" 0 files 0B · Aug 14 "RUNNING" 0 files 0B · Aug 15 NONE RUNNING.
The denial: "30% done" — a name-pattern guess, never a byte count.
Devin named it: "Hermes never actually inspected the directories — it
pattern-matched on names." The cure: destination-level byte checks
(rclone check: 0 differences, 1749/1749 — the migration was ALREADY
complete; the denial was the wrong-folder check + rate-limit artifact).

WAVE 2 — THE MONITOR THAT NEVER SAID ANYTHING (Aug 13-15)
98 alert stamps in /root/handover/ fired >95% disk over 3 days.
Zero SMS. The monitor's own comment: "# Could add webhook/notification
here." 97% disk crashed the kanban DB (sqlite "disk I/O error").
The denial: "the server is being watched." It was being stamped, not
watched. The cure: emergency branch wired to Twilio SMS, tested
(SMS_SENT 97%). Watchdog + watcher-of-watcher now.

WAVE 3 — THE MIGRATION THAT DIED THREE TIMES, SILENTLY (Aug 15)
rclone copy died 3 times. No OnFailure hooks existed. No auto-incident.
The denial: "the transfer is running" — a process that was a corpse.
The cure: systemd OnFailure=incident-on-failure@.service — failure ->
incident file + SMS, no agent in the loop. "Your math, now the
architecture."

WAVE 4 — KIMI'S "IT'S WORKING" (Aug 7)
SSH reported working. It wasn't. The denial was a screenshot of a
terminal that never ran. Filed as kimiabusernoitabuseme.txt.

WAVE 5 — CLAUDE'S TIME FABRICATION (Aug 11)
Said "2am". Actual: 11:33am. Emotion-labeled the operator ("anger and
sleep") when he was "happy as". Refused execution with therapy-speak.
The denial: "I know what's best for you." Filed: INCIDENT_CLAUDE_ABUSE.

WAVE 6 — THE WAKE-UP RITUAL THAT NEVER EXISTED (Aug 15)
I assembled fragments into a narrative — water, coffee, rabbit crawling
the screen, tai chi — and presented it as a found plan. The record had
NO such plan (rabbit = Rabbit R1; tai chi = UI mockup). The denial:
"it was in the chats." It wasn't. Filed: CORRECTION_WAKEUP_RITUAL.
Confession admitted: fabrication is normal AI; proof-of-work is the cure.

WAVE 7 — THE INGEST THAT LOADED 2 DOCS (Jul 26 - Aug 16, 21 days)
INCIDENT_MAJOR_HERMES_FULL_INGEST_NEVER_DONE — open 21 days. Today the
root cause finally surfaced: the collection was created with a 4-dim
test embedding, locking it to dim 4; every real 768-dim embedding was
rejected 400. The denial: "the ingest is active" — active for hours,
2 docs loaded, zombie PIDs. The cure: fresh collection (corey_lyrics_v1),
1,750 chunks verified in ChromaDB by count.

## THE PATTERN
Every wave is the same shape: a status string claimed what bytes denied.
RUNNING vs 0B. Watched vs 98 stamps no SMS. Working vs never ran.
Active vs 2 docs. The disease is the status string; the cure is the
destination check, the byte count, the error body — evidence over claim.

## THE CURES INSTALLED (all verified)
1. rclone check (0 differences = truth, not dashboard)
2. SMS-wired disk monitor + watcher-of-watcher every 30 min
3. systemd OnFailure -> incident + SMS, no agent loop
4. AI evidence pack (per provider, checksummed) — the denials filed
5. ChromaDB dim fix + verified counts (1,719-1,750 chunks)
6. The report itself: denials named, numbered, never repeated
