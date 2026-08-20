# INCIDENT — POWER-CAP LOAD TEST RESULT (2026-08-15)
Severity: EVIDENCE (confirms hardware fault; rules out power-draw and thermal triggers)

## TEST
- Cap: nvidia-smi -pl 115W (from 165W default, 30% reduction), set via admin
- Load: gpu_push.py sustained FP16 matmul chain, 5-min window, VRAM watchdog 7000MiB
- Baseline before: clean since 8/14 3:21 PM (no Event-41), cap verified 115W

## RESULT
- FAULT at iter 44: "CUDA error: unspecified launch failure" (cudaErrorLaunchFailure)
- Conditions at fault: 57°C core, 63W draw, 26% util, 1061 MiB VRAM
- System did NOT reset — error caught by process, exited clean
- Cap restored to 165W after; no crash post-test

## WHAT IT PROVES
1. Power draw is NOT the trigger — faulted at 63W, <40% of cap, trivial load.
2. Thermal is NOT the trigger — 57°C is cool; thermal-pad/VRAM-temp theory dead by measurement.
3. Utilization is NOT the trigger — 26% GPU busy.
4. Fault is non-deterministic silicon-level instability, independent of electrical/thermal stress.

## FAULT MATRIX NOW (4 independent reproductions)
- torch uncapped: ~iter 35 (Aug 8)
- matmul uncapped: ~iter 78 + system reset 0x133 (Aug 12)
- ollama uncapped: immediate (Aug 15)
- torch capped 115W: iter 44 (Aug 15) ← NEW

## SEPARATION OF FAILURE CLASSES
- LOAD faults (4×, every stack, all power levels): compute-unit instability = RMA signature for the card.
- IDLE resets (BugcheckCode=0, no dump): separate class; power-delivery path (solar/pump/PSU) still primary suspect for THOSE — but they are not what kills CUDA jobs.

## DOCTRINE UPDATE
- GPU doc's two primary fixes (TDR delay, thermal pads) both ruled out by live measurement.
- Power cap does NOT stabilize the card — tested, failed.
- Standing: card RMA direction confirmed; idle-reset class still needs PSU/pump correlation separately.
