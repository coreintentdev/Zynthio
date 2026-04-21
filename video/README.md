# Video Directory — DJ Zynrose / SongPal

Store short-form video assets here: Spotify Canvas clips, YouTube Shorts, Reels previews.

## File Naming Convention

```
TRK-XXX_DJ-Zynrose_[Track-Title]_CANVAS.mp4     — Spotify Canvas (3–8 s loop)
TRK-XXX_DJ-Zynrose_[Track-Title]_SHORTS.mp4     — YouTube Shorts / Instagram Reels (≤ 60 s)
TRK-XXX_DJ-Zynrose_[Track-Title]_LYRICVIDEO.mp4 — Full lyric video
```

## Specs by Use Case

| Asset | Dimensions | Duration | Format | Notes |
|-------|-----------|----------|--------|-------|
| Spotify Canvas | 1080 × 1920 (9:16) | 3–8 s loop | MP4 (H.264) | No text, no logos; seamless loop preferred |
| Spotify Clips | 1080 × 1920 (9:16) | ≤ 30 s | MP4 | Upload via Spotify for Artists |
| YouTube Shorts | 1080 × 1920 (9:16) | ≤ 60 s | MP4 | Released same day as track |
| Instagram Reels | 1080 × 1920 (9:16) | 15–90 s | MP4 | Hook in first 3 s |
| TikTok | 1080 × 1920 (9:16) | 15–60 s | MP4 | 15 s hook clip auto-selected from DistroKid delivery |
| Apple Music MV | 1920 × 1080 (16:9) | Full track | MP4/MOV | Delivered through DistroKid music video delivery |

## Git Storage Note

Video files are large — do NOT commit MP4s directly to git without LFS:

```
# .gitignore entries (add as needed)
video/*.mp4
video/*.mov
```

Use cloud storage (Google Drive, Dropbox, Backblaze B2) and reference the external path in `TRACK_MANIFEST.md`.

---

*Maintained by: Corey McIvor — corey@coreyai.ai*
