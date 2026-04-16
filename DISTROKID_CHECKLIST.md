# DistroKid Release Checklist — DJ Zynrose / SongPal

> **Artist:** DJ Zynrose (legal name: Corey McIvor)
> **DistroKid account:** _(link your DK account URL here)_
> **Jurisdiction:** New Zealand
> **Last updated:** 2026-04-16

Use this checklist for every track or release before submitting to DistroKid. Copy the per-release section for each new upload.

---

## 1. Account & Artist Profile

- [ ] DistroKid account active and subscription current
- [ ] Artist name locked in as **DJ Zynrose** (consistent across all releases)
- [ ] Spotify for Artists claimed: `open.spotify.com/artist/...`
- [ ] Apple Music for Artists claimed
- [ ] YouTube Music OAC (Official Artist Channel) linked
- [ ] Amazon Music for Artists claimed
- [ ] Hyperfollow link created for pre-saves (DistroKid HyperFollow tool)
- [ ] Bank/payout details verified (NZ bank account or Payoneer)
- [ ] Tax info filed (NZ — no US withholding required; complete W-8BEN for IRS exemption)

---

## 2. Audio Master Requirements

| Spec | Requirement | Status |
|------|-------------|--------|
| Format | WAV (lossless) | |
| Bit depth | 24-bit (minimum) | |
| Sample rate | 44,100 Hz (44.1 kHz) or 48,000 Hz | |
| Channels | Stereo (2-channel interleaved) | |
| Loudness | -14 LUFS integrated (Spotify/Apple standard) | |
| True peak | -1.0 dBTP maximum | |
| Silence | No DC offset; no clipping; clean tail | |
| File naming | `DJ Zynrose - Track Title (Master).wav` | |

### Mastering Notes
- Use a proper limiter — do not clip the master bus.
- Aim for -14 LUFS integrated for streaming; can go louder (-10 LUFS) for club/DJ releases but expect normalisation.
- Leave 1–2 seconds of silence at start and end (DistroKid trims automatically but cleaner is better).
- Check mono compatibility — sum to mono and verify no phase cancellation.

---

## 3. Cover Art Requirements

| Spec | Requirement | Status |
|------|-------------|--------|
| Dimensions | Exactly 3000 × 3000 pixels | |
| Format | JPG or PNG | |
| Colour space | RGB (not CMYK) | |
| Resolution | 72 DPI minimum (300 DPI print-quality recommended) | |
| File size | Under 10 MB | |
| Content | No URLs, social handles, or pricing text | |
| Content | No explicit imagery (follow platform content policies) | |
| Content | No third-party logos without clearance | |
| File naming | `DJ Zynrose - Track Title - Cover.jpg` | |

### Cover Art Tips
- Square format is non-negotiable — platforms reject rectangular art.
- Text must be legible at 150×150 px (thumbnail size on mobile).
- High-contrast backgrounds perform better in dark-mode UI.
- Store master PSD/AI source files in `assets/covers/source/` (do NOT commit to git — use cloud storage).

---

## 4. Metadata — Per Track

Copy this block for each release.

```
Release Title:        ___________________________________
Artist Name:          DJ Zynrose
Featuring Artist(s):  (if applicable)
Album / EP / Single:  ___________________________________
Track Number:         ___________________________________  (for albums/EPs)
Genre:                ___________________________________
Sub-genre:            ___________________________________
Release Date:         YYYY-MM-DD  (Fridays recommended)
Language:             English
Explicit:             Yes / No / Clean version
Lyrics:               Yes / No
ISRC:                 (auto-assigned by DistroKid — record after upload)
UPC:                  (auto-assigned per album — record after upload)
Label Name:           SongPal  (or "DJ Zynrose" for self-release)
Copyright Year:       2026
Copyright Owner:      Corey McIvor
Publishing Info:      (if registered with APRA AMCOS — NZ) 
```

### Metadata Rules
- Title case for track and album names.
- No ALL CAPS titles (platforms may reject).
- No featuring credits in the main Artist Name field — use the "Featuring" field.
- No emojis in title or artist name.
- Verify spelling before submit — ISRC is tied to the metadata; errors require a re-upload.

---

## 5. Lyrics (Optional but Recommended)

- [ ] Lyrics written and reviewed
- [ ] Saved to `lyrics/track-name-slug.txt` in this repo
- [ ] Lyrics formatted as plain text, line-by-line (no chords, no brackets)
- [ ] Uploaded to DistroKid's lyrics field (enables Spotify lyrics display)
- [ ] Synced lyrics (`.lrc` format) created if you want karaoke-style sync

### Lyrics File Format
```
Verse 1
Line one of lyrics
Line two of lyrics

Chorus
Chorus line one
Chorus line two

Verse 2
...
```

---

## 6. Distribution Platform Selection

| Platform | Include? | Notes |
|----------|----------|-------|
| Spotify | Yes | Priority — largest streaming base |
| Apple Music | Yes | Second priority |
| YouTube Music | Yes | Also auto-creates Content ID for YouTube |
| Amazon Music | Yes | Includes Prime Music & Unlimited |
| Tidal | Yes | HiFi audience — good for electronic/DJ |
| Deezer | Yes | Strong in EU and LATAM markets |
| Pandora | Yes | US-heavy but worth including |
| iHeartRadio | Yes | |
| TikTok / Reels / Shorts | Yes | Critical for viral discovery |
| Beatport | Optional | Best for club-oriented electronic; separate upload |
| Traxsource | Optional | House/deep house specialist |
| Bandcamp | Optional | Direct-to-fan; good for DJ community |
| SoundCloud | Optional | DistroKid can push, or upload directly |

---

## 7. Pre-Release Checklist

- [ ] Release date set at least **7 days out** (minimum for editorial consideration)
- [ ] Pitching to Spotify editorial via Spotify for Artists (submit at least 7 days before release)
- [ ] Apple Music editorial pitch submitted
- [ ] HyperFollow pre-save link created and shared
- [ ] Social teaser content prepared (15-sec clip, artwork reveal)
- [ ] Press kit prepared (bio, hi-res photo, cover art)

---

## 8. Post-Release Checklist

- [ ] ISRC recorded in `TRACK_MANIFEST.md`
- [ ] UPC recorded in `TRACK_MANIFEST.md`
- [ ] Track appears on all selected platforms (allow 24–72 hours)
- [ ] Spotify for Artists — confirm stream counts appearing
- [ ] Apple Music for Artists — confirm
- [ ] YouTube Content ID active (check DistroKid dashboard)
- [ ] Submit to independent playlist curators (see `MUSIC_MARKETING.md`)
- [ ] Update track status in `TRACK_MANIFEST.md` to `released`
- [ ] Collect release stats at Day 7, Day 30, Day 90

---

## 9. APRA AMCOS Registration (NZ Performing Rights)

- [ ] Registered with APRA AMCOS (New Zealand performing rights organisation)
- [ ] Each track registered as a work with APRA AMCOS
- [ ] IPI/CAE number obtained
- [ ] Publishing share confirmed (100% if self-written, adjust for co-writes)
- [ ] APRA AMCOS connected to DistroKid publishing admin (if using DK's publishing arm)

> APRA AMCOS: [www.apra-amcos.com.au](https://www.apra-amcos.com.au) — covers both Australia and NZ, but Corey McIvor is registered as a **New Zealand** member.

---

## 10. Common Rejection Reasons (Avoid These)

| Issue | Fix |
|-------|-----|
| Cover art not square | Resize to exactly 3000×3000 |
| Cover art has URLs or prices | Remove all URLs/pricing |
| WAV is MP3-encoded (transcoded) | Export fresh WAV from DAW |
| Track title has ™ or ® | Remove symbols |
| Metadata has ALL CAPS title | Use Title Case |
| Audio clipping | Re-master, re-export |
| Duplicate ISRC | Use unique ISRC per track version |
| Explicit content not flagged | Mark explicit if any strong language |

---

_All releases under NZ jurisdiction. Founder: Corey McIvor. Platform: SongPal. Distribution: DistroKid._
