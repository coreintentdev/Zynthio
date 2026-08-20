# BILLING LEDGER — 9-MONTH FULL REVIEW (2026-08-15)
Source: 1,423 payment/receipt/billing emails across 3 exports on VDS
(18,359 total .eml scanned · 1,423 payment-related)

## PROVIDER TOTALS (receipts)
| Provider | Count | Notes |
|---|---|---|
| Anthropic | 459 | LARGEST — Claude charges, the 9-month burn never on any burn-first list |
| Cloudflare | 87 | domains/DNS/registrar |
| Perplexity | 42 | AI search subs (auto-reload flagged P1) |
| Brave | 24 | $1.12 payments repeatedly UNSUCCESSFUL |
| LiveAvatar | 24 | subscription; payment FAILED 2026-03-30 |
| Google | 19 | Google Pay Australia |
| ElevenLabs | 12 | voice API |
| X | 12 | X Premium |
| HeyGen | 9 | avatar video |
| Kits AI | 6 | receipt 2026-03-28 (#2531-8292) + FAILED payment 2026-03-27; key ZERO calls |
| Suno | 6 | the working lane |
| PINNACLE | 6 | unidentified |
| Infiniti | 6 | unidentified |
| Moonshot | 3 | invoice download |
| AWS/Amazon | 3 | billing statements |
| Others/unparsed | ~700 | need per-email amount extraction |

## KNOWN ZERO-USE PAID SERVICES (verified)
- Kits AI: charged, failed payment, key never used (KITS_API_KEY in env, no calls)
- LELAPA/Vulavula: $9.99/mo since 2026-06-29, token expires 2026-09-27, ZERO calls
- LiveAvatar: subscription with failed payment — service state unknown
- Brave: $1.12 charges failing repeatedly — likely dead card entry, not real product

## ACTION
1. Full per-email AMOUNT extraction (the 1,423) → $ total per provider per month
2. Verify each paid service: used / unused / failed → cancel unused
3. Add Anthropic to the digest burn-first list (it was MISSING despite 459 receipts)
4. Monthly billing review cron: count new charges, flag unused paid services

## THE NUMBER
Not yet summed (amount extraction pending) — but the shape is known:
459 Anthropic charges dominate. The 9-month loss is real and countable.
