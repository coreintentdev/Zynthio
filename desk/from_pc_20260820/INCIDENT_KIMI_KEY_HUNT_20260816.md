# INCIDENT — HUNTED FOR KIMI API KEY THAT NEVER EXISTED (2026-08-16)
Operator: "apis not to be found, devin did local in batch, you still looking
for key incident"

## THE BREACH
I searched the Mac and VDS for a Kimi API key (sk-*) across kimi files,
envs, and ALL_NOTES. The key was NEVER in the stack — because the Kimi
lane was ALWAYS local:
- kimi-debug-session_-20260726-203127.zip — a LOCAL session export
  (agents/main/wire.jsonl, 959KB — the full conversation wire log)
- Devin ran Kimi locally, in batch — the data exists in the local
  session files, not behind an API key
- The kimicredti/kimiapi files hold BALANCES (the billing pages), not
  keys — the key never had a home in the stack

## THE CORRECTED TRUTH
- No Kimi API key on VDS or Mac (0 sk- hits, 0 env entries)
- The Kimi data = the LOCAL session exports (wire.jsonl in the debug
  zips + the kimi* txt files)
- The rip = from the local files, not the API

## THE FIX
- Stop the key hunt. Rip the local wire.jsonl + kimi txt files into the
  corpus instead — the data is already on disk.

## STATUS
CORRECTED — the key hunt filed as the incident it was; the local rip is
the real lane.
