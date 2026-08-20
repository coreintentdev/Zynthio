# INCIDENT — 30-YEAR ARCHIVE BACKUP INITIATED (2026-08-15)
Severity: CRITICAL-ASSET (unreleased catalog at risk, no prior verified backup)

## CONTEXT (operator)
- "my mac and google etc are 30+ years with my music tracks too. not many if any [backups]"
- "30 years of email on the stack and google docs and pdf etc but where were you? is still there if you dare"
- Mac key confirmed by operator ("mac key was done and this key for this device and tailscale and headscale lost and found safe and sound")

## INVENTORY (verified live via Mac SSH, PC key)
- ~/Music/ZYNTHIO_MUSIC: 6.8G (the catalog core)
- ~/Music/Music: 1.4G (Apple Music library)
- ~/Music/Suno_AllAccounts_20260429: 400M
- ~/Music/Suno_zynthio_20260429: 126M · Suno_zynrose_20260429: 85M · others
- Music file count: 1,154
- GDrive corey.mcivor@gmail.com: 30G (cloud mount on Mac)
- GDrive perthvideo@gmail.com: 7.4G
- GDrive zynthioai@gmail.com: 11M
- ~/Library/Mail: 96M (30 years of mail, V7/V10 stores)
- TOTAL ≈ 46G irreplaceable

## BACKUP PATH (all hops authenticated)
Mac (SSH zynthio_dc key, added to authorized_keys this session) → VDS rsync (resumable)
→ VDS → Proton (rclone, token valid, 481G free) → music_stack_gen_20260815 + mac_archive_20260815

## STATUS
- PC→Mac: worked (existing key)
- VDS→Mac: key added (zynthio_dc pubkey derived + appended), VERIFIED: VDS_TO_MAC_OK
- Music rsync: IN FLIGHT (background, resumable, --partial)
- GDrive 30G: QUEUED after music (gdrive rclone token dead on VDS; will pull via Mac path or re-auth)
- Mail 96M: QUEUED
- Suno tracks already on Proton: suno_library_backup_20260802 was EMPTY — real backup now in flight

## KEY CHANGES THIS SESSION
- /root/.ssh/zynthio_dc pubkey derived (ssh-keygen -y) + appended to Mac authorized_keys
- Mac authorized_keys now: PC id_ed25519 + VDS zynthio_dc

## NEXT
- Monitor music rsync → push to Proton
- Pull GDrive corey.mcivor 30G via Mac path → Proton
- Pull Mail 96M → Proton
- Verify byte counts on Proton before declaring done
