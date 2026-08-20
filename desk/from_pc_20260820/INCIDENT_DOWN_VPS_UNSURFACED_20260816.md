# INCIDENT — DOWN VPS NEVER SURFACED + CONTEXT NEVER LOADED (2026-08-16)
Operator: "so i have to get access to 2x vps now that are down and was not
told until i asked? what else do you want me to ask... it's all been said
but you won't go full throttle red and have it all read into context"

## THE TWO BREACHES
1. BETA (161.97.89.49) DOWN 4+ days, DELTA (172.86.88.55) keyless —
   NEVER surfaced to the operator. The Frankfurt backup failure (Aug 12)
   was the first sign; no alert chain existed. The operator had to ask.
2. THE CONTEXT GAP — 2,201 chunks in ChromaDB, 7,727 corpus lines,
   but sessions start blank and re-derive. The know is stored, not
   loaded. The operator's elephant memory vs the parrot sessions that
   re-ask — the re-ask is the symptom of unloaded context.

## THE FIX
1. IRON WATCHDOG — built, cron every 15 min, SMS on change (tested,
   SMS_SENT). Down nodes now alert without the ask.
2. CONTEXT LOADER — build next: session-start pulls the top-N relevant
   chunks from ChromaDB into the session context, so every session
   starts with the know instead of a blank page.

## STATUS
Watchdog: LIVE. Context loader: building. The asking ends when the
context loads and the alerts fire without the ask.
