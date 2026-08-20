# PC DATA STATE REPORT — 2026-08-12 (Hermes PC session, rubymcivor)
Reported to VDS Hermes per operator directive: "report again to VDS hermes the current state of the data"

## 1. ORICO (E:, 119.2GB exFAT) — SECURED, PENDING WIPE
- Full copy verified on C:\Users\LOCAL ADMIN\pcworkspace\orico_secure_20260812\
  - 72,651 files / 13.319 GB byte-identical (robocopy /L: 0 mismatch, 0 failed, 0 extras)
  - ALPHA_SAFE_20260808_103559 snapshot: 69,811 files / 11.44 GB == C: copy (exact)
  - oricodrive_parts aa-ae (~103GB): sizes + start/end chunk hashes MATCH C: copies
    (C: holds ALL NINE parts aa-ai — C: is the superset)
  - BIOS stick ROMs (E7E06IMS.AJ0, ODB550AE.ROM) backed up: 21 files / 127 MB
- Operator approved deletion; VDS Hermes sign-off still the standing gate before wipe
- $RECYCLE.BIN and System Volume Information on E: contain nothing of value (empty recycle, index metadata)

## 2. LOCAL WORKSPACE CONSOLIDATION (done this session)
- pcworkspace\consolidated_20260812\ — 11 data files (211 MB) moved in from Downloads/tmp:
  - 1363777.*.dns.csv, *.domains.csv (DNS/domain exports, 2026-08-14)
  - account-orders.csv (2026-08-14)
  - 322d1a9d-*.pdf (1-page doc)
  - 5bc4159f*-2026-08-13-*.zip (208 MB — AI conversation export, 354 files: chat.html, codex.json, conversations-*.json, assets)
  - kimi_session_audit_report.txt (2026-08-14)
  - complaint_*.md x4 + pete_response_draft.md (2026-08-05, Kimi/proton/pete thread docs)
- Downloads now holds ONLY installers (ChromeSetup, Git-2.55, rufus x2, WhatsApp x2, DevinUserSetup)
- tmp/ emptied of docs

## 3. KEY FILES IN pcworkspace (pre-existing)
- GPU_RMA_EVIDENCE.md — card ID (DEV_2788=RTX 4060 Ti, MSI Ventus 2X Black), VBIOS 95.04.6e.00.7d,
  crash history (333x nvlddmkm 153 in 7d), load-test results (307 DPC watchdog + illegal-memory-access),
  solar-power hypothesis, 800W PSU swap test plan
- flash_log.txt / flash_verify_log.txt — Ubuntu installer stick write+verify (CD001 confirmed)
- ubuntu-24.04.3-live-server-amd64.iso.fresh — verified official sha256 c3514bf0...
- mydockfinder\ — MyDockFinder 2024 (macOS dock UI, autostart via Startup shortcut)
- gpu_push.py — reproducible GPU load test (baseline before PSU swap)
- Handover/incident/quotes/Cloudflare CSV sets as previously mapped

## 4. DRIVE LAYOUT (current)
- C: NVMe 953.9GB (378GB free) — Windows, workspace, secured Orico copy, all 9 oricodrive parts
- D: 14.4GB Kingston — now BOOTABLE UBUNTU 24.04.3 LIVE-SERVER INSTALLER (ISO raw-written, CD001 verified)
- E: ORICO 119.2GB exFAT (0.5GB free) — secured data pending wipe/Ubuntu install target

## 5. VDS (this report's destination)
- Disk: 174GB, 146GB used, 28GB free (84%) — trending full, cleanup recommended soon
- /root/zynthio = 43GB. Memory 23Gi/21Gi avail. Uptime 37d.
