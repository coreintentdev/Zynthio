# SAMSUNG A07 DUAL BOOT INSTALLATION — READY TO EXECUTE
Step-by-step guide for installing your custom zynthio dual boot

## WHAT YOU NEED (gather these before starting)
- Samsung Galaxy A07
- USB cable
- PC/laptop with adb/fastboot tools
- Your custom zynthio dual boot image
- Backup of any important data on phone

## STEP 1: ENABLE OEM UNLOCK
1. Go to Settings → About phone → Software information
2. Tap "Build number" 7 times until "Developer mode is enabled"
3. Go back to Settings → Developer options
4. Enable "OEM unlocking"
5. Enable "USB debugging"

## STEP 2: ENTER DOWNLOAD MODE
1. Power off the Samsung Galaxy A07
2. Press and hold: Volume Down + Power button
3. Release when you see "Warning" screen
4. Press Volume Up to continue to download mode
5. Phone should show "Downloading..." screen

## STEP 3: CONNECT VIA USB
1. Connect USB cable to PC
2. On PC, verify phone is connected:
   ```bash
   adb devices
   # or
   fastboot devices
   ```

## STEP 4: FLASH CUSTOM ZYNTHIO DUAL BOOT
1. On PC, navigate to your custom zynthio dual boot image
2. Use your custom installer (you designed this)
3. Flash the dual boot system:
   ```bash
   # Replace with your actual installer command
   ./your-zynthio-dual-boot-installer.sh --device samsung-a07
   ```
4. Wait for flash to complete
5. Phone will reboot automatically

## STEP 5: BOOT INTO CUSTOM SYSTEM
1. Phone should boot into custom zynthio dual boot
2. Verify system loads correctly
3. Check that tmux, tailscale, telegram are present

## STEP 6: CONFIGURE CONNECTION METHODS
### tmux (already installed)
```bash
# Start persistent tmux session
tmux new -s zynthio
# Configure for persistence (backup your .tmux.conf)
```

### tailscale (already installed)
```bash
# Connect to your tailnet
tailscale up
# Check connection
tailscale status
# Note your tailscale IP for VDS connection
```

### telegram (already installed)
```bash
# Connect to your bot
# Bot: vdssongpalbot
# Token: 8632493719:AAFOkDgYQqhZ34v6z03_b_8srRDvAiTu_50
# Send /start to test connection
```

## STEP 7: STACK CONNECTION TEST
```bash
# Test VDS connection via tailscale
ssh root@100.64.0.1
# Or direct IP if tailscale fails
ssh root@5.189.143.170
# Test command
hostname
```

## STEP 8: BACKUP PROCEDURES
### Configuration backup
```bash
# Backup tmux config
cp ~/.tmux.conf ~/tmux.conf.backup

# Backup tailscale state
tailscale status > ~/tailscale-status-backup.txt

# Backup telegram settings
# Document your bot token and home channel
```

### System backup
- Document your dual boot image location
- Document recovery procedure
- Note any special flashing steps

## STEP 9: LOCKOUT PREVENTION
### Multiple connection methods (test each)
1. **tailscale**: `tailscale status` → should show connected
2. **SSH**: `ssh root@5.189.143.170` → should connect
3. **telegram**: Send /status to bot → should respond
4. **USB**: Re-enter download mode → should detect device

### Recovery test
1. Simulate connection failure (disconnect from network)
2. Test alternative connection method
3. Verify you can recover without lockout

## SUCCESS CRITERIA
- ✅ Custom zynthio dual boot boots successfully
- ✅ tmux sessions persist
- ✅ tailscale connects to tailnet
- ✅ telegram bot responds to commands
- ✅ Can connect to VDS via multiple methods
- ✅ Backup procedures documented
- ✅ Recovery procedures tested

## TROUBLESHOOTING
### Flash fails
- Check USB cable (try different cable)
- Check USB port (try different port)
- Verify download mode is active
- Reboot phone and re-enter download mode

### Boot fails
- Re-enter download mode
- Re-flash the image
- Check image integrity

### tailscale fails
- Check internet connection
- Verify tailscale auth
- Check tailscale service status

### telegram fails
- Verify bot token is correct
- Check internet connection
- Test bot via Telegram web interface

## NEXT ACTION (your turn)
1. Gather the materials listed above
2. Follow Steps 1-9 sequentially
3. Report back at each step if issues occur
4. Document any deviations from this plan

---
Samsung A07 installation guide: 2026-08-20
Ready to execute: Step-by-step dual boot installation
Focus: Get your custom zynthio dual boot running with connection backup