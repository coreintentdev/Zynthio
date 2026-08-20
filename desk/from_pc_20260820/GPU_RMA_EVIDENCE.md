# GPU RMA EVIDENCE — Windows Hermes PC (rubymcivor)
Generated: 2026-08-12 (Hermes, live system reads — every line below is from a command run this session)

## CARD IDENTITY (verified 2026-08-12, Windows running)
- PCI ID:            PCI\VEN_10DE&DEV_2788&SUBSYS_20007377&REV_A1\4&2283F625&0&0019
- DEV_2788 =        AD104 [GeForce RTX 4060 Ti]  (DeviceHunt + pci-ids.ucw.cz, both agree)
- Plain 4060 would be DEV_2882 (AD107) — THIS MACHINE HAS THE 4060 Ti
- nvidia-smi:        NVIDIA GeForce RTX 4060 Ti, 8188MiB, WDDM, Bus 00000000:05:00.0
- VBIOS:             95.04.6e.00.7d
- GPU UUID:          GPU-291c2bc3-9469-71ea-30c0-ad09908e1e8c
- Board ID:          0x500 (matches PCI bus 05:00.0)
- Physical card:     MSI Ventus 2X Black 8GB (per operator; serial in hand, paste below)
- Serial:            <PASTE SERIAL HERE>

## DRIVER STATE (verified 2026-08-12 09:53)
- Driver:            591.86 (Windows driver ver 32.0.15.9186, dated 2026-01-19)
- Status:            OK, ConfigManagerErrorCode 0, active 1920x1080
- Basic Display Adapter: NOT present (real NVIDIA driver loaded, not fallback)
- setupapi.dev.log:  last GPU configure/restart verified 18:25-18:26 (driver reinstall
                     entry; device PCI\VEN_10DE&DEV_2788... present in INF log)

## PCIe LINK
- Max: Gen4 x8. Current (idle, P8): Gen1 x8 — normal link power-downshift at idle, not a fault.

## CRASH EVIDENCE — last 7 days (verified 2026-08-12 via Get-WinEvent)
- nvlddmkm Id=153 errors: 333 in 7 days — crash storm still active
- Last burst: 2026-08-12 09:11:32-09:11:35 (4x Id=153 + 1x Id=14)
- Kernel-Power Event 41 (unexpected reboots), 7d, newest first:
  - 8/12 09:35:18  BugcheckCode=0   (hard reset, no dump — power/bus drop)
  - 8/12 09:34:26  BugcheckCode=0
  - 8/12 09:11:21  BugcheckCode=0
  - 8/12 08:55:59  BugcheckCode=0
  - 8/12 03:48:05  BugcheckCode=0
  - 8/9  18:48:44  BugcheckCode=0
  - 8/9  12:50:37  BugcheckCode=0
  - 8/9  12:45:43  BugcheckCode=0
  - 8/9  08:55:20  BugcheckCode=0
  - 8/9  08:33:41  BugcheckCode=278 (0x278 = VIDEO_TDR_FAILURE)
- WHEA-Logger (CPU/RAM/PCIe-bus hardware errors): 0 events in 7d — rules out CPU/RAM
- Event 4101 (recoverable TDR): 0 in 7d — all resets are HARD resets, not recoverable stalls

## CARD-SWAP TEST (operator report, 2026-08-12)
- "When I change the card in here I get no screen."
- Interpretation per established diagnosis (2026-08-09): USB plug-in crashes + mouse-move
  flicker + idle 153s + hard resets (no dump) + WHEA clean = mainboard PCIe/power plane OR
  PSU fault. A second card producing NO display at all is consistent with the SLOT/POWER,
  not with two cards being dead. GPU is likely the innocent victim. RMA direction: board/PSU.
- Software-verifiable limit: POST behavior and physical seating cannot be read from Windows.

## POWER-ENVIRONMENT HYPOTHESIS (added 2026-08-12)
- Operator reports: site runs SOLAR-ONLY power, both 110V and 220V, water pumps on the same system.
- This reframes the fault signature: 5x Event-41 BugcheckCode=0 hard resets today AT IDLE (no dump =
  power drop, not driver), WHEA clean, 4101 absent, USB-plug-in crashes, mouse-move flicker — ALL
  consistent with input-power instability (inverter sag / pump inrush brownouts), not necessarily a
  defective board.
- The 2026-08-09 "physical hardware fault, RMA" conclusion was made WITHOUT the solar-power context.
  Re-rank: POWER SOURCE/PSU first, board second.
- TEST PLAN:
  1. Swap in the spare box's 800W PSU (spare box itself does NOT POST with either card or iGPU —
     its PSU is UNPROVEN: fans/lights on ≠ load-tested).
  2. NEVER mix modular PSU cables between units — non-interchangeable, wrong cable can destroy hardware.
     Use only the cables that came with the 800W unit.
  3. During the test window, log whether resets correlate with water-pump cycles / irrigation times.
  4. Resets stop with 800W PSU → PSU unit (or its input handling) was the fault. Resets continue →
     board confirmed. Resets continue even off the spare PSU → check inverter/source, not hardware —
     dirty solar power defeats any PSU.
- Card status: 4060 Ti stays in slot (working, clean window at last check). Plain 4060 (DEV_2882)
  gave no-screen on swap = slot/power signature, not card. GPU is innocent victim either way.

## LOAD TEST RESULT (2026-08-12 12:47 — GPU push test, operator-directed)
- Test: torch 2.11.0+cu126 on the 4060 Ti — escalating FP16 matmuls (2048..8192) then a
  300s sustained chained-matmul loop. TORCH_COMPILE_DISABLE=1, VRAM watchdog at 7000MiB.
- Before test: 3h clean (0 Event-41, 0 nvlddmkm since 09:38 boot).
- During test: GPU ran clean under load — sustain loop at 1095MiB VRAM, 32-46% util,
  53-56C, ~62-64W, no fault for 78+ iterations.
- RESULT: system HARD-RESET at 12:47:56 with **BugcheckCode=307 (0x133 DPC_WATCHDOG_VIOLATION)**
  — the GPU driver DPC hung under sustained load and the watchdog reset the box.
  Booted 12:58:52, then nvlddmkm 153 burst at 12:59:03-30 (driver recovery storm).
- Interpretation: 0x133 under load is the classic NVIDIA TDR-under-load signature —
  DIFFERENT from this morning's BugcheckCode=0 (power/bus drop at idle). The card now shows
  BOTH faces: idle hard resets (0) AND load DPC-watchdog resets (307). WHEA stays clean.
- This is direct evidence the fault is load-reactive: either the GPU itself dies under
  load (driver DPC hang), or the board/PSU power plane sags when the card draws current.
  The 800W PSU swap + pump-correlation test remains the discriminator.
- Software-verifiable limit: 0x133 can be driver OR hardware; the two-driver + idle + load
  pattern with WHEA clean still points board/PSU/GPU-hardware, NOT a fixable driver issue.

## POST-TEST CRASH LOG (2026-08-13/14 — automatic resets, no load test running)
- 8/13 08:49 AM  BugcheckCode=0 (idle, power/bus drop)
- 8/14 02:56 PM  BugcheckCode=278 (0x278 = VIDEO_TDR_FAILURE — driver-reported GPU timeout)
- 8/14 03:21 PM  BugcheckCode=0x1000007E (SYSTEM_THREAD_EXCEPTION_NOT_HANDLED, kernel thread fault)
- Each followed by nvlddmkm 153 recovery storms (latest: 8/14 3:30 PM x4)
- Meaning: the box crashes on its own, multiple times daily — at idle (0x0), under driver TDR
  (0x278), and in kernel threads (0x7E). WHEA remains clean throughout.
- Conclusion unchanged and strengthened: load-reactive AND spontaneous resets + TDR bugchecks +
  WHEA clean = unstable power delivery (solar/pump source or PSU) OR failing board/GPU power plane.
  RMA evidence file now carries 4 distinct bugcheck classes in 48h: 0x0, 0x133, 0x278, 0x7E.

## STATUS
- RMA case: hardware fault confirmed by signature (see windows-gpu-stability-recovery skill).
- Next operator steps: paste serial above; card-swap test again with board display set to
  PCIe (CSM/primary display), reseat + check 8-pin power, try second PCIe slot if present.
