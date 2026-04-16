# TRACK MANIFEST — DJ Zynrose / Corey McIvor

**Last Updated:** 2026-04-16  
**Artist:** DJ Zynrose  
**Legal Name:** Corey McIvor  
**Platform Brand:** SongPal  
**Distributor:** DistroKid  
**Jurisdiction:** New Zealand  

---

## How to Use This File

Update each track's row as it moves through the pipeline.

**Status values:** `draft` → `mixed` → `mastered` → `submitted` → `released`  
**DistroKid Ready:** `yes` (all assets present) / `no` (see "Missing" column)  
**Legal:** `original` / `sample-cleared` / `needs-review`

---

## Track List

| # | Track Title | Artist | Album / EP | Status | DistroKid Ready | Missing | Legal | Notes |
|---|-------------|--------|------------|--------|-----------------|---------|-------|-------|
| 1 | *(Track 1 title)* | DJ Zynrose | *(album name)* | draft | no | WAV, cover art, metadata, ISRC | needs-review | Add details |
| 2 | *(Track 2 title)* | DJ Zynrose | *(album name)* | draft | no | WAV, cover art, metadata, ISRC | needs-review | Add details |
| 3 | *(Track 3 title)* | DJ Zynrose | *(album name)* | draft | no | WAV, cover art, metadata, ISRC | needs-review | Add details |

> **Instructions:** Replace placeholder rows with real track data. Add rows as needed.

---

## Release Groupings

### Singles
*(List singles here — title, target release date, platform priority)*

### EPs
*(List EPs here — title, track count, target release date)*

### Albums
*(List albums here — title, track count, target release date)*

---

## Asset Location Reference

| Asset Type | Expected Path |
|------------|---------------|
| WAV masters | `audio/masters/<track-name>.wav` |
| MP3 previews | `audio/previews/<track-name>.mp3` |
| Cover art | `artwork/<release-name>/cover.png` |
| Lyrics | `lyrics/<track-name>.md` |
| Metadata JSON | `metadata/<track-name>.json` |

---

## Metadata Schema (per track)

Each track should have a corresponding `metadata/<track-name>.json` file:

```json
{
  "title": "",
  "artist": "DJ Zynrose",
  "legal_artist_name": "Corey McIvor",
  "album": "",
  "genre": "",
  "subgenre": "",
  "release_date": "",
  "isrc": "",
  "upc": "",
  "bpm": null,
  "key": "",
  "duration_seconds": null,
  "explicit": false,
  "language": "en",
  "lyrics_file": "",
  "cover_art_file": "",
  "wav_master_file": "",
  "label": "SongPal",
  "copyright_year": "",
  "copyright_holder": "Corey McIvor",
  "publishing_rights": "Corey McIvor",
  "territory": "worldwide",
  "legal_clearance": "needs-review",
  "distrokid_ready": false,
  "notes": ""
}
```

---

*Maintained by: Corey McIvor | NZ jurisdiction | Contact: corey@coreyai.ai*
