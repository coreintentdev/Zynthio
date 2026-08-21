# MASTER SCOPE UPDATE — 2026-08-20
## Architecture doctrine (operator-directive)
- **VDS is BOSS** — the zynthio VDS is the authority. All ops route through it.
- **PC and MacBook are INDEPENDENT of each other** — neither depends on the other.
  Both report TO the VDS; they are peers, not a chain.
- **Hermes is the master of all us puppets** — Hermes orchestrates all the endpoints.
- **masterofall.com** — the master domain / locus. (REGISTER + ZONE + POINT here.)

## Free-model lane (THE paying groundhog-day FIX — 2026-08-20)
- Hermes defaults to FREE qwen3:8b-64k (config base_url 127.0.0.1:11435).
- The tunnel at 11435 was DOWN -> every free call failed -> silent fallback to
  PAID deepseek/claude-sonnet-4 -> credit billed for the same work.
- FIXED: free_lane.sh forwards 127.0.0.1:11435 -> VDS ollama 100.64.0.2:11434.
  Run `bash free_lane.sh` whenever port 11435 is closed.
- Verify: `curl -s http://127.0.0.1:11435/v1/chat/completions ...` returns tokens.
- Free QLoRA base (qwen7b, 4 safetensor shards ~11.2GB) lives at
  C:\Users\LOCAL ADMIN\pcworkspace\twin_corpus\base_qwen7b\  for local training.

## Remaining (from todo list)
- Masterofall.com: REGISTER, zone on CF, point to VDS — the master locus.
- Domains: SEARCHITCENTRAL done; review the rest + CF zone.
- Data off PC/Mac -> Proton consolidation (verify ALL accounts + keys).
- QLoRA qwen7b model training start (free local).
- Mac wake -> read migration report, fold into Proton map, Mac Mail bridge.

## Key access
- Direct to VDS (no-pay): `ssh -i ~/.ssh/zynrose root@5.189.143.170`
- VDS Hermes shell: `ssh -i ~/.ssh/zynrose root@5.189.143.170 "hermes"` (or zynthio.sh)
- Handover docs: /root/zynthio/desk/from_pc_20260820/ (125 docs, commit 669c21c)
