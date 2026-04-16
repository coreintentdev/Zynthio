# Lyrics Directory

**Artist:** DJ Zynrose (Corey McIvor)
**Status:** Empty — no tracks registered yet

---

## Directory Structure

One `.txt` file per track, named using the track slug:

```
lyrics/
├── README.md                   (this file)
├── [track-slug].txt            (one file per track)
└── ...
```

## File Naming Convention

- Use lowercase, hyphens for spaces
- No special characters
- Match the slug used in TRACK_MANIFEST.md

Example: A track titled "Neon Drift" → `neon-drift.txt`

## Lyrics File Format

```
[TRACK NAME]
Artist: DJ Zynrose
Album/Single: [Release Title]
Status: draft | final
Last Updated: YYYY-MM-DD

---

[Verse 1]
Line 1
Line 2
...

[Chorus]
Line 1
Line 2
...

[Verse 2]
...

[Outro]
...

---
[Instrumental]   ← use this for instrumental sections
```

## Rules

- Original content only — never reproduce copyrighted lyrics
- Mark drafts clearly with `Status: draft`
- Keep a local backup alongside your WAV masters
- Upload final version to DistroKid at submission time
- For timed/synced lyrics (Apple Music, Spotify): use LRC format in a separate `[slug].lrc` file
