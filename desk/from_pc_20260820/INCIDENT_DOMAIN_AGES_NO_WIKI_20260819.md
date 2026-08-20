# INCIDENT — DOMAIN AGES/HISTORY NOT RECORDED, NO WIKI/MASTER-SCOPE (2026-08-19)
Operator: "investigate alldmans. incident if not got args of all and
reveal and history if applicable. all need wiki and master scope. no
plan you have but i will make you plan"

## THE BREACH / GAP (verified)
- MASTER_DOMAIN_20260813.csv: 1,670 domains — columns only
  [domain, porkbun_expiry, cf_account, cf_status, sources]
  NO age, NO registration-date, NO history, NO backlinks.
- DOMAINS_ACTUAL_20260813.csv: domain/expires/source only.
- No per-site WIKI_*.md docs exist for the owned domains (only
  unrelated *.wiki archive files).
- The operator's explicit doctrine (research age/backlinks/history per
  site, wiki per site, master scope per doc) is NOT in place.

## THE FIX (build the tracking infra)
1. Domain audit script: pull RDAP (age, registrar, dates) + whois for
   each owned domain -> populate the missing columns.
2. Per-domain WIKI_<domain>.md + a MASTER scope entry per domain.
3. The wiki = age, history, backlinks, role, build status.
4. Master scope = the one-line role each domain plays in the portfolio.

## THE OPERATOR'S DIRECTION
"no plan you have but I will make you plan" -> I build the tracking
INFRASTRUCTURE, the operator drives the PLAN/priorities. I don't decide
which domains get built first — I make sure every one has its wiki +
scope so the operator can plan with full data.

## STATUS
OPEN — tracking infra being built (audit + wiki scaffold).
