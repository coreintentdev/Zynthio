# INCIDENT — "LOST COMMS WITH MAC AGAIN" (2026-08-19) — PC MESH NOT MASK
Operator: "report incident lost comms with mac again. on the same network
tailscale and vds keys done but you lost it again!"

## THE DIAGNOSIS (measured, not assumed)
- VDS MESH: MAC VISIBLE at 100.64.0.1 (lilroblox-gamer, macOS), ping 0%
  loss, VDS->Mac SSH WORKS (lilRoblox-gamer.local, MAC_REACHED via the
  zynthio_dc key on the VDS).
- PC->Mac SSH: TIMES OUT.
- PC's OWN Tailscale: STUCK at "Tailscale is starting / NoState" — the
  PC is NOT on the mesh (wedged service).

## THE REAL CAUSE
The Mac was NEVER lost — its mesh + keys on the VDS work perfectly. The
loss is the PC's Tailscale service being wedged (NoState, "starting"
forever). Every "lost comms with mac" from THIS session was actually
"the PC can't get on the mesh," not the Mac or the keys.

## THE DISTINCTION (the operator's core point)
The VDS keys (zynthio_dc) are FINE — proven (MAC_REACHED). Nothing about
the keys was lost. The failure is the PC's network path, a separate
layer that keeps being conflated with "lost the keys / lost the mac."

## THE FIX
- [x] Diagnose: VDS->Mac confirmed working (keys intact)
- [ ] Fix PC Tailscale service (NoState wedge) so this PC can reach the
      mesh directly
- [ ] The "lost again" framing is corrected: keys never lost, PC mesh
      was the broken path

## STATUS
OPEN — PC Tailscale wedge being fixed; Mac + keys confirmed healthy on
the mesh from the VDS.
