# DistroKid Release Checklist — DJ Zynrose / SongPal

**Distributor:** DistroKid
**Artist Name:** DJ Zynrose
**Legal Name:** Corey McIvor
**Jurisdiction:** New Zealand
**Last Updated:** 2026-04-16

---

## Pre-Submission Master Checklist

Use this before submitting any release to DistroKid.

---

## 1. Audio File Requirements

### Single / Album Track (WAV — required for high-quality stores)

- [ ] Format: WAV (preferred) or FLAC
- [ ] Bit depth: 16-bit minimum, **24-bit recommended**
- [ ] Sample rate: **44,100 Hz (44.1kHz)** — industry standard
  - 48kHz accepted by most stores; avoid 88.2kHz/96kHz (can cause issues)
- [ ] Channels: **Stereo** (2 channels)
- [ ] No DC offset (check in DAW before export)
- [ ] No clipping — true peak ≤ **-1.0 dBTP** (leave headroom for streaming normalisation)
- [ ] Recommended loudness target: **-14 LUFS integrated** (Spotify/Apple norm level)
- [ ] Silence: max 2 seconds silence at start and end
- [ ] File naming: `[ArtistSlug]_[TrackSlug]_MASTER.wav`
  - Example: `DJZynrose_TrackName_MASTER.wav`

### What DistroKid Accepts

| Format | Accepted |
|--------|----------|
| WAV (16 or 24-bit) | Yes (recommended) |
| FLAC | Yes |
| MP3 (320kbps) | Yes (lower quality stores only) |
| AIFF | Yes |

---

## 2. Cover Art Requirements

- [ ] **Dimensions:** 3000 × 3000 pixels (square, 1:1 ratio)
- [ ] **Minimum:** 1400 × 1400 px (DistroKid minimum — always use 3000×3000)
- [ ] **Format:** JPG or PNG
- [ ] **Color space:** sRGB
- [ ] **File size:** ≤ 10 MB
- [ ] **DPI:** 72 dpi (screen — stores don't use print DPI)
- [ ] **No explicit content in art** unless flagged for explicit stores
- [ ] **No URLs, social handles, or prices** in artwork (Apple/Spotify will reject)
- [ ] **No third-party logos** (Apple, Spotify, etc.) in artwork
- [ ] Text must be legible at 200×200px (thumbnail size on streaming platforms)
- [ ] File naming: `[ReleaseSlug]_cover_3000x3000.jpg`

---

## 3. Metadata — Required Fields

### Release-Level Metadata

| Field | Required | Notes |
|-------|----------|-------|
| Release Title | Yes | Exact capitalisation — no ALL CAPS unless stylistic |
| Artist Name | Yes | `DJ Zynrose` — must match DistroKid artist profile |
| Label | Yes | `SongPal` or `Corey McIvor` (if self-releasing) |
| Genre (Primary) | Yes | Choose from DistroKid's genre list |
| Genre (Secondary) | No | Optional but recommended |
| Release Date | Yes | YYYY-MM-DD format; minimum 3 days ahead for most stores |
| Language | Yes | `English` (or track language) |
| Country of Origin | Yes | `New Zealand` |
| UPC / EAN | Auto | DistroKid assigns free UPC — or supply your own |

### Track-Level Metadata (per track)

| Field | Required | Notes |
|-------|----------|-------|
| Track Title | Yes | Match filename exactly |
| Artist | Yes | `DJ Zynrose` |
| Featured Artist(s) | If applicable | Format: `DJ Zynrose feat. [Name]` |
| Composer(s) | Yes | Legal name(s) — `Corey McIvor` for originals |
| Lyricist(s) | Yes if lyrics exist | `Corey McIvor` or collaborator |
| Publisher | If registered | APRA AMCOS / SongPal if applicable |
| ISRC | Auto/Manual | DistroKid assigns free; supply own if you have one |
| Explicit | Yes | `Clean` or `Explicit` — be accurate |
| Track Number | Yes for albums | Sequential, starts at 1 |
| Disc Number | Albums only | Usually `1` |
| BPM | No | Recommended for electronic/dance genres |
| Key | No | Recommended for DJ/sync licensing |
| Lyrics | If applicable | Plain text via DistroKid lyrics uploader |

---

## 4. Lyrics Requirements

- [ ] Plain text format (`.txt`) — no HTML, no markdown
- [ ] Each line break = new lyric line
- [ ] Instrumental sections marked: `[Instrumental]`
- [ ] Ad-libs / background vocals: optional, mark as `(ad lib)` or `(background)`
- [ ] Explicit words: spell out fully (for platforms that display lyrics)
- [ ] Timed lyrics (LRC format): optional but improves sync display on Apple Music / Spotify
- [ ] File per track: `lyrics/[track-slug].txt`
- [ ] **NEVER reproduce copyrighted lyrics** — only upload original content

---

## 5. Store Distribution Selection

### Recommended Stores (DistroKid)

- [ ] Spotify
- [ ] Apple Music / iTunes
- [ ] YouTube Music
- [ ] Amazon Music
- [ ] Tidal
- [ ] Deezer
- [ ] Pandora
- [ ] iHeart Radio
- [ ] Napster
- [ ] Beatport (for electronic/dance — requires separate DistroKid add-on)
- [ ] Traxsource (for house/techno — separate add-on)
- [ ] SoundCloud (separate add-on)
- [ ] TikTok / Instagram / Facebook (included in most DistroKid plans)

### Territories

- [ ] Worldwide (recommended unless specific licensing conflicts)

---

## 6. Pre-Release Checklist (Final QA)

- [ ] Audio plays back without artefacts, pops, or clicks
- [ ] Track starts cleanly (no premature cutoff)
- [ ] Track ends cleanly (fade or proper ending — no abrupt silence gap > 2s)
- [ ] Cover art displays correctly at thumbnail size (test at 200×200px)
- [ ] All metadata proofread — spelling, capitalisation, artist name exact match
- [ ] Explicit tag correct
- [ ] Release date confirmed and calendared
- [ ] Lyrics reviewed and uploaded (if applicable)
- [ ] Backup of all files kept locally (WAV + cover art + metadata sheet)
- [ ] Track registered with APRA AMCOS (if publishing rights apply) — NZ

---

## 7. Post-Submission Actions

- [ ] Screenshot DistroKid confirmation / submission ID
- [ ] Note ISRC(s) assigned — add to `TRACK_MANIFEST.md`
- [ ] Note UPC assigned — add to `TRACK_MANIFEST.md`
- [ ] Set up Spotify for Artists / Apple Music for Artists (claim profile)
- [ ] Create Spotify Canvas (8-second looping video, 720×1280px)
- [ ] Schedule social media posts for release day (see `MUSIC_MARKETING.md`)
- [ ] Submit to playlist curators 4+ weeks before release date
- [ ] Update `TRACK_MANIFEST.md` status to `submitted` → `released`

---

## 8. Account Settings to Confirm (One-Time)

- [ ] DistroKid artist name set to `DJ Zynrose`
- [ ] Bank / payment details correct (NZD or USD payout)
- [ ] YouTube Content ID enabled (optional — catches covers / samples of your tracks)
- [ ] Store artist page links set up (Spotify for Artists URI in DistroKid)
- [ ] Songwriter / publisher profile reviewed

---

## Notes

- DistroKid processes most releases within 1–7 business days (Spotify can be faster)
- Apple Music requires minimum 10 days for new artists
- Always submit at least **2 weeks before** target release date to be safe
- Keep originals of all WAV masters offline (external drive or cloud backup)
