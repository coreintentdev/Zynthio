#!/usr/bin/env python3
"""Run the reassembled SmolLM2 model LOCALLY on the RTX 4060Ti."""
import torch, time, sys
from transformers import AutoModelForCausalLM, AutoTokenizer

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[local-infer] device={DEVICE} gpu={torch.cuda.get_device_name(0) if DEVICE=='cuda' else 'cpu'}", flush=True)

t0 = time.time()
tok = AutoTokenizer.from_pretrained("./smollm2", local_files_only=True)
model = AutoModelForCausalLM.from_pretrained("./smollm2", local_files_only=True,
    torch_dtype=torch.float16).to(DEVICE)
print(f"[local-infer] model loaded on {DEVICE} in {time.time()-t0:.1f}s", flush=True)

PROMPT = "The Zynthio sovereign stack serves Corey by"
inputs = tok(PROMPT, return_tensors="pt").to(DEVICE)
with torch.no_grad():
    gen = model.generate(**inputs, max_new_tokens=120, do_sample=True, temperature=0.7, pad_token_id=tok.eos_token_id)
out = tok.decode(gen[0], skip_special_tokens=True)
print("\n=== LOCAL INFERENCE OUTPUT ===\n", flush=True)
print(out, flush=True)
print(f"\n=== GPU {torch.cuda.get_device_name(0)} :: {time.time()-t0:.1f}s total ===", flush=True)
