# MACBOOK SETUP NOTES — 2026-08-20 (for when the Mac wakes)
## Doctation governing this
- **VDS is BOSS.** PC and MacBook are INDEPENDENT peers — neither depends on the other.
  Both are puppets of Hermes. All routes back to the VDS.
- **stop relying on the Mac for mail** — VDS runs its OWN Proton bridge where possible.
  The Mac-as-mail-bridge (100.64.0.1:1143) made the VDS LOSE the bio reading when the
  Mac slept. That was the mail incident. Stand up the VDS bridge, not the Mac.

## What the Mac should bring back, independently
1. The Mac migration report (what's on the Mac) -> NOT the only copy of anything.
   Fold into the Proton map (/root/zynthio/.../proton map).
2. Mac's own drive contents -> consolidate to Proton (rclone check, NOT delete until
   Proton holds bytes). The Mac holds unique data that only the VDS knows about.
3. USB-debugged phones (Kelvin S22 R5CT70XS8XF) — Termux F-Droid stable installed
   (bundled bootstrap). Tailscale present. SU shared-docs ready once the phone screen
   completes the Termux first-run.

## If the Mac sleeps mid-lane again
- THE PC/MAC INDEPENDENCE MEANS: no lane depends on the other.
- VDS is boss — check the VDS, fetch from it, don't wait on the Mac.

## This file
- Master scope of record: /root/zynthio/desk/MASTER_SCOPE_20260820.md (and MASTER_SCOPE on VDS)
- Leave it here as the Mac->VDS handover note.
