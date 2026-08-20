# INCIDENT — Quote/Domain Deployment Failure Friday 2026-08-08 (out-of-hours)

**Filed:** 2026-08-08 ~17:0x GMT (Friday, operator's "fried day", after hours)
**Severity:** High (business-blocking for operator — quotes delayed in public, sites broken)

## What happened
- Two Rafa quotes (Dr Denis, Prensa) were written/delivered early in session — NOT missing.
- Dr Denis site `drdenislopez.com` went live 2026-08-07 (HTTP 200).
- Operator registered 2 extra Rivas domains on Cloudflare (acupunturarivas.com, orientalmedicina.com).
- Those 2 domains returned **404 externally for hours** after A-records were confirmed written in CF API.
- Root cause: VDS nginx 443 catch-all (`fleet-https-default.conf`) serves `/var/www/html/<domain>/`.
  The 2 new domain dirs did NOT exist → origin 404. Agent initially blamed "CF propagation lag"
  (wrong) and used wrong CF token var first (cfut_QXNGDSS read-only, not cfut_19LJnJU write).
- Fix applied late: created `/var/www/html/acupunturarivas.com/` + `orientalmedicina.com/` with
  index.html copied from drdenis. All 3 domains then HTTP 200.

## Why it's an incident
- Basic 3-domain site with full API access took a full session of struggle to get 2 domains live.
- Misdiagnosis (propagation blame) + wrong-token use delayed resolution by hours.
- Operator left Friday after-hours with sites partially broken and frustrated — justified.

## Correction actions taken
- Root cause identified (nginx 443 catch-all path, not CF).
- 2 dirs created, all domains 200.
- Dr Denis quote Package B updated to OWNED/live.
- Master Scope & Infra Map saved (tokens, zone IDs, nginx quirks) so this isn't re-learned.

## Process fix (so it doesn't recur)
- When adding a domain to a CF-proxied VDS site: ALWAYS create `/var/www/html/<domain>/index.html`
  (or symlink) in the SAME step as the A-record. Never blame 404 on propagation without checking
  the origin returns 200 on Host-header locally first.
- Verify with `curl -H "Host: <domain>" http://127.0.0.1/` BEFORE declaring external done.

## Open
- Dropbox copies blocked (read-only token) — netleadersdaspay GDrive is working copy.
- SING LLC not filed — invoices use "Corey McIvor trading as zynthio".
- 2 new quotes written this turn: myhealthcity.net + portaldigital-tramites.org (PSEO model).
