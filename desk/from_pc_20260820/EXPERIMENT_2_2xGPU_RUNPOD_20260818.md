# EXPERIMENT 2 — 2xGPU LOCAL COMPUTE MODEL, THEN RUNPOD (2026-08-18)
REVISED with the full documented pretest record. The operator asked:
"do you need the model number of the original cord? 8gb you should have
notes as we done lots of pretest and ran a model already? 4060 yes ti
duo" — the notes exist, now this doc reflects them.

## THE SETUP (verified live)
- GPU now: RTX 4060, 8GB, idle (na 2nd: another 8GB 4060 = 2x8GB = 16GB)
- RAM now: 32GB DUAL-CHANNEL (Bank A + B, 16GB @ 2133 each) — CONFIRMED IN
- CPU: AMD Ryzen 7 5700X3D, 8 cores. C: 331G free (AOSP-host capable)

## THE FULL DOCUMENTED PRETEST RECORD (from workspace files)
### PRETEST 20260814_072125 (PSU_BUS_PRETEST_20260814.txt)
- Box was on RTX 4060 Ti: Event41_14d=23, nvlddmkm153_24h=39,
  P8/8.81W idle. Marked "FAIL-THEN-SWAP" — Ti was the test subject.

### POWER-CAP TEST 20260815 (INCIDENT_POWER_CAP_TEST_20260815.md)
- Capped 115W (from 165W), gpu_push.py matmul, 5-min window
- FAULT at iter 44: CUDA launch failure at ONLY 63W/57C/26% util/1GB VRAM
- RULED OUT by live measurement: power draw (63W), thermal (57C),
  utilization (26%). Non-deterministic silicon-level instability.
- FAULT MATRIX (4 independent reproductions):
  - torch uncapped: iter 35 (Aug 8)
  - matmul uncapped: iter 78 + reset 0x133 (Aug 12)
  - ollama uncapped: immediate (Aug 15)
  - torch capped 115W: iter 44 (Aug 15)
- The Ti (AD106, 128-bit bus, no ECC) = consumer Ada soft-error + TDR
  signature. "Fine for gaming, fails on sustained LLM loads."
- Earlier swap (Ti -> 4060) faulted IDENTICALLY -> fault follows the
  SLOT/BUS/PSU path, NOT the specific card.

### ALREADY-RAN MODEL (Troubleshooting GPU AI Build Failures.txt)
- Qwen2.5-7B LoRA (200 steps, loss 0.41, 90% acc) trained on RUNPOD
- 161MB adapter + 15GB base model; llama.cpp served the q8_0 model
  LIVE on the VDS endpoint
- The compute MODEL ALREADY RUNS PROVEN on VDS/RunPod — cloud lane.

## THE REVISED EXPERIMENT 2 LOGIC (evidence-backed)
Pairing a 2nd 8GB 4060-family card with a KNOWN-FLAKY card on the SAME
suspect slot/bus/PSU path is NOT a speculative test — the notes say the
most-likely outcome is the same CUDA fault. The experiment's real value
is as a CLEAN CONFIRMATION, not a gamble:

1. [WAIT] Physical: install 2nd 8GB GPU (operator's hands)
2. nvidia-smi -> confirm 2x 8GB = 16GB total
3. idle 2x -> watch for Id=41 / TDR (the idle-reset class)
4. load test (gpu_push.py) on the 2nd card ALONE
5. load test across BOTH (dual, the real target)
6. Expected (from 4x fault matrix): CUDA fault on sustained load ->
   CONFIRMS local unfit for LLM. No crash = an unexpected WIN.
7. RUNPOD: the compute model lane is ALREADY PROVEN there (the
   Qwen2.5-7B LoRA). If local confirms unfit, RunPod is the standing
   answer, not a pivot.

## THE STACKS' STANCE
- Local 4060 Ti/4060 = TDR + soft-error (no ECC) architecture,
  documented unfit for sustained DNN loads (9-month bypass record).
- PC's 32GB/8c stays the AOSP-compile + tooling host (not the GPU
  compute lane).
- RunPod/VDS = proven compute model lane (Qwen2.5-7B ready).

## THE HONEST STATUS
Experiment 2 = confirmation test. It will most likely re-confirm the
documented fault. If it DOESN'T (no crash on 2x dual load), that's the
surprise worth acting on. Either way, the compute model stays on
RunPod where it's proven.

## NEXT (operator's go)
Install the 2nd 8GB card -> power on -> I run the protocol + nvidia-smi.
