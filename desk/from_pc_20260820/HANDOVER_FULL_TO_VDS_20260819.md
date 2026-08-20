# HANDOVER — FULL SESSION TO VDS (2026-08-19)
Operator: "handover all session in this ui to the vds. i work direct from
vds now. no more of this ui sandbox bs. context to a focus that is just
lost."

## WHERE EVERYTHING LIVES (work from here)
- Desk (incidents/findings/plans): /root/zynthio/desk/
- Seamstress (weave engine): /root/zynthio/seamstress/master_seamstress.py
- Research (POV/AGENTIC): /root/zynthio/research/
- Domain wiki/audit: /root/zynthio/wiki_all/ + domain_ages_audit.csv
- Credential vault: /root/zynthio-tools/zynthio/secure/vault.env.gpg + CREDENTIAL_MAP.md
- ACCC legal/evidence: /root/.hermes/memories/ingested_docs/zynthio_handover/AI_FABRICATION_EVIDENCE_ACCC_20260819.md
- ChromaDB: neverend-chroma container (port 8001) — NOTE: persist volume EMPTY (184KB ephemeral)

## THE FLEET (live state)
- gamma VDS 5.189.143.170 — brain, twin, gateway, qwen3:8b-64k (port 11434)
- alpha 84.247.137.105 — hot-standby qwen3:8b + redundant watchdog
- delta 172.86.88.55 — rekeyed (cloudzy API), light-lane watchdog
- beta 161.97.89.49 — DECOMMISSIONED (unreachable)
- PC: 4060Ti (torch-cu121 cuda=True, RUNS models local) + 32GB dual

## THE OPEN WORK (the real todo, in operator priority)
1. ChromaDB persist — MOUNT a real volume, re-ingest for real (45 days
   lost to ephemeral layer = the core data-loss bug)
2. Seamstress — patched (zynrip handler added) but weave STILL returns
   0 threads (272-byte output); needs the weave debugged against the
   8,232-item harvest
3. Local model — WORKS (4060Ti). Next: run a real model, not toy SmolLM.
4. Domains — 536 audited + wikis; SEARCHITCENTRAL live, aingestion live.
   Operator decides build order.
5. Training — RunPod (local 4060Ti is inference, not heavy training).

## THE BINDING DOCTRINE (this session's hard lessons)
- Evidence gate: no "done/fixed/delivered" without a filled EVIDENCE
  block (TASK_EVIDENCE_GATE.md). Mirror before claim.
- No fabrication: evidence-verbatim or silence. "9 months non-deployment"
  is the metric — ship or say blocked.
- Check the mirror before reversing a claim.
- The word's home: CREDENTIAL_MAP.md → vault, never re-hunt.
- ACCC legal record: AI fabrication is now documented (insurance).

## STATUS
Handover complete. All session files synced to /root/zynthio/desk/.
Operator works from the VDS now. The UI sandbox is done.
