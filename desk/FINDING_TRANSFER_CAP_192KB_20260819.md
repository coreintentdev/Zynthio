# FINDING — PC LARGE-FILE TRANSFER CAP ~192KB (2026-08-19)
Discovered while moving the local model to the 4060Ti.

## THE SYMPTOM
Every single direct file transfer TO this PC landed as a 197,121-byte
(~192KB) STUB regardless of source or size:
- HF download (huggingface-cli / snapshot_download) -> 192KB stub
- scp of 723MB model.safetensors from VDS -> 192KB stub
- rclone/HF -> stalled or 192KB

## THE WORKAROUND (WORKING)
Chunk the file on the VDS into 50MB parts, scp each part separately.
Each chunk transfers FULL-SIZE (verified `wc -c` = 50,000,000). Then
reassemble. 9/15 chunks landed clean so far.

## WHY IT MATTERS (the day's root cause)
This ~192KB cap explains many of today's "failures":
- The model download stalls/fails -> local model was "blocked"
- Workspace->Proton / backup pushes appeared to fail
- Everything that needed a large file to the PC hit the wall
It's likely a proxy/buffer/firewall cap on the PC's receive path
(Hermes terminal file handling or an ISP/AV shaper).

## ONGOING ACTIONS
- [ ] Finish chunk transfer (9/15) + reassemble model.safetensors
- [ ] Run the model LOCAL on the 4060Ti (the operator's core ask)
- [ ] Identify the ~192KB cap source (Hermes path? firewall? shaper?)
