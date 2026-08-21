#!/usr/bin/env python3
"""zyn-pb / pb_api — Porkbun CLI (Signal 336)

HOST RULE (HARD):
  https://api.porkbun.com/api/json/v3
  NEVER https://porkbun.com/api  → AWS ELB HTML 403 (looks like ban, is not)

KEY RULE:
  Prefer live pair. Probe files in order; first pair that pings SUCCESS wins.
  Dead keys in ~/.zynthio.env alone are common — pb-cf.env holds the live pair.

DNS RULE:
  Delete pixie ALIAS / parking CNAME before apex A.

Examples:
  zyn-pb ping
  zyn-pb which-key
  zyn-pb retrieve musicbackup.dev
  zyn-pb point musicbackup.dev
  zyn-pb point cfmusic.dev 5.189.143.170
  zyn-pb list-a musicbackup.dev
  zyn-pb cart-remove acidicsoftware.com
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path
from urllib.error import HTTPError

SIGNAL = 336
BASE = "https://api.porkbun.com/api/json/v3"
VDS_DEFAULT = "5.189.143.170"
REPO = Path(__file__).resolve().parents[1]  # 18JUNE

# Search order: live sources first
ENV_CANDIDATES = [
    Path("/root/STACK_LIVE.env"),
    Path("/root/.env"),
    Path("/root/pb-cf.env"),
    REPO / ".secure" / "pb-live-336.env",  # VDS-proven live pair (restore 2026-07-29)
    REPO / "evny" / "STACK_LIVE.env",
    REPO / "evny" / "pb-cf.env",
    REPO / ".secure" / "pb-cf.env",
    REPO / "zynthio.env",
    Path.home() / ".zynthio.env",
    REPO / "evny" / "pb-cf.env.save",
]


def _parse_env_file(path: Path) -> list[tuple[str, str, str]]:
    """Return list of (label, pk, sk) pairs found in one file."""
    if not path.exists():
        return []
    api: dict[str, str] = {}
    sec: dict[str, str] = {}
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.lower().startswith("export "):
            line = line[7:].strip()
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip("'").strip('"')
        if not v.startswith(("pk1_", "sk1_")):
            continue
        if "PORKBUN" in k.upper() and "API" in k.upper() and "SECRET" not in k.upper() and v.startswith("pk1_"):
            api[k] = v
        elif "PORKBUN" in k.upper() and "SECRET" in k.upper() and v.startswith("sk1_"):
            sec[k] = v

    pairs: list[tuple[str, str, str]] = []
    for ak, pk in api.items():
        # match by suffix after API_KEY
        suf = ""
        if "API_KEY" in ak:
            suf = ak.split("API_KEY", 1)[1]
        sk = None
        for sn, sv in sec.items():
            if suf and sn.endswith(suf):
                sk = sv
                break
        if sk is None and "PORKBUN_SECRET_KEY" in sec and ak in (
            "PORKBUN_API_KEY",
            "export PORKBUN_API_KEY",
        ):
            sk = sec["PORKBUN_SECRET_KEY"]
        if sk is None and len(api) == 1 and len(sec) == 1:
            sk = next(iter(sec.values()))
        if sk:
            pairs.append((f"{path.name}:{ak}", pk, sk))

    # single-file single-pair fallback: first pk + first sk
    if not pairs and api and sec:
        pk = next(iter(api.values()))
        sk = next(iter(sec.values()))
        pairs.append((f"{path.name}:first", pk, sk))
    return pairs


def _ping_raw(pk: str, sk: str) -> dict:
    body = json.dumps({"apikey": pk, "secretapikey": sk}).encode()
    req = urllib.request.Request(
        f"{BASE}/ping",
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": f"zyn-pb/{SIGNAL}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except Exception:
            return {"status": "ERROR", "message": f"HTTP {e.code}"}


def resolve_keys() -> tuple[str, str, str]:
    """Return (label, pk, sk) for first live pair. Env override wins if valid."""
    # explicit env override (if both set and live)
    env_pk = os.environ.get("PORKBUN_API_KEY", "")
    env_sk = os.environ.get("PORKBUN_SECRET_KEY", "")
    if env_pk.startswith("pk1_") and env_sk.startswith("sk1_"):
        res = _ping_raw(env_pk, env_sk)
        if res.get("status") == "SUCCESS":
            return ("env:PORKBUN_API_KEY", env_pk, env_sk)

    seen: set[tuple[str, str]] = set()
    for path in ENV_CANDIDATES:
        for label, pk, sk in _parse_env_file(path):
            if (pk, sk) in seen:
                continue
            seen.add((pk, sk))
            res = _ping_raw(pk, sk)
            if res.get("status") == "SUCCESS":
                return (label, pk, sk)
    raise SystemExit(
        "No live Porkbun key pair found.\n"
        "Checked: env + " + ", ".join(str(p) for p in ENV_CANDIDATES) + "\n"
        "Create key at https://porkbun.com/account/api and put pk1_/sk1_ in "
        "18JUNE/evny/pb-cf.env as PORKBUN_API_KEY / PORKBUN_SECRET_KEY"
    )


def api(path: str, extra: dict | None = None) -> dict:
    _label, pk, sk = resolve_keys()
    body: dict = {"apikey": pk, "secretapikey": sk}
    if extra:
        body.update(extra)
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": f"zyn-pb/{SIGNAL}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except HTTPError as e:
        return json.loads(e.read().decode())


def cmd_ping() -> int:
    label, pk, sk = resolve_keys()
    res = _ping_raw(pk, sk)
    out = {
        "signal": SIGNAL,
        "host": BASE,
        "key_source": label,
        "pk_prefix": pk[:12] + "…",
        "result": res,
    }
    print(json.dumps(out, indent=2))
    return 0 if res.get("status") == "SUCCESS" else 1


def cmd_which_key() -> int:
    label, pk, _sk = resolve_keys()
    print(f"live_key_source={label}")
    print(f"pk_prefix={pk[:12]}…")
    print(f"host={BASE}")
    print(f"signal={SIGNAL}")
    return 0


def cmd_retrieve(domain: str) -> int:
    data = api(f"/dns/retrieve/{domain}")
    print(json.dumps(data, indent=2))
    return 0 if data.get("status") == "SUCCESS" else 1


def cmd_list_a(domain: str) -> int:
    data = api(f"/dns/retrieve/{domain}")
    if data.get("status") != "SUCCESS":
        print(json.dumps(data, indent=2))
        return 1
    for rec in data.get("records") or []:
        if rec.get("type") in ("A", "ALIAS", "CNAME", "AAAA"):
            print(
                f"{rec.get('type'):6} {rec.get('name') or '':30} "
                f"{rec.get('content')} id={rec.get('id')}"
            )
    return 0


def cmd_point(domain: str, ip: str = VDS_DEFAULT) -> int:
    data = api(f"/dns/retrieve/{domain}")
    if data.get("status") != "SUCCESS":
        print(json.dumps(data, indent=2))
        return 1
    for rec in data.get("records") or []:
        rtype = rec.get("type")
        content = rec.get("content") or ""
        rid = rec.get("id")
        name = rec.get("name") or ""
        drop = False
        cl = content.lower()
        # Drop pixie/BODIS/parking ALIAS+CNAME (not only porkbun.com parking)
        if rtype in ("ALIAS", "CNAME") and any(
            x in cl
            for x in (
                "porkbun",
                "bodis",
                "parkingcrew",
                "sedoparking",
                "parklogic",
                "above.com",
                "afternic",
            )
        ):
            drop = True
        # Drop wildcard CNAME parking
        if rtype == "CNAME" and (name.startswith("*.") or name in ("*", f"*.{domain}")):
            drop = True
        if rtype == "A" and content != ip and (
            name == domain or name.startswith("www.") or name in ("", "www")
        ):
            drop = True
        if drop and rid:
            out = api(f"/dns/delete/{domain}/{rid}")
            print(f"delete {rid} {rtype} -> {out.get('status')}")
    for name in ("", "www"):
        out = api(
            f"/dns/create/{domain}",
            {"name": name, "type": "A", "content": ip, "ttl": "600"},
        )
        status = out.get("status")
        detail = out.get("id") or out.get("message")
        if isinstance(detail, dict) and detail.get("message") == "Duplicate record exists locally.":
            print(f"create {name or '@'} -> already present")
        else:
            print(f"create {name or '@'} -> {status} {detail}")
    print("--- final ---")
    return cmd_list_a(domain)


def cmd_list_all() -> int:
    """List every domain in the account (name + status + expiry), paginated."""
    start = 0
    all_domains: list[dict] = []
    while True:
        res = api("/domain/listAll", {"start": start})
        if res.get("status") != "SUCCESS":
            print(f"ERROR: {res.get('status')} - {res.get('message', '')}", file=sys.stderr)
            return 1
        batch = res.get("domains", [])
        all_domains.extend(batch)
        if len(batch) < 1000:
            break
        start += 1000
    print(f"# {len(all_domains)} domains")
    for d in sorted(all_domains, key=lambda x: x.get("domain", "")):
        print(f"{d.get('domain', '?'):42s} {d.get('status', '?'):10s} exp {d.get('expireDate', '?')}")
    return 0


def usage() -> None:
    print(
        f"""zyn-pb · Porkbun CLI · signal {SIGNAL}

HOST:  {BASE}
VDS:   {VDS_DEFAULT}

Commands:
  ping                         Prove live key + host
  which-key                    Show which key file won (prefix only)
  list-all                     Every domain in account (name + status + expiry)
  count                        Just the portfolio total (fast, 2 API calls)
  retrieve <domain>            Full DNS JSON
  list-a <domain>              A/ALIAS/CNAME lines only
  point <domain> [ip]          Drop pixie parking; apex+www A → ip (default VDS)
  cart-remove <domain>         Remove domain from Porkbun cart
  add-txt <domain> <value>    Add TXT record for verification
  update-ns <domain> <ns1> <ns2> Update nameservers for domain

Key search order:
  1) env PORKBUN_API_KEY + SECRET if live
  2) 18JUNE/evny/pb-cf.env
  3) 18JUNE/zynthio.env
  4) ~/.zynthio.env

Examples:
  zyn-pb ping
  zyn-pb point musicbackup.dev
  zyn-pb point cfmusic.dev
  zyn-pb list-a musicbackup.dev
  zyn-pb cart-remove acidicsoftware.com
  zyn-pb add-txt cats.gold afternic-verification-ednZizim8sUgamWDUa3Gid

Do NOT use https://porkbun.com/api — that 403 is ELB, not your ban.
"""
    )


def cmd_cart_remove(domain: str) -> int:
    """Remove domain from Porkbun cart via API."""
    try:
        _label, api_key, secret = resolve_keys()
    except SystemExit:
        print("ERROR: No live Porkbun key found", file=sys.stderr)
        return 1
    
    # Use POST with JSON body for cart removal
    url = f"{BASE}/shoppingCart/removeItem"
    payload = {"apikey": api_key, "secretapikey": secret, "name": domain.lower()}
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("status") == "SUCCESS":
                print(f"Removed {domain} from cart")
                return 0
            else:
                print(f"ERROR: {result.get('status', 'UNKNOWN')} - {result.get('message', '')}", file=sys.stderr)
                return 1
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP ERROR {e.code}: {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_add_txt(domain: str, txt_value: str) -> int:
    """Add TXT record to domain for Afternic verification."""
    try:
        _label, api_key, secret = resolve_keys()
    except SystemExit:
        print("ERROR: No live Porkbun key found", file=sys.stderr)
        return 1
    
    # First retrieve current DNS to check if TXT exists
    retrieve_data = api(f"/dns/retrieve/{domain}")
    if retrieve_data.get("status") != "SUCCESS":
        print(f"ERROR: Could not retrieve DNS for {domain}", file=sys.stderr)
        return 1
    
    # Check if TXT record already exists
    txt_exists = False
    txt_id = None
    for rec in retrieve_data.get("records") or []:
        if rec.get("type") == "TXT" and rec.get("content") == txt_value:
            txt_exists = True
            txt_id = rec.get("id")
            break
    
    if txt_exists:
        print(f"TXT record already exists for {domain}: {txt_value}")
        return 0
    
    # Delete pixie parking CNAME records if they exist
    for rec in retrieve_data.get("records") or []:
        rtype = rec.get("type")
        content = rec.get("content") or ""
        rid = rec.get("id")
        if rtype in ("CNAME", "ALIAS") and "porkbun" in content.lower():
            delete_data = api(f"/dns/delete/{domain}/{rid}")
            print(f"Deleted pixie parking {rtype} record: {delete_data.get('status')}")
    
    # Create TXT record
    create_data = api(
        f"/dns/create/{domain}",
        {"name": "", "type": "TXT", "content": txt_value, "ttl": "600"}
    )
    
    status = create_data.get("status")
    if status == "SUCCESS":
        print(f"Added TXT record to {domain}: {txt_value}")
        return 0
    else:
        print(f"ERROR: {status} - {create_data.get('message', '')}", file=sys.stderr)
        return 1


def cmd_update_ns(domain: str, ns1: str, ns2: str) -> int:
    """Set domain nameservers (Porkbun v3: POST /domain/updateNs/{domain} with ns[])."""
    try:
        resolve_keys()
    except SystemExit:
        print("ERROR: No live Porkbun key found", file=sys.stderr)
        return 1

    # Canonical Porkbun path is updateNs + ns array — NOT updateNameservers/ns1/ns2
    # (wrong path returns HTML 404 → JSON parse "Expecting value")
    ns = [ns1, ns2]
    # allow extra NS args via env-free path: only two required; more can be appended later
    try:
        update_data = api(f"/domain/updateNs/{domain}", {"ns": ns})
    except Exception as e:
        print(f"ERROR: Nameserver update failed - {e}", file=sys.stderr)
        print("Note: Nameserver updates may require manual intervention via Porkbun UI", file=sys.stderr)
        return 1

    status = update_data.get("status")
    if status == "SUCCESS":
        print(f"Updated nameservers for {domain}: {', '.join(ns)}")
        return 0
    else:
        print(f"ERROR: {status} - {update_data.get('message', '')}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("help", "-h", "--help"):
        usage()
        return 0
    cmd = argv[0]
    try:
        if cmd == "ping":
            return cmd_ping()
        if cmd == "which-key":
            return cmd_which_key()
        if cmd == "retrieve" and len(argv) >= 2:
            return cmd_retrieve(argv[1].lower())
        if cmd == "list-all":
            return cmd_list_all()
        if cmd == "count":
            total = 0
            start = 0
            while True:
                res = api("/domain/listAll", {"start": start})
                batch = res.get("domains", []) if res.get("status") == "SUCCESS" else []
                total += len(batch)
                if len(batch) < 1000:
                    break
                start += 1000
            print(total)
            return 0
        if cmd in ("list-a", "lista", "list") and len(argv) >= 2:
            return cmd_list_a(argv[1].lower())
        if cmd == "point" and len(argv) >= 2:
            ip = argv[2] if len(argv) >= 3 else VDS_DEFAULT
            return cmd_point(argv[1].lower(), ip)
        if cmd == "cart-remove" and len(argv) >= 2:
            return cmd_cart_remove(argv[1].lower())
        if cmd == "add-txt" and len(argv) >= 3:
            return cmd_add_txt(argv[1].lower(), argv[2])
        if cmd == "update-ns" and len(argv) >= 4:
            return cmd_update_ns(argv[1].lower(), argv[2], argv[3])
    except SystemExit as e:
        if e.code not in (0, None):
            print(e, file=sys.stderr)
        return int(e.code) if isinstance(e.code, int) else 1
    usage()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
