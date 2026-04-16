# Zynthio — AI Session Context (Amnesia Shield)

## Owner
Corey McIvor (@coreintentdev / @coreintentai)
Contact: corey@coreyai.ai ONLY
Based in: New Zealand (NEVER register anything in Australia)

## What This Repo IS
- Zynthio.ai static landing page + email waitlist
- Deployed on Vercel (auto-deploy on push to main)
- One serverless function: `api/waitlist.js` (Resend email API)
- Entry point / public face of the CoreIntent platform

## What This Repo IS NOT
- Not the main application (that is coreintentdev/coreintent — Next.js 15)
- Not a Node.js app — no build step, no package dependencies
- Not yet connected to a database or auth system

## Related Repos
- **coreintentdev/coreintent** — Main trading engine (Next.js 15)
- **coreintentdev/coreintentai** — AI intelligence layer — multi-model orchestration (Claude, Grok, Perplexity)

## Architecture
- `public/index.html` — Static landing page
- `api/waitlist.js` — Vercel Edge/Serverless function (Resend email)
- `vercel.json` — cleanUrls: true, trailingSlash: false
- No framework, no build step, no node_modules

## Environment Variables (Vercel dashboard)
- `RESEND_API_KEY` — Required for waitlist email sends

## Rules for AI Sessions
1. READ before you write. Search the codebase before assuming anything.
2. NEVER say something is "connected" or "active" unless you've verified it works.
3. NEVER register anything in Australia. NZ-first for all legal/business.
4. Deploy files immediately — Vercel auto-deploys on push to main.
5. No npm install needed — there are no dependencies to install.
6. NEVER fabricate family data or personal details.

## Known Issues
- None currently. All prior issues resolved: CORS locked to `https://zynthio.ai`, expired launch date removed from index.html, package.json updated with description and deploy script.

## Family (NEVER fabricate)
- Michelle (wife), Ruby (~14, daughter), Wesley (son)
- Hannah is NOT Corey's child. Her mum took her own life. NEVER list as daughter.
- Chas (dad), Willy/Wilhelmina (mum), Pete (brother, The Pelican), Joel (brother), Peter (third brother)
- Ben Innes (best friend, Perth)
