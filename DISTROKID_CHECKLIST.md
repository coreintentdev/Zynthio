# DistroKid Submission Checklist — DJ Zynrose

**Maintained by:** Corey McIvor (corey@coreyai.ai)
**Jurisdiction:** New Zealand
**Last Updated:** 2026-04-16
**Distribution:** DistroKid (Musician Plus or higher recommended)

---

## Account Setup (One-Time)

- [ ] DistroKid account created under Corey McIvor (NZ)
- [ ] Artist name set to **DJ Zynrose**
- [ ] Payment account linked (NZ bank account or PayPal — NZ jurisdiction)
- [ ] Spotify for Artists claimed
- [ ] Apple Music for Artists claimed
- [ ] YouTube Music OAC (Official Artist Channel) claimed
- [ ] Beatport / Traxsource added (if Electronic/Dance releases)
- [ ] ISRC auto-generation enabled (DistroKid can assign these)
- [ ] UPC auto-generation enabled

---

## Per-Track Submission Requirements

Use this checklist for every track before clicking Submit in DistroKid.

---

### 1. Audio File

| Requirement | Spec | Status |
|------------|------|--------|
| Format | WAV (preferred) or FLAC | ☐ |
| Sample Rate | 44,100 Hz (44.1 kHz) minimum | ☐ |
| Bit Depth | 24-bit minimum (32-bit float acceptable) | ☐ |
| Channels | Stereo (2-channel) | ☐ |
| Peak Level | -1.0 dBTP true peak maximum (leave headroom for streaming loudness normalisation) | ☐ |
| Integrated Loudness | -14 LUFS (Spotify/Apple target); master at -14 to -16 LUFS | ☐ |
| No clipping | Confirmed via meter / limiter | ☐ |
| No silence at start/end | First transient within 0.5s; tail fades cleanly | ☐ |
| Filename | `[TrackID]_[ArtistName]_[TrackTitle]_MASTER.wav` | ☐ |

**Loudness reference:**
- Spotify: −14 LUFS
- Apple Music: −16 LUFS
- YouTube: −14 LUFS
- Tidal: −14 LUFS
> Master to −14 LUFS integrated; streaming platforms will apply normalisation. Do NOT brick-wall limit to −8 LUFS.

---

### 2. Cover Art

| Requirement | Spec | Status |
|------------|------|--------|
| Dimensions | Exactly **3000 × 3000 px** | ☐ |
| Format | JPG or PNG | ☐ |
| Colour Mode | RGB (not CMYK) | ☐ |
| File Size | Under 10 MB | ☐ |
| Resolution | 300 DPI minimum | ☐ |
| No text violations | No website URLs, social handles, or pricing in artwork | ☐ |
| No explicit imagery | Or mark track as Explicit if needed | ☐ |
| Artist name visible | "DJ Zynrose" legible at thumbnail size (200×200) | ☐ |
| Track title visible | Legible at thumbnail size | ☐ |
| Filename | `[TrackID]_[TrackTitle]_COVER_3000x3000.jpg` | ☐ |

---

### 3. Metadata

Fill in for every release in DistroKid's upload form:

| Field | Example / Notes | Status |
|-------|----------------|--------|
| **Track Title** | Exact capitalisation; no ALL CAPS unless stylistic | ☐ |
| **Primary Artist** | `DJ Zynrose` | ☐ |
| **Featuring Artists** | Only if a feature exists | ☐ |
| **Album / Release Title** | Single title or EP/Album name | ☐ |
| **Release Type** | Single / EP / Album | ☐ |
| **Genre (Primary)** | e.g. Electronic | ☐ |
| **Genre (Secondary)** | e.g. Dance / Techno / Synthwave | ☐ |
| **Release Date** | At least 7 days out for standard; 4+ weeks for Spotify editorial pitch | ☐ |
| **Language** | English (or correct language) | ☐ |
| **Explicit / Clean** | Mark honestly | ☐ |
| **ISRC** | Auto-assigned by DistroKid or enter if pre-assigned | ☐ |
| **UPC** | Auto-assigned by DistroKid | ☐ |
| **Composers / Writers** | Corey McIvor (full legal name) | ☐ |
| **Publishers** | Leave blank if self-published / no PRO deal | ☐ |
| **PRO Affiliation** | APRA AMCOS (NZ/AU) or SOCAN — register if not yet done | ☐ |
| **Copyright Year** | Current year (e.g. 2026) | ☐ |
| **Copyright Holder** | Corey McIvor | ☐ |
| **Lyrics** | Paste or upload (see section 4) | ☐ |

---

### 4. Lyrics

| Requirement | Notes | Status |
|------------|-------|--------|
| Plain text file exists | `lyrics/[TrackTitle].txt` in this repo | ☐ |
| Lyrics are original | No copyrighted third-party content reproduced | ☐ |
| Synced lyrics (LRC) | Optional but recommended for Spotify Canvas & Apple | ☐ |
| Language tagged correctly | Match metadata language field | ☐ |
| Explicit words flagged | If marked Explicit, confirm lyrics match | ☐ |

---

### 5. Distribution Settings

| Setting | Recommendation | Status |
|---------|---------------|--------|
| Store Selection | All stores (default) — deselect only if specific exclusions needed | ☐ |
| TikTok / Reels | Enable — important for discovery | ☐ |
| Beatport (if Electronic) | Enable if genre qualifies | ☐ |
| Pre-save campaign | Set up via DistroKid SmartLink or third-party (e.g. feature.fm) | ☐ |
| Spotify Pitch | Submit to Spotify editorial via Spotify for Artists dashboard at least 7 days before release | ☐ |

---

### 6. Pre-Release Checklist

- [ ] Track uploaded to DistroKid — status shows "Pending Review"
- [ ] Cover art accepted (no rejection email within 24h)
- [ ] Spotify pre-save link created and shared
- [ ] Editorial pitch submitted (Spotify for Artists)
- [ ] Social posts scheduled (see MUSIC_MARKETING.md)
- [ ] Pre-release announcement posted
- [ ] YouTube Content ID opted in (DistroKid option)

---

### 7. Post-Release Checklist

- [ ] Track live on Spotify — confirm via Spotify for Artists
- [ ] Track live on Apple Music
- [ ] Track live on YouTube Music
- [ ] ISRC recorded in TRACK_MANIFEST.md
- [ ] UPC recorded in TRACK_MANIFEST.md
- [ ] Analytics tracking started (Spotify for Artists, Apple Music for Artists)
- [ ] Track status updated to `RELEASED` in TRACK_MANIFEST.md
- [ ] Release Calendar updated

---

## APRA AMCOS Registration (NZ/AU PRO)

> Register as a writer/publisher with APRA AMCOS for performance royalty collection.
> This is separate from DistroKid and covers radio, live, and sync royalties.

- [ ] APRA AMCOS account created: https://www.apra-amcos.com.au
- [ ] Each released track registered with APRA AMCOS
- [ ] IPI number recorded for metadata

---

## Notes

- DistroKid retains 0% of revenue (flat annual fee model) — confirm current plan
- For Electronic/Dance tracks, consider Beatport direct distribution via DistroKid
- SongPal platform brand can be used for artist/label name in future if desired
- All business/legal is NZ jurisdiction — NEVER register as an Australian entity
