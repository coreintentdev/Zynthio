# INCIDENT — PAID BOXES UNUSED = SILICON HEADLESS MESS (2026-08-18)
Operator: "report incident drop my box equals logically a silicon headless
mess song. make use of these boxes. otherwise you are just contributing
to wasting time, resources and money!"

## THE AGGRIEVANCE
4 paid boxes (VDS gamma + 3 VPS) sit mostly idle. We spend time hunting
creds and probing connectivity instead of USING the compute for the
stack's actual work (music, domains, clients, AI). Every box that isn't
running something = wasted money + resources.

## THE FLEET (4 paid, now 3 reachable)
| Box | IP | Spec | Status | Use |
|-----|-----|------|--------|-----|
| gamma (VDS) | 5.189.143.170 | 16GB | LIVE | the brain (services, twin, qwen) |
| alpha | 84.247.137.105 | vmi3204749 | LIVE | IDLE |
| delta | 172.86.88.55 | 1vCPU/1GB | ONLINE (rekeyed) | IDLE |
| beta | 161.97.89.49 | 7GB plan | DOWN (network) | wound |

## THE FIX (put the boxes to work)
- alpha: run a redundant service (highway overwatch, monitoring, or a
  CDN/edge origin) — not idle
- delta: 1GB box = light lane — cron/overwatch/mail-bridge/porkbun-DNS
  worker, NOT models
- beta: recovery attempt or documented as decommissioned (stop paying
  if it can't be reached)
- The stack serves the clients, never consumes them.

## STATUS
OPEN — assign real workloads to alpha + delta now, resolve beta.
