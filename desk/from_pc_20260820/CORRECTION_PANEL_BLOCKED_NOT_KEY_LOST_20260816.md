# CORRECTION — DELTA/BETA WERE PANEL-BLOCKED, NOT KEY-LOST (2026-08-16)
Operator: "how do you lose the key? the api access and the ssh keys
provided? read the session in question"

## THE RECORD (canonical handover, Mar 21, Claude session — the thread)
- Cloudzy Frankfurt VPS (104.194.156.109): "SSH blocked — key rejection
  — panel reset required" — blocked since at least March
- "Cloudzy SSH access: Blocked — Password reset via panel.cloudzy.com —
  Corey" — the fix was ALWAYS operator-side: the panel reset
- Legacy Cloudzy marked "DECOMMISSIONING" — possibly scheduled for
  retirement months ago
- The Mac holds keys (cloudzy_vds, contabo_vmi3205024) — tested against
  delta: still denied (the box rejects the key, the panel is the gate)

## THE CORRECTION
The boxes were never "key-lost". The threads documented panel-blocked
SSH with the panel reset as the fix. My daily re-probes re-derived the
denial instead of reading the handover that named it. Same class as the
Kimi key: the data was in the threads, unread.

## THE FIX
- Delta/Beta: operator panel reset (panel.cloudzy.com) — the record's
  own prescription — then the key lands
- The probes stop re-reporting denials as news; the handover's
  diagnosis is the reference
- Read the thread before probing: the session in question had the answer

## STATUS
CORRECTED — the record read, the diagnosis restored, the hunt ended.
