# INCIDENT — CARD SWAP TEST: FAULT FOLLOWS THE SLOT, NOT THE CARD (2026-08-16)
Operator: "changed card removed 1 memory stick. geoforce other installed.
using usb wifi instead of ethernet variables matter... i say software but there
must be a bus or usb problem or that whole rear bar get a spike or short.
localised?"

## THE TEST (2026-08-16, live)
- New GPU: RTX 4060 (8GB, driver 560.94) — REPLACED the 4060 Ti
- RAM: 16GB single stick (one removed)
- Network: USB wifi (Realtek 8812AU); ethernet reconnected at 1 Gbps
- Test: ollama llama3.2:3b generation on the new 4060
- RESULT: Connection reset mid-generation — same signature as the Ti

## THE EVIDENCE
- Power-loss events (Id=41): 2026-08-16 04:23 and 04:37 — during GPU load
- GPU idle now: 51C, 1% — stable when idle
- The 4060 Ti faulted 4 times (torch 08-08, matmul 08-12, ollama 08-15,
  capped test iter 44). The 4060 faulted on its FIRST load test today.
- 4060 Ti vs 4060 = different silicon. Same crash. => NOT the card.

## THE CONCLUSION
The fault follows the SLOT/BUS/POWER path, not the GPU:
- PCIe slot power delivery (the 800W PSU swap is the remaining test)
- Motherboard rear I/O bar spike/short (operator's hypothesis)
- USB controller sharing the LAN/USB bus (keyboard Unknown after ethernet plug)
- Solar-only supply + water-pump inrush (idle resets, BugcheckCode=0)

## OPERATOR'S DIAGNOSIS (endorsed by the test)
"there must be a bus or usb problem or that whole rear bar get a spike or
short. localised?" — YES. Localized to the slot/bus/power path. The card
swap PROVES it: new card, same crash.

## REMAINING TESTS (physical only)
1. 800W PSU swap (own cables ONLY)
2. Card in a different PCIe slot (the slot itself)
3. Pump-correlation logging (power inrush)
4. SystemRescue live-USB diagnostics (Devin's plan, stick ready)
