# GROQ DECOMMISSION NOTE — Llama 3.3 70B Versatile (2026-08-16)
Source: GroqCloud email received (decommission date Aug 16, 2026).

## THE EVENT
- Llama 3.3 70B Versatile DECOMMISSIONED Aug 16, 2026 — requests no
  longer served.
- Groq recommends: GPT OSS 120B or Qwen3.6 27B as replacements.

## STACK STATE
- GROQ keys: 1 in /root/.zynthio.env (operator says multiple accounts
  exist — inventory them if more keys surface)
- llama-3.3-70b-versatile referenced ONLY in incident/handover docs
  (historical record, Aug 7 incidents) — NO live script uses it
- No code migration required: nothing live depends on the model

## ACTIONS TAKEN
- [x] Verified no live dependency (grep: only desk docs)
- [x] Noted replacement models: GPT OSS 120B / Qwen3.6 27B
- [ ] Optional: switch Groq lane to Qwen3.6 27B if a Groq rail is
      needed (the stack's primary lane is now local qwen3:8b-64k)

## STATUS
NOTED — no live breakage, replacement models on record.
