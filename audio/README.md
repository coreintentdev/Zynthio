# Audio Directory — DJ Zynrose / SongPal

Store WAV master files here. Do NOT commit large binary files to git — use git-lfs or store on a separate drive/cloud and reference the path in TRACK_MANIFEST.md.

## File Naming Convention

```
TRK-XXX_DJ-Zynrose_[Track-Title]_MASTER.wav
```

## Technical Requirements (DistroKid / DSP)

| Spec | Requirement |
|------|------------|
| Format | WAV or FLAC |
| Bit depth | 16-bit minimum; 24-bit preferred |
| Sample rate | 44.1 kHz minimum |
| Channels | Stereo |
| Peak level | ≤ −0.3 dBFS (no clipping) |
| Integrated loudness | −14 LUFS (Spotify) / −16 LUFS (Apple) |
| Head silence | ≤ 0.5 s |
| Tail silence | ≤ 2 s (unless intentional fade) |

## Note on Git Storage

Audio files are typically large (30–100 MB each). Add to `.gitignore` or use Git LFS:
```
# .gitignore entry
audio/*.wav
audio/*.flac
audio/*.aif
```
