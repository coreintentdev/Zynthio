# INCIDENT — GROK KEYS "LOST" 3× WITH HERMES (2026-08-18) — RESOLVED
Operator: "report major incident grok keys done 3 times with hermes and
still lost. find them all sources all vds"

## THE COMPLAINT
Grok keys given to Hermes 3 times, still lost.

## THE EVIDENCE FOUND (all sources swept)
1. **KEY 1 — gsk_lOzJ... (56 chars)** — in /root/STACK_LIVE.env + 3
   dated backups (anthropic_20260807, ingest_20260729, pre_keypush_
   20260729). The LIVE /root/.zynthio.env held a 7-char STUB — the
   value was stripped at some point (env surgery).
2. **KEY 2 — gsk_tioz8...oPoD (56 chars)** — pasted into Hermes API
   setup on 2026-05-28, captured 3× in VDS Log captures (9:44am,
   1:12pm, 1:13pm — the "done 3 times"): txt_one_home/VDS_Log at
   2026-05-28*.txt. Never reached the env — the pastes stayed in the
   logs.

## VERIFICATION
- Restored KEY 1 to live env: GROQ_API_KEY now 56 chars
- BOTH keys tested against api.groq.com: AUTH OK, 13 models each
- Neither was lost: one stubbed, one unimported from the logs

## THE TRUTH
The stack holds TWO verified-working Groq keys, not "12 odd". If more
accounts exist, they were never on the VDS. The claim "12 keys lost"
was the same class as the Kimi key: not lost, never there / never
consolidated.

## ACTIONS
- [x] Restore KEY 1 to live env (56 chars, verified AUTH OK)
- [x] KEY 2 preserved in corpus (May 28 logs), verified AUTH OK
- [x] Both keys committed to the desk record (values masked)
- [ ] Optional: consolidate both into STACK_LIVE.env canonical store
- [ ] VDS mesh: VERIFIED ONLINE (100.64.0.2 active, PC ping 0% loss)

## STATUS
RESOLVED — keys found, restored, verified live.
