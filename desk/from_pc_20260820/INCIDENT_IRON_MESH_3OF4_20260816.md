# INCIDENT — IRON MESH CHECK: 3 OF 4 NODES UNREACHABLE (2026-08-16)
Operator: "3x vds 1 vds 1 proton stack check meshed head and tail not a coin toss"

## THE CHECK (live, not guessed)
- GAMMA 5.189.143.170 (VDS): ALIVE — zynthio-vds-7372, 93%/14G, load 0.06
- ALPHA 84.247.137.105: PERMISSION DENIED — zynrose key not accepted
- BETA 161.97.89.49: TIMEOUT — port 22 unreachable
- DELTA 172.86.88.55: HOST KEY VERIFICATION FAILED — key changed/reinstall
- PROTON: ALIVE (pills verified all day, 467GB free)

## THE TRUTH
The mesh was claimed "nothing dead" in master_scope. The live check:
1 of 4 nodes answering. The Iron has 3 wounds — never checked until
the operator asked. This is the undercount the scope's own law names.

## THE FIX (queued)
- ALPHA: find the correct key (mesh.sh / other keys in ~/.ssh)
- BETA: check DNS/firewall — is the IP still the box?
- DELTA: re-accept host key, verify identity before trusting
- Head (gamma) + tail (Proton) confirmed. The mesh gets re-meshed.

## STATUS
OPEN — 3 nodes unverified. The check is filed; the repair is queued.
