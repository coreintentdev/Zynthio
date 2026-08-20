# INCIDENT — GPU TROUBLESHOOTING DOC REVIEW (2026-08-15)
Severity: MINOR (theory vs live-state verification) · Operator-supplied doc: "Troubleshooting GPU AI Build Failures.txt"

## DOC'S CENTRAL CLAIMS VS LIVE STATE (verified this session)
1. "Default TDR 2s, raise TdrDelay to 60s+" → **ALREADY DONE, FAILED.** Live: TdrDelay=0x3c(60s), TdrDdiDelay=0x3c(60s). Faults persisted anyway (ollama "illegal instruction" today; torch "illegal memory access" Aug 8/12). TDR-timeout theory KILLED for this machine.
2. "Audit per-chip VRAM junction temps, replace thermal pads" → **UNVERIFIABLE.** Live: 4060 Ti Memory Current Temp = N/A (no sensor exposed). Thermal-pad branch cannot be diagnosed or verified on this card.
3. "Switch to TCC mode" → **UNAVAILABLE.** Display GPU on Windows; TCC kills display.

## WHAT THE DOC MISSES (strongest evidence on file)
- Idle hard resets: BugcheckCode=0, no dump, 5x in one day, AT IDLE (not under load). Thermal/TDR explain load faults; they do NOT explain idle resets. No-dump hard resets = power/bus drop → solar-only supply + water-pump inrush (site context) remains primary suspect for idle resets.
- 4 bugcheck classes in 48h: 0x0 (idle power), 0x133 (load DPC), 0x278 (TDR), 0x7E (kernel thread).

## DOC'S VALID CORE
- Non-deterministic fault iterations (35/78/607) = hardware-level instability, not code bug — matches 3-stack evidence.
- Soft-error/no-ECC theory plausible for consumer VRAM.
- Cloud endpoint as correct fallback — matches reality.

## STANDING ACTIONS (unchanged)
- Power-limit test (nvidia-smi -pl)
- 800W PSU swap (own cables ONLY — never mix modular cables)
- Pump-correlation logging during test window
- Card-swap retest with CSM/primary-display = PCIe

## CONCLUSION
Doc = good general theory, wrong for THIS machine on its two primary fixes (TDR already set & failed; VRAM temp unmeasurable). The idle-reset evidence (power delivery) is the doc's blind spot and remains the leading lead.
