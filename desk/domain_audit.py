#!/usr/bin/env python3
"""DOMAIN AUDIT — pull age/registrar/history for owned domains, scaffold per-domain wiki.
Reads the master + actual domain lists, queries RDAP for registration dates, writes
WIKI_<domain>.md per domain. Run: python3 domain_audit.py --domains [file] --out [dir]
"""
import json, subprocess, sys, os, urllib.request, datetime, re

def rdap_age(domain):
    """Return (created, expires, registrar) via RDAP, or (None,None,None)."""
    for base in [f"https://rdap.verisign.com/com/v1/domain/{domain}",
                 f"https://rdap.org/domain/{domain}"]:
        try:
            req = urllib.request.Request(base, headers={"Accept":"application/rdap+json"})
            with urllib.request.urlopen(req, timeout=12) as r:
                d = json.load(r)
            ev = {e.get("eventAction"): e.get("eventDate","") for e in d.get("events",[])}
            created = ev.get("registration") or ev.get("created") or ""
            expires = ev.get("expiration") or ev.get("registry expiry") or ""
            reg = ""
            for e in d.get("entities",[]):
                if "registrar" in e.get("roles",[]):
                    va = e.get("vcardArray",[None,[]])[1]
                    for item in va:
                        if item and item[0]=="fn" and len(item)>3:
                            reg = item[3]; break
            return (created[:10], expires[:10], reg[:60])
        except Exception:
            continue
    return (None,None,None)

def main():
    domains_file = sys.argv[1] if len(sys.argv)>1 else "domains_output.csv"
    out_dir = sys.argv[2] if len(sys.argv)>2 else "wiki"
    os.makedirs(out_dir, exist_ok=True)
    # read domains
    domains = set()
    with open(domains_file, encoding="utf-8", errors="replace") as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith("#"): continue
            # take first field as domain
            dom = line.split(",")[0].strip().lower()
            if re.match(r"^[a-z0-9-]+\.(com|net|org|io|ai|fyi|boats|news|quest|online|me|co)$", dom):
                domains.add(dom)
    print(f"[audit] {len(domains)} domains to process")
    rows=[]
    for i, d in enumerate(sorted(domains),1):
        created, expires, reg = rdap_age(d)
        row = {"domain":d,"created":created,"expires":expires,"registrar":reg}
        rows.append(row)
        # scaffold the wiki
        age = ""
        if created:
            try:
                c=datetime.date.fromisoformat(created); t=datetime.date.today()
                years=(t-c).days/365.25
                age = f"{years:.1f} yrs" if years>=1 else f"{int((t-c).days)} days"
            except: age=created
        wiki = f"""# WIKI — {d} (auto-audit 2026-08-19)
- Registered: {created or 'unknown'}
- Expires: {expires or 'unknown'}
- Registrar: {reg or 'unknown'}
- Approx age: {age}
- History/backlinks: [[PENDING deeper pull]]
- Role: [[pending master-scope entry]]
"""
        with open(os.path.join(out_dir, f"WIKI_{d}.md"),"w") as w:
            w.write(wiki)
        if i%50==0: print(f"[audit] {i}/{len(domains)}")
    # write summary csv
    import csv
    with open("domain_ages_audit.csv","w",newline="",encoding="utf-8") as o:
        w=csv.writer(o); w.writerow(["domain","created","expires","registrar","age"])
        for r in rows:
            w.writerow([r["domain"],r["created"],r["expires"],r["registrar"]])
    print(f"[audit] done. {len(rows)} rows -> domain_ages_audit.csv, wikis in {out_dir}/")

if __name__=="__main__":
    main()
