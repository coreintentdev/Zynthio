# INCIDENT — DELTA VPS UNREACHABLE (2026-08-18) — RESOLVED VIA CLOUDZY API
Operator: gave the one and only cloudzy vps login (coreymc@tutanota.com)
many times + API token 5eb7f38d-e1d3-4379-8eb3-dfe934984774.

## THE ACCESS PATH (all panel views empty due to Las Vegas outage)
The Cloudzy panel (logged in with the right account) rendered ZERO
instances — Las Vegas VM outage notice. But the API saw the box:
GET https://api.cloudzy.com/developers/v1/instances (API-Token header)
-> ubuntu-Dallas-1Highvcpu-1gb id 77c42e4a, status active, mainIp
172.86.88.55, sshKeys: [] (no key attached).

## THE FIX (via API)
1. change-pass endpoint -> new root password 4ZsDw97LtTfco3
2. ssh root@172.86.88.55 with it -> DELTA_REACHED
3. Installed /root/.ssh/cloudzy_new.pub + vps30-contabo-new.pub into
   authorized_keys (3 entries)
4. Key auth verified: ssh -i cloudzy_new root@172.86.88.55 -> WORKS from
   VDS AND from PC (delta_cloudzy_key file)
5. Documented in secure/DELTA_ACCESS.md

## THE LESSON
The panel's empty view LIED. The API (api.cloudzy.com/developers) and the
API token the operator provided were the real path — always try the API
before trusting a panel that may render empty under an outage.
The operator was RIGHT: the tutanota account IS the Cloudzy login.

## STATUS
RESOLVED — DELTA online, key-accessible from VDS + PC. BETA remains the
only VPS down (network path).
