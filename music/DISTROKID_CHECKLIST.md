# DistroKid Upload Checklist — DJ Zynrose / SongPal
**Artist:** DJ Zynrose (Corey McIvor)  
**Distributor:** DistroKid  
**Jurisdiction:** New Zealand  
**Last Updated:** 2026-04-16  
**Status:** DRAFT — verify against current DistroKid requirements before uploading

---

## Global Account Settings (One-Time Setup)

- [ ] Artist name set to: **DJ Zynrose**
- [ ] Legal name (real name) set to: **Corey McIvor**
- [ ] Country of residence: **New Zealand**
- [ ] Bank/payment details configured for NZD or preferred currency
- [ ] Spotify for Artists claim completed
- [ ] Apple Music for Artists claim completed
- [ ] YouTube Official Artist Channel linked
- [ ] PRO (Performing Rights Organisation) registered — *APRA AMCOS recommended for NZ*
- [ ] Publisher name set (if applicable)
- [ ] DistroKid Musician Plus or higher plan active (required for ISRC customisation)

---

## Per-Track Checklist

Copy this section for each track. Replace `[TRACK NAME]` with the actual title.

---

### Track: [TRACK NAME]

#### 1. Audio File
- [ ] Format: **WAV** (preferred) or FLAC
- [ ] Bit depth: **24-bit minimum** (16-bit acceptable, 24-bit strongly preferred)
- [ ] Sample rate: **44.1 kHz or 48 kHz**
- [ ] Channels: **Stereo** (not mono, not surround)
- [ ] Duration: > 30 seconds (Spotify royalty threshold)
- [ ] No silence at start/end beyond 0.5 seconds
- [ ] No clipping — peaks at **-0.3 dBFS or lower**
- [ ] LUFS target: **-14 LUFS integrated** (Spotify normalisation standard)
- [ ] File naming: `DJZynrose_[TrackName]_Master_24bit_44.1kHz.wav`

#### 2. Cover Art
- [ ] Resolution: **3000 × 3000 pixels minimum** (3000×3000 exact is ideal)
- [ ] File format: **JPG or PNG**
- [ ] File size: under 10 MB
- [ ] Colour mode: **RGB** (not CMYK)
- [ ] No blurriness — must be sharp at 3000×3000
- [ ] No explicit content visible unless flagged as explicit
- [ ] No URLs, social handles, pricing, or third-party logos in the artwork
- [ ] No misleading artist names or references to other major artists
- [ ] Font is legible (DistroKid may reject low-contrast or unreadable text)
- [ ] File naming: `DJZynrose_[TrackName]_CoverArt_3000x3000.jpg`

#### 3. Track Metadata
- [ ] **Title:** exact track name, correct capitalisation
- [ ] **Artist:** DJ Zynrose
- [ ] **Featuring artists:** listed if applicable (format: `DJ Zynrose feat. [Name]`)
- [ ] **Album / Single title:** confirmed and consistent with other tracks if part of a project
- [ ] **Genre (primary):** *(TBC)*
- [ ] **Genre (secondary):** *(TBC)*
- [ ] **Release date:** planned date set (minimum 3–5 business days ahead for DistroKid processing; 3–4 weeks recommended for Spotify editorial pitching)
- [ ] **Explicit content flag:** Yes / No / Clean version
- [ ] **Language:** English
- [ ] **Lyrics language:** English
- [ ] **Country of recording:** New Zealand
- [ ] **Copyright line:** `℗ [YEAR] Corey McIvor / SongPal`
- [ ] **Publishing line:** `© [YEAR] Corey McIvor / SongPal`

#### 4. ISRC Code
- [ ] ISRC assigned (format: `NZ-XXX-YY-NNNNN`)
  - Country code: `NZ` (New Zealand)
  - Registrant: *(register with RECORDED MUSIC NZ or via DistroKid auto-assign)*
- [ ] ISRC recorded in `TRACK_MANIFEST.md`
- [ ] ISRC embedded in WAV metadata (optional but best practice)

#### 5. UPC / Barcode (for albums/EPs)
- [ ] UPC assigned (DistroKid auto-assigns or you can provide one)
- [ ] UPC recorded in `TRACK_MANIFEST.md`

#### 6. Lyrics
- [ ] Plain-text lyrics file created at `music/lyrics/[track-slug].txt`
- [ ] Lyrics uploaded to DistroKid (enables Spotify Canvas lyrics, Apple Music lyrics sync)
- [ ] Lyrics proofread — no spelling errors
- [ ] Timed lyrics (LRC format) prepared if available: `music/lyrics/[track-slug].lrc`

#### 7. Legal Clearance Sign-Off
- [ ] Composition: 100% original **OR** all co-writers listed and splits agreed
- [ ] Samples: none **OR** all samples licensed (attach licence documents to release folder)
- [ ] Cover song: N/A **OR** mechanical licence obtained via DistroKid's cover song licensing
- [ ] Clearance status updated in `TRACK_MANIFEST.md`

#### 8. Pre-Release Tasks
- [ ] Spotify editorial pitch submitted (requires release date ≥ 7 days out; submit via Spotify for Artists)
- [ ] Apple Music Connect post scheduled
- [ ] Pre-save / pre-order link created (via DistroKid HyperFollow or Toneden)
- [ ] Smart link (HyperFollow) QR code generated for promo materials
- [ ] Press kit updated with new track info

---

## DistroKid Distribution Store Targets

Check all stores you want the track distributed to:

- [ ] Spotify
- [ ] Apple Music / iTunes
- [ ] Amazon Music Unlimited
- [ ] YouTube Music
- [ ] Tidal
- [ ] Deezer
- [ ] Pandora (US)
- [ ] iHeartRadio
- [ ] Napster
- [ ] TikTok / Resso
- [ ] Instagram / Facebook (audio library)
- [ ] Soundtrack by Twitch
- [ ] Beatport / Traxsource *(electronic genres — may require separate submission)*

---

## Post-Upload Verification

- [ ] DistroKid dashboard shows "Delivered" status for all stores
- [ ] Spotify listing live — verify metadata matches exactly
- [ ] Apple Music listing live — verify metadata
- [ ] ISRC confirmed on Spotify track page (via Spotify for Artists)
- [ ] Royalty split partners (if any) have accepted DistroKid split invitation
- [ ] Track added to relevant Spotify playlists (own playlists first)
- [ ] Track added to `TRACK_MANIFEST.md` with status `released`

---

## Common Rejection Reasons (Avoid These)

| Issue | Fix |
|-------|-----|
| Cover art under 3000×3000 px | Upscale using AI or re-export at correct size |
| Cover art contains URL or social handle | Remove all URLs/handles from artwork |
| Audio clips/distorts | Re-master with peaks at -0.3 dBFS or lower |
| Misleading artist name | Ensure name matches DistroKid account name exactly |
| Missing explicit tag | Tag any track with profanity or explicit content |
| Cover song without licence | Obtain licence via DistroKid cover song tool |
| Silence > 5 seconds at end | Trim audio file |
| Sample not cleared | Do not upload until sample is licensed |
