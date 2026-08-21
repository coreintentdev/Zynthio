#!/usr/bin/env python3
"""MASTER DOMAIN LIST builder — Porkbun + Cloudflare registrars, with ages.
Groundhog-killer: single canonical file for all future sessions.
Signal 336."""
import json, os, re, sys, urllib.request, urllib.error
from datetime import datetime, timezone

sys.path.insert(0, "/Users/coreymcivor/Desktop/zynthio-tools/18JUNE/scripts")
import pb_api

DESK = os.environ.get("ZYNDESK", "/Users/coreymcivor/Desktop/zynthio-tools/18JUNE/desk")
OUT_JSON = os.path.join(DESK, "MASTER_DOMAIN_LIST_LIVE.json")
OUT_CSV = os.path.join(DESK, "MASTER_DOMAIN_LIST_LIVE.csv")
OUT_MD = os.path.join(DESK, "MASTER_DOMAIN_LIST_LIVE.md")

def pb_post(path, body):
    req = urllib.request.Request(f"{pb_api.BASE}/{path}", data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "zyn-pb/336"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception:
        return {"status": "ERROR"}

def load_env(path):
    env = {}
    try:
        for line in open(os.path.expanduser(path)):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.lower().startswith("export "):
                line = line[7:].strip()
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return env

def cf_get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"success": False, "errors": [{"message": str(e)[:80]}]}

# ---- 1. Porkbun ----
label, pk, sk = pb_api.resolve_keys()
auth = {"apikey": pk, "secretapikey": sk}
pb_domains = {}
for start in (0, 1000, 2000, 3000, 4000):
    r = pb_post("domain/listAll", {**auth, "start": start})
    if r.get("status") != "SUCCESS":
        print("PB_ERR", r.get("message", "")[:80])
        break
    doms = r.get("domains", [])
    for d in doms:
        name = d.get("domain", "").lower()
        pb_domains[name] = {
            "status": d.get("status"),
            "tld": d.get("tld"),
            "createDate": d.get("createDate"),
            "expiryDate": d.get("expiryDate"),
            "autoRenew": d.get("autoRenew"),
        }
    if len(doms) < 1000:
        break

# ---- 2. Cloudflare registrar ----
env = load_env("~/.zynthio.env")
cf_token = env.get("MAIN_CF_TOKEN") or env.get("CF_API_TOKEN") or env.get("SECONDARY_CF_TOKEN")
raw_acct = env.get("CLOUDFLARE_ACCOUNT_ID") or env.get("CF_ACCOUNT_ID") or ""
m = re.match(r"([0-9a-f]{32})", raw_acct.strip())
cf_acct = m.group(1) if m else ""
cf_domains = {}
cf_err = None
if cf_token and cf_acct:
    cf_domains = {}
    page = 1
    while True:
        r = cf_get(f"https://api.cloudflare.com/client/v4/accounts/{cf_acct}/registrar/domains?per_page=50&page={page}", cf_token)
        if not r.get("success"):
            cf_err = str(r.get("errors", [{}])[0].get("message", ""))[:100]
            break
        res = r.get("result", [])
        for d in res:
            name = d.get("name", "").lower()
            cf_domains[name] = {
                "status": d.get("state") or d.get("status"),
                "createDate": (d.get("created_at") or "").replace("T", " ")[:19],
                "expiryDate": (d.get("expires_at") or "").replace("T", " ")[:19],
            }
        if len(res) < 50:
            break
        page += 1
else:
    cf_err = f"no usable token/acct (acct_len={len(raw_acct)})"

# ---- 3. Merge ----
SNAP = "/Users/coreymcivor/Desktop/zynthio-tools/18JUNE/desk/cf_registered_snapshot.json"
snap_domains = {}
if os.path.exists(SNAP):
    try:
        snap_domains = json.load(open(SNAP)).get("domains", {})
    except Exception:
        pass

def age_years(create):
    if not create:
        return None
    try:
        dt = datetime.strptime(create[:10], "%Y-%m-%d")
        return round((datetime.now(timezone.utc) - dt.replace(tzinfo=timezone.utc)).days / 365.25, 1)
    except Exception:
        return None

merged = {}
for name, info in pb_domains.items():
    merged[name] = {"registrar": "Porkbun", "status": info["status"], "tld": info["tld"],
                    "createDate": info["createDate"], "expiryDate": info["expiryDate"],
                    "ageYears": age_years(info["createDate"]), "autoRenew": info["autoRenew"]}
for name, info in cf_domains.items():
    if name in merged:
        merged[name]["registrar"] = "Porkbun+Cloudflare"
    else:
        merged[name] = {"registrar": "Cloudflare", "status": info["status"], "tld": name.split(".")[-1],
                        "createDate": info["createDate"], "expiryDate": info["expiryDate"],
                        "ageYears": age_years(info["createDate"]), "autoRenew": None}
for name, info in snap_domains.items():
    name = name.lower()
    if name in merged:
        if "snapshot" not in merged[name].get("registrar", ""):
            merged[name]["registrar"] = merged[name]["registrar"] + "+CFsnap"
    else:
        merged[name] = {"registrar": "Cloudflare(snapshot)", "status": info.get("status", "ACTIVE"),
                        "tld": name.split(".")[-1], "createDate": info.get("createDate"),
                        "expiryDate": info.get("expiryDate"),
                        "ageYears": age_years(info.get("createDate")), "autoRenew": None}

rows = [{"domain": n, **v} for n, v in merged.items()]
rows.sort(key=lambda r: r["ageYears"] if r["ageYears"] is not None else -1, reverse=True)

# ---- 4. Write ----
stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "signal": 336,
    "id": "MASTER_DOMAIN_LIST_LIVE",
    "updated": stamp,
    "groundhog_fix": "Single canonical domain truth. Refresh with scripts/master_domain_list_builder.py. Never re-derive from scratch.",
    "counts": {"total": len(rows), "porkbun": len(pb_domains), "cloudflare": len(cf_domains), "both": sum(1 for r in rows if r["registrar"] == "Porkbun+Cloudflare")},
    "cf_registrar_error": cf_err,
    "domains": rows,
}
with open(OUT_JSON, "w") as f:
    json.dump(payload, f, indent=1, ensure_ascii=False)

with open(OUT_CSV, "w") as f:
    f.write("domain,registrar,tld,status,createDate,expiryDate,ageYears,autoRenew\n")
    for r in rows:
        f.write(f"{r['domain']},{r['registrar']},{r['tld']},{r['status']},{r['createDate']},{r['expiryDate']},{r['ageYears']},{r['autoRenew']}\n")

now = datetime.now(timezone.utc)
def days_to(exp):
    try:
        return (datetime.strptime(exp[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc) - now).days
    except Exception:
        return 999
expiring = [r for r in rows if days_to(r["expiryDate"]) <= 120]
aged = [r for r in rows if r["ageYears"] is not None and r["ageYears"] >= 10]

md = f"""# MASTER DOMAIN LIST — LIVE
**Signal:** 336 · **Updated:** {stamp}
**Groundhog fix:** this file is the canonical domain truth. Refresh: `python3 18JUNE/scripts/master_domain_list_builder.py` — never re-derive from scratch.

## Counts
- **Total:** {len(rows)} · Porkbun: {len(pb_domains)} · Cloudflare registrar: {len(cf_domains)} · both: {sum(1 for r in rows if r['registrar']=='Porkbun+Cloudflare')}
- CF registrar error: {cf_err or 'none'}

## Oldest 20 (age years)
| domain | registrar | age | create |
|---|---|---|---|
"""
for r in rows[:20]:
    md += f"| {r['domain']} | {r['registrar']} | {r['ageYears']} | {r['createDate']} |\n"
md += "\n## Expiring within 120 days\n| domain | registrar | expiry |\n|---|---|---|\n"
for r in sorted(expiring, key=lambda x: days_to(x["expiryDate"])):
    md += f"| {r['domain']} | {r['registrar']} | {r['expiryDate']} |\n"
md += "\n## Files\n- Full JSON: `desk/MASTER_DOMAIN_LIST_LIVE.json`\n- CSV (ages, expiry): `desk/MASTER_DOMAIN_LIST_LIVE.csv`\n"
with open(OUT_MD, "w") as f:
    f.write(md)

# ---- 5. Summary print ----
print(f"TOTAL={len(rows)} PB={len(pb_domains)} CF={len(cf_domains)} BOTH={sum(1 for r in rows if r['registrar']=='Porkbun+Cloudflare')}")
print("OLDEST:")
for r in rows[:8]:
    print(f"  {r['ageYears']}y | {r['createDate']} | {r['registrar']} | {r['status']}")
print("EXPIRING<=120d:", len(expiring))
for r in sorted(expiring, key=lambda x: days_to(x['expiryDate']))[:10]:
    print(f"  {days_to(r['expiryDate'])}d | {r['expiryDate']} | {r['status']}")
# spot-check disputed names
for probe in ["rareggaeton.com", "bettertimethannow.com", "urbanomusica.com", "logicalcli.com", "drdisorder.com", "drsyntax.com", "agitin.com", "noerus.net", "noeruscapital.com"]:
    hit = merged.get(probe)
    print(f"PROBE {probe} ->", (f"{hit['registrar']} age={hit['ageYears']}y create={hit['createDate']}" if hit else "NOT FOUND"))
