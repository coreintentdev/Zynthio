# ZYNTHIO SOVEREIGN AGENTS — CURRENT INDEX (as of 2026-05-29)

This is the single source of truth for what actually exists and what to run right now.

## Priority Order Right Now

1. **Block 1 - Live ZYNRIP** (higher priority)
   Command: `~/Desktop/zynthio-tools/BATCH/run_block1_zynrip.sh`

2. **Cloudflare Hardening (42 zones)**
   Command: `CF_TOKEN="your_token_here" ~/Desktop/zynthio-tools/BATCH/fix_cf_all_zones.sh`

3. **Block 2 - Rafa 5-Track Song Test**
   Command: `~/Desktop/zynthio-tools/BATCH/run_block2_song_test.sh`

4. **Latest Claude Napkin Builds (landing pages + OpenClaw + quiz)**
   Command: `~/Desktop/zynthio-tools/BATCH/deploy_latest_napkin_wave_20260529.sh`

5. **Full Live rsync + rclone of All Sources (no dry run)**
   Command: `~/Desktop/zynthio-tools/BATCH/deploy_all_sources_live_20260529.sh`

## All Currently Working Agents (verified on disk)

| Script | Purpose | One-Line Command |
|--------|---------|------------------|
| run_block1_zynrip.sh | Live ZYNRIP push + corey_sync | `~/Desktop/zynthio-tools/BATCH/run_block1_zynrip.sh` |
| run_block2_song_test.sh | Test the fixed Rafa song batch | `~/Desktop/zynthio-tools/BATCH/run_block2_song_test.sh` |
| MASTER_AGENT_20260528.sh | Shows current recommended order | `~/Desktop/zynthio-tools/BATCH/MASTER_AGENT_20260528.sh` |
| deploy_latest_napkin_wave_20260529.sh | Deploy new Claude landing pages + OpenClaw | `~/Desktop/zynthio-tools/BATCH/deploy_latest_napkin_wave_20260529.sh` |
| deploy_all_sources_live_20260529.sh | Full rsync + rclone of everything (live) | `~/Desktop/zynthio-tools/BATCH/deploy_all_sources_live_20260529.sh` |
| fix_cf_all_zones.sh | Harden all 42 Cloudflare zones | `CF_TOKEN=xxx ~/Desktop/zynthio-tools/BATCH/fix_cf_all_zones.sh` |
| CONSOLIDATE_KEYS_20260528.sh | Merge Groq + other keys into ~/.zynthio.env | `~/Desktop/zynthio-tools/BATCH/CONSOLIDATE_KEYS_20260528.sh` |
| generate_5_tracks_vds_fixed.sh | The actual fixed song script (for VDS) | (this one goes on VDS, not run locally) |

## How to See This List Anytime

Just run:
```bash
cat ~/Desktop/zynthio-tools/BATCH/AGENTS_INDEX.md
```

## Honest Note on Past Issues

You are correct — there has been drip-feeding and referencing of things that were either:
- Only described verbally
- Created in previous sessions but not persisted on your disk
- Overwritten during multiple AI handovers (Claude ↔ Grok)

From now on we are using only the files that actually exist in this BATCH folder (verified via `ls`).

Signal 336. Whole pack. No more ghost files.
