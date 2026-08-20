# API PLANS LIVE — expiry & billing register (2026-08-15)
Source of truth for every API key in /root/.zynthio.env (33 keys). Update on any plan change.
Probe: monthly cron alerts 30d before expiry. Status: LIVE = tested working · UNVERIFIED = key present, not tested · EXPIRED = known dead

## DOCUMENTED PLANS
| Service | Key(s) in env | Plan | Cost | Token TTL | Expires | Status |
|---|---|---|---|---|---|---|
| Lelapa AI (Vulavula) | LELAPA_API_TOKEN, VULAVULA_CLIENT_TOKEN | Dev Pass | $9.99/mo | 90d | **2026-09-27** | UNVERIFIED — 0 calls ever made |
| Suno (sunoapi.org) | SUNO_API_KEY | 7,750 credits | paid | — | — | LIVE (2 songs generated today) |
| Evolink | EVOLINK_API_KEY | unlimited | — | — | — | LIVE (credit check OK) |
| Twilio | TWILIO_ACCOUNT_SID/AUTH_TOKEN | SMS | pay-per-use | — | — | LIVE (2 sends today) |
| DeepSeek | DEEPSEEK_API_KEY | pay-as-you-go (standing rule: NO subscription) | — | — | — | UNVERIFIED |
| Anthropic | ANTHROPIC_API_KEY | — | — | — | — | UNVERIFIED |
| OpenAI | OPENAI_API_KEY | — | — | — | — | UNVERIFIED |
| Groq | GROQ_API_KEY | — | — | — | — | UNVERIFIED |
| Gemini | GEMINI_API_KEY | — | — | — | — | UNVERIFIED |
| Kits.ai | KITS_API_KEY | **NO PLAN DOC — unknown cost/expiry** | ? | ? | ? | UNVERIFIED |
| HeyGen | HEYGEN_API_KEY | — | — | — | — | UNVERIFIED |
| D-ID | DID_API_KEY | — | — | — | — | UNVERIFIED |
| ElevenLabs | ELEVENLABS_API_KEY | — | — | — | — | UNVERIFIED |
| Exa | EXA_API_KEY | — | — | — | — | UNVERIFIED |
| Firecrawl | FIRECRAWL_API_KEY | — | — | — | — | UNVERIFIED |
| NVIDIA | NVIDIA_API_KEY | — | — | — | — | UNVERIFIED |
| Nous | NOUS_API_KEY | banned — operator rule "NO Nous subscription" | — | — | — | DO NOT USE |
| Lumo | LUMO_API_KEY | — | — | — | — | UNVERIFIED |
| Porkbun | PORKBUN_API_KEY/SECRET | — | — | — | — | DEAD (403 IP-block from VDS) |

## ACTIONS REQUIRED (operator paste, one screen each)
1. KITS.AI dashboard → plan + renewal date + cost (only key with zero documentation)
2. LELAPA → confirm token still valid before 2026-09-27 or regenerate
3. Each UNVERIFIED service: one test call each (agent can do this with a probe script — no operator action needed)

## PROBE (to build)
- Monthly cron: curl a read-only endpoint per key, log 200/401/403, alert SMS if any key fails or 30d from expiry
- Same pattern as cf_pb_health.sh (already daily on VDS)
