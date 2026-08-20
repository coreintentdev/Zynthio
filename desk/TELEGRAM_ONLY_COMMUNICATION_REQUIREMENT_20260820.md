# TELEGRAM-ONLY COMMUNICATION REQUIREMENT
Critical requirement: Server communication must work even if API credits run out

## THE REQUIREMENT
**"Make sure if you run out of credit how do I communicate with server telegram only?"**

## THE SOLUTION

### WHY TELEGRAM WORKS WITHOUT CREDITS
- Telegram bot communication = bot token + webhook/polling
- No API credits required for basic bot functionality
- Bot can execute server commands without AI layer
- Commands work even if OpenAI/Anthropic/DeepSeek credits are exhausted

### TELEGRAM-ONLY ARCHITECTURE

#### 1. CORE TELEGRAM COMMANDS (no AI needed)
```python
# Basic server commands via Telegram
/status → Server status (CPU, memory, disk)
/restart → Restart services
/logs → View recent logs
/deploy → Deploy from git
/backup → Create backup
/health → Health check
```

#### 2. TELEGRAM FALLBACK MODE
- **Normal mode**: AI processes requests, responds with generated content
- **Credit exhausted mode**: Telegram still works, AI disabled, basic commands only
- **Communication preserved**: You can always reach the server via Telegram

#### 3. CREDIT MONITORING
```python
# Telegram command to check credit status
/credits → Show API credit status for all providers
/alerts → Configure credit alerts (warn when low)
```

## IMPLEMENTATION PLAN

### PHASE 1: TELEGRAM INFRASTRUCTURE (already done)
- ✅ Bot token configured: `8632493719:AAFOkDgYQqhZ34v6z03_b_8srRDvAiTu_50`
- ✅ Home channel set: `8528109613` (Corey McIvor)
- ✅ Gateway restarted: PID 1127209
- ✅ Model fixed: `zynthio-twin-7b:latest` (local, no credits needed)

### PHASE 2: TELEGRAM-ONLY COMMANDS
```python
# Add to Telegram bot
@bot.command('/status')
async def status_command(message):
    # Check server status (no AI needed)
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    await message.reply(f"CPU: {cpu}%, RAM: {memory}%, Disk: {disk}%")

@bot.command('/restart')
async def restart_command(message):
    # Restart services (no AI needed)
    subprocess.run(['systemctl', 'restart', 'hermes-gateway'])
    await message.reply("Gateway restarted")

@bot.command('/credits')
async def credits_command(message):
    # Check credit status (no AI needed)
    # Query API providers for remaining credits
    await message.reply(credit_status)
```

### PHASE 3: CREDIT-EXHAUSTED FALLBACK
```python
# Automatic fallback when credits exhausted
def check_credits():
    if openai_credits <= 0 and anthropic_credits <= 0:
        # Disable AI responses
        enable_ai = False
        # Keep Telegram commands working
        enable_telegram_commands = True
        # Notify Corey
        send_telegram_message("Credits exhausted. Telegram-only mode active.")
```

### PHASE 4: COMMUNICATION REDUNDANCY
- **Primary**: Telegram bot (always works)
- **Secondary**: SSH (always works)
- **Tertiary**: Direct console (always works)
- **AI layer**: Optional, disabled when credits exhausted

## ANTI-CREDIT-EXHAUSTION RULES

### RULE 1: TELEGRAM ALWAYS WORKS
- Telegram bot never depends on API credits
- Basic commands always available
- Communication always preserved

### RULE 2: LOCAL MODEL FIRST
- Use local Ollama (zynthio-twin-7b:latest) by default
- No credits needed for local inference
- External APIs only when explicitly requested

### RULE 3: CREDIT MONITORING
- Monitor credit levels automatically
- Warn when credits are low
- Switch to local-only mode before exhaustion

### RULE 4: GRACEFUL DEGRADATION
- When credits exhausted: disable AI, keep Telegram
- No service interruption
- Clear communication about mode change

## SERVER STATUS VIA TELEGRAM

### NORMAL MODE (credits available)
```
/status → Server status + AI status
/chat → AI-powered chat
/deploy → AI-assisted deployment
/logs → AI-summarized logs
```

### CREDIT-EXHAUSTED MODE (credits gone)
```
/status → Server status (AI disabled)
/chat → "Credits exhausted, use local model or /commands"
/deploy → Manual deployment (no AI assistance)
/logs → Raw logs (no AI summary)
```

### EMERGENCY MODE (everything broken)
```
/status → Basic status only
/restart → Force restart
/reboot → Server reboot
/ssh → Enable SSH access
```

## IMPLEMENTATION PRIORITY

### IMMEDIATE (Phase 1)
1. Add basic Telegram commands (/status, /restart, /health)
2. Implement credit monitoring
3. Test Telegram commands work without AI

### SHORT TERM (Phase 2)
1. Add credit exhaustion fallback
2. Implement graceful degradation
3. Add notification system

### ONGOING
1. Monitor credit levels
2. Test fallback mode regularly
3. Ensure Telegram always works

## COMMUNICATION GUARANTEE

**GUARANTEED**: You can always communicate with the server via Telegram, regardless of credit status.

**HOW**: Telegram bot commands work independently of AI credits. Basic server management commands always available.

**FALLBACK**: If Telegram fails, SSH always works. If SSH fails, direct console always works.

**AI LAYER**: Optional enhancement, not required for basic communication.

---
Telegram-only communication plan: 2026-08-20
Requirement: Server communication must work even if API credits run out
Solution: Telegram commands work without AI, credit monitoring, graceful degradation
Guarantee: Telegram always works for server communication regardless of credit status