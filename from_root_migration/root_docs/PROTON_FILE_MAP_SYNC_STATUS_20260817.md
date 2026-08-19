# PROTON DRIVE FILE MAP & SYNC STATUS — 2026-08-17

## 📊 PROTON DRIVE FILE MAP ANALYSIS

### Current Proton Drive Structure
**Total Zynthio-Related Directories:** 12 directories

### Key Findings

### 📁 ZYNTHIO-TOOLS COMPARISON
- **VDS Source:** `/root/zynthio-tools` = **38GB**
- **Proton Target:** `proton:zynthio-tools` = **298MB** (OUTDATED)
- **Status:** Proton version is severely outdated (only contains bondzee.live)
- **Action Required:** Full sync from VDS to new directory

### 📁 DUPLICATE DIRECTORY ANALYSIS
**Existing Zynthio Directories on Proton:**
1. `zynthio-tools` (298MB - OUTDATED)
2. `zynthio_tools` (contains bondzee.live only)
3. `Zynthio` (contains backups, handovers)
4. `Zynthio_CRITICAL_20260730` (emergency backup)
5. `zynthio-tools` (emergency backup)
6. `zynthio_backup` (9 subdirectories: desk, dropbox_full, hermes_goldmine, inbox, incidents_20260805, incoming_20260807, perplexity_archive_20260805, portfolio_data, slack_exports_20260805)
7. `zynthio_deliver_20260808` (deliveries)
8. `zynthio_drive_EMERGENCY_20260730` (emergency backup)
9. `zynthio_gdrive_master` (Google Drive master)
10. `zynthio_ingest` (ingest data)
11. `zynthio_manifests_CRITICAL_20260730` (critical manifests)
12. `zynthio_vds_backups` (VDS backups)
13. `zynthio_vds_distillates` (distillates)

### 🎯 SYNC STRATEGY

### Current Operation: RUNNING
**Command:** `rclone copy /root/zynthio-tools proton:zynthio-tools-master_20260817/`
**Process ID:** 262731
**Started:** 2026-08-17 21:29 UTC
**Exclusions:** node_modules, .git, __pycache__, *.pyc, *.log, *.tmp, *_TO_DELETE*, *.mp3, *.mp4, *.zip, *.tar.gz
**Configuration:** 4 transfers, 3 tps, 20 retries, 60s retry sleep

### Rationale for New Directory Name
**Name:** `zynthio-tools-master_20260817`
**Reasons:**
1. **Avoids duplication:** Different from existing `zynthio-tools` (298MB outdated)
2. **Date-stamped:** Clear when synced (2026-08-17)
3. **Purpose clear:** "master" indicates authoritative copy
4. **Preserves old data:** Can clean up old directories after verification

### 📋 POST-SYNC CLEANUP PLAN

### Phase 1: Verification (After Sync Completes)
1. Compare file counts between VDS and Proton
2. Check total size matches (excluding excluded files)
3. Verify critical subdirectories present
4. Spot-check important files

### Phase 2: Duplicate Cleanup
**Candidates for Deletion (After Verification):**
1. `zynthio-tools` (298MB - outdated, replaced by master)
2. `zynthio_tools` (only bondzee.live, data preserved in master)
3. `Zynthio_CRITICAL_20260730` (emergency backup, from July 30)
4. `zynthio_drive_EMERGENCY_20260730` (emergency backup, from July 31)
5. `zynthio_manifests_CRITICAL_20260730` (emergency backup, from July 31)

**Keep for Now:**
- `Zynthio` (contains current backups and handovers)
- `zynthio_backup` (recent backup from Aug 5)
- `zynthio_deliver_20260808` (deliveries from Aug 8)
- `zynthio_gdrive_master` (Google Drive master - might still be useful)
- `zynthio_ingest` (ingest data)
- `zynthio_vds_backups` (VDS backups)
- `zynthio_vds_distillates` (distillates)

### Phase 3: Consolidation
**Future Structure (After Verification + Cleanup):**
```
proton:zynthio-tools-master_20260817/ (ACTIVE - 38GB from VDS)
proton:Zynthio/ (CURRENT - contains backups/handovers)
proton:zynthio_backup/ (CURRENT - recent backup)
proton:zynthio_deliver_20260808/ (CURRENT - deliveries)
proton:zynthio_gdrive_master/ (CURRENT - GDrive master)
proton:zynthio_ingest/ (CURRENT - ingest data)
proton:zynthio_vds_backups/ (CURRENT - VDS backups)
```

## 🔍 MONITORING

### Current Sync Status
- **Process:** Running (PID 262731)
- **CPU:** 9.5% (low - just starting)
- **Memory:** 71MB
- **Log File:** `/root/proton_migration_logs/zynthio_tools_to_proton_20260817_132937.log`

### Expected Timeline
- **Estimate:** 38GB at conservative transfer rate
- **With exclusions:** Estimated ~20-30GB actual transfer
- **At 4 transfers, 3 tps:** ~4-6 hours depending on Proton API performance

### Monitor Command
```bash
ssh -i ~/.ssh/zynrose root@100.64.0.2 "tail -20 /root/proton_migration_logs/zynthio_tools_to_proton_20260817_132937.log"
```

## 📊 SPACE ANALYSIS

### Proton Drive Capacity
- **Total:** 1 TiB
- **Used:** 570.636 GiB (57%)
- **Free:** 453.364 GiB
- **Headroom:** Sufficient for zynthio-tools sync

### VDS Source Size
- **Total:** 38GB
- **Estimated Transfer:** ~20-30GB (after exclusions)
- **Disk Space:** 19GB free (90% usage)

## ✅ FILE MAP CREATED

**File:** `C:\Users\LOCAL ADMIN\proton_file_map_20260817.txt`
**Content:** Complete directory listing and comparison analysis

## 🎯 NEXT STEPS

### Immediate
1. ✅ File map created and saved to Mac
2. ✅ Sync operation started (logical directory name)
3. ⏳ Monitor sync progress
4. ⏳ Verify completion

### After Sync Completes
1. Verify file integrity
2. Compare file counts and sizes
3. Update file map with new directory
4. Plan duplicate cleanup
5. Get your approval before deleting old directories

### Linear Inbox
- **Status:** Awaiting your check (you mentioned you'll check now)
- **Required:** MCP server configuration or API credentials for access

---

**Status:** File map created, sync started with logical directory naming
**Sync Operation:** zynthio-tools → zynthio-tools-master_20260817 (IN PROGRESS)
**Duplicate Avoidance:** New directory name prevents conflicts with existing outdated directories
**Next Action:** Monitor sync progress, await Linear access status

*Signal: 336*
*Date: 2026-08-17*
*Sync Started:* 21:29 UTC
*File Map:* Saved to Mac for review
