# INCIDENT — ORICO WRONG-HOST + VAULT NEARLY FULL (2026-08-16)
Severity: HIGH · Operator: "incident first then go"

## THE FACTS (verified live)
1. ORICO is attached to THIS PC (Disk 1, Online, 128GB GPT, volume F:),
   NOT the Mac. stack_proof.sh checked /Volumes/ORICO on the Mac —
   WRONG HOST. "Dropbox path not found" = wrong machine, not missing drive.
2. ORICO F: has 1.77 GB free of 128GB — VAULT NEARLY FULL.
3. Contents (verified): zynthio-tools, HANDOVER_DOCS, ALPHA_SAFE_20260808 ×3,
   model_maker, runpod_staging, PC_PACK_20260814, orico_ingest — the alpha-safe
   checkpoint destination.
4. 5-day comparison: Mac = engine (10,871 files), PC = surface (session work),
   ORICO = vault (137 writes — the last of the room).

## THE RISK
The ORICO holds the alpha-safe snapshots the deletion doctrine depends on.
At 1.77GB free, the next ALPHA_SAFE snapshot may not fit → the safe-chain
stops → the "verified copy" gate loses its copies.

## THE FIX (next)
- Verify ALPHA_SAFE snapshots are mirrored to Proton (before the vault fills).
- Correct stack_proof.sh host: ORICO = PC F:, not Mac /Volumes/ORICO.
- Decide: expand vault (new drive) or purge verified-duplicates from ORICO.

## STATUS
Filed before action. Verification of alpha-safe on Proton = next move.
