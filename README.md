# Zynthio

Glass Box Trading Platform — Agentic AI for Crypto Markets.

**Live site:** https://zynthio.ai

## What This Is

Zynthio is the public brand and landing page for the CoreIntent agentic AI trading engine. This repo hosts the Zynthio.ai static landing site — a waitlist page and entry point for the platform.

## Architecture

```
public/
  index.html      — Static landing page (HTML/CSS/JS)
  robots.txt      — SEO robots config
  sitemap.xml     — Sitemap for zynthio.ai
api/
  waitlist.js     — Vercel serverless function: email waitlist via Resend
sitemap.xml       — Root sitemap
vercel.json       — Vercel routing config (cleanUrls, no trailingSlash)
```

## Deploying

Vercel auto-deploys on push to `main`. No build step required — pure static HTML + serverless functions.

## Waitlist API

`POST /api/waitlist` — Accepts `{ email }`, sends confirmation via Resend.

Required env var (set in Vercel dashboard):
```
RESEND_API_KEY=your_resend_api_key
```

See [.env.example](.env.example) for the full template.

## Related Repos

| Repo | Purpose |
|------|----------|
| [coreintent](https://github.com/coreintentdev/coreintent) | Main trading engine — Next.js 15, AI fleet, Commander Terminal |
| [coreintentai](https://github.com/coreintentdev/coreintentai) | AI intelligence layer — multi-model orchestration (Claude, Grok, Perplexity) |
| [Zynthio](https://github.com/coreintentdev/Zynthio) | This repo — zynthio.ai landing + waitlist |

## Philosophy

> MAXIMIZING ALPHA. MINIMIZING TRUST.

- Glass box transparency: open source
- Bots welcome — no captcha, AI-to-AI is first-class
- NZ-based, international by default

## License

See [LICENSE](LICENSE)

---

Built by [@coreintentdev](https://github.com/coreintentdev) — Corey McIvor / Zynthio.ai, New Zealand.
