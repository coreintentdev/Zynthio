# INCIDENT — DESKTOP APP MODEL SELECTION OVERRIDES CONFIG (2026-08-18)
Operator OOB: "2nd new session reported after long wait HTTP 400: The
supported API model names are deepseek-v4-pro or deepseek-v4-flash, but
you passed anthropic/claude-sonnet-4."

## THE EVIDENCE (request dumps, 5 sessions)
- 2026-08-16 19:12  llama3.2:3b -> 100.64.0.2:11434 (max_retries_exhausted
  = the dead local lane, the original sin)
- 2026-08-16 19:17  anthropic/claude-sonnet-4 -> api.deepseek.com (400)
- 2026-08-17 05:50  anthropic/claude-sonnet-4 -> api.deepseek.com (400)
- 2026-08-18 07:47  anthropic/claude-sonnet-4 -> api.deepseek.com (400)
- 2026-08-18 07:56  anthropic/claude-sonnet-4 -> api.deepseek.com (400)
- 2026-08-18 08:34  anthropic/claude-sonnet-4 -> api.deepseek.com (400)

## THE ROOT CAUSE
The desktop app's Electron Local Storage (leveldb) holds a stale
"claude-sonnet-4" model selection that OVERRIDES config.yaml. The app
routes it to deepseek's API (api.deepseek.com), which only serves
deepseek-v4-pro/flash -> HTTP 400 every time. config.yaml edits alone
cannot fix it: the app-level selection wins.

## THE FIX
1. config.yaml: qwen3:8b-64k via tunnel (DONE, verified, free lane)
2. Desktop app: model picker must select qwen3:8b-64k (or the leveldb
   entry must be rewritten with the app closed)
3. Tunnel: ollama_tunnel.bat in Startup (DONE) + live session proc
4. PC gateway: startup_failed (TWILIO_PHONE_NUMBER not set in PC env)

## STATUS
OPEN — config side done, app-side selection pending.
