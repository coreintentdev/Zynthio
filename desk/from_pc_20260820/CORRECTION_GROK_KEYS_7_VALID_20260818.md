# CORRECTION — GROK KEYS: 7 VALID, NOT 2 (2026-08-18)
Operator: "so you only got 2x grok keys?"

## THE FIRST PASS WAS WRONG
The targeted grep found 2 keys (lOzJs, tioz8). The FULL filesystem
sweep found 13 distinct gsk_ entries — 7 UNIQUE VALID keys, all AUTH
tested against api.groq.com (13 models each).

## THE VERIFIED COUNT (13 entries -> 7 valid, 3 unique invalid)
VALID (7):
- gsk_3kQZ1...  herms.env (proton-onboarding)
- gsk_QzaNX...  GROQ_KEYS_ACTIVE.md + claude-conversations-93.json
- gsk_WEgp2...  GROQ_KEYS_ACTIVE.md + claude-conversations-93.json
- gsk_dDlk6...  Google AI Studio paste Mar 29 2026
- gsk_lOzJs...  STACK_LIVE.env + 3 backups (restored to live env)
- gsk_nd2m7...  GROQ_KEYS_ACTIVE.md
- gsk_tioz8...  zynthio.env backups + May 28 VDS Logs (the "3 times")

INVALID (3 unique, rotated/stale):
- gsk_BBnce...  claude-conversations-93.json
- gsk_jqpps...  claude-conversations-93.json (x3 occurrences)
- gsk_QzaNX...  one rotated variant

## SOURCES MAPPED
- env files: STACK_LIVE.env(.bak x3), zynthio.env (STATE_BACKUP +
  proton-onboarding), herms.env
- corpus: GROQ_KEYS_ACTIVE.md (the documented active list),
  claude-conversations-93.json, Google AI Studio pastes, VDS Logs
  May 28, INCIDENT_55_ALL_CHATBOTS_BROKEN_20260326.md,
  FULL_PERPLEXITY_ACCOUNT_HANDOVER.md

## STATUS
CORRECTED — 7 valid live keys, 3 stale, full source map on record.
