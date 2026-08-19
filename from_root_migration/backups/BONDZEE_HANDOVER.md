# Bondzee — Artist pages handover

**Operator:** Corey James McIVOR · ZYNTHIO™  
**Date:** 2026-07-03  
**Domains:** bondzee.live (live station apex) · bondzee.bond (bond lane)  
**VDS root:** `/var/www/bondzee.bond` (nginx: `pork_bondzee_lookcy.conf`)

## Operator relationship (Corey memory — 2026-07-03)

| Fact | Detail |
|------|--------|
| **HIP live** | Bondzee played live at **The HIP** bar, San Juan del Sur — Corey ran **audio production + live feed** |
| **Greg intro** | **Greg (The HIP)** suggested Corey and Bondzee work together — same Greg lane as `clearstreamchurch.com` |
| **Fame** | Already known on multiple channels (YouTube, FB, TikTok, IG) — full audit not done in TTL |
| **Production manager** | Has or had one — **ZYNTHIO stack** target: prompts → stems → pages → distro in one seamless lane |
| **Earn model** | Artist earns from **typing ideas/prompts** into stack + recording contract path — not platform rent |
| **Vocal lane** | Loves to sing **The Tragically Hip** — **Gord Downie** / Canadian rock. Demo should be Hip-adjacent (poetic, gritty, live-room) not generic template |

## TTL / Grok lookup result

**18JUNE TTL export has zero Bondzee artist intel** — only Porkbun domain rows (`bondzee.live`, `bondzee.bond` added 2026-07-02). Public research + operator HIP memory used for copy:

| Field | Detail |
|-------|--------|
| Host | **Bondzee** — Brett **"Bonzi"** · also **Wellness With Bondzee** |
| Show | **Trippin With Bondzee** — raw, humorous **podcast + live broadcast** |
| Topics | Life adventures, entertainment news, sports, musician interviews |
| Guests (public) | **Trevor Hurst** (Econoline Crush) · **Brett Emmons** (The Glorious Sons) |
| Platforms | **Apple Podcasts**, **YouTube** (+ Facebook, TikTok, IG, X) |
| Ref | `BONDZEE_PUBLIC_INTEL_20260703.json` |

| Source | Handle | Notes |
|--------|--------|-------|
| Instagram | @bondzeelive | Wellness With Bondzee |
| X | @bondzeelive | Creator · dad · #811overeverything |
| Facebook | Bmayzee | Buffalo roots |

## Offer to Bondzee

1. **Recording artist spot** on SongPal / ZYNTHIO roster (artist keeps masters; SongPal 80/20 model available).
2. **Sovereign pages** on bondzee.live + bondzee.bond (deployed from this folder).
3. **Stack walkthrough** — how to promote via network cross-links (808.radio, show funnel, Pelican, Nica, Discover RE lanes).

## Pages

| Path | File | Purpose |
|------|------|---------|
| `/` | `index.html` | Artist hub — show, socials, domains |
| `/stack/` | `stack/index.html` | Recording artist offer + promotion playbook |

## Deploy

```bash
cd ~/Desktop/zynthio-tools/18JUNE/bondzee.live
./deploy_bondzee.sh
```

Then purge CF cache for bondzee.live + bondzee.bond if stale placeholder shows.

## Proof (live now)

- https://bondzee.live/ — artist hub (origin + public **200**)
- https://bondzee.live/stack/ — recording artist offer
- https://bondzee.bond/ — same stack (bond lane)
- https://336orchestra.xyz/roster/ — Bondzee on 336 Orchestra roster

## Outreach draft (send + one song attachment)

> Bondzee — Corey McIvor (ZYNTHIO). We already worked the room together: I mixed and ran the **live feed when you played The HIP** in San Juan. Greg said we should link up — I built you two domains before asking for anything back.
>
> **bondzee.live** + **bondzee.bond** are live. Open **bondzee.live/stack/** — that’s your recording artist spot on our network: sovereign pages (not Linktree), Trippin → one hub, production that doesn’t fight your manager workflow, and a path to **earn from prompts and ideas** on the stack — masters stay yours.
>
> You sing **The Tragically Hip** — **Gord Downie** country. I hear that. Attached: **[Gord-style room demo — Corey picks or fresh stem]** — recorded like the HIP bar, not a template.
>
> If it hits, book a 20-min walkthrough: **corey@zynthio.ai**. No obligation — pages are proof. Call if you like it.

### Demo brief (Suno / studio)

- **Vocal:** male, gritty-poetic, Gord Downie lane — not impersonation, **original lyrics only**
- **Band:** Canadian rock room — mid-tempo, live drums, Hammond-ish, bar-room warmth (SJDS HIP memory)
- **Avoid:** generic trap template; copyrighted Hip lyrics on first send (cover lane later if he wants)

## Next (operator)

- [ ] Pick **one song/demo** to attach (no Bondzee-titled track in manifests — Suno pick or fresh stem)
- [ ] Send via IG DM @bondzeelive or channel he replies on fastest
- [ ] Bondzee walkthrough call — confirm email + music links
- [ ] Add Spotify/Apple/YouTube Music URLs when provided
- [ ] Embed latest Trippin episode on index
- [ ] Mention Greg/HIP connection on call — warm intro already earned
- [ ] SongPal apply link if he wants formal roster paperwork

Signal 336. No drift.