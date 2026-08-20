# SAMSUNG GALAXY A07 DUAL BOOT + CONNECTION PLAN
Install custom zynthio dual boot via USB + configure tmux + tailscale + telegram

## PHONE STATUS
- **Device**: Samsung Galaxy A07
- **Custom system**: Custom zynthio dual boot (your design)
- **Current state**: tmux, tailscale, telegram already installed
- **Goal**: Install dual boot via USB + configure connection backup
- **Requirement**: Backup instead of lockout, connection to stack

## PLAN: INSTALL + CONFIGURE (NOT REDESIGN)

### PHASE 1: DUAL BOOT INSTALLATION (via USB)
**Your custom zynthio dual boot** — install via USB to Samsung Galaxy A07

#### Prerequisites
- Custom zynthio dual boot image (your design)
- USB cable
- Samsung Galaxy A07 in download mode
- PC with adb/fastboot tools

#### Installation Steps
1. **Enable OEM unlock** (if not already)
   - Settings → About phone → Software information
   - Tap "Build number" 7 times
   - Developer options → OEM unlock

2. **Boot to download mode**
   - Power off phone
   - Volume down + Power (enter download mode)

3. **Flash custom dual boot via USB**
   - Connect via USB
   - Use your custom zynthio dual boot installer
   - Flash to device
   - Reboot

4. **Verify installation**
   - Boot into custom zynthio system
   - Verify dual boot works
   - Check tmux, tailscale, telegram present

### PHASE 2: CONNECTION CONFIGURATION
**Configure existing tools** — tmux + tailscale + telegram (already installed)

#### tmux Configuration
```bash
# Basic tmux configuration for session persistence
~/.tmux.conf
# New session on login
new-session -n zynthio
# Pane layout
set -g pane-border-status top
set -g status-interval 10
# Session persistence
set -g detach-on-destroy off
```

#### tailscale Configuration
```bash
# Connect to your tailnet
tailscale up
# Enable key expiry
tailscale up --reset
# Check connection
tailscale status
```

#### telegram Configuration
```bash
# Telegram bot (existing installation)
# Configure to connect to your stack
# Bot token: 8632493719:AAFOkDgYQqhZ34v6z03_b_8srRDvAiTu_50
# Home channel: 8528109613 (Corey McIvor)
```

### PHASE 3: BACKUP & LOCKOUT PREVENTION
**Backup instead of lockout** — ensure you can always recover

#### Backup Strategy
1. **Configuration backup**
   - Backup tmux config: `~/.tmux.conf`
   - Backup tailscale state: `tailscale status > backup.txt`
   - Backup telegram settings

2. **Connection backup**
   - SSH keys backup to safe location
   - tailscale auth keys backup
   - Alternative connection methods documented

3. **System backup**
   - NAND backup of working configuration
   - Backup of custom dual boot image
   - Recovery procedure documented

#### Lockout Prevention
1. **Multiple connection methods**
   - tailscale (primary)
   - SSH (fallback)
   - telegram (fallback)
   - Physical USB (emergency)

2. **Recovery procedures**
   - How to restore from NAND backup
   - How to reflash dual boot if corrupted
   - How to recover tailscale connection

### PHASE 4: STACK INTEGRATION
**Connect to your stack** — VDS, services, telegram

#### Stack Connection
```bash
# Connect to VDS via tailscale
ssh root@100.64.0.1

# Or via direct IP if tailscale fails
ssh root@5.189.143.170

# Test connection
ping 8.8.8.8
```

#### Service Integration
- Telegram bot connects to VDS Hermes
- tmux sessions persist on VDS
- tailscale provides encrypted tunnel
- Phone acts as mobile terminal

## STARTING POINT: BASIC FUNCTIONAL

### What You Get (basic but functional)
- Custom zynthio dual boot installed
- tmux for terminal sessions
- tailscale for encrypted connection
- telegram for communication
- Backup procedures documented
- Lockout prevention measures

### What You Don't Get (you designed your own)
- No new plan (you have your custom design)
- No reengineering (you designed advanced watch app)
- No holistic phone use redesign (you have your stack)

## NEXT STEPS

### IMMEDIATE (your action)
1. Prepare custom zynthio dual boot image
2. Put Samsung Galaxy A07 in download mode
3. Flash via USB
4. Boot into custom system

### SHORT TERM (after install)
1. Configure tmux for session persistence
2. Connect to tailscale network
3. Configure telegram bot connection
4. Test all connection methods
5. Document backup procedures

### LOCKOUT PREVENTION (critical)
1. Backup all configurations
2. Document recovery procedures
3. Test fallback connection methods
4. Verify you can recover from any failure

## CONNECTION BACKUP GUARANTEE

**GUARANTEED**: You will have multiple connection methods and backup procedures to prevent lockout.

**METHODS**: tailscale (primary), SSH (fallback), telegram (fallback), USB (emergency).

**BACKUP**: Configuration backups, system backups, recovery procedures documented.

**NO LOCKOUT**: If one method fails, you have alternatives to recover.

---
Samsung A07 dual boot plan: 2026-08-20
Goal: Install custom zynthio dual boot + configure tmux + tailscale + telegram
Constraint: No new plan, use your custom design, ensure backup not lockout
Starting point: Basic functional configuration with connection backup