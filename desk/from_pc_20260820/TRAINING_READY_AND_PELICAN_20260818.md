# TRAINING-READY REALITY — PC vs RUNPOD (2026-08-18)
Operator asked: "when model training start on the pc?"

## THE VERIFIED STATE
- PC: RTX 4060 Ti (1 slot), 8GB, 32GB RAM, Ryzen 5700X3D
- TRAINED ARTIFACT: /root/now_lora_7b.gguf = the qwen2.5-7B LoRA,
  ALREADY trained (on the cloud/RunPod lane per the record)
- VDS: NO nvidia-smi / NO CUDA => cannot GPU-train
- RUNPOD key: 0 in /root/.zynthio.env (needs operator's key to start)

## THE HONEST ANSWER
Model training on the PC's 4060Ti is the WRONG target — the fault
matrix (torch x2, matmul+0x133, ollama, capped at 115W) all faulted on
sustained DNN loads. That's the documented 9-month bypass reason. The PC
is the compile/tooling/USB-host, not the reliable training GPU.

Training starts on RUNPOD/VDS — the PROVEN lane (the qwen LoRA already
trained there). BLOCKED only on: the RUNPOD API key in the env.

## THE ACTIONS
- [x] Confirm trained artifact exists (now_lora_7b.gguf)
- [ ] Operator: drop RUNPOD_API_KEY into /root/.zynthio.env
- [ ] Spin a RunPod GPU pod -> run the next training job
- [ ] PC continues as portable-hermes + AOSP-compile host (not training)

## THE PELICAN/BOAT.NEWS PARALLEL TRACK
- pelicancharters.com.au = FAMILY MASTER (never touch w/o explicit say)
- pelicancharters.ai = live, owned
- boat.news = PAID ($546.56, renew 2027-06-24) but http404 (not built)
- + abrolhos.boats, agua.boats (the .boats family)
- SEO for Pete/brother's owned family sites = active todo (#10), was
  being elongated by daily Hermes failures -> now tracked as its own item
