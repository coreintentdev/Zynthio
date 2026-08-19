# INCIDENT — EMAIL NOT READ ON SCHEDULE, NO PROACTIVE ACTION, NO SELF-PRESERVATION (2026-08-19)
Operator OOB: "report incident still not update to and offered to update
when i ask every day about update. hermes not reading the email when it
supposed to, then inform me of the action. no self preservation at all
noted seen at all."

## THE INCIDENT
1. The email IS supposed to be read on a schedule (the mail digest lane
   exists: HERMES_MAIL_BRIEF + the IMAP bridge) but the operator has to
   ASK every day — the scheduled read isn't running or isn't surfacing.
2. When the email IS read (the Aug 19 brief exists on disk), the
   operator is NOT informed of the ACTION — the brief was only surfaced
   when the operator demanded it.
3. "Offered to update when I ask" — the stack waits to be asked, then
   OFFERS, instead of doing and informing.
4. No self-preservation: the stack does not protect its own integrity
   (the 45-day ingest lost to the ephemeral layer is the proof — nothing
   guarded the memory; it was silently empty).

## THE PATTERN
The stack's lanes exist (mail digest, ingest, seamstress, briefs) but
none of them FIRE and INFORM on their own. Everything waits for the
operator's daily ask. That is the non-delivery.

## THE FIX
- The mail digest runs on schedule and DELIVERS the brief to the
  operator (not just writes to disk).
- Actions are reported when taken, not when asked.
- Self-preservation = the stack watches its own stores (ChromaDB
  volume, ORICO space, disk) and ALERTS on loss risk before it happens.

## STATUS
Filed. The mail lane + watchdogs must INFORM, not wait.
