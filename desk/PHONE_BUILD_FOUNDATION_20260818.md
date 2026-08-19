# PHONE BUILD — FOUNDATION STAGED (2026-08-18)
From the sovereign AOSP architecture doc (Zynthio Custom Android OS.txt).
This is the NEXT substantive project, #1 on the master scope.

## THE BUILD (documented, actionable)
- Compile a Zynthio GSI from AOSP, deploy via DSU (no destructive flash)
- Inject ollama-arm64 + Bifrost gateway + Mnemosyne natively via
  cc_prebuilt_binary Soong module (Android.bp in vendor/zynthio/)
- Boot-time daemon via init_rc -> the phone is a ready compute node on
  power-up, no manual terminal init
- Uses precompiled ARM64 binaries (no building ollama from source)

## THE COMPILE HOST (verified — THIS PC is capable)
- CPU: AMD Ryzen 7 5700X3D, 8 cores
- RAM: 32GB dual-channel
- Disk: C: 331GB free (AOSP full build ~350-400GB = TIGHT, may need to
  clear space or trim the build)
- git 2.54 available; no repo/AOSP checkout yet

## NEXT STEPS (the concrete kickoff)
1. Clear ~50-100GB on C: (or build minimal/lineage to fit 331G)
2. Install repo tool (google's git repo bootstrap)
3. repo init a Treble-compatible AOSP/GSI manifest (e.g. phhusson/
   treble_experimentations or LineageOS treble)
4. Add vendor/zynthio/Android.bp with the prebuilt binaries
5. Build the GSI -> system.img -> simg2img -> DSU zip
6. Deploy on the target phone via DSU

## STATUS
STAGED — host verified capable, build path documented. Needs the
disk-trim + repo bootstrap to start the actual compile.
